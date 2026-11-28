"""
R61-T042 checker — extracts the Java code block from the article, compiles it
with javac, runs it, and asserts the expected output.

Usage:
    python3 work/R61-T042/check.py

Exits non-zero when any assertion fails or a subprocess fails.
"""

import re
import subprocess
import sys
import tempfile
import os

ARTICLE = os.path.join(
    os.path.dirname(__file__),
    "../../docs/extra/algorithms/sorting-algorithms/CocktailShakerSort.md",
)

# ---------------------------------------------------------------------------
# 1. Extract the Java code block from the article
# ---------------------------------------------------------------------------
with open(ARTICLE, encoding="utf-8") as fh:
    source = fh.read()

java_blocks = re.findall(r"```java\n(.*?)```", source, re.DOTALL)
assert java_blocks, "No ```java block found in the article"

java_code = java_blocks[0]

# ---------------------------------------------------------------------------
# 2. Compile
# ---------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmpdir:
    src_path = os.path.join(tmpdir, "CocktailShakerSort.java")

    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(java_code)

    compile_result = subprocess.run(
        ["javac", src_path],
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
        ["java", "-cp", tmpdir, "CocktailShakerSort"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if run_result.returncode != 0:
        print("RUNTIME ERROR:")
        print(run_result.stderr)
        sys.exit(1)

    actual = run_result.stdout.rstrip("\n")

# ---------------------------------------------------------------------------
# 4. Assert expected output
# ---------------------------------------------------------------------------
expected_lines = [
    "=== Worked example ===",
    "Sorted array:",
    "1 2 3 4 5 ",
    "=== Boundary: single element ===",
    "Sorted array:",
    "42 ",
    "=== Boundary: already sorted ===",
    "Sorted array:",
    "1 2 3 4 5 ",
]
expected = "\n".join(expected_lines)

if actual != expected:
    print("ASSERTION FAILED")
    print(f"Expected:\n{expected}")
    print(f"\nActual:\n{actual}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 5. Deliberate wrong-result check
# ---------------------------------------------------------------------------
wrong = "5 4 3 2 1 "
if wrong in actual:
    print("WRONG RESULT CHECK FAILED: got reverse order (deliberate wrong result)")
    sys.exit(1)

print("All checks passed.")
print(f"\nActual output:\n{actual}")

# ---------------------------------------------------------------------------
# 6. Save evidence
# ---------------------------------------------------------------------------
evidence_path = os.path.join(os.path.dirname(__file__), "results.txt")
java_ver = subprocess.run(
    ["java", "-version"], capture_output=True, text=True
).stderr.splitlines()[0]

with open(evidence_path, "w", encoding="utf-8") as fh:
    fh.write(f"Tool version: {java_ver}\n")
    fh.write(f"Python: {sys.version}\n\n")
    fh.write("Inputs and expected outputs:\n")
    fh.write("  Worked example     — {5,3,1,4,2}       -> 1 2 3 4 5\n")
    fh.write("  Boundary single    — {42}               -> 42\n")
    fh.write("  Boundary sorted    — {1,2,3,4,5}        -> 1 2 3 4 5\n\n")
    fh.write(f"Expected output:\n{expected}\n\n")
    fh.write(f"Actual output:\n{actual}\n\n")
    fh.write("Status: PASS\n")

print(f"Evidence saved to {evidence_path}")
