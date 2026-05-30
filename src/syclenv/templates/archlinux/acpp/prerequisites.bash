function check_prerequisites {
    mandatory_packages=(
        base-devel
        git
        cmake
        boost
        openmp
        lld
    )

    missing_packages=()
    for package in "${mandatory_packages[@]}"; do
        if ! pacman -Q "$package" >/dev/null 2>&1; then
            missing_packages+=("$package")
        fi
    done

    LLVM_INSTALL_DIR=""
    for ver in 21 20; do
        if pacman -Q "llvm${ver}" &>/dev/null && [ -d "/usr/lib/llvm${ver}" ]; then
            LLVM_INSTALL_DIR="/usr/lib/llvm${ver}"
            break
        fi
    done
    if [ -z "$LLVM_INSTALL_DIR" ]; then
        echo "syclenv: no LLVM 20 or 21 found via pacman. Install one with:"
        echo "     sudo pacman -S llvm20 clang20"
        echo "  or sudo pacman -S llvm21 clang21"
        LLVM_INSTALL_DIR="not found"
        missing_packages+=("llvm20")
        missing_packages+=("clang20")
    fi

    if [ ${#missing_packages[@]} -gt 0 ]; then
        echo "Missing packages: ${missing_packages[*]}"
        echo "Install all missing packages using 'install_prerequisites' function"
        echo "  or manually with: sudo pacman -S ${missing_packages[*]}"
        return 1
    fi

    echo "All prerequisites are installed"
    echo "LLVM_INSTALL_DIR = $LLVM_INSTALL_DIR"

}

function install_prerequisites {
    echo " -- install prerequisites -- "
    sudo pacman -Syu --noconfirm \
       base-devel \
       git \
       cmake \
       boost \
       ninja \
       openmp \
       llvm20 \
       clang20 \
       lld \
       numactl
}
