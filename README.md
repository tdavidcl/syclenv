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
