import os
import sys
import subprocess


def run(command: str, root=False):
    cmd = ['bash', '-c', command]
    if root:
        cmd = ['sudo'] + cmd
    proc = subprocess.run(cmd, capture_output=True)

    if proc.returncode == 0:
        return str(proc.stdout, 'utf-8'), None
    else:
        return str(proc.stdout, 'utf-8'), str(proc.stderr, 'utf-8')


def sudo(command: str):
    return run(command, root=True)
