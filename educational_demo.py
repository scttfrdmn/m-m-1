#!/usr/bin/env python3
"""
Educational demonstration of ρ=1 optimization strategies
Shows why 100% utilization is problematic in practice
"""

from main import MM1Queue, UtilizationOptimizer
import time

def demonstrate_strategy(strategy_name, description, queue_params, duration=300):
    """Demonstrate a specific optimization strategy"""
    print(f"\n📚 EDUCATIONAL DEMO: {strategy_name.upper().replace('_', ' ')}")
    print("=" * 70)
    print(f"Goal: {description}")
    print(f"Initial parameters: λ={queue_params[0]:.1f}, μ={queue_params[1]:.1f}")
    print()
    
    queue = MM1Queue(queue_params[0], queue_params[1])
    optimizer = UtilizationOptimizer(queue, target_utilization=1.0)
    optimizer.set_strategy(strategy_name)
    optimizer.optimization_enabled = True
    
    print("Step │ λ     │ μ     │ ρ     │ Queue │ Util% │ Educational Observation")
    print("─────┼───────┼───────┼───────┼───────┼───────┼────────────────────────")
    
    for step in range(0, duration, 25):
        # Run simulation
        for _ in range(25):
            queue.step()
            optimizer.optimize_step()
        
        stats = queue.get_statistics()
        rho = queue.arrival_rate / queue.service_rate
        queue_len = stats['queue_length']
        util = stats['avg_utilization']
        
        # Educational observation
        if strategy_name == "arrival_rate":
            if rho > 1.02:
                observation = "⚠️ λ>μ: Queue exploding!"
            elif rho > 0.98:
                observation = "⚡ λ≈μ: Critical instability"
            else:
                observation = "💡 λ<μ: Stable but low util"
        elif strategy_name == "service_rate":
            if queue.service_rate > queue_params[1] * 1.5:
                observation = "💰 High service rate needed!"
            elif abs(rho - 1.0) < 0.05:
                observation = "🎯 Close to ρ=1, very sensitive"
            else:
                observation = "📈 Adjusting service capacity"
        elif strategy_name == "balanced":
            if abs(rho - 1.0) < 0.02:
                observation = "🎲 Attempting stable ρ=1"
            elif rho > 1.0:
                observation = "🔥 Still unstable despite balance"
            else:
                observation = "⚖️ Balancing λ and μ"
        else:  # demonstrate_instability
            if step < 200:
                observation = "📈 Pushing toward instability"
            elif step < 400:
                observation = "📉 Demonstrating recovery"
            else:
                observation = "🔄 Cycle complete"
        
        print(f"{step:4d} │ {queue.arrival_rate:5.2f} │ {queue.service_rate:5.2f} │ "
              f"{rho:5.3f} │ {queue_len:5d} │ {util*100:5.1f} │ {observation}")
    
    # Final analysis
    final_stats = queue.get_statistics()
    final_rho = queue.arrival_rate / queue.service_rate
    
    print("\n📊 FINAL ANALYSIS:")
    print(f"   Final ρ: {final_rho:.3f}")
    print(f"   Final utilization: {final_stats['avg_utilization']:.1%}")
    print(f"   Final queue length: {final_stats['queue_length']}")
    print(f"   Average wait time: {final_stats['avg_wait_time']:.2f}")
    
    if strategy_name == "arrival_rate":
        print("\n💡 KEY INSIGHT: With fixed μ, achieving ρ=1 requires λ=μ exactly.")
        print("   Any λ>μ leads to instability. Any λ<μ gives lower utilization.")
        print("   Perfect ρ=1 is impossible to maintain in practice!")
        
    elif strategy_name == "service_rate":
        print("\n💡 KEY INSIGHT: Achieving high utilization with fixed λ requires")
        print("   very precise service rates. Small errors lead to instability.")
        print("   This shows why service capacity planning is critical!")
        
    elif strategy_name == "balanced":
        print("\n💡 KEY INSIGHT: Even adjusting both parameters, stable ρ=1")
        print("   is extremely difficult. Any small perturbation causes problems.")
        print("   Real systems aim for ρ≈0.8-0.9 for safety margin!")
        
    else:  # demonstrate_instability
        print("\n💡 KEY INSIGHT: This shows the queue explosion when ρ>1.")
        print("   Notice how quickly queues grow and how long recovery takes.")
        print("   This is why traffic intensity must stay below 1!")

def main():
    print("🎓 M/M/1 QUEUEING THEORY EDUCATIONAL SIMULATOR")
    print("=" * 70)
    print("This demonstration shows why ρ=1 (100% utilization) is problematic")
    print("and explores different strategies for approaching this theoretical limit.")
    print()
    
    demos = [
        ("arrival_rate", "Show instability when only adjusting λ", (1.5, 2.0)),
        ("service_rate", "Show required service rates when only adjusting μ", (2.0, 1.5)),
        ("balanced", "Attempt stable ρ=1 by adjusting both λ and μ", (1.8, 2.2)),
        ("demonstrate_instability", "Educational demo of ρ>1 queue explosion", (2.5, 2.0))
    ]
    
    for i, (strategy, description, params) in enumerate(demos, 1):
        print(f"\n🔹 DEMONSTRATION {i}/4")
        demonstrate_strategy(strategy, description, params)
        
        if i < len(demos):
            print(f"\n{'─' * 70}")
            input("Press Enter to continue to next demonstration...")
    
    print(f"\n{'=' * 70}")
    print("🎉 EDUCATIONAL DEMONSTRATION COMPLETE!")
    print()
    print("📚 SUMMARY OF KEY LESSONS:")
    print("1. ρ=1 is theoretically possible but practically impossible to maintain")
    print("2. Any ρ>1 leads to unbounded queue growth (instability)")
    print("3. Achieving high utilization requires either:")
    print("   • Very precise parameter control (impractical)")
    print("   • High service capacity (expensive)")
    print("   • Lower target utilization (recommended: ρ≈0.8-0.9)")
    print()
    print("4. Real queueing systems build in safety margins to avoid instability")
    print("5. Small perturbations near ρ=1 have large consequences")
    print()
    print("🚀 Try the interactive simulator: python3 main.py -a 2.0 -s 2.1 --optimize")
    print("   Use [T] key to cycle through different optimization strategies!")

if __name__ == "__main__":
    main()