#!/usr/bin/env python3
"""
M/M/1 Queue Simulator with HPC Context

A comprehensive educational simulator for M/M/1 queuing systems that demonstrates 
fundamental queueing theory concepts through interactive visualization and analysis.

Features:
- Real-time ASCII visualization of queue dynamics
- Educational insights including Little's Law verification
- Individual customer journey tracking
- HPC job scheduling context mode
- Multiple optimization strategies
- Comprehensive statistical analysis

The simulator implements an event-driven M/M/1 queue where:
- M: Markovian (Poisson) arrival process
- M: Markovian (exponential) service times  
- 1: Single server

This model is fundamental for understanding system performance, capacity planning,
and the relationship between utilization and response times.

Author: Scott Friedman (with Claude Code Assistant)
License: MIT License - Copyright (c) 2025 Scott Friedman
Repository: https://github.com/scttfrdmn/m-m-1
Web Demo: https://scttfrdmn.github.io/m-m-1/
"""

import random
import time
import math
import argparse
from collections import deque
from dataclasses import dataclass
from typing import List, Optional
import os
import sys
import threading


@dataclass
class Customer:
    """
    Represents a single customer/job in the M/M/1 queue system.
    
    Tracks the complete journey of a customer from arrival through service completion,
    enabling detailed analysis of individual experiences within the system.
    
    Attributes:
        id: Unique identifier for the customer
        arrival_time: When the customer arrived at the system
        service_time: How long the customer's service takes
        start_service_time: When service began (None if still waiting)
        departure_time: When customer left the system (None if still in system)
    """
    id: int
    arrival_time: float
    service_time: float
    start_service_time: Optional[float] = None
    departure_time: Optional[float] = None
    
    @property
    def wait_time(self) -> float:
        """Time spent waiting in queue"""
        if self.start_service_time is None:
            return 0.0
        return self.start_service_time - self.arrival_time
    
    @property
    def time_in_system(self) -> float:
        """Total time in system (wait + service)"""
        if self.departure_time is None:
            return 0.0
        return self.departure_time - self.arrival_time
    
    @property
    def is_completed(self) -> bool:
        """Whether customer has left the system"""
        return self.departure_time is not None


