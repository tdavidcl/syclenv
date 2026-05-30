from syclenv.templates.SetupArg import SetupArg
from pathlib import Path

NAME = "Hello world env"


def setup(arg: SetupArg):
    print(f"Hello, World! {arg.path}")


    # create a dir at the path
    Path(arg.path).mkdir(parents=True, exist_ok=True)

    # create a file called activate.sh
    with open(arg.path + "/activate.sh", "w") as f:
        f.write("#!/bin/sh\n")
        f.write("echo 'Activating environment'\n")

    # create a file called activate.zsh
    with open(arg.path + "/activate.zsh", "w") as f:
        f.write("#!/bin/zsh\n")
        f.write("echo 'Activating environment'\n")
