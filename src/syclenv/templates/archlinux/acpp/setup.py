from pathlib import Path

from syclenv.templates.SetupArg import SetupArg

NAME = "Hello world env"


def setup(arg: SetupArg):
    print(f"Hello, World! {arg.path}")

    ENV_VARS = {"SYCLENV_CURRENT_ENV_PATH": Path(arg.path).absolute()}

    # create a dir at the path
    Path(arg.path).mkdir(parents=True, exist_ok=True)

    # load template file
    with open(Path(__file__).parent / "template.bash") as f:
        template = f.read()

    # add env vars to template
    for var, value in ENV_VARS.items():
        line = f"export {var}={value}"
        template = line + "\n" + template

    # create a file called activate.bash
    with open(arg.path + "/activate.bash", "w") as f:
        f.write(template)

    with open(arg.path + "/activate.zsh", "w") as f:
        f.write(template)

    with open(arg.path + "/activate.sh", "w") as f:
        f.write(template)
