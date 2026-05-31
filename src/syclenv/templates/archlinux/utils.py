from syclenv.run_cmd import run_cmd


def has_pacman_package(package: str) -> bool:
    return run_cmd(f"pacman -Q {package} >/dev/null 2>&1", log_error=False)


def get_pacman_llvm_version() -> str:
    for ver in [21, 20]:
        if has_pacman_package(f"llvm{ver}") and has_pacman_package(f"clang{ver}"):
            return ver
    return None


def get_pacman_llvm_install_dir() -> str:
    llvm_version = get_pacman_llvm_version()
    if llvm_version is None:
        return None
    return f"/usr/lib/llvm{llvm_version}"
