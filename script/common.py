#!/usr/bin/env python3
"""
common.py — Загрузка данных, вычисление Δ, sweep.
Данные никогда не покидают этот модуль.
"""

import torch
import numpy as np
import os
import time
from PIL import Image
from dataclasses import asdict
from params import VIZ

USE_MNIST = True
SAMPLE_SIZE = None

_data = None


def _ensure_loaded():
    global _data
    if _data is not None:
        return _data

    t0 = time.time()
    device = torch.device("mps")
    print(f"[{time.strftime('%H:%M:%S')}] Загрузка данных...", flush=True)

    if USE_MNIST:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mnist_path = os.path.join(script_dir, "..", "..", "eugenia_data", "mnist.npz")
        f = np.load(mnist_path)
        print(
            f"[{time.strftime('%H:%M:%S')}]   npz загружен, 10 образцов...", flush=True
        )
        y_all = f["y_train"]
        indices = [np.where(y_all == c)[0][0] for c in range(VIZ.hist_n_classes)]
        indices = np.array(indices)
        X_train = torch.from_numpy(f["x_train"][indices].astype(np.float32)).to(device)
        y_train_t = torch.from_numpy(f["y_train"][indices].astype(np.int32)).to(device)
        H, W, C = 28, 28, 1
        X_test = X_train.clone()
        y_test_t = y_train_t.clone()
        D_train_flat = (torch.log(X_train + 1) - torch.log(256.0 - X_train)).reshape(
            X_train.shape[0], -1
        )
        D_test_flat = (torch.log(X_test + 1) - torch.log(256.0 - X_test)).reshape(
            X_test.shape[0], -1
        )
    else:
        raise NotImplementedError("use_mnist=False пока не реализован")

    D_train_grid = D_train_flat.view(-1, H, W, C)
    D_test_grid = D_test_flat.view(-1, H, W, C)
    X_train_grid = X_train.view(-1, H, W, C)

    N = X_train.shape[0]
    symbols_delta = [D_train_grid[i, :, :, 0] for i in range(N)]
    n_classes = VIZ.hist_n_classes

    _data = {
        "device": device,
        "D_train_flat": D_train_flat,
        "D_test_flat": D_test_flat,
        "X_train_flat": X_train,
        "y_train": y_train_t,
        "y_test": y_test_t,
        "D_train_grid": D_train_grid,
        "D_test_grid": D_test_grid,
        "X_train_grid": X_train_grid,
        "delta_min": D_train_flat.min().item(),
        "delta_max": D_train_flat.max().item(),
        "H": H,
        "W": W,
        "C": C,
        "N": N,
        "n_classes": n_classes,
        "symbols_delta": symbols_delta,
        "viz": asdict(VIZ),
    }
    print(
        f"[{time.strftime('%H:%M:%S')}] Данные: X={X_train.shape}, D={D_train_flat.shape}, Δ=[{_data['delta_min']:.4f}, {_data['delta_max']:.4f}] ({time.time() - t0:.1f}с)"
    )
    return _data


_sweep = None


def _ensure_sweep():
    global _sweep
    if _sweep is not None:
        return _sweep

    d = _ensure_loaded()
    device = d["device"]
    D_train, y_train_t = d["D_train_flat"], d["y_train"]
    N = D_train.shape[0]

    print(f"[{time.strftime('%H:%M:%S')}] Sweep Δ... ", flush=True, end="")
    t0 = time.time()

    thresholds = np.arange(VIZ.sweep_min, VIZ.sweep_max, VIZ.sweep_step)
    n_thr = len(thresholds)

    D_exp = D_train.view(N, 1, 784)
    T_exp = torch.from_numpy(thresholds.astype(np.float32)).to(device).view(1, n_thr, 1)
    binary = (D_exp > T_exp).float()

    bits_tr_all = torch.zeros(n_thr, VIZ.hist_n_classes, device=device)
    for c in range(VIZ.hist_n_classes):
        mask = (y_train_t == c).view(-1, 1, 1)
        masked = binary * mask
        count_c = mask.sum().item()
        if count_c > 0:
            bits_tr_all[:, c] = masked.sum(dim=(0, 2)) / (count_c * 784) * 100

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
