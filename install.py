import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
VENV_DIR = BASE_DIR / ".venv"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
VENV_PIP = VENV_DIR / ("Scripts/pip.exe" if sys.platform == "win32" else "bin/pip")

MIN_PYTHON = (3, 9)


def main():
    print()
    print("=" * 50)
    print("  Worksmith Automation — First-Time Setup")
    print("=" * 50)
    print()

    if sys.version_info < MIN_PYTHON:
        print(f"ERROR: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required.")
        print(f"       You have Python {sys.version_info.major}.{sys.version_info.minor}.")
        print()
        print("Download the latest version from: https://www.python.org/downloads/")
        raise SystemExit(1)

    print(f"Python {sys.version_info.major}.{sys.version_info.minor} found.")
    print()

    print("Step 1 of 3: Creating a private Python environment...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    print("Done.")
    print()

    print("Step 2 of 3: Installing required packages...")
    subprocess.run([str(VENV_PIP), "install", "--upgrade", "pip", "--quiet"], check=True)
    subprocess.run([str(VENV_PIP), "install", "-r", "requirements.txt"], check=True)
    print("Done.")
    print()

    print("Step 3 of 3: Installing Firefox for the automation...")
    print("(This downloads about 100 MB and may take a few minutes.)")
    subprocess.run([str(VENV_PYTHON), "-m", "playwright", "install", "firefox"], check=True)
    print("Done.")
    print()

    print("=" * 50)
    print("  Setup complete!")
    print()
    print("  To run the automation:")
    if sys.platform == "win32":
        print("    python run.py")
    else:
        print("    python3 run.py")
    print()
    print("  The first run will open Firefox and ask you")
    print("  to log in to Worksmith. After that, your")
    print("  session is saved automatically.")
    print("=" * 50)
    print()


if __name__ == "__main__":
    main()
