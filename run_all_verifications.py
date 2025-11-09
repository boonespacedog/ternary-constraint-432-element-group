#!/usr/bin/env python3
"""
432 Doubly Stochastic Matrices Over F₃
Paper: "Doubly Stochastic Matrices Over F₃: Binary Trace Stratification"
Repository: https://github.com/boonespacedog/ternary-constraint-432-element-group
Updated: 2025-11-09

Master Verification Runner
Executes all GAP scripts and generates complete output suite
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

# === CONFIG ===
GAP_DIR = Path(__file__).parent / "gap"
OUTPUTS_DIR = Path(__file__).parent / "outputs"
GAP_BINARY = "gap"  # Assumes GAP is in PATH

# Scripts to run (in order)
SCRIPTS = [
    {
        "name": "Row Stochastic (432)",
        "script": "enum_row_stochastic.g",
        "output": "row_stochastic_432.csv",
        "description": "Enumerate all row-stochastic matrices"
    },
    {
        "name": "Doubly Stochastic (54)",
        "script": "enum_doubly_stochastic.g",
        "output": "doubly_stochastic_54.json",
        "description": "Enumerate doubly-stochastic subset"
    },
    {
        "name": "Trace Stratification",
        "script": "trace_stratification_analysis.g",
        "output": "trace_stratification.json",
        "description": "Analyze binary trace stratification"
    },
    {
        "name": "Group Structure Verification",
        "script": "verify_group_structures.g",
        "output": "group_structure_verification.json",
        "description": "Verify group closure and structure"
    }
]


def run_gap_script(script_name: str) -> dict:
    """Execute single GAP script and capture output"""
    script_path = GAP_DIR / script_name

    print(f"\n  Running: {script_name}...")
    start_time = time.time()

    try:
        result = subprocess.run(
            [GAP_BINARY, "-q", str(script_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        elapsed = time.time() - start_time

        return {
            "script": script_name,
            "success": result.returncode == 0,
            "elapsed_sec": round(elapsed, 2),
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "script": script_name,
            "success": False,
            "error": "Timeout (>300s)"
        }
    except Exception as e:
        return {
            "script": script_name,
            "success": False,
            "error": str(e)
        }


def main():
    """Run all verification scripts"""
    print("=" * 60)
    print("432 Doubly Stochastic Matrix Verification Suite")
    print("=" * 60)

    OUTPUTS_DIR.mkdir(exist_ok=True)

    results = []
    success_count = 0

    for item in SCRIPTS:
        print(f"\n[{item['name']}]")
        print(f"  Description: {item['description']}")

        result = run_gap_script(item["script"])
        results.append(result)

        if result["success"]:
            success_count += 1
            output_path = OUTPUTS_DIR / item["output"]
            if output_path.exists():
                print(f"  ✓ Output generated: {item['output']}")
            else:
                print(f"  ⚠ Script succeeded but output not found")
        else:
            print(f"  ✗ FAILED: {result.get('error', 'See logs')}")

    # Generate summary report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = OUTPUTS_DIR / f"verification_run_log_{timestamp}.json"

    summary = {
        "timestamp": timestamp,
        "total_scripts": len(SCRIPTS),
        "successful": success_count,
        "failed": len(SCRIPTS) - success_count,
        "results": results
    }

    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{len(SCRIPTS)} scripts succeeded")
    print(f"Log saved: {summary_path}")
    print("=" * 60)

    return 0 if success_count == len(SCRIPTS) else 1


if __name__ == "__main__":
    exit(main())
