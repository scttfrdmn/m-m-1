#!/usr/bin/env python3
"""
Test CLI functionality of the enhanced M/M/1 simulator
"""

import subprocess
import time
import signal
import os

def test_cli_help():
    """Test the help command"""
    print("Testing CLI help...")
    result = subprocess.run(['python3', 'main.py', '--help'], 
                          capture_output=True, text=True, timeout=5)
    
    if result.returncode == 0 and 'M/M/1 Queue Simulator' in result.stdout:
        print("✅ Help command works")
        return True
    else:
        print(f"❌ Help command failed: {result.stderr}")
        return False

def test_cli_parameters():
    """Test running with command line parameters"""
    print("Testing CLI with parameters...")
    
    # Start the process
    proc = subprocess.Popen(['python3', 'main.py', '-a', '2.0', '-s', '3.0'], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Let it run for 2 seconds
    time.sleep(2)
    
    # Terminate gracefully
    proc.terminate()
    stdout, stderr = proc.communicate(timeout=3)
    
    if 'Starting with λ=2.0, μ=3.0' in stdout or 'Starting with λ=2.0, μ=3.0' in stderr:
        print("✅ CLI parameters work")
        return True
    else:
        print(f"❌ CLI parameters failed")
        print(f"stdout: {stdout[:200]}")
        print(f"stderr: {stderr[:200]}")
        return False

def test_cli_optimization():
    """Test optimization flag"""
    print("Testing optimization flag...")
    
    proc = subprocess.Popen(['python3', 'main.py', '-a', '1.5', '-s', '2.0', '--optimize'], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    time.sleep(2)
    proc.terminate()
    stdout, stderr = proc.communicate(timeout=3)
    
    output = stdout + stderr
    if 'Optimization enabled' in output:
        print("✅ Optimization flag works")
        return True
    else:
        print(f"❌ Optimization flag failed")
        return False

def test_direct_import():
    """Test importing and using the classes directly"""
    print("Testing direct import...")
    
    try:
        from main import MM1Queue, UtilizationOptimizer
        
        # Test basic functionality
        queue = MM1Queue(2.0, 3.0)
        optimizer = UtilizationOptimizer(queue)
        
        # Run a few steps
        for _ in range(10):
            queue.step()
            optimizer.optimize_step()
        
        stats = queue.get_statistics()
        
        if stats['total_customers'] > 0:
            print("✅ Direct import and usage works")
            return True
        else:
            print("❌ Direct import failed - no customers processed")
            return False
            
    except Exception as e:
        print(f"❌ Direct import failed: {e}")
        return False

def main():
    print("Testing M/M/1 CLI Enhanced Simulator")
    print("=" * 50)
    
    # Change to the correct directory
    os.chdir('/Users/scttfrdmn/src/m-m-1')
    
    tests = [
        test_cli_help,
        test_cli_parameters, 
        test_cli_optimization,
        test_direct_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All CLI tests passed!")
        print("\nYou can now use:")
        print("  python3 main.py                              # Interactive mode")
        print("  python3 main.py -a 2.0 -s 3.0               # With parameters")
        print("  python3 main.py -a 2.0 -s 3.0 --optimize    # With optimization")
        print("  python3 main.py -a 2.0 -s 3.0 --continuous  # Continuous mode")
    else:
        print("❌ Some tests failed")

if __name__ == "__main__":
    main()