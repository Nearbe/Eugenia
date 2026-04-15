#!/usr/bin/env python3
"""
common.py — Unified data loader for all sources: mnist, png, cmyk.
"""

import os
import time
import torch
import numpy as np
from PIL import Image
from scipy import ndimage
from dataclasses import asdict
from params import VIZ

SOURCE = os.environ.get("VIZ_SOURCE", "mnist")
SOURCE_FILE = os.environ.get("VIZ_SOURCE_FILE", "")

_data = None


def _load_mnist():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mnist_path = os.path.join(script_dir, "..", "..", "eugenia_data", "mnist.npz")
    f = np.load(mnist_path)
    y_all = f["y_train"]
    indices = [np.where(y_all == c)[0][0] for c in range(VIZ.hist_n_classes)]
    indices = np.array(indices)
    X_train = torch.from_numpy(f["x_train"][indices].astype(np.float32))
    y_train = torch.arange(VIZ.hist_n_classes, dtype=torch.int32)
    H, W, C = 28, 28, 1
    return X_train, y_train, H, W, C


def _load_png():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    filename = SOURCE_FILE or "cyrillic.png"

    # Check script dir and parent dir
    for d in [script_dir, parent_dir]:
        path = os.path.join(d, filename)
        if os.path.exists(path):
            break
    else:
        path = os.path.join(script_dir, filename)

    if not os.path.exists(path):
        path = path.replace(".png", ".jpeg")
    img = Image.open(path).convert("L")
    arr = np.array(img).astype(np.float32)
    H, W = arr.shape
    X_train = torch.from_numpy(255.0 - arr)
    y_train = None

    threshold = -4.0
    mask = (X_train.numpy() > threshold).astype(np.uint8)
    labeled, n = ndimage.label(mask)
    symbols = []
    for i in range(1, n + 1):
        coords = np.where(labeled == i)
        y1, y2 = coords[0].min(), coords[0].max() + 1
        x1, x2 = coords[1].min(), coords[1].max() + 1
        symbols.append(X_train[y1:y2, x1:x2])
    X_train = symbols[0] if symbols else X_train.view(1, H, W)
    y_train = torch.arange(len(symbols) if symbols else 1)
    return (
        X_train.unsqueeze(0),
        y_train,
        symbols[0].shape[0] if symbols else H,
        symbols[0].shape[1] if symbols else W,
        1,
    )


def _load_cmyk():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    filename = SOURCE_FILE or "Eugene_cmyk.tiff"

    # Check script dir and parent dir
    for d in [script_dir, parent_dir]:
        path = os.path.join(d, filename)
        if os.path.exists(path):
            break
    else:
        path = os.path.join(script_dir, filename)

    if not os.path.exists(path):
        jpeg_path = os.path.join(parent_dir, "Eugene.jpeg")
        if os.path.exists(jpeg_path):
            img = Image.open(jpeg_path).convert("CMYK")
            img.save(path)
    img = Image.open(path).convert("CMYK")
    arr = np.array(img).astype(np.float32)
    H, W, C = arr.shape
    X_train = torch.from_numpy(arr)
    y_train = torch.arange(C)
    return X_train, y_train, H, W, C


def _ensure_loaded():
    global _data
    if _data is not None:
        return _data

    t0 = time.time()
    device = torch.device("mps")
    print(f"[{time.strftime('%H:%M:%S')}] Загрузка {SOURCE}...", flush=True)

    if SOURCE == "mnist":
        X_train, y_train, H, W, C = _load_mnist()
    elif SOURCE == "png":
        X_train, y_train, H, W, C = _load_png()
    elif SOURCE == "cmyk":
        X_train, y_train, H, W, C = _load_cmyk()
    else:
        raise ValueError(f"Unknown source: {SOURCE}")

    X_train = X_train.to(device)
    D = torch.log(X_train + 1) - torch.log(256.0 - X_train)

    if SOURCE == "cmyk":
        symbols_delta = [D[:, :, c] for c in range(C)]
    else:
        symbols_delta = [D[i] for i in range(D.shape[0])]

    n_classes = len(symbols_delta)
    print(
        f"[{time.strftime('%H:%M:%S')}] Данные: {X_train.shape}, Δ=[{D.min():.2f}, {D.max():.2f}] ({time.time() - t0:.1f}s)"
    )

    is_color = SOURCE == "cmyk"
    symbol_names = ["C", "M", "Y", "K"] if is_color else None

    _data = {
        "device": device,
        "D": D,
        "X": X_train,
        "y_train": y_train,
        "H": H,
        "W": W,
        "C": C,
        "n_classes": n_classes,
        "symbols_delta": symbols_delta,
        "is_color": is_color,
        "color_space": "CMYK" if is_color else "RGB",
        "symbol_names": symbol_names,
        "delta_min": D.min().item(),
        "delta_max": D.max().item(),
        "viz": asdict(VIZ),
    }
    return _data


