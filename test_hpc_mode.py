#!/usr/bin/env python3
"""
Test the HPC context mode implementation
"""

from main import MM1Queue, SimulatorUI, UtilizationOptimizer, get_hpc_scenarios

def test_hpc_terminology():
    print("Testing HPC Terminology Mapping")
    print("=" * 50)
    
    # Test regular mode
    regular_ui = SimulatorUI(hpc_mode=False)
    print("Regular Mode Terminology:")
    print(f"  customer: {regular_ui.term('customer')}")
    print(f"  server: {regular_ui.term('server')}")
    print(f"  queue: {regular_ui.term('queue')}")
    print(f"  arrivals: {regular_ui.term('arrivals')}")
    
    print()
    
    # Test HPC mode
    hpc_ui = SimulatorUI(hpc_mode=True)
    print("HPC Mode Terminology:")
    print(f"  customer: {hpc_ui.term('customer')}")
    print(f"  server: {hpc_ui.term('server')}")
    print(f"  queue: {hpc_ui.term('queue')}")
    print(f"  arrivals: {hpc_ui.term('arrivals')}")
    
    print()

def test_hpc_scenarios():
    print("Testing HPC Scenario Presets")
    print("=" * 50)
    
    scenarios = get_hpc_scenarios()
    
    for name, config in scenarios.items():
        arrival_rate = config['arrival_rate']
        service_rate = config['service_rate']
        description = config['description']
        rho = arrival_rate / service_rate
        
        print(f"{name.upper()}:")
        print(f"  Submission rate: {arrival_rate:.1f} jobs/hr ({arrival_rate*24:.0f} jobs/day)")
        print(f"  Completion rate: {service_rate:.1f} jobs/hr ({service_rate*24:.0f} jobs/day)")
        print(f"  Load factor (ρ): {rho:.3f}")
        print(f"  Description: {description}")
        print()

def test_hpc_display():
    print("Testing HPC Display Mode")
    print("=" * 50)
    
    # Create HPC simulator
    hpc_ui = SimulatorUI(hpc_mode=True)
    hpc_ui.queue = MM1Queue(2.0, 2.5)  # Normal HPC workload
    hpc_ui.optimizer = UtilizationOptimizer(hpc_ui.queue)
    
    # Run some simulation steps
    for _ in range(60):
        hpc_ui.queue.step()
    
    # Show HPC display
    stats = hpc_ui.queue.get_statistics()
    print("HPC Mode Display:")
    print("-" * 30)
    hpc_ui.draw_compact_display(stats)
    hpc_ui.draw_compact_controls()

def test_regular_vs_hpc_comparison():
    print("\n" + "=" * 50)
    print("Regular vs HPC Mode Comparison")
    print("=" * 50)
    
    # Same parameters for both
    arrival_rate = 2.0
    service_rate = 2.5
    
    print("1. REGULAR MODE:")
    print("-" * 20)
    regular_ui = SimulatorUI(hpc_mode=False)
    regular_ui.queue = MM1Queue(arrival_rate, service_rate)
    regular_ui.optimizer = UtilizationOptimizer(regular_ui.queue)
    
    # Run simulation
    for _ in range(40):
        regular_ui.queue.step()
    
    stats_regular = regular_ui.queue.get_statistics()
    regular_ui.draw_compact_display(stats_regular)
    
    print("\n2. HPC MODE:")
    print("-" * 20)
    hpc_ui = SimulatorUI(hpc_mode=True)
    hpc_ui.queue = MM1Queue(arrival_rate, service_rate)
    hpc_ui.optimizer = UtilizationOptimizer(hpc_ui.queue)
    
    # Run simulation
    for _ in range(40):
        hpc_ui.queue.step()
    
    stats_hpc = hpc_ui.queue.get_statistics()
    hpc_ui.draw_compact_display(stats_hpc)

def test_hpc_educational_insights():
    print("\n" + "=" * 50)
    print("HPC Educational Insights")
    print("=" * 50)
    
    scenarios_to_test = [
        ("underutilized", 1.0, 3.0),
        ("optimal", 2.1, 2.5), 
        ("busy", 3.4, 4.0),
        ("overloaded", 4.0, 3.5)
    ]
    
    for scenario_name, arrival_rate, service_rate in scenarios_to_test:
        print(f"{scenario_name.upper()} SCENARIO:")
        print("-" * 25)
        
        hpc_ui = SimulatorUI(hpc_mode=True)
        hpc_ui.queue = MM1Queue(arrival_rate, service_rate)
        
        # Run enough simulation to get insights
        for _ in range(80):
            hpc_ui.queue.step()
        
        stats = hpc_ui.queue.get_statistics()
        rho = arrival_rate / service_rate
        
        # Show just the educational note
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
        
        print(f"Load factor: {rho:.1%}")
        print(f"Education: {edu_note}")
        print()

if __name__ == "__main__":
    test_hpc_terminology()
    test_hpc_scenarios()
    test_hpc_display()
    test_regular_vs_hpc_comparison()
    test_hpc_educational_insights()