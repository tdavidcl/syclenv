import subprocess
import sys

import rich
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def ask_run_cmd(
    command,
    log_cmd=False,
    bash=True,
    log_error=True,
    live_output=False,
    noconfirm=False,
):
    print(f"   Running command : bash -c '{command}'")

    if noconfirm:
        answer = "y"
    else:
        answer = input("   Run command? (y/n) ")

    if answer == "y":
        return run_cmd(command, log_cmd, bash, log_error, live_output)

    raise ValueError("Aborting by user request")


def run_bash_cmd(command, log_error=True, live_output=False):
    """Run a command in bash and return True if successful, False otherwise"""
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


def confirm_command_prompt_nice(command):
    syntax = Syntax(
        command, "bash", theme="monokai", line_numbers=False, word_wrap=True
    )

    panel = Panel(
        syntax,
        # title="Execute command?",
        border_style="grey50",
        subtitle="Do you want to run the command? (y/n)",
    )

    console.print(panel)

    answer = input("> ").strip().lower()

    if answer != "y":
        raise ValueError("Aborted")


def confirm_command_prompt(command, ask_confirm=False):
    if ask_confirm:
        confirm_command_prompt_nice(command)


def run_cmd(
    command,
    log_cmd=False,
    bash=True,
    log_error=True,
    live_output=False,
    ask_confirm=False,
):
    sys.stdout.flush()
    sys.stderr.flush()

    if bash:
        if log_cmd:
            confirm_command_prompt(command, ask_confirm)
            rich.print(f"Running command : bash -c '{command}'")

        return run_bash_cmd(command, log_error, live_output)

    else:
        raise NotImplementedError("Only bash=True is currently supported for run_cmd")
