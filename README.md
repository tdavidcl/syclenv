# syclenv

You want SYCL on arch linux. BOOM just do
```bash
uv run syclvenv create --install-prerequisites archlinux.acpp .yolo
eval "$(uv run syclvenv activate .yolo)"
```

To add a new env just create a folder somewhere in src/syclenv/envs with a setup.py in it.
It should when called write activate scripts into the supplied path.
