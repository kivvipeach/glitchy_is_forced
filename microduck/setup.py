"""Download the pinned model and create a local simulation environment."""
from pathlib import Path
import subprocess
import sys
import venv


ROOT = Path(__file__).resolve().parent
REVISION = "b02fdea4902c2b93b7d34a83a6f05da4ececb7d3"
SOURCE = "https://github.com/pollen-robotics/microduck_rl.git"


def main():
    upstream = ROOT / "upstream" / "microduck_rl"
    if upstream.exists():
        revision = subprocess.check_output(
            ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True
        ).strip()
        changes = subprocess.check_output(
            ["git", "-C", str(upstream), "status", "--porcelain"], text=True
        ).strip()
        if revision != REVISION or changes:
            raise RuntimeError("Existing upstream differs from the pinned clean checkout; preserve your changes before setup.")
    else:
        upstream.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", SOURCE, str(upstream)], check=True)
        subprocess.run(["git", "-C", str(upstream), "checkout", "--detach", REVISION], check=True)
    environment = ROOT / ".venv"
    if not environment.exists():
        venv.EnvBuilder(with_pip=True).create(environment)
    python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")], check=True)
    subprocess.run([str(python), str(ROOT / "simulate.py"), "--headless", "--seconds", "10"], check=True)
    print("Setup complete. On Windows, double-click start-simulation.cmd.")


if __name__ == "__main__":
    main()