class MM1Queue:
    """
    M/M/1 Queue Simulation Engine
    
    Implements a discrete-event simulation of a single-server queue with Poisson 
    arrivals and exponential service times. This is the core mathematical model
    that demonstrates fundamental queueing theory principles.
    
    The simulator uses event-driven simulation, processing arrivals and departures
    in chronological order while maintaining detailed statistics for educational
    analysis and Little's Law verification.
    
    Key Features:
    - Event-driven simulation with accurate timing
    - Real-time statistics collection and analysis
    - Little's Law verification (L = λW)
    - Individual customer journey tracking
    - Steady-state confidence assessment
    - Educational insights and pattern detection
    
    Mathematical Background:
    - λ (lambda): Arrival rate (customers per time unit)
    - μ (mu): Service rate (customers per time unit)  
    - ρ (rho): Traffic intensity = λ/μ
    - System is stable when ρ < 1
    
    Args:
        arrival_rate: Average customer arrivals per time unit (λ)
        service_rate: Average service completions per time unit (μ)
    
    Example:
        >>> queue = MM1Queue(arrival_rate=2.0, service_rate=3.0)
        >>> for _ in range(100):
        ...     queue.step()
        >>> stats = queue.get_statistics()
        >>> print(f"Average queue length: {stats['queue_length']}")
    """
    def __init__(self, arrival_rate: float, service_rate: float):
        self.arrival_rate = arrival_rate  # lambda (customers per time unit)
        self.service_rate = service_rate  # mu (customers per time unit)
        self.queue = deque()
        self.server_busy = False
        self.current_time = 0.0
        self.next_arrival_time = 0.0
        self.next_departure_time = float('inf')
        self.total_customers = 0
        self.customers_served = 0
        self.total_wait_time = 0.0
        self.total_service_time = 0.0
        
        # Statistics tracking
        self.queue_length_history = []
        self.time_history = []
        self.utilization_history = []
        self.server_busy_time = 0.0
        self.last_update_time = 0.0
        
        # Enhanced educational tracking
        self.next_customer_id = 1
        self.completed_customers = []  # List of completed customers
        self.current_customer = None   # Customer being served
        self.recent_journeys = deque(maxlen=5)  # Last 5 customer journeys
        self.total_time_in_system = 0.0  # For Little's Law calculation
        
        # Little's Law: track time-weighted average number in system
        self.time_weighted_customers = 0.0  # ∫ L(t) dt
        self.last_measurement_time = 0.0
        
        # Steady-state detection
        self.steady_state_threshold = 100  # Customers needed for steady state
        self.confidence_level = 0.0
        
        # Generate first arrival
        self.schedule_next_arrival()
    
    def schedule_next_arrival(self):
        """Schedule the next customer arrival using exponential distribution"""
        inter_arrival_time = random.expovariate(self.arrival_rate)
        self.next_arrival_time = self.current_time + inter_arrival_time
    
    def schedule_next_departure(self, customer: Customer):
        """Schedule departure for customer currently being served"""
        service_time = random.expovariate(self.service_rate)
        customer.service_time = service_time
        customer.start_service_time = self.current_time
        self.next_departure_time = self.current_time + service_time
    
    def arrive_customer(self):
        """Process customer arrival"""
        customer = Customer(
            id=self.next_customer_id,
            arrival_time=self.current_time, 
            service_time=0
        )
        self.next_customer_id += 1
        self.total_customers += 1
        
        if not self.server_busy:
            # Server is free, start service immediately
            self.server_busy = True
            self.current_customer = customer
            self.schedule_next_departure(customer)
        else:
            # Server is busy, add to queue
            self.queue.append(customer)
        
        # Schedule next arrival
        self.schedule_next_arrival()
    
    def depart_customer(self):
        """Process customer departure"""
        # Complete the current customer
        if self.current_customer:
            self.current_customer.departure_time = self.current_time
            self.customers_served += 1
            
            # Track statistics
            wait_time = self.current_customer.wait_time
            time_in_system = self.current_customer.time_in_system
            self.total_wait_time += wait_time
            self.total_time_in_system += time_in_system
            
            # Add to completed customers and recent journeys
            self.completed_customers.append(self.current_customer)
            self.recent_journeys.append(self.current_customer)
            
            # Keep only recent completed customers for memory efficiency
            if len(self.completed_customers) > 1000:
                self.completed_customers = self.completed_customers[-500:]
        
        if self.queue:
            # Serve next customer in queue
            next_customer = self.queue.popleft()
            next_customer.start_service_time = self.current_time
            self.current_customer = next_customer
            self.schedule_next_departure(next_customer)
        else:
            # No customers waiting, server becomes idle
            self.server_busy = False
            self.current_customer = None
            self.next_departure_time = float('inf')
    
    def step(self):
        """Execute one simulation step"""
        # Update time-weighted customer count for Little's Law
        time_delta = self.current_time - self.last_measurement_time
        customers_in_system = len(self.queue) + (1 if self.server_busy else 0)
        self.time_weighted_customers += customers_in_system * time_delta
        self.last_measurement_time = self.current_time
        
        # Update server busy time
        if self.server_busy:
            self.server_busy_time += (self.current_time - self.last_update_time)
        
        # Record current state
        self.queue_length_history.append(len(self.queue))
        self.time_history.append(self.current_time)
        
        # Calculate running utilization
        if self.current_time > 0:
            current_utilization = self.server_busy_time / self.current_time
            self.utilization_history.append(current_utilization)
        
        self.last_update_time = self.current_time
        
        # Determine next event
        if self.next_arrival_time <= self.next_departure_time:
            # Next event is arrival
            self.current_time = self.next_arrival_time
            self.arrive_customer()
        else:
            # Next event is departure
            self.current_time = self.next_departure_time
            self.depart_customer()
    
    def get_statistics(self):
        """Calculate current system statistics"""
        if self.customers_served == 0:
            avg_wait_time = 0
        else:
            avg_wait_time = self.total_wait_time / self.customers_served
        
        queue_length = len(self.queue)
        instantaneous_utilization = 1.0 if self.server_busy else 0.0
        
        # Calculate running average utilization
        if self.current_time > 0:
            avg_utilization = self.server_busy_time / self.current_time
        else:
            avg_utilization = 0.0
        
        # Theoretical values for M/M/1 queue
        rho = self.arrival_rate / self.service_rate if self.service_rate > self.arrival_rate else 1.0
        theoretical_avg_queue_length = (rho * rho) / (1 - rho) if rho < 1 else float('inf')
        theoretical_utilization = rho if rho < 1 else 1.0
        
        # Educational metrics
        little_law_verification = self.get_little_law_verification()
        time_breakdown = self.get_time_breakdown()
        steady_state_info = self.get_steady_state_info()
        
        return {
            'queue_length': queue_length,
            'server_busy': self.server_busy,
            'utilization': instantaneous_utilization,
            'avg_utilization': avg_utilization,
            'total_customers': self.total_customers,
            'customers_served': self.customers_served,
            'avg_wait_time': avg_wait_time,
            'current_time': self.current_time,
            'theoretical_queue_length': theoretical_avg_queue_length,
            'theoretical_utilization': theoretical_utilization,
            # Educational enhancements
            'little_law': little_law_verification,
            'time_breakdown': time_breakdown,
            'steady_state': steady_state_info,
            'recent_journeys': list(self.recent_journeys)
        }
    
    def get_little_law_verification(self):
        """Calculate Little's Law verification: L = λW"""
        if self.customers_served < 10 or self.current_time <= 0:
            return None
            
        # L = time-weighted average number in system
        L = self.time_weighted_customers / self.current_time
        
        # λ = arrival rate (use actual observed rate)
        lambda_observed = self.total_customers / self.current_time
            
        # W = average time in system
        W = self.total_time_in_system / self.customers_served
            
        # Calculate λW
        lambda_times_W = lambda_observed * W
        
        # Verification
        error = abs(L - lambda_times_W)
        relative_error = error / max(L, 0.001)  # Avoid division by zero
        
        return {
            'L': L,
            'lambda': lambda_observed,
            'W': W,
            'lambda_times_W': lambda_times_W,
            'error': error,
            'relative_error': relative_error,
            'verified': relative_error < 0.20  # Within 20% (allow for simulation variance)
        }
    
    def get_time_breakdown(self):
        """Get breakdown of time components"""
        if self.customers_served < 5:
            return None
            
        total_wait = self.total_wait_time
        total_service = sum(c.service_time for c in self.completed_customers)
        total_system = self.total_time_in_system
        
        avg_wait = total_wait / self.customers_served
        avg_service = total_service / self.customers_served if self.customers_served > 0 else 0
        avg_system = total_system / self.customers_served
        
        return {
            'avg_wait_time': avg_wait,
            'avg_service_time': avg_service,
            'avg_time_in_system': avg_system,
            'wait_fraction': avg_wait / max(avg_system, 0.001),
            'service_fraction': avg_service / max(avg_system, 0.001)
        }
    
    def get_steady_state_info(self):
        """Assess whether system is in steady state"""
        customers_needed = self.steady_state_threshold
        progress = min(self.customers_served / customers_needed, 1.0)
        
        # Simple confidence based on number of customers served
        if self.customers_served < 20:
            confidence = "Very Low"
            reliability = "Not reliable"
        elif self.customers_served < 50:
            confidence = "Low" 
            reliability = "Use with caution"
        elif self.customers_served < 100:
            confidence = "Medium"
            reliability = "Moderately reliable"
        else:
            confidence = "High"
            reliability = "Reliable"
            
        return {
            'customers_served': self.customers_served,
            'customers_needed': customers_needed,
            'progress': progress,
            'confidence': confidence,
            'reliability': reliability,
            'is_steady_state': self.customers_served >= customers_needed
        }


