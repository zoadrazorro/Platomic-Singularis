"""
Beta v3 Test Runner

Runs all Beta v3 tests with comprehensive reporting.

Usage:
    python run_beta_v3_tests.py              # Run all tests
    python run_beta_v3_tests.py --quick      # Run quick tests only
    python run_beta_v3_tests.py --verbose    # Verbose output
    python run_beta_v3_tests.py --coverage   # With coverage report
"""

import sys
import os
import subprocess
import time
from pathlib import Path


class BetaV3TestRunner:
    """Test runner for Beta v3 system."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tests_dir = self.project_root / "tests"
        self.results = {}
        
    def print_header(self):
        """Print test suite header."""
        print("\n" + "="*80)
        print("SINGULARIS BETA V3 TEST SUITE".center(80))
        print("="*80)
        print(f"Project Root: {self.project_root}")
        print(f"Tests Directory: {self.tests_dir}")
        print("="*80 + "\n")
    
    def print_section(self, title):
        """Print section header."""
        print("\n" + "-"*80)
        print(f"  {title}")
        print("-"*80)
    
    def run_test_file(self, test_file, verbose=False):
        """Run a single test file."""
        print(f"\n▶ Running: {test_file.name}")
        
        cmd = ["pytest", str(test_file), "-v" if verbose else "-q"]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        self.results[test_file.name] = {
            'passed': result.returncode == 0,
            'elapsed': elapsed,
            'output': result.stdout,
            'errors': result.stderr
        }
        
        if result.returncode == 0:
            print(f"  ✅ PASSED ({elapsed:.2f}s)")
        else:
            print(f"  ❌ FAILED ({elapsed:.2f}s)")
            if verbose:
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
        
        return result.returncode == 0
    
    def run_core_tests(self, verbose=False):
        """Run core system tests."""
        self.print_section("CORE SYSTEM TESTS (BeingState, TemporalBinding)")
        
        test_file = self.tests_dir / "test_beta_v3_core.py"
        if test_file.exists():
            return self.run_test_file(test_file, verbose)
        else:
            print(f"  ⚠ Test file not found: {test_file}")
            return False
    
    def run_arbiter_tests(self, verbose=False):
        """Run ActionArbiter tests."""
        self.print_section("ACTION ARBITER TESTS (Phase 2 & 3)")
        
        test_file = self.tests_dir / "test_beta_v3_arbiter.py"
        if test_file.exists():
            return self.run_test_file(test_file, verbose)
        else:
            print(f"  ⚠ Test file not found: {test_file}")
            return False
    
    def run_phase3_tests(self, verbose=False):
        """Run Phase 3 integration tests."""
        self.print_section("PHASE 3 INTEGRATION TESTS")
        
        test_file = self.tests_dir / "test_phase3_integration.py"
        if test_file.exists():
            return self.run_test_file(test_file, verbose)
        else:
            print(f"  ⚠ Test file not found: {test_file}")
            return False
    
    def run_action_arbiter_tests(self, verbose=False):
        """Run original ActionArbiter tests."""
        self.print_section("ORIGINAL ACTION ARBITER TESTS (Phase 2)")
        
        test_file = self.tests_dir / "test_action_arbiter.py"
        if test_file.exists():
            return self.run_test_file(test_file, verbose)
        else:
            print(f"  ⚠ Test file not found: {test_file}")
            return False
    
    def run_all_tests(self, verbose=False, quick=False):
        """Run all test suites."""
        self.print_header()
        
        all_passed = True
        
        # Core tests
        if not self.run_core_tests(verbose):
            all_passed = False
        
        # ActionArbiter tests
        if not self.run_arbiter_tests(verbose):
            all_passed = False
        
        if not quick:
            # Phase 3 integration tests
            if not self.run_phase3_tests(verbose):
                all_passed = False
            
            # Original ActionArbiter tests
            if not self.run_action_arbiter_tests(verbose):
                all_passed = False
        
        return all_passed
    
    def run_with_coverage(self, verbose=False):
        """Run tests with coverage report."""
        self.print_header()
        print("Running tests with coverage analysis...\n")
        
        cmd = [
            "pytest",
            str(self.tests_dir / "test_beta_v3_core.py"),
            str(self.tests_dir / "test_beta_v3_arbiter.py"),
            str(self.tests_dir / "test_phase3_integration.py"),
            "--cov=singularis",
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v" if verbose else "-q"
        ]
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n✅ Coverage report generated in htmlcov/index.html")
        
        return result.returncode == 0
    
    def print_summary(self):
        """Print test results summary."""
        print("\n" + "="*80)
        print("TEST RESULTS SUMMARY".center(80))
        print("="*80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r['passed'])
        failed_tests = total_tests - passed_tests
        total_time = sum(r['elapsed'] for r in self.results.values())
        
        print(f"\nTotal Test Files: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Total Time: {total_time:.2f}s")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for name, result in self.results.items():
                if not result['passed']:
                    print(f"  ❌ {name}")
        
        print("\n" + "="*80)
        
        if failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! 🎉\n")
            return True
        else:
            print(f"\n⚠ {failed_tests} TEST FILE(S) FAILED\n")
            return False


def main():
    """Main entry point."""
    runner = BetaV3TestRunner()
    
    # Parse arguments
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    quick = "--quick" in sys.argv or "-q" in sys.argv
    coverage = "--coverage" in sys.argv or "--cov" in sys.argv
    help_requested = "--help" in sys.argv or "-h" in sys.argv
    
    if help_requested:
        print(__doc__)
        return 0
    
    # Run tests
    if coverage:
        success = runner.run_with_coverage(verbose)
    else:
        success = runner.run_all_tests(verbose, quick)
        runner.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
