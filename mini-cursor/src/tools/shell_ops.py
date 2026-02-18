import subprocess
import subprocess
import shlex

ALLOWED_COMMANDS = {"python", "pip", "ls","mkdir", "echo", "cat"}

def execute_shell_command(command_str: str) -> str:
    """
    Executes a shell command in the workspace directory
    Capture stdout and stderr for self-healing.
    """

    try:
        args = shlex.split(command_str)
        if not args or args[0] not in ALLOWED_COMMANDS:
            return f"SECURITY ERROR: Command '{args[0]}' is not allowed. Allowed: {ALLOWED_COMMANDS}"
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            cwd="workspace",
            timeout=30
        )
        if result.returncode == 0:
            return f"COMMAND SUCCESS:\n{result.stdout}"
        else:
            return f"COMMAND FAILED (Code {result.returncode})\nSTDERR:{result.stderr}"
        
    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 30 seconds."
    except Exception as e:
        return f"SYSTEM ERROR: {str(e)}"