#!/usr/bin/env python3
"""
Test the new educational features: Little's Law, customer journeys, time breakdown
"""

from main import MM1Queue, UtilizationOptimizer, SimulatorUI
import time

def test_educational_features():
    print("Testing Educational Features")
    print("=" * 60)
    
    # Create a queue with moderate traffic
    queue = MM1Queue(2.0, 2.5)  # ρ = 0.8
    ui = SimulatorUI()
    ui.queue = queue
    ui.optimizer = UtilizationOptimizer(queue)
    
    print("Running simulation to build up educational data...")
    
    # Run simulation for different phases to show progression
    phases = [
        ("Early phase (20 steps)", 20),
        ("Building confidence (40 more steps)", 40), 
        ("Steady state (60 more steps)", 60)
    ]
    
    for phase_name, steps in phases:
        print(f"\n{phase_name}")
        print("-" * 50)
        
        # Run the simulation
        for _ in range(steps):
            queue.step()
        
        # Get statistics
        stats = queue.get_statistics()
        
        print(f"Customers served: {stats['customers_served']}")
        print(f"Current queue length: {stats['queue_length']}")
        print(f"Simulation time: {stats['current_time']:.1f}")
        print()
        
        # Show educational insights
        ui.draw_educational_insights(stats)
        print()

def test_little_law_verification():
    print("\n" + "=" * 60)
    print("Little's Law Verification Test")
    print("=" * 60)
    
    scenarios = [
        ("Light Traffic (ρ=0.3)", 0.6, 2.0),
        ("Moderate Traffic (ρ=0.7)", 2.1, 3.0),
        ("Heavy Traffic (ρ=0.9)", 2.7, 3.0)
    ]
    
    for scenario_name, arrival_rate, service_rate in scenarios:
        print(f"\n{scenario_name}")
        print("-" * 30)
        
        queue = MM1Queue(arrival_rate, service_rate)
        
        # Run until we have enough data for Little's Law
        for _ in range(150):
            queue.step()
        
        stats = queue.get_statistics()
        little_law = stats['little_law']
        
        if little_law:
            L = little_law['L']
            lam = little_law['lambda']
            W = little_law['W']
            lam_W = little_law['lambda_times_W']
            error = little_law['relative_error']
            verified = little_law['verified']
            
            print(f"ρ = {arrival_rate/service_rate:.2f}")
            print(f"L (avg in system): {L:.2f}")
            print(f"λ (arrival rate): {lam:.3f}")
            print(f"W (avg time in system): {W:.3f}")
            print(f"λ × W = {lam_W:.2f}")
            print(f"Error: {error:.1%}")
            print(f"Little's Law verified: {'✅ YES' if verified else '❌ NO'}")

def test_customer_journeys():
    print("\n" + "=" * 60)
    print("Customer Journey Tracking Test")
    print("=" * 60)
    
    queue = MM1Queue(3.0, 2.0)  # ρ = 1.5 (unstable for variety)
    
    print("Running unstable system to show variety in customer experiences...")
    
    # Run simulation
    for _ in range(80):
        queue.step()
    
    stats = queue.get_statistics()
    recent_journeys = stats['recent_journeys']
    
    if recent_journeys:
        print("\nRecent Customer Experiences:")
        print("Customer │ Arrival │ Start Service │ Departure │ Wait Time │ Service Time │ Total Time")
        print("─────────┼─────────┼───────────────┼───────────┼───────────┼──────────────┼───────────")
        
        for customer in recent_journeys:
            arrival = customer.arrival_time
            start_service = customer.start_service_time
            departure = customer.departure_time
            wait = customer.wait_time
            service = customer.service_time
            total = customer.time_in_system
            
            print(f"C#{customer.id:4d}   │ {arrival:7.2f} │ {start_service:13.2f} │ {departure:9.2f} │ "
                  f"{wait:9.2f} │ {service:12.2f} │ {total:10.2f}")
    
    # Show time breakdown
    time_breakdown = stats['time_breakdown']
    if time_breakdown:
        print(f"\nAverage Time Analysis:")
        print(f"Average wait time: {time_breakdown['avg_wait_time']:.2f}")
        print(f"Average service time: {time_breakdown['avg_service_time']:.2f}")
        print(f"Average total time: {time_breakdown['avg_time_in_system']:.2f}")
        print(f"Wait fraction: {time_breakdown['wait_fraction']:.1%}")
        print(f"Service fraction: {time_breakdown['service_fraction']:.1%}")

def test_steady_state_progression():
    print("\n" + "=" * 60)
    print("Steady State Progression Test")
    print("=" * 60)
    
    queue = MM1Queue(2.0, 3.0)  # ρ = 0.67
    
    checkpoints = [10, 25, 50, 100, 150]
    
    print("Customers │ Confidence │ Progress Bar    │ Reliability")
    print("──────────┼────────────┼─────────────────┼─────────────────")
    
    step = 0
    for checkpoint in checkpoints:
        # Run to checkpoint
        while queue.customers_served < checkpoint:
            queue.step()
            step += 1
        
        stats = queue.get_statistics()
        steady_state = stats['steady_state']
        
        served = steady_state['customers_served']
        confidence = steady_state['confidence']
        progress = steady_state['progress']
        reliability = steady_state['reliability']
        
        progress_bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))
        
        print(f"{served:8d}  │ {confidence:10s} │ [{progress_bar}] │ {reliability}")

if __name__ == "__main__":
    test_educational_features()
    test_little_law_verification()
    test_customer_journeys()
    test_steady_state_progression()