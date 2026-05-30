
function clone_acpp {

    ACPP_URL="https://github.com/AdaptiveCpp/AdaptiveCpp.git"

    if [ -z ${ACPP_GIT_DIR+x} ]; then echo "ACPP_GIT_DIR is unset"; return 1; fi

    if [ ! -f "$ACPP_GIT_DIR/README.md" ]; then
        echo " ------ Clonning AdaptiveCpp ------ "

        if [ -z ${ACPP_VERSION+x} ]
        then
            echo "-> git clone $ACPP_URL $ACPP_GIT_DIR"
            git clone $ACPP_URL $ACPP_GIT_DIR || return
        else
            echo "-> git clone -b $ACPP_VERSION $ACPP_URL $ACPP_GIT_DIR"
            git clone -b $ACPP_VERSION $ACPP_URL $ACPP_GIT_DIR || return
        fi

        echo " ------  AdaptiveCpp Cloned  ------ "

    fi

}

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

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "Missing packages: ${missing_packages[*]}"
    echo "Install all missing packages using 'install_prerequisites' function"
    echo "  or manually with: sudo pacman -S ${missing_packages[*]}"
fi


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
export LLVM_INSTALL_DIR


VALID_ENV=true
if [ ${#missing_packages[@]} -gt 0 ]; then
    VALID_ENV=false
fi

export ACPP_VERSION=develop
export ACPP_APPDB_DIR=/tmp/acpp-appdb # otherwise it would we in the $HOME/.acpp
export ACPP_GIT_DIR=$SYCLENV_CURRENT_ENV_PATH/acpp-git
export ACPP_BUILD_DIR=$SYCLENV_CURRENT_ENV_PATH/acpp-builddir
export ACPP_INSTALL_DIR=$SYCLENV_CURRENT_ENV_PATH/acpp-installdir

function setupcompiler {

    if [ "$VALID_ENV" = false ]; then
        return 1
    fi

    echo "-- setup variables -- "
    echo "- LLVM_INSTALL_DIR = $LLVM_INSTALL_DIR"
    echo "- ACPP_VERSION = $ACPP_VERSION"
    echo "- ACPP_APPDB_DIR = $ACPP_APPDB_DIR"
    echo "- ACPP_GIT_DIR = $ACPP_GIT_DIR"
    echo "- ACPP_BUILD_DIR = $ACPP_BUILD_DIR"
    echo "- ACPP_INSTALL_DIR = $ACPP_INSTALL_DIR"
    echo "--------------------- "

    clone_acpp || return
    cmake -S ${ACPP_GIT_DIR} -B ${ACPP_BUILD_DIR} \
        ${CCACHE_CMAKE_ARG} \
        -DCMAKE_INSTALL_PREFIX=${ACPP_INSTALL_DIR} \
        -DCMAKE_C_COMPILER=${LLVM_INSTALL_DIR}/bin/clang \
        -DCMAKE_CXX_COMPILER=${LLVM_INSTALL_DIR}/bin/clang++ \
        -DLLVM_DIR=${LLVM_INSTALL_DIR}/lib/cmake/llvm/ \
        -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
        -DACPP_LLD_PATH=/usr/bin/ld.lld ||
        return
    (cd ${ACPP_BUILD_DIR} && $MAKE_EXEC "${MAKE_OPT[@]}" && $MAKE_EXEC install) || return
}

if [ "$VALID_ENV" = false ]; then
    echo " -- environment is not valid, please install the missing packages -- "
else

    if [ ! -f "$ACPP_INSTALL_DIR/bin/acpp" ]; then
        echo " ----- acpp is not configured, compiling it ... -----"
        setupcompiler || return
        echo " ----- acpp configured ! -----"
    fi

    echo " -- environment enabled -- "
    echo "acpp available in \$ACPP_INSTALL_DIR = $ACPP_INSTALL_DIR"

fi
