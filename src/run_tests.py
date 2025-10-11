import subprocess
import sys
import os

def run_tests():
    """Running all test suites systematically"""
    print("STARTING COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Created by: Tatenda Sikweche")
    print("Assignment: ISYS3015 Assessment 2 - Quality Assurance Engineer")
    print("=" * 60)
    
    test_files = [
        "tests/test_security.py",
        "tests/test_database.py", 
        "tests/test_functionality.py",
        "tests/test_simple.py"
    ]
    
    all_passed = True
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n RUNNING: {test_file}")
            print("-" * 40)
            
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, "-v", "--tb=short"
            ], capture_output=True, text=True)
            
            print(result.stdout)
            if result.stderr:
                print("ERRORS:", result.stderr)
                
            if result.returncode != 0:
                all_passed = False
        else:
            print(f"  File not found: {test_file}")
    
    print("=" * 60)
    if all_passed:
        print(" ALL TEST SUITES PASSED!")
        print(" Your Code Review findings have been validated!")
    else:
        print(" SOME TESTS FAILED - Check details above")
        
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)