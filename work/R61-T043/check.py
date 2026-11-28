"""
R61-T043 checker — extracts the Python code block from the article, runs it
with the system Python 3 interpreter, and asserts the expected output.

Usage:
    python3 work/R61-T043/check.py

Exits non-zero when any assertion fails or a subprocess fails.
"""

import re
import subprocess
import sys
import tempfile
import os

ARTICLE = os.path.join(
    os.path.dirname(__file__),
    "../../docs/extra/Queue/Problem-Practice.md",
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
# 2. Run the extracted code
# ---------------------------------------------------------------------------
with tempfile.TemporaryDirectory() as tmpdir:
    src_path = os.path.join(tmpdir, "queue_example.py")

    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(py_code)

    run_result = subprocess.run(
        [sys.executable, src_path],
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
# 3. Assert expected output
# ---------------------------------------------------------------------------
expected_lines = [
    "=== Worked example ===",
    "Two-stack: [1, 2, 3]",
    "Deque: [1, 2, 3]",
    "=== Boundary: single element ===",
    "Two-stack: 42",
    "Deque: 42",
    "=== Boundary: interleaved ops ===",
    "Two-stack: 10, 20, 30",
    "Deque: 10, 20, 30",
]
expected = "\n".join(expected_lines)

if actual != expected:
    print("ASSERTION FAILED")
    print(f"Expected:\n{expected}")
    print(f"\nActual:\n{actual}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 4. Deliberate wrong-result check
# ---------------------------------------------------------------------------
wrong = "Two-stack: [3, 2, 1]"
if wrong in actual:
    print("WRONG RESULT CHECK FAILED: got reverse order (deliberate wrong result)")
    sys.exit(1)

print("All checks passed.")
print(f"\nActual output:\n{actual}")

# ---------------------------------------------------------------------------
# 5. Save evidence
# ---------------------------------------------------------------------------
evidence_path = os.path.join(os.path.dirname(__file__), "results.txt")
py_version = sys.version

with open(evidence_path, "w", encoding="utf-8") as fh:
    fh.write(f"Tool version: Python {py_version}\n\n")
    fh.write("Inputs:\n")
    fh.write("  Worked example     — enqueue(1,2,3), dequeue all\n")
    fh.write("  Boundary single    — enqueue(42), dequeue\n")
    fh.write("  Boundary interleaved — enqueue(10,20), dequeue, enqueue(30), dequeue, dequeue\n\n")
    fh.write(f"Expected output:\n{expected}\n\n")
    fh.write(f"Actual output:\n{actual}\n\n")
    fh.write("Status: PASS\n")

print(f"Evidence saved to {evidence_path}")
