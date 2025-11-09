#!/usr/bin/env python3
"""
File: run_all_gap_scripts.py
Purpose: Execute all GAP scripts sequentially with proper delays
Author: Oksana Sudoma, Claude (Anthropic)
Date: 2025-11-09

TDD Protocol:
- Sequential execution (no parallel)
- 0.5s delays between scripts (prevent IDE crashes)
- Capture all stdout/stderr
- Save execution log
- Report success/failure for each script
"""

import subprocess
import time
import json
import datetime
import sys
from pathlib import Path

# === CONFIG ===
GAP_PATH = "/Users/mac/Downloads/gap-4.12.2/gap"
BASE_PATH = Path("/Users/mac/Desktop/egg-paper/ternary-constraint-432-element-group/paper1_432_agl23")
GAP_DIR = BASE_PATH / "gap"
OUTPUTS_DIR = BASE_PATH / "outputs"

# Scripts to execute in order
SCRIPTS = [
    "enum_row_stochastic.g",
    "enum_doubly_stochastic_fixed.g",
    "trace_stratification_analysis.g",
    "verify_group_structures.g"
]

# Expected outputs (for verification)
EXPECTED_OUTPUTS = {
    "enum_row_stochastic.g": "row_stochastic_432.csv",
    "enum_doubly_stochastic_fixed.g": "doubly_stochastic_54.json",
    "trace_stratification_analysis.g": "trace_stratification.json",
    "verify_group_structures.g": "group_structure_verification.json"
}

def run_gap_script(script_name):
    """
    Execute a single GAP script and capture output.

    Args:
        script_name: Name of GAP script file

    Returns:
        dict: Execution results
    """
    script_path = GAP_DIR / script_name

    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        result = subprocess.run(
            [GAP_PATH, "-q", str(script_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        elapsed = time.time() - start_time

        # Print stdout
        if result.stdout:
            print(result.stdout)

        # Print stderr (if any)
        if result.stderr:
            print(f"STDERR:\n{result.stderr}", file=sys.stderr)

        success = result.returncode == 0

        return {
            "script": script_name,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "elapsed_seconds": round(elapsed, 2),
            "success": success,
            "timestamp": datetime.datetime.now().isoformat()
        }

    except subprocess.TimeoutExpired:
        print(f"ERROR: {script_name} timed out after 5 minutes")
        return {
            "script": script_name,
            "returncode": -1,
            "stdout": "",
            "stderr": "Timeout after 300 seconds",
            "elapsed_seconds": 300.0,
            "success": False,
            "timestamp": datetime.datetime.now().isoformat()
        }

    except Exception as e:
        print(f"ERROR: {script_name} failed with exception: {e}")
        return {
            "script": script_name,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "elapsed_seconds": 0.0,
            "success": False,
            "timestamp": datetime.datetime.now().isoformat()
        }

def verify_outputs(script_name):
    """
    Verify that expected output file exists.

    Args:
        script_name: Name of GAP script

    Returns:
        bool: True if output exists
    """
    expected_output = EXPECTED_OUTPUTS.get(script_name)
    if not expected_output:
        return True  # No expected output defined

    output_path = OUTPUTS_DIR / expected_output
    exists = output_path.exists()

    if exists:
        print(f"✓ Output file created: {expected_output}")
    else:
        print(f"✗ Output file missing: {expected_output}")

    return exists

def main():
    """
    Main execution loop.
    """
    print("="*60)
    print("GAP SCRIPT EXECUTION SUITE")
    print("="*60)
    print(f"Base path: {BASE_PATH}")
    print(f"GAP executable: {GAP_PATH}")
    print(f"Scripts to run: {len(SCRIPTS)}")
    print(f"Execution order: {', '.join(SCRIPTS)}")
    print("="*60)

    # Ensure outputs directory exists
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # Results accumulator
    all_results = []
    failed_scripts = []

    # Execute each script sequentially
    for i, script in enumerate(SCRIPTS):
        print(f"\n[{i+1}/{len(SCRIPTS)}] Executing {script}...")

        # Run script
        result = run_gap_script(script)
        all_results.append(result)

        # Verify output
        output_verified = verify_outputs(script)
        result["output_verified"] = output_verified

        # Check for failure
        if not result["success"]:
            print(f"\n✗ {script} FAILED (return code: {result['returncode']})")
            failed_scripts.append(script)
            break  # Stop on first failure
        elif not output_verified:
            print(f"\n✗ {script} completed but output missing")
            failed_scripts.append(script)
            break
        else:
            print(f"\n✓ {script} completed successfully ({result['elapsed_seconds']}s)")

        # Delay before next script (crash prevention)
        if i < len(SCRIPTS) - 1:
            print(f"Pausing 0.5 seconds before next script...")
            time.sleep(0.5)

    # Save execution log
    log_file = OUTPUTS_DIR / f"verification_run_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w') as f:
        json.dump({
            "metadata": {
                "date": datetime.datetime.now().isoformat(),
                "gap_path": GAP_PATH,
                "scripts_executed": len(all_results),
                "scripts_planned": len(SCRIPTS),
                "all_succeeded": len(failed_scripts) == 0
            },
            "results": all_results
        }, f, indent=2)

    print(f"\nExecution log saved to: {log_file}")

    # Final summary
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)

    success_count = sum(1 for r in all_results if r["success"])
    print(f"Scripts executed: {len(all_results)}/{len(SCRIPTS)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(failed_scripts)}")

    if failed_scripts:
        print(f"\nFailed scripts: {', '.join(failed_scripts)}")
        print("\n✗ VERIFICATION INCOMPLETE")
        return 1
    else:
        print("\n✓ ALL SCRIPTS COMPLETED SUCCESSFULLY")
        return 0

if __name__ == "__main__":
    sys.exit(main())
