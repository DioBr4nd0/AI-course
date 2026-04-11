import subprocess
import shlex
import os

ALLOWED_BASE = {"python3", "python", "pip3", "pip", "ls", "mkdir", "echo", "cat", ".venv"}

def execute_shell_command(command_str: str) -> str:
    try:
        args = shlex.split(command_str)
        if not args:
            return "ERROR: Empty command"
        
        cmd = args[0]
        if cmd.startswith(".venv"):
            pass
        elif cmd not in ALLOWED_BASE:
            return f"SECURITY ERROR: Command '{cmd}' not allowed"
        
        result = subprocess.run(
            command_str,
            shell=True,
            capture_output=True,
            text=True,
            cwd="workspace",
            timeout=60
        )
        if result.returncode == 0:
            return f"COMMAND SUCCESS:\n{result.stdout}"
        else:
            return f"COMMAND FAILED (Code {result.returncode})\nSTDERR:{result.stderr}"
        
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 60 seconds."
    except Exception as e:
        return f"SYSTEM ERROR: {str(e)}"
