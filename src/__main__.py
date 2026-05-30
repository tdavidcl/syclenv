import os
import sys

sys.path.append(os.path.dirname(__file__))

import syclenv.main


def main() -> None:
    syclenv.main.main()


if __name__ == "__main__":
    main()
