SPACER = "\n###########################################################################"


def fetch_helper_script(path: str) -> str:
    with open(path) as f:
        helper_script = ""
        helper_script += f"{SPACER}\n# Imported script " + path + f"{SPACER}\n"
        helper_script += f.read()
        helper_script += f"{SPACER}{SPACER}{SPACER}\n"

        return helper_script
