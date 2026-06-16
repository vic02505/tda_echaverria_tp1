#!/usr/bin/env python3

from pathlib import Path
import sys
import time


def load_expected_results():
    """Load expected results from resultados.txt"""
    resultados_file = Path(__file__).resolve().parent / "inputs" / "resultados.txt"

    if not resultados_file.exists():
        print(f"Error: Results file not found: {resultados_file}")
        return None

    content = resultados_file.read_text(encoding="utf-8").strip()
    try:
        expected = [int(x.strip()) for x in content.split(",")]
        return expected
    except ValueError:
        print(f"Error: Invalid format in resultados.txt")
        return None


REPETITIONS = 20

def extract_values(output):
    """Extract moneda falsa and pesadas from output."""
    moneda = pesadas = None
    for line in output.split("\n"):
        if line.startswith("Moneda falsa:"):
            moneda = int(line.split(":")[1].strip())
        elif line.startswith("Pesadas:"):
            pesadas = int(line.split(":")[1].strip())
    return moneda, pesadas


def run_all_inputs():
    """Run monedas.py with all input files and verify against expected results."""
    inputs_dir = Path(__file__).resolve().parent / "inputs"

    if not inputs_dir.exists():
        print(f"Error: Input directory not found: {inputs_dir}")
        return 1

    input_files = sorted(inputs_dir.glob("*.txt"))
    input_files = [f for f in input_files if f.name != "resultados.txt"]

    if not input_files:
        print("No input files found in inputs directory")
        return 1

    expected_results = load_expected_results()
    if expected_results is None:
        return 1

    if len(expected_results) != len(input_files):
        print(f"Error: Expected {len(input_files)} results but got {len(expected_results)}")
        return 1

    sys.path.insert(0, str(Path(__file__).parent))
    from monedas import encontrar_moneda_falsa, leer_monedas

    print(f"\n{'Input':<12} {'Expected':<10} {'Actual':<10} {'Status':<8} {'Pesadas':<10} {'Tiempo avg (us)':<16}")
    print("-" * 78)

    passed = 0
    failed = 0

    for idx, input_file in enumerate(input_files):
        expected_coin = expected_results[idx]

        monedas = leer_monedas(input_file)
        encontrar_moneda_falsa(monedas)  # warm-up

        tiempos = []
        actual_coin = pesadas = None
        for _ in range(REPETITIONS):
            t0 = time.perf_counter()
            actual_coin, pesadas = encontrar_moneda_falsa(monedas)
            t1 = time.perf_counter()
            tiempos.append(t1 - t0)

        avg_us = (sum(tiempos) / len(tiempos)) * 1e6

        status = "OK" if actual_coin == expected_coin else "FAIL"
        if actual_coin == expected_coin:
            passed += 1
        else:
            failed += 1

        print(f"{input_file.name:<12} {expected_coin:<10} {actual_coin:<10} {status:<8} {pesadas:<10} {avg_us:<16.2f}")

    print("-" * 70)
    print(f"Results: {passed}/{len(input_files)} passed")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run_all_inputs())
