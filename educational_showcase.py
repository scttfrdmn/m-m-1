#!/usr/bin/env python3
"""
Educational Feature Showcase - Quick demonstration of new capabilities
"""

from main import MM1Queue, SimulatorUI, UtilizationOptimizer

def showcase_educational_features():
    print("🎓 M/M/1 EDUCATIONAL FEATURES SHOWCASE")
    print("=" * 65)
    print("Demonstrating the enhanced educational capabilities")
    print()
    
    # Create a moderately loaded system
    queue = MM1Queue(arrival_rate=2.2, service_rate=3.0)  # ρ = 0.73
    ui = SimulatorUI()
    ui.queue = queue
    ui.optimizer = UtilizationOptimizer(queue)
    
    print("🔬 Running simulation to build educational data...")
    print("   (This shows progression from unreliable to reliable statistics)")
    print()
    
    # Show progression through confidence levels
    milestones = [
        (15, "Early Stage - Statistics Not Yet Reliable"),
        (35, "Building Confidence - Use With Caution"), 
        (75, "Good Sample Size - Moderately Reliable"),
        (120, "Steady State - Reliable Statistics")
    ]
    
    current_step = 0
    for target_customers, description in milestones:
        # Run simulation to target
        while queue.customers_served < target_customers:
            queue.step()
            current_step += 1
        
        print(f"📊 {description}")
        print("-" * 50)
        
        # Show the educational display
        stats = queue.get_statistics()
        ui.draw_educational_insights(stats)
        print()
    
    print("🎯 KEY EDUCATIONAL INSIGHTS DEMONSTRATED:")
    print()
    
    print("1. 📐 LITTLE'S LAW VERIFICATION")
    print("   • Shows live verification that L = λ × W")
    print("   • Students see the fundamental queueing relationship")
    print("   • ✅ indicates when the relationship holds")
    print()
    
    print("2. 👥 INDIVIDUAL CUSTOMER EXPERIENCES")
    print("   • Tracks specific customers through their journey")
    print("   • Shows wait time + service time = total time")
    print("   • Makes abstract averages concrete")
    print()
    
    print("3. ⏱️ TIME BREAKDOWN ANALYSIS")
    print("   • Separates wait time from service time")
    print("   • Shows where customer time is actually spent")
    print("   • Connects to capacity planning decisions")
    print()
    
    print("4. 📈 STATISTICAL CONFIDENCE")
    print("   • Progress bar shows measurement reliability")
    print("   • Students learn when to trust statistics")
    print("   • Teaches importance of adequate sample size")
    print()
    
    print("🚀 USAGE FOR EDUCATORS:")
    print()
    print("• Classroom Demo:")
    print("  python3 main.py -a 2.0 -s 3.0")
    print("  Watch Little's Law verification in real-time")
    print()
    print("• Individual vs Average Exploration:")
    print("  python3 main.py -a 3.0 -s 2.5  # Unstable system")
    print("  See wide variation in individual customer experiences")
    print()
    print("• Statistical Learning:")
    print("  python3 main.py -a 1.5 -s 2.0")
    print("  Watch confidence build from 'Very Low' to 'High'")
    print()
    
    print("📚 EDUCATIONAL VALUE TRANSFORMATION:")
    print("• Before: Students saw parameter effects")
    print("• After: Students understand queueing relationships")
    print("• Impact: Theory becomes practical and verifiable")

if __name__ == "__main__":
    showcase_educational_features()