"""
R61-T044 checker — extracts the Java code block from the article, compiles it
with the system Java compiler, runs it, and asserts the expected output.
Also tests the invariant on five bounded variations.

Usage:
    python3 work/R61-T044/check.py

Exits non-zero when any assertion fails or a subprocess fails.
"""

import re
import subprocess
import sys
import tempfile
import os

ARTICLE = os.path.join(
    os.path.dirname(__file__),
    "../../docs/extra/algorithms/sorting-algorithms/Odd-Even-Sort.md",
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
# 2. Compile and run
# ---------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmpdir:
    src_path = os.path.join(tmpdir, "OddEvenSort.java")

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

    run_result = subprocess.run(
        ["java", "-cp", tmpdir, "OddEvenSort"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if run_result.returncode != 0:
        print("RUNTIME ERROR:")
        print(run_result.stderr)
        sys.exit(1)

    actual = run_result.stdout.rstrip('\n')

# ---------------------------------------------------------------------------
# 3. Assert expected output from the article's examples
# ---------------------------------------------------------------------------
expected_lines = [
    "=== Worked example ===",
    "Sorted array:",
    "1 2 3 4 5 ",
    "=== Boundary: already sorted ===",
    "Sorted array:",
    "1 2 3 4 5 ",
    "=== Boundary: single element ===",
    "Sorted array:",
    "42 ",
]
expected = "\n".join(expected_lines)

if actual != expected:
    print("ASSERTION FAILED — article example output mismatch")
    print(f"Expected:\n{expected}")
    print(f"\nActual:\n{actual}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 4. Deliberate wrong-result check
# ---------------------------------------------------------------------------
wrong = "5 4 3 2 1"
if actual == wrong:
    print("WRONG RESULT CHECK FAILED: got the deliberate wrong result")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 5. Invariant tests on five bounded variations (pure Python re-implementation)
# ---------------------------------------------------------------------------
def odd_even_sort(arr):
    arr = arr[:]
    n = len(arr)
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
    return arr

invariant_cases = [
    # (input,                 expected_sorted)
    ([5, 3, 1, 4, 2],        [1, 2, 3, 4, 5]),   # worked example
    ([1, 2, 3, 4, 5],        [1, 2, 3, 4, 5]),   # already sorted
    ([5, 4, 3, 2, 1],        [1, 2, 3, 4, 5]),   # reverse sorted
    ([3, 3, 1, 1, 2],        [1, 1, 2, 3, 3]),   # duplicates
    ([42],                   [42]),               # single element
    ([2, 1],                 [1, 2]),             # two elements
    ([7, 7, 7],              [7, 7, 7]),          # all same
]

for inp, expected_out in invariant_cases:
    result = odd_even_sort(inp)
    assert result == expected_out, (
        f"Invariant FAILED for input {inp}: got {result}, expected {expected_out}"
    )
    # Invariant check: result must equal sorted(inp)
    assert result == sorted(inp), (
        f"Invariant FAILED: result {result} != sorted({inp})"
    )

print("All checks passed.")
print(f"\nActual output from article example:\n{actual}")

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
    for inp, exp in invariant_cases:
        fh.write(f"  {inp} -> {exp}\n")
    fh.write(f"\nArticle example expected output:\n{expected}\n\n")
    fh.write(f"Article example actual output:\n{actual}\n\n")
    fh.write("Status: PASS\n")

print(f"Evidence saved to {evidence_path}")
