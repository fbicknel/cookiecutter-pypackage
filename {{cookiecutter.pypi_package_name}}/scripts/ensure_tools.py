#!/usr/bin/env python3
import sys, subprocess

need = ["pipdeptree", "pip-tools", "tox", "pytest"]
out = subprocess.run([sys.executable, "-m", "pip", "list", "--format=freeze"],
                     capture_output=True, text=True).stdout
installed = {line.split("==")[0].lower() for line in out.splitlines() if "==" in line}
to_install = [p for p in need if p.lower() not in installed]

if to_install:
    print("Installing:", " ".join(to_install))
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + to_install)
else:
    print("Tools present.")
