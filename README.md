# SYCLenv (what if python venvs existed for SYCL)

## TLDR

You want SYCL on a system. BOOM just do
```bash
git clone https://github.com/tdavidcl/syclenv.git && cd syclenv
./syclenv create <system config> .yolo --install-prerequisites
eval "$(./syclenv activate .yolo)"
```
where `<system config>` is the name of a supported template (e.g. `archlinux.acpp`, `macos.brew.acpp`, ...). You can check the list by doing `./syclenv list`.

now that the environment is activated you can compile some SYCL like this (`syclcc` is an alias to the compiler and `SYCL_FLAGS` to the default compile flags)
```bash
syclcc $SYCL_FLAGS main.cpp
```

## What is considered a valid environment ?

To add a new env just create a folder somewhere in src/syclenv/envs with a setup.py in it.
It should when called write activate scripts into the supplied path.

The philosophy is that the env creation should be instantaneous (almost). Then the actual compilation and all occurs on first activation.

Any valid environment satisfy the following:
```bash
# Can be created like so (should take at most 1/2 seconds)
./syclenv create <template name> <env name> -- <template specific flags>

# Can add --install-prerequisites to setup depencies
./syclenv create <> <> --install-prerequisites  -- <>

# Can be activated by doing (exemple for bash/zsh here)
# Will setup the env at this stage if not already done.
eval "$(./syclenv activate <env name>)"

# To compile we provide alias + default flags
syclcc $SYCL_FLAGS main.cpp

# provide deactivate command that MUST restore the env
# in the same state as before the activation
deactivate
```