_sweep = None


def _ensure_sweep():
    global _sweep
    if _sweep is not None:
        return _sweep

    d = _ensure_loaded()
    device = d["device"]
    symbols = d["symbols_delta"]
    n_classes = d["n_classes"]

    print(f"[{time.strftime('%H:%M:%S')}] Sweep...", flush=True)
    t0 = time.time()

    thresholds = np.arange(VIZ.sweep_min, VIZ.sweep_max, VIZ.sweep_step)
    n_thr = len(thresholds)

    bits = torch.zeros(n_thr, n_classes, device=device)
    for c in range(n_classes):
        sym = symbols[c].cpu().numpy().flatten()
        hist, _ = np.histogram(
            sym, bins=np.linspace(VIZ.sweep_min, VIZ.sweep_max, n_thr + 1)
        )
        cumsum = np.cumsum(hist[::-1])[::-1]
        bits[:, c] = torch.from_numpy(cumsum / len(sym) * 100)

    jumps = []
    delta = torch.abs(bits[1:] - bits[:-1])
    mask = delta > VIZ.jump_threshold
    idxs = torch.where(mask)
    for i, c in zip(idxs[0].tolist(), idxs[1].tolist()):
        jumps.append(
            (
                round(thresholds[i + 1], 4),
                c,
                bits[i, c].item(),
                bits[i + 1, c].item(),
                abs(bits[i + 1, c].item() - bits[i, c].item()),
            )
        )

    _sweep = {
        "thresholds": thresholds,
        "bits_tr_all": bits,
        "jump_events": jumps,
        "jump_count": len(jumps),
    }
    print(f"  {n_thr} thresholds, {len(jumps)} jumps ({time.time() - t0:.1f}s)")
    return _sweep


def run_all_visualizations():
    d = _ensure_loaded()
    s = _ensure_sweep()

    out_dir = os.environ.get("VIZ_OUT_DIR", os.path.dirname(os.path.abspath(__file__)))
    script_dir = os.path.dirname(os.path.abspath(__file__))

    scripts = [
        ("delta_histograms_by_class", "render"),
        ("individual_delta_histograms", "render"),
        ("horizon_heatmap", "render"),
        ("horizon_animation", "render"),
        ("scatter_mean_std", "render"),
        ("jumps_analysis", "render"),
        ("tsne_binary_profiles", "render"),
        ("surface_3d", "render"),
        ("cdf_by_class", "render"),
        ("entropy_analysis", "render"),
        ("original_vs_binary", "render"),
        ("betti0_components", "render"),
        ("betti1_holes", "render"),
        ("euler_persistence", "render"),
        ("persistence_landscape", "render"),
        ("stress_map", "render"),
        ("phase_volume", "render"),
    ]

    print(f"\n{'=' * 60}")
    print(f"[{time.strftime('%H:%M:%S')}] Rendering {len(scripts)} visualizations")
    print(f"{'=' * 60}")

    t0 = time.time()
    for i, (name, fn) in enumerate(scripts):
        path = os.path.join(script_dir, f"{name}.py")
        if not os.path.exists(path):
            print(f"  ⚠ {name}.py not found")
            continue
        spec = __import__("importlib.util").util.spec_from_file_location(name, path)
        mod = __import__("importlib.util").util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        render_fn = getattr(mod, fn, None)
        if not render_fn:
            print(f"  ✗ {name}: no {fn}()")
            continue
        print(f"\n[{time.strftime('%H:%M:%S')}] ({i + 1}/{len(scripts)}) {name}")
        try:
            render_fn(data=d, sweep=s, out_dir=out_dir)
            print(f"  ✓ done")
        except Exception as e:
            print(f"  ✗ error: {e}")

    print(f"\n{'=' * 60}")
    print(f"Total: {time.time() - t0:.0f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_all_visualizations()
