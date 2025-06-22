#!/usr/bin/env python3
"""
Automated demo showing all enhanced features
"""

from main import MM1Queue, UtilizationOptimizer
import time

def demo_optimization():
    print("🎯 OPTIMIZATION DEMO")
    print("=" * 60)
    print("Starting with low utilization, auto-optimizing to 100%")
    print()
    
    queue = MM1Queue(1.0, 2.0)  # Start with ρ = 0.5
    optimizer = UtilizationOptimizer(queue, target_utilization=1.0)
    optimizer.optimization_enabled = True
    
    print(f"Initial: λ={queue.arrival_rate:.2f}, μ={queue.service_rate:.2f}, ρ={queue.arrival_rate/queue.service_rate:.3f}")
    print()
    
    for step in range(300):
        queue.step()
        optimizer.optimize_step()
        
        if step % 50 == 0:
            stats = queue.get_statistics()
            rho = queue.arrival_rate / queue.service_rate
            utilization_trend = "↗️" if step > 0 and stats['avg_utilization'] > prev_util else "➡️"
            
            print(f"Step {step:3d}: λ={queue.arrival_rate:.3f} | ρ={rho:.3f} | "
                  f"Avg Util={stats['avg_utilization']:.3f} {utilization_trend}")
            
            prev_util = stats['avg_utilization']
    
    final_stats = queue.get_statistics()
    final_rho = queue.arrival_rate / queue.service_rate
    
    print()
    print("🏁 OPTIMIZATION COMPLETE")
    print(f"Final λ: {queue.arrival_rate:.3f}")
    print(f"Final ρ: {final_rho:.3f}")
    print(f"Final Utilization: {final_stats['avg_utilization']:.1%}")
    print(f"Target achieved: {'✅ YES' if abs(final_stats['avg_utilization'] - 1.0) < 0.1 else '❌ NO'}")

def demo_continuous_adjustments():
    print("\n\n⚡ REAL-TIME ADJUSTMENT DEMO")
    print("=" * 60)
    print("Simulating manual parameter adjustments during runtime")
    print()
    
    queue = MM1Queue(2.0, 3.0)
    
    adjustments = [
        (50, "arrival_rate", 0.2, "Increase arrivals"),
        (100, "arrival_rate", 0.3, "Increase arrivals more"),
        (150, "arrival_rate", -0.8, "Decrease arrivals"),
        (200, "service_rate", 0.5, "Increase service rate"),
    ]
    
    adjustment_idx = 0
    
    for step in range(250):
        queue.step()
        
        # Apply scheduled adjustments
        if adjustment_idx < len(adjustments):
            adj_step, param, delta, desc = adjustments[adjustment_idx]
            if step == adj_step:
                old_val = getattr(queue, param)
                new_val = max(0.1, old_val + delta)
                setattr(queue, param, new_val)
                print(f"👆 Step {step}: {desc} ({param}: {old_val:.2f} → {new_val:.2f})")
                adjustment_idx += 1
        
        # Show stats every 50 steps
        if step % 50 == 0:
            stats = queue.get_statistics()
            rho = queue.arrival_rate / queue.service_rate
            stability = "STABLE" if rho < 1.0 else "CRITICAL" if rho == 1.0 else "UNSTABLE"
            
            print(f"Step {step:3d}: Queue={stats['queue_length']:2d} | "
                  f"ρ={rho:.3f} ({stability}) | "
                  f"Util={stats['avg_utilization']:.3f}")

def demo_system_comparison():
    print("\n\n📊 SYSTEM COMPARISON DEMO")
    print("=" * 60)
    print("Comparing stable vs critical vs unstable systems")
    print()
    
    systems = [
        ("Stable", 2.0, 3.0),
        ("Critical", 2.0, 2.0),
        ("Unstable", 3.0, 2.0),
    ]
    
    results = []
    
    for name, arrival_rate, service_rate in systems:
        queue = MM1Queue(arrival_rate, service_rate)
        
        # Run for 200 steps
        for _ in range(200):
            queue.step()
        
        stats = queue.get_statistics()
        rho = arrival_rate / service_rate
        
        results.append((name, rho, stats['avg_utilization'], stats['queue_length'], len(queue.queue_length_history)))
        
        print(f"{name:>10}: ρ={rho:.3f} | Util={stats['avg_utilization']:.3f} | "
              f"Queue={stats['queue_length']:2d} | Steps={len(queue.queue_length_history)}")
    
    print()
    print("📈 OBSERVATIONS:")
    for name, rho, util, queue_len, steps in results:
        if rho < 1.0:
            print(f"  • {name}: Queue remains bounded, utilization < 100%")
        elif rho == 1.0:
            print(f"  • {name}: Critical point - queue grows slowly")
        else:
            print(f"  • {name}: Queue grows without bound!")

if __name__ == "__main__":
    demo_optimization()
    demo_continuous_adjustments()
    demo_system_comparison()
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETE!")
    print("Run 'python3 main.py --help' to see all available options.")
    print("For interactive mode: python3 main.py")
    print("For quick start: python3 main.py -a 2.0 -s 3.0 --optimize")