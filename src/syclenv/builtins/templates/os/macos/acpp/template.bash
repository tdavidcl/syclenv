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

function deactivate {
    _internal_deactivate
    unset CCACHE_COMPILERTYPE
    unset CCACHE_CMAKE_ARG
    unset SYCL_CXXFLAGS
    unset SYCL_LINKERFLAGS
    unset SYCL_FLAGS
    unset SYCLCC_PATH
    unset -f deactivate
    unset -f syclcc
}

SYCLCC_PATH=$(which acpp)
syclcc() {
  $SYCLCC_PATH "$@" || return
}
export SYCL_CXXFLAGS="-std=c++17 -O3"
export SYCL_LINKERFLAGS=""
export SYCL_FLAGS="$SYCL_CXXFLAGS $SYCL_LINKERFLAGS"

echo " -- environment enabled -- "
echo "syclcc = $SYCLCC_PATH"
echo "SYCL_CXXFLAGS = $SYCL_CXXFLAGS"
echo "SYCL_LINKERFLAGS = $SYCL_LINKERFLAGS"
echo "SYCL_FLAGS = $SYCL_FLAGS"
echo " -- ------------------- -- "
