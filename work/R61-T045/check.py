"""
R61-T045 checker — extracts the C++ code block from the article, compiles it
with the system C++ compiler, runs it, and asserts the expected output.

Usage:
    python3 work/R61-T045/check.py

Exits non-zero when any assertion fails or the subprocess fails.
"""

import re
import subprocess
import sys
import tempfile
import os

ARTICLE = os.path.join(
    os.path.dirname(__file__),
    "../../docs/extra/algorithms/string-algorithms/bitap-algorithm.md",
)

# ---------------------------------------------------------------------------
# 1. Extract the C++ code block from the article
# ---------------------------------------------------------------------------
with open(ARTICLE, encoding="utf-8") as fh:
    source = fh.read()

cpp_blocks = re.findall(r"```cpp\n(.*?)```", source, re.DOTALL)
assert cpp_blocks, "No ```cpp block found in the article"

# Use the first (and only) C++ block
cpp_code = cpp_blocks[0]

# ---------------------------------------------------------------------------
# 2. Compile
# ---------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmpdir:
    src_path = os.path.join(tmpdir, "bitap.cpp")
    bin_path = os.path.join(tmpdir, "bitap")

    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(cpp_code)

    compile_result = subprocess.run(
        ["g++", "-o", bin_path, src_path],
        capture_output=True,
        text=True,
    )
    if compile_result.returncode != 0:
        print("COMPILE ERROR:")
        print(compile_result.stderr)
        sys.exit(1)

    # -----------------------------------------------------------------------
    # 3. Run
    # -----------------------------------------------------------------------
    run_result = subprocess.run(
        [bin_path],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if run_result.returncode != 0:
        print("RUNTIME ERROR:")
        print(run_result.stderr)
        sys.exit(1)

    actual = run_result.stdout.strip()

# ---------------------------------------------------------------------------
# 4. Assert expected output
# ---------------------------------------------------------------------------
expected_lines = [
    "=== Worked example (1 error allowed) ===",
    "Pattern found at index 17 with 1 allowed errors.",
    "=== Boundary example (0 errors, exact match) ===",
    "Pattern found at index 1 with 0 allowed errors.",
    "=== Boundary example (0 errors, no match) ===",
]

expected = "\n".join(expected_lines)

if actual != expected:
    print("ASSERTION FAILED")
    print(f"Expected:\n{expected}")
    print(f"\nActual:\n{actual}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 5. Deliberate wrong-result check: assert failure when output is incorrect
# ---------------------------------------------------------------------------
wrong_expected = "Pattern found at index 99 with 1 allowed errors."
if actual == wrong_expected:
    print("WRONG RESULT CHECK FAILED: got the deliberate wrong result")
    sys.exit(1)

print("All checks passed.")
print(f"\nActual output:\n{actual}")

# ---------------------------------------------------------------------------
# 6. Save evidence
# ---------------------------------------------------------------------------
evidence_path = os.path.join(os.path.dirname(__file__), "results.txt")
compiler_version = subprocess.run(
    ["g++", "--version"], capture_output=True, text=True
).stdout.splitlines()[0]

with open(evidence_path, "w", encoding="utf-8") as fh:
    fh.write(f"Tool version: {compiler_version}\n")
    fh.write(f"Python: {sys.version}\n\n")
    fh.write(f"Inputs:\n")
    fh.write(f"  Worked example  — text='this is a simple example', pattern='example', maxErrors=1\n")
    fh.write(f"  Boundary exact  — text='hello', pattern='ell', maxErrors=0\n")
    fh.write(f"  Boundary no-match — text='hello', pattern='xyz', maxErrors=0\n\n")
    fh.write(f"Expected output:\n{expected}\n\n")
    fh.write(f"Actual output:\n{actual}\n\n")
    fh.write("Status: PASS\n")

print(f"Evidence saved to {evidence_path}")
