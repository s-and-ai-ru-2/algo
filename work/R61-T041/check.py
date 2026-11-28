"""
R61-T041 checker — extracts the Python code block from the article, runs it
with the system Python 3 interpreter, and asserts the expected output.

Usage:
    python3 work/R61-T041/check.py

Exits non-zero when any assertion fails or a subprocess fails.
"""

import re
import subprocess
import sys
import tempfile
import os
import platform

ARTICLE = os.path.join(
    os.path.dirname(__file__),
    "../../docs/extra/algorithms/modular-exponentiation-algorithm.md",
)

# ---------------------------------------------------------------------------
# 1. Extract the Python code block from the article
# ---------------------------------------------------------------------------
with open(ARTICLE, encoding="utf-8") as fh:
    source = fh.read()

py_blocks = re.findall(r"```python\n(.*?)```", source, re.DOTALL)
assert py_blocks, "No ```python block found in the article"

py_code = py_blocks[0]

# ---------------------------------------------------------------------------
# 2. Run the extracted code (it already contains assert statements)
# ---------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmpdir:
    src_path = os.path.join(tmpdir, "modexp.py")

    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(py_code)

    run_result = subprocess.run(
        [sys.executable, src_path],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if run_result.returncode != 0:
        print("RUNTIME ERROR / ASSERTION FAILED:")
        print(run_result.stderr)
        print(run_result.stdout)
        sys.exit(1)

    actual = run_result.stdout.rstrip("\n")

# ---------------------------------------------------------------------------
# 3. Assert expected output lines
# ---------------------------------------------------------------------------
expected_lines = [
    "=== Worked example ===",
    "24",
    "=== Boundary: exp = 0 ===",
    "1",
    "=== Boundary: base = 0 ===",
    "0",
    "All assertions passed.",
]
expected = "\n".join(expected_lines)

if actual != expected:
    print("OUTPUT MISMATCH")
    print(f"Expected:\n{expected}")
    print(f"\nActual:\n{actual}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 4. Deliberate wrong-result check: code must fail when result is wrong
# ---------------------------------------------------------------------------
wrong_code = py_code.replace("assert result == 24", "assert result == 999")
with tempfile.TemporaryDirectory() as tmpdir:
    src_path = os.path.join(tmpdir, "modexp_wrong.py")
    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(wrong_code)

    wrong_result = subprocess.run(
        [sys.executable, src_path],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if wrong_result.returncode == 0:
        print("WRONG RESULT CHECK FAILED: deliberate wrong assertion did not fail")
        sys.exit(1)

print("All checks passed.")
print(f"\nActual output:\n{actual}")

# ---------------------------------------------------------------------------
# 5. Save evidence
# ---------------------------------------------------------------------------
evidence_path = os.path.join(os.path.dirname(__file__), "results.txt")

with open(evidence_path, "w", encoding="utf-8") as fh:
    fh.write(f"Tool version: Python {sys.version}\n")
    fh.write(f"Platform: {platform.platform()}\n\n")
    fh.write("Inputs and expected outputs:\n")
    fh.write("  Worked example  — modular_exponentiation(2, 10, 1000) -> 24\n")
    fh.write("  Boundary exp=0  — modular_exponentiation(5, 0, 13)    -> 1\n")
    fh.write("  Boundary base=0 — modular_exponentiation(0, 5, 7)     -> 0\n\n")
    fh.write(f"Expected output:\n{expected}\n\n")
    fh.write(f"Actual output:\n{actual}\n\n")
    fh.write("Deliberate wrong-result check: PASS (assertion correctly raised AssertionError)\n\n")
    fh.write("Status: PASS\n")

print(f"Evidence saved to {evidence_path}")
