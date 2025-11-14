@echo off
REM Quick test script for Beta v3 system
REM Runs in test mode without requiring API keys or Skyrim

echo ================================================================================
echo SINGULARIS BETA V3 - QUICK TEST
echo ================================================================================
echo.
echo Running Beta v3 in test mode for 30 seconds...
echo - No API keys required
echo - No Skyrim required
echo - Mock AGI for testing
echo.

python run_beta_v3.py --test-mode --no-gpt5 --duration 30 --stats-interval 10

echo.
echo ================================================================================
echo Test complete! Check output above for results.
echo ================================================================================
echo.
echo To run with GPT-5 coordination:
echo   1. Set OPENAI_API_KEY environment variable
echo   2. Run: python run_beta_v3.py --test-mode --duration 60
echo.
echo To run full test suite:
echo   python run_beta_v3_tests.py
echo.
pause
