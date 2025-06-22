#!/usr/bin/env python3
"""
Test script for M/M/1 Queue Simulator
"""

from main import MM1Queue
import time

def test_mm1_queue():
    print("Testing M/M/1 Queue Simulator")
    print("=" * 40)
    
    # Test with stable system (λ < μ)
    arrival_rate = 2.0
    service_rate = 3.0
    
    queue = MM1Queue(arrival_rate, service_rate)
    
    print(f"Parameters:")
    print(f"  Arrival rate (λ): {arrival_rate}")
    print(f"  Service rate (μ): {service_rate}")
    print(f"  Traffic intensity (ρ): {arrival_rate/service_rate:.2f}")
    print()
    
    # Run simulation for 100 steps
    print("Running simulation for 100 steps...")
    for i in range(100):
        queue.step()
        
        if i % 20 == 0:  # Print every 20 steps
            stats = queue.get_statistics()
            print(f"Step {i:3d}: Queue={stats['queue_length']:2d}, "
                  f"Server={'Busy' if stats['server_busy'] else 'Idle'}, "
                  f"Time={stats['current_time']:6.2f}")
    
    # Final statistics
    stats = queue.get_statistics()
    print("\nFinal Statistics:")
    print("-" * 20)
    print(f"Queue Length:         {stats['queue_length']}")
    print(f"Server Busy:          {stats['server_busy']}")
    print(f"Total Arrivals:       {stats['total_customers']}")
    print(f"Customers Served:     {stats['customers_served']}")
    print(f"Average Wait Time:    {stats['avg_wait_time']:.2f}")
    print(f"Simulation Time:      {stats['current_time']:.2f}")
    
    print("\nTheoretical Values:")
    print("-" * 20)
    rho = arrival_rate / service_rate
    theoretical_queue_length = (rho * rho) / (1 - rho)
    theoretical_utilization = rho
    
    print(f"Expected Queue Length: {theoretical_queue_length:.2f}")
    print(f"Expected Utilization:  {theoretical_utilization:.2f}")
    
    # Test queue length history
    if len(queue.queue_length_history) > 0:
        avg_queue_length = sum(queue.queue_length_history) / len(queue.queue_length_history)
        print(f"Observed Avg Queue:    {avg_queue_length:.2f}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_mm1_queue()