class UtilizationOptimizer:
    def __init__(self, queue: MM1Queue, target_utilization: float = 1.0):
        self.queue = queue
        self.target_utilization = target_utilization
        self.optimization_enabled = False
        self.adjustment_rate = 0.01
        self.measurement_window = 100
        
        # Strategy for achieving ρ=1
        self.strategy = "arrival_rate"  # "arrival_rate", "service_rate", "balanced", "demonstrate_instability"
        self.max_arrival_rate = 10.0  # Safety bound
        self.min_service_rate = 0.5   # Safety bound
        self.demonstration_phase = 0  # For educational demonstration
        
    def set_strategy(self, strategy: str):
        """Set optimization strategy for achieving ρ=1"""
        valid_strategies = ["arrival_rate", "service_rate", "balanced", "demonstrate_instability"]
        if strategy in valid_strategies:
            self.strategy = strategy
            self.demonstration_phase = 0
        
    def get_strategy_info(self):
        """Get current strategy description"""
        descriptions = {
            "arrival_rate": "Adjust λ only (μ fixed) - Show instability when λ≥μ",
            "service_rate": "Adjust μ only (λ fixed) - Show high service rates needed",
            "balanced": "Adjust both λ,μ - Attempt stable ρ=1",
            "demonstrate_instability": "Deliberately show ρ>1 queue explosion"
        }
        return descriptions.get(self.strategy, "Unknown strategy")
        
    def optimize_step(self):
        """Adjust parameters to achieve target utilization using selected strategy"""
        if not self.optimization_enabled:
            return
            
        if len(self.queue.utilization_history) < self.measurement_window:
            return
            
        # Get recent utilization average
        recent_util = sum(self.queue.utilization_history[-self.measurement_window:]) / self.measurement_window
        current_rho = self.queue.arrival_rate / self.queue.service_rate
        
        # Calculate adjustment based on strategy
        if self.strategy == "arrival_rate":
            self._optimize_arrival_rate_only(recent_util, current_rho)
        elif self.strategy == "service_rate":
            self._optimize_service_rate_only(recent_util, current_rho)
        elif self.strategy == "balanced":
            self._optimize_balanced(recent_util, current_rho)
        elif self.strategy == "demonstrate_instability":
            self._demonstrate_instability(recent_util, current_rho)
    
    def _optimize_arrival_rate_only(self, recent_util, current_rho):
        """Strategy 1: Only adjust λ, keep μ fixed - shows impossibility of stable ρ=1"""
        util_error = self.target_utilization - recent_util
        
        if abs(util_error) > 0.02:
            if util_error > 0:  # Need higher utilization
                # Increase λ but this will lead to ρ>1 and instability
                self.queue.arrival_rate = min(self.max_arrival_rate, 
                                            self.queue.arrival_rate + self.adjustment_rate)
            else:  # Need lower utilization
                # Decrease λ which gives stable system but lower utilization
                self.queue.arrival_rate = max(0.1, self.queue.arrival_rate - self.adjustment_rate)
    
    def _optimize_service_rate_only(self, recent_util, current_rho):
        """Strategy 2: Only adjust μ, keep λ fixed - shows required service rates"""
        util_error = self.target_utilization - recent_util
        
        if abs(util_error) > 0.02:
            if util_error > 0:  # Need higher utilization
                # For ρ=1 with fixed λ, need μ = λ exactly
                # But any small decrease leads to instability
                target_mu = self.queue.arrival_rate / self.target_utilization
                self.queue.service_rate = max(self.min_service_rate, 
                                            min(target_mu, self.queue.service_rate - self.adjustment_rate/2))
            else:  # Need lower utilization  
                # Increase μ for stability
                self.queue.service_rate += self.adjustment_rate
    
    def _optimize_balanced(self, recent_util, current_rho):
        """Strategy 3: Adjust both λ and μ to attempt stable ρ=1"""
        util_error = self.target_utilization - recent_util
        
        if abs(util_error) > 0.02:
            if util_error > 0:  # Need higher utilization
                # Carefully increase λ while adjusting μ to maintain ρ≈1
                if current_rho < 0.98:
                    self.queue.arrival_rate += self.adjustment_rate / 2
                    # Adjust μ to keep ratio close to 1
                    self.queue.service_rate = self.queue.arrival_rate + 0.01  # Slight buffer
                else:
                    # Very close to ρ=1, make tiny adjustments
                    self.queue.arrival_rate += self.adjustment_rate / 10
                    self.queue.service_rate = self.queue.arrival_rate + 0.005
            else:  # Need lower utilization
                # Increase the buffer between λ and μ
                self.queue.service_rate += self.adjustment_rate
    
    def _demonstrate_instability(self, recent_util, current_rho):
        """Strategy 4: Educational demonstration of ρ>1 instability"""
        self.demonstration_phase += 1
        
        if self.demonstration_phase < 200:
            # Phase 1: Gradually push ρ > 1 to show queue explosion
            if current_rho < 1.2:
                self.queue.arrival_rate += 0.005
        elif self.demonstration_phase < 400:
            # Phase 2: Show recovery by decreasing λ
            if current_rho > 0.8:
                self.queue.arrival_rate -= 0.01
        else:
            # Phase 3: Reset demonstration
            self.demonstration_phase = 0
    
    def toggle_optimization(self):
        self.optimization_enabled = not self.optimization_enabled
        return self.optimization_enabled
    
    def cycle_strategy(self):
        """Cycle through different optimization strategies"""
        strategies = ["arrival_rate", "service_rate", "balanced", "demonstrate_instability"]
        current_index = strategies.index(self.strategy)
        next_index = (current_index + 1) % len(strategies)
        self.strategy = strategies[next_index]
        self.demonstration_phase = 0
        return self.strategy


