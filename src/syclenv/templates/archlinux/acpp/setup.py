from syclenv.templates.SetupArg import SetupArg

NAME = "Hello world env"


def setup(arg: SetupArg):
    print(f"Hello, World! {arg.path}")
