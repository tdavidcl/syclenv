if which ccache &>/dev/null; then
    # to debug
    #export CCACHE_DEBUG=1
    #export CCACHE_DEBUGDIR=$BUILD_DIR/ccache-debug

    export CCACHE_COMPILERTYPE=clang
    export CCACHE_CMAKE_ARG="-DCMAKE_CXX_COMPILER_LAUNCHER=ccache"
    echo " ----- ccache found, using it ----- "
else
    export CCACHE_COMPILERTYPE=clang
    export CCACHE_CMAKE_ARG=""
fi

export ACPP_GIT_DIR=$SYCLENV_CURRENT_ENV_PATH/acpp-git
export ACPP_BUILD_DIR=$SYCLENV_CURRENT_ENV_PATH/acpp-builddir
export ACPP_INSTALL_DIR=$SYCLENV_CURRENT_ENV_PATH/acpp-installdir

function run_setup {

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

function deactivate {
    _internal_deactivate
    unset ACPP_GIT_DIR
    unset ACPP_BUILD_DIR
    unset ACPP_INSTALL_DIR
    unset CCACHE_COMPILERTYPE
    unset CCACHE_CMAKE_ARG
    unset -f clone_acpp
    unset -f run_setup
    unset -f deactivate
}

if [ ! -f "$ACPP_INSTALL_DIR/bin/acpp" ]; then
    echo " -- environment not configured, running setup -- "
    run_setup || return
    echo " -- environment setup complete -- "
fi


syclcc() {
  "$ACPP_INSTALL_DIR/bin/acpp" "$@"
}
export SYCL_CXXFLAGS="-std=c++17 -O3"
export SYCL_LINKERFLAGS=""
export SYCL_FLAGS="$SYCL_CXXFLAGS $SYCL_LINKERFLAGS"

echo " -- environment enabled -- "
echo "syclcc = $(which syclcc)"
echo "SYCL_CXXFLAGS = $SYCL_CXXFLAGS"
echo "SYCL_LINKERFLAGS = $SYCL_LINKERFLAGS"
echo "SYCL_FLAGS = $SYCL_FLAGS"
