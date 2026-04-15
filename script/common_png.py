#!/usr/bin/env python3
"""
common_png.py — Загрузка данных из PNG спрайт-листов.
"""

import torch
import numpy as np
import os
import time
from PIL import Image
from dataclasses import asdict
from params import VIZ
from scipy import ndimage

PNG_SOURCE = "cyrillic"
_data = None


def _extract_classes_from_delta(D_flat, H, W):
    threshold = -4.0
    mask = (D_flat > threshold).astype(np.uint8).reshape(H, W)
    labeled, n_labels = ndimage.label(mask)
    symbols = []
    positions = []
    for i in range(1, n_labels + 1):
        coords = np.where(labeled == i)
        y_min, y_max = coords[0].min(), coords[0].max() + 1
        x_min, x_max = coords[1].min(), coords[1].max() + 1
        symbol_delta = D_flat[y_min:y_max, x_min:x_max].copy()
        symbols.append(symbol_delta)
        positions.append((y_min, y_max, x_min, x_max))
    return symbols, positions


def _ensure_loaded():
    global _data
    if _data is not None:
        return _data

    t0 = time.time()
    device = torch.device("mps")
    print(f"[{time.strftime('%H:%M:%S')}] Загрузка PNG: {PNG_SOURCE}...", flush=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    png_path = os.path.join(script_dir, f"{PNG_SOURCE}.png")
    if not os.path.isfile(png_path):
        png_path = os.path.join(script_dir, f"{PNG_SOURCE}.jpeg")

    img = Image.open(png_path).convert("L")
    arr = np.array(img).astype(np.float32)
    H, W = arr.shape

    X_np = 255.0 - arr
    X_train = torch.from_numpy(X_np).to(device)

    D_flat = (torch.log(X_train + 1) - torch.log(256.0 - X_train)).cpu().numpy()
    D_train = torch.from_numpy(D_flat).to(device)

    symbols, positions = _extract_classes_from_delta(D_flat, H, W)
    n_classes = len(symbols)

    symbol_metadata = []
    for i, sym in enumerate(symbols):
        y_min, y_max, x_min, x_max = positions[i]
        symbol_metadata.append(
            {
                "id": i,
                "bbox": (int(y_min), int(y_max), int(x_min), int(x_max)),
                "delta_min": float(sym.min()),
                "delta_max": float(sym.max()),
                "delta_mean": float(sym.mean()),
                "n_pixels": int(sym.size),
            }
        )

    max_h = max(s.shape[0] for s in symbols)
    max_w = max(s.shape[1] for s in symbols)
    y_train_t = torch.arange(n_classes, device=device, dtype=torch.int32)

    _data = {
        "device": device,
        "X_full": X_train,
        "D_full": D_train,
        "H_full": H,
        "W_full": W,
        "n_classes": n_classes,
        "symbol_metadata": symbol_metadata,
        "symbols_delta": [torch.from_numpy(s).to(device) for s in symbols],
        "symbol_positions": positions,
        "delta_min": float(D_flat.min()),
        "delta_max": float(D_flat.max()),
        "viz": asdict(VIZ),
        "H": max_h,
        "W": max_w,
        "C": 1,
        "N": n_classes,
        "y_train": y_train_t,
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

    print(f"[{time.strftime('%H:%M:%S')}] Sweep Δ... ", flush=True, end="")
    t0 = time.time()

    thresholds = np.arange(VIZ.sweep_min, VIZ.sweep_max, VIZ.sweep_step)
    n_thr = len(thresholds)

    bins_edges = np.linspace(VIZ.sweep_min, VIZ.sweep_max + VIZ.sweep_step, n_thr + 1)
    bits_tr_all = torch.zeros(n_thr, n_classes, device=device)
    for c in range(n_classes):
        sym = symbols[c].cpu().numpy()
        sym_flat = sym.flatten()
        sym_size = sym_flat.size
        hist, _ = np.histogram(sym_flat, bins=bins_edges)
        cumsum_from_end = np.cumsum(hist[::-1])[::-1].astype(np.float32)
        bits_tr_all[:, c] = torch.from_numpy(cumsum_from_end / sym_size * 100).to(
            device
        )

    jump_events = []
    deltas = torch.abs(bits_tr_all[1:] - bits_tr_all[:-1])
    jumps_mask = deltas > VIZ.jump_threshold
    jump_indices = torch.where(jumps_mask)
    for idx_pos, c in zip(jump_indices[0].tolist(), jump_indices[1].tolist()):
        prev = bits_tr_all[idx_pos, c].item()
        curr = bits_tr_all[idx_pos + 1, c].item()
        jump_events.append(
            (round(thresholds[idx_pos + 1], 4), c, prev, curr, abs(curr - prev))
        )

    _sweep = {
        "thresholds": thresholds,
        "bits_tr_all": bits_tr_all,
        "jump_events": jump_events,
        "jump_count": len(jump_events),
    }
    print(
        f"готово: {n_thr} порогов, {_sweep['jump_count']} скачков ({time.time() - t0:.1f}с)",
        flush=True,
    )
    return _sweep


def run_all_visualizations():
    d = _ensure_loaded()
    s = _ensure_sweep()
    out_dir = os.path.dirname(os.path.abspath(__file__))
    viz_dir = os.path.dirname(out_dir)

    scripts = [
        ("00a_delta_histograms_by_class", "render"),
        ("individual_delta_hists", "render"),
        ("01_horizon_heatmap", "render"),
        ("02_horizon_animation", "render"),
        ("03_scatter_mean_std", "render"),
        ("04_jumps_analysis", "render"),
        ("05_tsne_binary_profiles", "render"),
        ("06_3d_surface", "render"),
        ("07_cdf_by_class", "render"),
        ("08_entropy_analysis", "render"),
        ("09_original_vs_binary", "render"),
        ("10_betti0_components", "render"),
        ("11_betti1_holes", "render"),
        ("12_euler_persistence_complexity", "render"),
        ("13_persistence_landscape", "render"),
        ("14_stress_map", "render"),
        ("15_phase_volume", "render"),
    ]

    t_all = time.time()
    print(f"\n{'=' * 60}", flush=True)
    print(
        f"[{time.strftime('%H:%M:%S')}] Запуск {len(scripts)} визуализаций", flush=True
    )
    print(f"{'=' * 60}", flush=True)

    for i, (mod_name, func_name) in enumerate(scripts):
        mod_path = os.path.join(out_dir, mod_name + ".py")
        if not os.path.isfile(mod_path):
            print(f"  ⚠ {mod_name}.py не найден", flush=True)
            continue
        import importlib.util

        spec = importlib.util.spec_from_file_location(mod_name, mod_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        render_fn = getattr(mod, func_name, None)
        if render_fn is None:
            print(f"  ✗ {mod_name}: нет {func_name}()", flush=True)
            continue
        print(
            f"\n[{time.strftime('%H:%M:%S')}] ({i + 1}/{len(scripts)}) {mod_name}",
            flush=True,
        )
        try:
            render_fn(data=d, sweep=s, out_dir=viz_dir)
            print(f"  ✓ готово", flush=True)
        except Exception as e:
            print(f"  ✗ ошибка: {e}", flush=True)

    print(f"\n{'=' * 60}", flush=True)
    print(f"ВСЕГО: {time.time() - t_all:.0f} секунд", flush=True)
    print(f"{'=' * 60}", flush=True)


if __name__ == "__main__":
    run_all_visualizations()
