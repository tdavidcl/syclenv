import subprocess
import sys


def run_cmd(command, log_cmd=False, bash=True, log_error=True, live_output=False):
    sys.stdout.flush()
    sys.stderr.flush()
    if bash:
        if log_cmd:
            print(f"   Running command : bash -c '{command}'")

        try:
            subprocess.run(
                ["bash", "-c", command],
                check=True,
                stdout=sys.stdout if live_output else subprocess.PIPE,
                stderr=sys.stderr if live_output else subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            if log_error:
                print(f"Error running command: {e}")
            return False
        return True
    else:
        raise NotImplementedError("Only bash=True is currently supported for run_cmd")