class SimulatorUI:
    def __init__(self, hpc_mode=False):
        self.queue = None
        self.optimizer = None
        self.running = False
        self.step_mode = False
        self.continuous_mode = False
        self.auto_optimize = False
        
        # HPC context mode
        self.hpc_mode = hpc_mode
        self.time_unit = "hours" if hpc_mode else "time units"
        self.rate_unit = "jobs/hr" if hpc_mode else "customers/time"
        
        # HPC terminology mapping
        self.terminology = self._get_terminology_map()
        
    def _get_terminology_map(self):
        """Get terminology mapping based on mode"""
        if self.hpc_mode:
            return {
                'customer': 'job',
                'customers': 'jobs', 
                'server': 'cluster',
                'queue': 'job queue',
                'service_time': 'runtime',
                'wait_time': 'queue wait',
                'arrival_rate': 'submission rate',
                'service_rate': 'completion rate',
                'utilization': 'cluster utilization',
                'arrivals': 'submissions',
                'served': 'completed',
                'simulator': 'scheduler'
            }
        else:
            return {
                'customer': 'customer',
                'customers': 'customers',
                'server': 'server', 
                'queue': 'queue',
                'service_time': 'service time',
                'wait_time': 'wait time',
                'arrival_rate': 'arrival rate',
                'service_rate': 'service rate',
                'utilization': 'utilization',
                'arrivals': 'arrivals',
                'served': 'served',
                'simulator': 'simulator'
            }
    
    def term(self, key):
        """Get terminology for current mode"""
        return self.terminology.get(key, key)
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_compact_display(self, stats):
        """Draw compact terminal-friendly display"""
        # Header line with educational context
        opt_status = "OPT" if self.optimizer and self.optimizer.optimization_enabled else "---"
        mode_status = "STEP" if self.step_mode else "CONT" if self.continuous_mode else "RUN"
        
        # Show optimization strategy if enabled
        strategy_info = ""
        if self.optimizer and self.optimizer.optimization_enabled:
            strategy_name = self.optimizer.strategy.replace("_", "-")
            strategy_info = f" │ Strategy: {strategy_name}"
        
        # Header adapts to mode
        if self.hpc_mode:
            title = "HPC Job Scheduler"
            opt_label = "Load Balancing"
        else:
            title = "M/M/1 Queue Simulator"
            opt_label = "Optimization"
            
        print(f"{title} │ Mode: {mode_status} │ {opt_label}: {opt_status}{strategy_info}")
        print("─" * 78)
        
        # Status line with key info
        server_icon = "●" if stats['server_busy'] else "○"
        queue_length = stats['queue_length']
        queue_viz = "█" * min(queue_length, 15) + ("⋯" if queue_length > 15 else "")
        
        rho = self.queue.arrival_rate / self.queue.service_rate
        stability = "STABLE" if rho < 0.95 else "CRITICAL" if rho <= 1.05 else "UNSTABLE"
        
        # Adapt terminology
        if self.hpc_mode:
            server_label = "Cluster"
            queue_label = f"Jobs({queue_length:2d})"
            load_label = f"Load={rho:.1%}"
        else:
            server_label = "Server"
            queue_label = f"Queue({queue_length:2d})" 
            load_label = f"ρ={rho:.3f}"
            
        print(f"{server_label}: {server_icon} │ {queue_label}: {queue_viz:<17} │ {load_label} ({stability})")
        
        # Statistics in columns
        if self.hpc_mode:
            rate_label1 = f"Submit={self.queue.arrival_rate:4.1f}/{self.time_unit.split('s')[0]}"
            rate_label2 = f"Complete={self.queue.service_rate:4.1f}/{self.time_unit.split('s')[0]}"
            time_label = f"Uptime: {stats['current_time']:6.1f}{self.time_unit.split('s')[0]}"
            arrivals_label = f"{self.term('arrivals').title()}: {stats['total_customers']:4d}"
        else:
            rate_label1 = f"λ={self.queue.arrival_rate:5.2f}"
            rate_label2 = f"μ={self.queue.service_rate:5.2f}"
            time_label = f"Time: {stats['current_time']:6.1f}"
            arrivals_label = f"{self.term('arrivals').title()}: {stats['total_customers']:4d}"
            
        print(f"{rate_label1} │ {rate_label2} │ " +
              f"Util: {stats['avg_utilization']:.1%} │ {time_label} │ " +
              f"{arrivals_label}")
        
        # Dynamic mini graph (queue length history)
        if len(self.queue.queue_length_history) >= 30:
            graph_title = f"\n{self.term('queue').title()} Length History (last 60 steps):"
            print(graph_title)
            history = self.queue.queue_length_history[-60:]
            max_len = max(history) if history else 0
            
            if max_len > 0:
                # Dynamic vertical scale - always show 3 levels but adapt to data
                if max_len <= 3:
                    levels = [3, 2, 1]
                elif max_len <= 6:
                    levels = [max_len, max_len//2, 1]
                elif max_len <= 12:
                    levels = [max_len, max_len//2, max_len//4]
                else:
                    # For very large queues, show top, middle, and low ranges
                    levels = [max_len, max_len//3, max_len//6]
                
                for level in levels:
                    if level > 0:
                        line = f"{level:3d}│"
                        for length in history:
                            if length >= level:
                                line += "█"
                            elif length >= level * 0.7:  # Partial fill for better granularity
                                line += "▄"
                            elif length >= level * 0.3:
                                line += "▁"
                            else:
                                line += " "
                        print(line)
                
                # Footer with scale indicators
                scale_info = f"Scale: 0 to {max_len}" if max_len > 10 else ""
                footer = "   └" + "─" * len(history)
                if scale_info:
                    footer += f" {scale_info}"
                print(footer)
        
        # Quick stats line with educational insights
        wait_time = stats['avg_wait_time']
        served = stats['customers_served']
        theoretical_util = stats['theoretical_utilization']
        theoretical_queue = stats.get('theoretical_queue_length', 0)
        
        # Educational note about current state - adapt to mode
        if self.hpc_mode:
            if rho >= 1.0:
                edu_note = "🚨 OVERLOADED: Job queue growing - need more nodes or job limits"
            elif rho > 0.95:
                edu_note = "⚠️ CRITICAL: Near capacity - implement job throttling"
            elif rho > 0.85:
                edu_note = "⚡ BUSY: High utilization - monitor queue growth"
            elif rho < 0.5:
                edu_note = "💡 UNDERUTILIZED: Cluster has spare capacity"
            else:
                edu_note = "✅ OPTIMAL: Good balance of throughput and responsiveness"
        else:
            if rho >= 1.0:
                edu_note = "⚠️ UNSTABLE: Queue will grow without bound!"
            elif rho > 0.95:
                edu_note = "⚡ CRITICAL: Very sensitive to small changes"
            elif rho < 0.5:
                edu_note = "💡 UNDERUTILIZED: Server idle often"
            else:
                edu_note = "✅ STABLE: Good balance"
        
        print(f"\nStats: Served={served:4d} │ AvgWait={wait_time:4.1f} │ " +
              f"Expected: Util={theoretical_util:.1%} │ Queue={theoretical_queue:.1f}")
        print(f"Education: {edu_note}")
        
        # Show optimization strategy explanation if active
        if self.optimizer and self.optimizer.optimization_enabled:
            strategy_explanation = self.optimizer.get_strategy_info()
            print(f"Strategy: {strategy_explanation}")
        
        # Educational enhancements
        self.draw_educational_insights(stats)
        
        print("─" * 78)
    
    def draw_educational_insights(self, stats):
        """Draw educational insights: Little's Law, customer journeys, etc."""
        
        # Little's Law verification - adapt terminology
        little_law = stats.get('little_law')
        if little_law:
            L = little_law['L']
            lam = little_law['lambda']
            W = little_law['W']
            lam_W = little_law['lambda_times_W']
            verified = "✅" if little_law['verified'] else "⚠️"
            
            if self.hpc_mode:
                print(f"\nLittle's Law: Jobs={L:.1f} │ Rate={lam:.2f}/{self.time_unit.split('s')[0]} │ Time={W:.2f}{self.time_unit.split('s')[0]} │ Rate×Time={lam_W:.1f} {verified}")
            else:
                print(f"\nLittle's Law: L={L:.1f} │ λ={lam:.2f} │ W={W:.2f} │ λ×W={lam_W:.1f} {verified}")
        
        # Time breakdown - adapt terminology
        time_breakdown = stats.get('time_breakdown')
        if time_breakdown:
            wait_time = time_breakdown['avg_wait_time']
            service_time = time_breakdown['avg_service_time']
            system_time = time_breakdown['avg_time_in_system']
            
            if self.hpc_mode:
                print(f"Time Breakdown: Total={system_time:.2f}{self.time_unit.split('s')[0]} = Queued={wait_time:.2f}{self.time_unit.split('s')[0]} + Runtime={service_time:.2f}{self.time_unit.split('s')[0]}")
            else:
                print(f"Time Breakdown: System={system_time:.2f} = Wait={wait_time:.2f} + Service={service_time:.2f}")
        
        # Recent journeys - adapt terminology  
        recent_journeys = stats.get('recent_journeys', [])
        if recent_journeys:
            if self.hpc_mode:
                print("Recent Job Completions:")
                for customer in recent_journeys[-3:]:  # Show last 3
                    wait = customer.wait_time
                    service = customer.service_time
                    total = customer.time_in_system
                    print(f"  Job#{customer.id}: Queued={wait:.1f}{self.time_unit.split('s')[0]} + Runtime={service:.1f}{self.time_unit.split('s')[0]} = Total={total:.1f}{self.time_unit.split('s')[0]}")
            else:
                print("Recent Customer Journeys:")
                for customer in recent_journeys[-3:]:  # Show last 3
                    wait = customer.wait_time
                    service = customer.service_time
                    total = customer.time_in_system
                    print(f"  C#{customer.id}: Wait={wait:.1f}min + Service={service:.1f}min = Total={total:.1f}min")
        
        # Steady-state indicator
        steady_state = stats.get('steady_state')
        if steady_state:
            confidence = steady_state['confidence']
            progress = steady_state['progress']
            reliability = steady_state['reliability']
            
            progress_bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
            print(f"Statistics Confidence: {confidence} [{progress_bar}] {reliability}")
    
    def draw_compact_controls(self):
        """Draw compact control instructions"""
        space_action = "Next" if self.step_mode else "Stop" if self.continuous_mode else "Pause"
        
        print(f"Controls: [SPACE]{space_action} [S]Step [C]Continuous [O]Optimize " +
              f"[+/-]Rate [R]Reset [Q]Quit")
        
        # Show strategy-specific controls if optimization is enabled
        if self.optimizer and self.optimizer.optimization_enabled:
            print("         [T]Strategy [A]λ-adjust [M]μ-adjust")
        elif self.step_mode or self.continuous_mode:
            print("         [A]λ-adjust [M]μ-adjust")
        print()
    
    def get_user_input(self):
        """Get user input with timeout"""
        try:
            import select
            import sys
            
            if select.select([sys.stdin], [], [], 0.1)[0]:
                return sys.stdin.read(1).lower()
            return None
        except (ImportError, OSError):
            # Fallback for systems without select or when stdin is not a tty
            return None
    
    def adjust_arrival_rate(self, delta=None):
        """Allow user to adjust arrival rate"""
        if delta is not None:
            # Quick adjustment
            new_rate = max(0.1, self.queue.arrival_rate + delta)
            self.queue.arrival_rate = new_rate
            return
            
        try:
            print(f"Current arrival rate: {self.queue.arrival_rate:.3f}")
            new_rate = float(input("Enter new arrival rate (λ): "))
            if new_rate > 0:
                self.queue.arrival_rate = new_rate
                print(f"Arrival rate set to {new_rate:.3f}")
            else:
                print("Rate must be positive!")
        except ValueError:
            print("Invalid input!")
        input("Press Enter to continue...")
    
    def adjust_service_rate(self):
        """Allow user to adjust service rate"""
        try:
            print(f"Current service rate: {self.queue.service_rate:.3f}")
            new_rate = float(input("Enter new service rate (μ): "))
            if new_rate > 0:
                self.queue.service_rate = new_rate
                print(f"Service rate set to {new_rate:.3f}")
            else:
                print("Rate must be positive!")
        except ValueError:
            print("Invalid input!")
        input("Press Enter to continue...")
    
    def reset_simulation(self):
        """Reset the simulation"""
        arrival_rate = self.queue.arrival_rate
        service_rate = self.queue.service_rate
        self.queue = MM1Queue(arrival_rate, service_rate)
        self.optimizer = UtilizationOptimizer(self.queue)
        print("Simulation reset!")
        time.sleep(1)
    
    def run_continuous_mode(self):
        """Run simulation continuously until stopped"""
        print("\nContinuous mode started. Press Ctrl+C to stop or 'Q' to quit.")
        try:
            while self.continuous_mode and self.running:
                for _ in range(10):  # Run 10 steps at a time
                    if not self.continuous_mode:
                        break
                    self.queue.step()
                    if self.optimizer:
                        self.optimizer.optimize_step()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.continuous_mode = False
            print("\nContinuous mode stopped.")
        time.sleep(1)
    
    def run(self):
        """Main simulation loop"""
        print("M/M/1 Queue Simulator")
        print("=====================")
        
        # Get initial parameters
        try:
            arrival_rate = float(input("Enter arrival rate (λ, customers/time): "))
            service_rate = float(input("Enter service rate (μ, customers/time): "))
            
            if arrival_rate <= 0 or service_rate <= 0:
                print("Rates must be positive!")
                return
                
            self.queue = MM1Queue(arrival_rate, service_rate)
            self.optimizer = UtilizationOptimizer(self.queue)
            
        except ValueError:
            print("Invalid input!")
            return
        
        print("\nStarting simulation...")
        print("Use SPACE to pause/resume, Q to quit")
        time.sleep(2)
        
        self.running = True
        
        # Configure terminal for non-blocking input
        old_settings = None
        try:
            import termios, tty
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except (ImportError, OSError, termios.error):
            # Silent fallback for non-interactive environments
            pass
        
        try:
            while self.running:
                self.clear_screen()
                
                stats = self.queue.get_statistics()
                
                self.draw_compact_display(stats)
                self.draw_compact_controls()
                
                # Handle user input
                user_input = self.get_user_input()
                if user_input:
                    if user_input == 'q':
                        self.running = False
                    elif user_input == ' ':
                        if self.step_mode:
                            self.queue.step()
                        else:
                            # Toggle pause
                            input("Paused. Press Enter to continue...")
                    elif user_input == 's':
                        self.step_mode = not self.step_mode
                        if self.step_mode:
                            self.continuous_mode = False
                    elif user_input == 'c':
                        self.continuous_mode = not self.continuous_mode
                        if self.continuous_mode:
                            self.step_mode = False
                            if old_settings:
                                try:
                                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                                except:
                                    pass
                            self.run_continuous_mode()
                            tty.setcbreak(sys.stdin.fileno())
                    elif user_input == 'o':
                        if self.optimizer:
                            enabled = self.optimizer.toggle_optimization()
                            status = "ENABLED" if enabled else "DISABLED"
                            strategy_name = self.optimizer.strategy.replace("_", " ").title()
                            print(f"\nOptimization {status}")
                            if enabled:
                                print(f"Strategy: {strategy_name}")
                                print(f"Goal: {self.optimizer.get_strategy_info()}")
                            time.sleep(2)
                    elif user_input == 't':
                        if self.optimizer and self.optimizer.optimization_enabled:
                            old_strategy = self.optimizer.strategy
                            new_strategy = self.optimizer.cycle_strategy()
                            print(f"\nStrategy changed: {old_strategy} → {new_strategy}")
                            print(f"New goal: {self.optimizer.get_strategy_info()}")
                            time.sleep(2)
                    elif user_input == '+':
                        self.adjust_arrival_rate(0.1)
                    elif user_input == '-':
                        self.adjust_arrival_rate(-0.1)
                    elif user_input == 'r':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        self.reset_simulation()
                        tty.setcbreak(sys.stdin.fileno())
                    elif user_input == 'a':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        self.adjust_arrival_rate()
                        tty.setcbreak(sys.stdin.fileno())
                    elif user_input == 'm':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        self.adjust_service_rate()
                        tty.setcbreak(sys.stdin.fileno())
                
                if not self.step_mode and not self.continuous_mode:
                    self.queue.step()
                    if self.optimizer:
                        self.optimizer.optimize_step()
                    time.sleep(0.1)  # Control simulation speed
                
        except KeyboardInterrupt:
            pass
        finally:
            if old_settings:
                try:
                    import termios
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                except:
                    pass
        
        print("\nSimulation ended.")


def get_hpc_scenarios():
    """Define HPC scenario presets"""
    return {
        'light': {
            'arrival_rate': 1.0,    # 24 jobs/day
            'service_rate': 2.0,    # 48 jobs/day capacity
            'description': 'Research cluster - low usage period'
        },
        'normal': {
            'arrival_rate': 2.0,    # 48 jobs/day  
            'service_rate': 2.5,    # 60 jobs/day capacity
            'description': 'Production cluster - typical workload'
        },
        'busy': {
            'arrival_rate': 3.5,    # 84 jobs/day
            'service_rate': 4.0,    # 96 jobs/day capacity  
            'description': 'High demand period - conference deadlines'
        },
        'overloaded': {
            'arrival_rate': 4.0,    # 96 jobs/day
            'service_rate': 3.5,    # 84 jobs/day capacity
            'description': 'Oversubscribed - more jobs than capacity'
        },
        'maintenance': {
            'arrival_rate': 2.0,    # Normal submission rate
            'service_rate': 1.5,    # Reduced capacity (nodes down)
            'description': 'Maintenance period - reduced capacity'
        }
    }

def main():
    parser = argparse.ArgumentParser(description='M/M/1 Queue Simulator / HPC Job Scheduler')
    parser.add_argument('--arrival-rate', '-a', type=float, default=None,
                        help='Initial arrival rate (λ) or job submission rate')
    parser.add_argument('--service-rate', '-s', type=float, default=None,
                        help='Initial service rate (μ) or job completion rate')
    parser.add_argument('--optimize', '-o', action='store_true',
                        help='Start with optimization enabled')
    parser.add_argument('--continuous', '-c', action='store_true',
                        help='Start in continuous mode')
    parser.add_argument('--hpc', type=str, default=None,
                        help='HPC scenario: light, normal, busy, overloaded, maintenance')
    parser.add_argument('--hpc-mode', action='store_true',
                        help='Enable HPC terminology and context')
    
    args = parser.parse_args()
    
    # Handle HPC mode and scenarios
    hpc_mode = args.hpc_mode or args.hpc is not None
    simulator = SimulatorUI(hpc_mode=hpc_mode)
    
    # Handle HPC scenario presets
    if args.hpc:
        hpc_scenarios = get_hpc_scenarios()
        if args.hpc in hpc_scenarios:
            scenario = hpc_scenarios[args.hpc]
            args.arrival_rate = scenario['arrival_rate']
            args.service_rate = scenario['service_rate']
            print(f"🖥️ HPC Scenario: {args.hpc}")
            print(f"📝 Description: {scenario['description']}")
        else:
            print(f"❌ Unknown HPC scenario: {args.hpc}")
            print(f"Available scenarios: {', '.join(hpc_scenarios.keys())}")
            return
    
    # Override initial parameters if provided
    if args.arrival_rate is not None and args.service_rate is not None:
        simulator.queue = MM1Queue(args.arrival_rate, args.service_rate)
        simulator.optimizer = UtilizationOptimizer(simulator.queue)
        
        if args.optimize:
            simulator.optimizer.optimization_enabled = True
        
        if args.continuous:
            simulator.continuous_mode = True
        
        simulator.running = True
        
        if hpc_mode:
            print(f"Starting HPC scheduler: Submit={args.arrival_rate:.1f}/hr, Complete={args.service_rate:.1f}/hr", flush=True)
        else:
            print(f"Starting with λ={args.arrival_rate}, μ={args.service_rate}", flush=True)
        if args.optimize:
            if hpc_mode:
                print("Load balancing enabled for optimal cluster utilization", flush=True)
            else:
                print("Optimization enabled for 100% utilization", flush=True)
        if args.continuous:
            print("Starting in continuous mode", flush=True)
        
        time.sleep(2)
        
        # Configure terminal for non-blocking input
        old_settings = None
        try:
            import termios, tty
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except (ImportError, OSError, termios.error):
            # Silent fallback for non-interactive environments
            pass
        
        try:
            while simulator.running:
                simulator.clear_screen()
                
                stats = simulator.queue.get_statistics()
                
                simulator.draw_compact_display(stats)
                simulator.draw_compact_controls()
                
                # Handle user input
                user_input = simulator.get_user_input()
                if user_input:
                    if user_input == 'q':
                        simulator.running = False
                    elif user_input == ' ':
                        if simulator.step_mode:
                            simulator.queue.step()
                        elif simulator.continuous_mode:
                            simulator.continuous_mode = False
                        else:
                            input("Paused. Press Enter to continue...")
                    elif user_input == 's':
                        simulator.step_mode = not simulator.step_mode
                        if simulator.step_mode:
                            simulator.continuous_mode = False
                    elif user_input == 'c':
                        simulator.continuous_mode = not simulator.continuous_mode
                        if simulator.continuous_mode:
                            simulator.step_mode = False
                            if old_settings:
                                try:
                                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                                except:
                                    pass
                            simulator.run_continuous_mode()
                            tty.setcbreak(sys.stdin.fileno())
                    elif user_input == 'o':
                        if simulator.optimizer:
                            enabled = simulator.optimizer.toggle_optimization()
                            status = "ENABLED" if enabled else "DISABLED"
                            strategy_name = simulator.optimizer.strategy.replace("_", " ").title()
                            print(f"\nOptimization {status}")
                            if enabled:
                                print(f"Strategy: {strategy_name}")
                                print(f"Goal: {simulator.optimizer.get_strategy_info()}")
                            time.sleep(2)
                    elif user_input == 't':
                        if simulator.optimizer and simulator.optimizer.optimization_enabled:
                            old_strategy = simulator.optimizer.strategy
                            new_strategy = simulator.optimizer.cycle_strategy()
                            print(f"\nStrategy changed: {old_strategy} → {new_strategy}")
                            print(f"New goal: {simulator.optimizer.get_strategy_info()}")
                            time.sleep(2)
                    elif user_input == '+':
                        simulator.adjust_arrival_rate(0.1)
                    elif user_input == '-':
                        simulator.adjust_arrival_rate(-0.1)
                    elif user_input == 'r':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        simulator.reset_simulation()
                        tty.setcbreak(sys.stdin.fileno())
                    elif user_input == 'a':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        simulator.adjust_arrival_rate()
                        tty.setcbreak(sys.stdin.fileno())
                    elif user_input == 'm':
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        simulator.adjust_service_rate()
                        tty.setcbreak(sys.stdin.fileno())
                
                if not simulator.step_mode and not simulator.continuous_mode:
                    simulator.queue.step()
                    if simulator.optimizer:
                        simulator.optimizer.optimize_step()
                    time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            if old_settings:
                try:
                    import termios
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                except:
                    pass
        
        print("\nSimulation ended.")
    else:
        simulator.run()


if __name__ == "__main__":
    main()