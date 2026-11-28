import json, platform, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/extra/algorithms/modular-exponentiation-algorithm.md"
OUT = Path(__file__).resolve().parent

def main() -> int:
    md = DOC.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\s*\n(.*?)```", md, flags=re.DOTALL)
    if not blocks:
        raise RuntimeError("No python block found")
    runner = blocks[0] + "\nassert modular_exponentiation(2, 10, 1000) == 24\nassert modular_exponentiation(5, 0, 13) == 1\n"
    proc = subprocess.run([sys.executable, "-c", runner], capture_output=True, text=True, check=False)
    report = {
        "exit_code": proc.returncode,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "checks": [
            {"args": [2, 10, 1000], "expected": 24, "actual": 24 if proc.returncode == 0 else None},
            {"args": [5, 0, 13], "expected": 1, "actual": 1 if proc.returncode == 0 else None},
        ],
    }
    (OUT / "results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        return proc.returncode
    print("CHECK_OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
