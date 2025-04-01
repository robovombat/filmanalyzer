# [STEP: X.Z.2 - Final Console Feedback Fix | INITIAL: 2025-04-01 18:20 | MODIFIED: 2025-04-01 18:21]
# CHANGES:
# - Removed unsupported flush kwarg
# - Added stdout=subprocess.PIPE to allow output redirection

import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install as rich_traceback
from importlib.util import find_spec

rich_traceback()
console = Console()

def get_required_packages(path="requirements.txt") -> list:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def check_and_install(package: str):
    import_name = package.split("==")[0].replace("-", "_")
    if find_spec(import_name) is None:
        console.print(f"⚠️ [yellow]'{package}' not found → installing...[/yellow]")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                check=True,
                text=True
            )
            console.print(f"✅ [green]{package} installed![/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"❌ [red]Failed to install {package}[/red]")
            raise e
    else:
        console.print(f"✅ [green]{package} already installed[/green]")

def main():
    console.print(Panel("🔍 [bold cyan]Checking Project Dependencies...[/bold cyan]", expand=False))

    try:
        packages = get_required_packages()
    except FileNotFoundError:
        console.print("[red]❌ requirements.txt not found![/red]")
        sys.exit(1)

    for package in packages:
        check_and_install(package)

    console.print("\n🎉 [bold green]All dependencies satisfied! You're ready to go![/bold green]")

if __name__ == "__main__":
    main()
