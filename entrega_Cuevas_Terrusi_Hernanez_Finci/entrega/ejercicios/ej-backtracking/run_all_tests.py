#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import ast


def load_expected_path(filename):
    """Load expected path from resultados file."""
    resultados_file = Path(__file__).resolve().parent / "resultados" / filename

    if not resultados_file.exists():
        return None

    try:
        content = resultados_file.read_text(encoding="utf-8").strip()
        return ast.literal_eval(content)
    except (ValueError, SyntaxError):
        return None


def run_all_tests():
    """Run laberinto.py with all input files and verify against expected results."""
    set_dir = Path(__file__).resolve().parent / "set_de_datos"

    if not set_dir.exists():
        print(f"Error: Input directory not found: {set_dir}")
        return 1

    input_files = sorted(set_dir.glob("*.txt"))

    if not input_files:
        print("No input files found in set_de_datos directory")
        return 1

    # Print header
    print(f"\n{'Input':<15} {'Status':<8} {'Tiempo':<15}")
    print("-" * 40)

    passed = 0
    failed = 0

    for input_file in input_files:
        filename = input_file.name
        expected_path = load_expected_path(filename)

        if expected_path is None:
            print(f"{filename:<15} {'❌':<8}")
            failed += 1
            continue

        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "laberinto.py"), str(input_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"{filename:<15} {'❌':<8}")
            failed += 1
            continue

        # Parse output: path, tiempo
        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:
            print(f"{filename:<15} {'❌':<8}")
            failed += 1
            continue

        try:
            actual_path = ast.literal_eval(lines[0])
            tiempo = float(lines[1])
        except (ValueError, SyntaxError, IndexError):
            print(f"{filename:<15} {'❌':<8}")
            failed += 1
            continue

        # Compare paths
        status = "✓" if actual_path == expected_path else "❌"
        if actual_path == expected_path:
            passed += 1
        else:
            failed += 1

        print(f"{filename:<15} {status:<8} {tiempo:.6f}s")

    print("-" * 40)
    print(f"Results: {passed}/{len(input_files)} passed\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
