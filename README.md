# syclenv

## TLDR

You want SYCL on arch linux. BOOM just do
```bash
git clone https://github.com/tdavidcl/syclenv.git && cd syclenv
./syclenv create --install-prerequisites archlinux.acpp .yolo
eval "$(./syclenv activate .yolo)"
```

To add a new env just create a folder somewhere in src/syclenv/envs with a setup.py in it.
It should when called write activate scripts into the supplied path.

The philosophy is that the env creation should be instantaneous (almost). Then the actual compilation and all occurs on first activation.

## What is considered a valid environment ?

Any valid environment satisfy the following:
```bash
# Can be created like so (should take at most 1/2 seconds)
./syclenv create <template name> <env name> -- <template specific flags>

# Can add --install-prerequisites to setup depencies
./syclenv create --install-prerequisites <> <> -- <>

# Can be activated by doing (exemple for bash/zsh here)
# Will setup the env at this stage if not already done.
eval "$(./syclenv activate <env name>)"

# provide deactivate command that MUST restore the env
# in the same state as before the activation
deactivate
```
