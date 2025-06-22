#!/usr/bin/env python3
"""
Test the new dynamic scaling graph display
"""

from main import MM1Queue, UtilizationOptimizer, SimulatorUI
import time

def test_graph_scaling():
    print("Testing Dynamic Graph Scaling")
    print("=" * 50)
    
    # Test different queue behaviors
    scenarios = [
        ("Low Queue (ρ=0.5)", MM1Queue(1.0, 2.0), 80),
        ("Medium Queue (ρ=0.8)", MM1Queue(2.4, 3.0), 80),
        ("High Queue (ρ=1.2)", MM1Queue(3.6, 3.0), 80),
        ("Explosive Queue (ρ=1.5)", MM1Queue(4.5, 3.0), 80)
    ]
    
    for scenario_name, queue, steps in scenarios:
        print(f"\n{scenario_name}")
        print("-" * 40)
        
        ui = SimulatorUI()
        ui.queue = queue
        ui.optimizer = UtilizationOptimizer(queue)
        
        # Run simulation to generate queue history
        for i in range(steps):
            queue.step()
        
        # Show the current state with graph
        stats = queue.get_statistics()
        rho = queue.arrival_rate / queue.service_rate
        max_queue = max(queue.queue_length_history) if queue.queue_length_history else 0
        avg_queue = sum(queue.queue_length_history) / len(queue.queue_length_history) if queue.queue_length_history else 0
        
        print(f"ρ = {rho:.2f}, Max Queue: {max_queue}, Avg Queue: {avg_queue:.1f}")
        
        # Display the compact graph
        ui.draw_compact_display(stats)
        
        print()

def test_graph_transitions():
    """Test how the graph adapts as queue length changes"""
    print("\nTesting Graph Scale Transitions")
    print("=" * 50)
    
    queue = MM1Queue(2.0, 2.0)  # Start at ρ=1
    ui = SimulatorUI()
    ui.queue = queue
    ui.optimizer = UtilizationOptimizer(queue)
    
    # Simulate different phases
    phases = [
        ("Phase 1: Building up (50 steps)", 50),
        ("Phase 2: High utilization (30 steps)", 30),
        ("Phase 3: Reduce load", 20)
    ]
    
    for phase_name, steps in phases:
        print(f"\n{phase_name}")
        print("-" * 30)
        
        # Adjust parameters mid-simulation
        if "Reduce load" in phase_name:
            queue.arrival_rate = 1.5  # Reduce to ρ=0.75
        
        for i in range(steps):
            queue.step()
        
        stats = queue.get_statistics()
        max_queue = max(queue.queue_length_history[-30:]) if len(queue.queue_length_history) >= 30 else 0
        current_queue = stats['queue_length']
        
        print(f"Current Queue: {current_queue}, Recent Max: {max_queue}")
        
        # Show just the graph part
        if len(queue.queue_length_history) >= 30:
            print("Queue Length History (last 60 steps):")
            history = queue.queue_length_history[-60:]
            max_len = max(history) if history else 0
            
            if max_len > 0:
                # Show the scaling logic
                if max_len <= 3:
                    levels = [3, 2, 1]
                    scale_type = "Small scale (≤3)"
                elif max_len <= 6:
                    levels = [max_len, max_len//2, 1]
                    scale_type = "Medium scale (≤6)"
                elif max_len <= 12:
                    levels = [max_len, max_len//2, max_len//4]
                    scale_type = "Large scale (≤12)"
                else:
                    levels = [max_len, max_len//3, max_len//6]
                    scale_type = "Very large scale (>12)"
                
                print(f"Using {scale_type}: levels {levels}")
                
                for level in levels:
                    if level > 0:
                        line = f"{level:3d}│"
                        for length in history:
                            if length >= level:
                                line += "█"
                            elif length >= level * 0.7:
                                line += "▄"
                            elif length >= level * 0.3:
                                line += "▁"
                            else:
                                line += " "
                        print(line)
                
                scale_info = f"Scale: 0 to {max_len}" if max_len > 10 else ""
                footer = "   └" + "─" * len(history)
                if scale_info:
                    footer += f" {scale_info}"
                print(footer)

if __name__ == "__main__":
    test_graph_scaling()
    test_graph_transitions()