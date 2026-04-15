#!/usr/bin/env python3
"""
common_cmyk.py — Загрузка данных из CMYK-изображений.
"""

import torch
import numpy as np
import os
import time
from PIL import Image
from dataclasses import asdict
from params import VIZ

CMYK_SOURCE = "Eugene_cmyk"
_data = None


def _ensure_loaded():
    global _data
    if _data is not None:
        return _data

    t0 = time.time()
    device = torch.device("mps")
    print(f"[{time.strftime('%H:%M:%S')}] Загрузка CMYK: {CMYK_SOURCE}...", flush=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_ext = [".tiff", ".tif", ".jpeg", ".jpg", ".png"]
    file_path = None
    for ext in possible_ext:
        candidate = os.path.join(script_dir, f"{CMYK_SOURCE}{ext}")
        if os.path.isfile(candidate):
            file_path = candidate
            break

    if file_path is None:
        jpeg_path = os.path.join(script_dir, "Eugene.jpeg")
        if os.path.isfile(jpeg_path):
            print(
                f"[{time.strftime('%H:%M:%S')}]   CMYK файл не найден, конвертирую Eugene.jpeg → CMYK...",
                flush=True,
            )
            img_rgb = Image.open(jpeg_path).convert("RGB")
            img_cmyk = img_rgb.convert("CMYK")
            cmyk_path = os.path.join(script_dir, f"{CMYK_SOURCE}.tiff")
            img_cmyk.save(cmyk_path)
            file_path = cmyk_path
        else:
            raise FileNotFoundError(f"Ни CMYK файл, ни Eugene.jpeg не найдены")

    img = Image.open(file_path).convert("CMYK")
    arr = np.array(img).astype(np.float32)
    H, W, C = arr.shape

    X_train = torch.from_numpy(arr).to(device)
    D_flat = (torch.log(X_train + 1) - torch.log(256.0 - X_train)).cpu().numpy()
    D_train = torch.from_numpy(D_flat).to(device)

    n_classes = C
    y_train_t = torch.arange(C, device=device, dtype=torch.int32)

    _data = {
        "device": device,
        "X_full": X_train,
        "D_full": D_train,
        "H_full": H,
        "W_full": W,
        "C_full": C,
        "is_color": True,
        "color_space": "CMYK",
        "n_classes": n_classes,
        "symbols_delta": [D_train[:, :, c] for c in range(C)],
        "symbol_names": ["C (Cyan)", "M (Magenta)", "Y (Yellow)", "K (Key/Black)"],
        "symbol_positions": [(0, H, 0, W)] * C,
        "delta_min": float(D_flat.min()),
        "delta_max": float(D_flat.max()),
        "viz": asdict(VIZ),
        "H": H,
        "W": W,
        "C": 1,
        "N": C,
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
    n_classes = d["N"]

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
