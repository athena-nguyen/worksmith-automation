import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
VENV_DIR = BASE_DIR / ".venv"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
CSV_PATH = BASE_DIR / "data" / "worksmith.csv"

INSTALL_CMD = "python run.py" if sys.platform == "win32" else "python3 install.py"


def main():
    if not VENV_PYTHON.exists():
        print()
        print("ERROR: Setup has not been run yet.")
        print()
        print(f"Please run:  {INSTALL_CMD}")
        print()
        raise SystemExit(1)

    if not CSV_PATH.exists():
        print()
        print("ERROR: Spreadsheet file not found.")
        print()
        print(f"Expected location: {CSV_PATH}")
        print()
        print("Add your worksmith.csv file there and try again.")
        print()
        raise SystemExit(1)

    result = subprocess.run([str(VENV_PYTHON), str(BASE_DIR / "main.py")])

    if result.returncode != 0:
        print()
        print("=" * 50)
        print("  Something went wrong.")
        print()
        print("  Common fixes:")
        print("   - Make sure worksmith.csv is not open in Excel")
        print("   - If your session expired, run the automation")
        print("     again and log in when Firefox opens")
        if sys.platform == "win32":
            print("   - If packages seem broken, re-run: python install.py")
        else:
            print("   - If packages seem broken, re-run: python3 install.py")
        print("=" * 50)
        print()
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
