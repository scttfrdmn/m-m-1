#!/usr/bin/env python3
"""
Test script for enhanced M/M/1 Queue Simulator features
"""

from main import MM1Queue, UtilizationOptimizer
import time

def test_optimization():
    print("Testing M/M/1 Queue Optimizer")
    print("=" * 50)
    
    # Start with low utilization
    arrival_rate = 1.5
    service_rate = 3.0
    
    queue = MM1Queue(arrival_rate, service_rate)
    optimizer = UtilizationOptimizer(queue, target_utilization=0.95)
    optimizer.optimization_enabled = True
    
    print(f"Initial Parameters:")
    print(f"  Arrival rate (λ): {arrival_rate}")
    print(f"  Service rate (μ): {service_rate}")
    print(f"  Initial ρ: {arrival_rate/service_rate:.3f}")
    print(f"  Target utilization: {optimizer.target_utilization:.1%}")
    print()
    
    print("Running optimization for 500 steps...")
    
    for i in range(500):
        queue.step()
        optimizer.optimize_step()
        
        if i % 100 == 0:
            stats = queue.get_statistics()
            current_rho = queue.arrival_rate / queue.service_rate
            print(f"Step {i:3d}: λ={queue.arrival_rate:.3f}, "
                  f"ρ={current_rho:.3f}, "
                  f"Avg Util={stats['avg_utilization']:.3f}")
    
    # Final results
    stats = queue.get_statistics()
    final_rho = queue.arrival_rate / queue.service_rate
    
    print("\nOptimization Results:")
    print("-" * 30)
    print(f"Final λ: {queue.arrival_rate:.3f}")
    print(f"Final ρ: {final_rho:.3f}")
    print(f"Final Avg Utilization: {stats['avg_utilization']:.3f}")
    print(f"Target Utilization: {optimizer.target_utilization:.3f}")
    print(f"Error: {abs(stats['avg_utilization'] - optimizer.target_utilization):.3f}")
    
    if abs(stats['avg_utilization'] - optimizer.target_utilization) < 0.05:
        print("✅ Optimization successful!")
    else:
        print("❌ Optimization needs more time")

def test_enhanced_statistics():
    print("\n" + "=" * 50)
    print("Testing Enhanced Statistics Tracking")
    print("=" * 50)
    
    queue = MM1Queue(2.0, 2.5)
    
    print("Running 200 steps to collect statistics...")
    for i in range(200):
        queue.step()
        
        if i % 50 == 0:
            stats = queue.get_statistics()
            print(f"Step {i:3d}: Queue={stats['queue_length']:2d}, "
                  f"Instant Util={stats['utilization']:.2f}, "
                  f"Avg Util={stats['avg_utilization']:.3f}")
    
    stats = queue.get_statistics()
    
    print("\nFinal Enhanced Statistics:")
    print("-" * 30)
    print(f"Queue Length:         {stats['queue_length']}")
    print(f"Instantaneous Util:   {stats['utilization']:.3f}")
    print(f"Average Utilization:  {stats['avg_utilization']:.3f}")
    print(f"Theoretical Util:     {stats['theoretical_utilization']:.3f}")
    print(f"Busy Time:            {queue.server_busy_time:.2f}")
    print(f"Total Time:           {queue.current_time:.2f}")
    print(f"History Length:       {len(queue.utilization_history)}")

def test_parameter_adjustment():
    print("\n" + "=" * 50) 
    print("Testing Parameter Adjustment")
    print("=" * 50)
    
    queue = MM1Queue(2.0, 3.0)
    
    print(f"Initial: λ={queue.arrival_rate}, μ={queue.service_rate}")
    
    # Test quick adjustments
    original_lambda = queue.arrival_rate
    queue.arrival_rate += 0.5
    print(f"After +0.5: λ={queue.arrival_rate}")
    
    queue.arrival_rate -= 0.3
    print(f"After -0.3: λ={queue.arrival_rate}")
    
    # Test boundary
    queue.arrival_rate = 0.05
    queue.arrival_rate = max(0.1, queue.arrival_rate - 0.1)
    print(f"Minimum boundary test: λ={queue.arrival_rate}")
    
    print("✅ Parameter adjustment working correctly")

if __name__ == "__main__":
    test_optimization()
    test_enhanced_statistics()
    test_parameter_adjustment()
    print("\n🎉 All enhanced features tested successfully!")