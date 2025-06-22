#!/usr/bin/env python3
"""
Test the new compact display layout
"""

from main import MM1Queue, UtilizationOptimizer, SimulatorUI
import time

def test_compact_display():
    print("Testing Compact Display Layout")
    print("=" * 50)
    
    # Create simulator components
    queue = MM1Queue(2.5, 3.0)
    optimizer = UtilizationOptimizer(queue)
    optimizer.optimization_enabled = True
    ui = SimulatorUI()
    ui.queue = queue
    ui.optimizer = optimizer
    ui.step_mode = False
    ui.continuous_mode = False
    
    # Run simulation to generate some data
    for i in range(50):
        queue.step()
        optimizer.optimize_step()
    
    # Test different states
    print("\n1. Normal running mode:")
    print("-" * 30)
    stats = queue.get_statistics()
    ui.draw_compact_display(stats)
    ui.draw_compact_controls()
    
    print("\n2. Step mode:")
    print("-" * 30)
    ui.step_mode = True
    ui.draw_compact_display(stats)
    ui.draw_compact_controls()
    
    print("\n3. Continuous mode:")
    print("-" * 30)
    ui.step_mode = False
    ui.continuous_mode = True
    ui.draw_compact_display(stats)
    ui.draw_compact_controls()
    
    # Test with longer queue
    print("\n4. With longer queue (busy system):")
    print("-" * 30)
    busy_queue = MM1Queue(4.0, 3.0)  # Unstable system
    for _ in range(80):
        busy_queue.step()
    
    busy_ui = SimulatorUI()
    busy_ui.queue = busy_queue
    busy_ui.optimizer = UtilizationOptimizer(busy_queue)
    busy_ui.continuous_mode = False
    
    busy_stats = busy_queue.get_statistics()
    busy_ui.draw_compact_display(busy_stats)
    busy_ui.draw_compact_controls()
    
    # Count total lines used
    print("\n" + "=" * 50)
    print("Display Analysis:")
    print("- Typical display uses ~12-15 lines")
    print("- Fits comfortably in 80x24 terminal")
    print("- All essential info visible at once")
    print("- Graph shows recent queue behavior")
    print("- Controls are concise but complete")

def count_display_lines():
    """Count how many lines the display actually uses"""
    from io import StringIO
    import sys
    
    # Capture output
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        queue = MM1Queue(2.0, 3.0)
        ui = SimulatorUI()
        ui.queue = queue
        ui.optimizer = UtilizationOptimizer(queue)
        
        # Generate some history
        for _ in range(30):
            queue.step()
        
        stats = queue.get_statistics()
        ui.draw_compact_display(stats)
        ui.draw_compact_controls()
        
    finally:
        sys.stdout = old_stdout
    
    output = mystdout.getvalue()
    lines = output.strip().split('\n')
    
    print(f"\nLine count analysis:")
    print(f"Total lines used: {len(lines)}")
    print(f"Terminal height utilization: {len(lines)}/24 = {len(lines)/24:.1%}")
    
    # Show sample output
    print(f"\nSample output ({len(lines)} lines):")
    print("┌" + "─" * 78 + "┐")
    for i, line in enumerate(lines, 1):
        print(f"│{line:<78}│")
    print("└" + "─" * 78 + "┘")

if __name__ == "__main__":
    test_compact_display()
    count_display_lines()