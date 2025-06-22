#!/usr/bin/env python3
"""
Demo script for M/M/1 Queue Simulator with ASCII visualization
"""

from main import MM1Queue
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_queue_ascii(queue_length, server_busy, max_display=15):
    """Draw simple ASCII representation of queue"""
    server_status = "[BUSY]" if server_busy else "[IDLE]"
    
    if queue_length == 0:
        queue_viz = "(empty)"
    else:
        displayed = min(queue_length, max_display)
        queue_viz = "".join(["[C]" for _ in range(displayed)])
        if queue_length > max_display:
            queue_viz += f"...+{queue_length - max_display}"
    
    return f"Server: {server_status}  |  Queue: {queue_viz}"

def run_demo():
    print("M/M/1 Queue Simulator Demo")
    print("=" * 50)
    print("Running automatic demo with λ=2.0, μ=3.0")
    print("Press Ctrl+C to stop")
    print()
    
    # Create queue with stable parameters
    queue = MM1Queue(arrival_rate=2.0, service_rate=3.0)
    
    try:
        step = 0
        while step < 200:  # Run for 200 steps
            clear_screen()
            
            print("M/M/1 Queue Simulator Demo")
            print("=" * 50)
            print(f"Step: {step}")
            print()
            
            # Get current statistics
            stats = queue.get_statistics()
            
            # Draw queue visualization
            queue_ascii = draw_queue_ascii(stats['queue_length'], stats['server_busy'])
            print(queue_ascii)
            print()
            
            # Show statistics
            print("Current Statistics:")
            print(f"  Queue Length:      {stats['queue_length']}")
            print(f"  Server Utilization: {stats['utilization']:.0%}")
            print(f"  Total Arrivals:    {stats['total_customers']}")
            print(f"  Customers Served:  {stats['customers_served']}")
            print(f"  Simulation Time:   {stats['current_time']:.2f}")
            print()
            
            # Show parameters
            print("Parameters:")
            print(f"  Arrival Rate (λ):   {queue.arrival_rate}")
            print(f"  Service Rate (μ):   {queue.service_rate}")
            print(f"  Traffic Intensity:  {queue.arrival_rate/queue.service_rate:.2f}")
            print()
            
            # Show theoretical values
            rho = queue.arrival_rate / queue.service_rate
            if rho < 1:
                theoretical_queue = (rho * rho) / (1 - rho)
                print(f"Expected Queue Length: {theoretical_queue:.2f}")
                print(f"Expected Utilization:  {rho:.2f}")
            else:
                print("System is unstable (ρ ≥ 1)")
            
            # Queue length history (simple bar chart)
            if len(queue.queue_length_history) >= 20:
                print("\nQueue Length History (last 20 steps):")
                recent_history = queue.queue_length_history[-20:]
                max_len = max(recent_history) if recent_history else 0
                
                if max_len > 0:
                    for level in range(min(max_len, 8), -1, -1):
                        line = f"{level:2d} |"
                        for length in recent_history:
                            line += "*" if length >= level else " "
                        print(line)
                    print("   +" + "-" * 20)
            
            # Step simulation
            queue.step()
            step += 1
            
            time.sleep(0.3)  # Pause for visibility
            
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user.")
    
    print(f"\nDemo completed after {step} steps.")

if __name__ == "__main__":
    run_demo()