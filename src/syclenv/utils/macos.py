from syclenv.run_cmd import run_cmd


def has_brew_packages(package_list: list[str]) -> bool:
    return run_cmd(
        f"brew list {' '.join(package_list)} >/dev/null 2>&1", log_error=False
    )
