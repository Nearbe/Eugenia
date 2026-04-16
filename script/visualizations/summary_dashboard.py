#!/usr/bin/env python3
"""
Beauty vision summary visualization.

Compiles multiple key visualizations into a single high-quality 
"beauty vision" summary, providing a comprehensive overview 
of the topological analysis.

========================================
WHAT IS THE BEAUTY VISION?
========================================

The "Beauty Vision" is a multi-panel dashboard that combines:

1. SOURCE IMAGE & BINARY MASK:
   - Direct comparison of input data and its topological representation.

2. 3D DELTA LANDSCAPE:
   - Geometric representation of the delta field as a 3D surface.

3. PERSISTENCE SKELETON:
   - Highlights only the most robust topological features.

4. JUMP ANALYSIS:
   - Shows critical threshold levels where the topology changes.

5. TOPOLOGICAL ENTROPY:
   - Measures the complexity and information content of the sweep.

6. EULER CHARACTERISTIC:
   - Global topological invariant across the threshold sweep.

========================================
WHY IS THIS USEFUL?
========================================

1. ALL-IN-ONE OVERVIEW:
   - No need to look at 16 separate files.
   - Summarizes the entire pipeline in one "poster".

2. AESTHETIC REPRESENTATION:
   - High-resolution, balanced layout.
   - Professional-grade visualization for reports or presentations.

3. CROSS-DOMAIN INSIGHTS:
   - See how geometric features (3D) relate to topological metrics (Euler/Jumps).
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from utils import (
    save_visualization,
    get_symbol_label,
    get_channel_config,
    hex_to_rgb,
    create_colored_mask,
    normalize_image,
    compute_gradient_magnitude
)


def _plot_delta_field(ax, delta_image, is_color, channel_colors, display_idx, configuration):
    """PANEL 1: Original Delta Field (Top Left)"""
    if is_color:
        color_rgb = hex_to_rgb(channel_colors[display_idx])
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("custom", ["black", color_rgb])
        im = ax.imshow(delta_image, cmap=cmap)
    else:
        im = ax.imshow(delta_image, cmap=configuration["colormap_grayscale"])
    ax.set_title("Original Delta Field (\u0394)", fontsize=20)
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.axis('off')


def _plot_binary_mask(ax, delta_image, is_color, channel_colors, display_idx, configuration):
    """PANEL 2: Binary Mask (Top Middle)"""
    # Use threshold near 0 for best visual representation
    t_val = 0.0
    binary_mask = (delta_image > t_val).astype(float)
    if is_color:
        color_rgb = hex_to_rgb(channel_colors[display_idx])
        rgb_image = create_colored_mask(binary_mask, color_rgb)
        ax.imshow(rgb_image)
    else:
        ax.imshow(binary_mask, cmap=configuration["colormap_binary"])
    ax.set_title(f"Binary Mask (\u0394 > {t_val})", fontsize=20)
    ax.axis('off')


def _plot_3d_landscape(ax, delta_image, channel_colormaps, display_idx):
    """PANEL 3: 3D Surface (Top Right)"""
    h, w = delta_image.shape
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    ax.plot_surface(
        x, y, delta_image,
        cmap=channel_colormaps[display_idx % len(channel_colormaps)],
        alpha=0.8,
        edgecolor='none'
    )
    ax.set_title("3D Landscape", fontsize=20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("\u0394")
    ax.view_init(elev=35, azim=45)


def _plot_persistence_skeleton(ax, delta_image, configuration):
    """PANEL 4: Persistence Skeleton (Middle Left)"""
    h, w = delta_image.shape
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    normalized = normalize_image(delta_image)
    p_thresh = configuration.get("persistence_threshold", 0.3)
    persistence_mask = normalized > p_thresh
    filtered_surface = np.where(persistence_mask, delta_image, np.nan)
    ax.plot_surface(
        x, y, filtered_surface,
        cmap=configuration["colormap_3d"],
        alpha=0.9,
        edgecolor='none'
    )
    ax.set_title(f"Persistence Skeleton (P > {p_thresh})", fontsize=20)
    ax.set_zlim(delta_image.min(), delta_image.max())
    ax.view_init(elev=35, azim=45)


def _plot_occupancy_jumps(ax, thresholds, class_occupancy, jump_events, display_idx):
    """PANEL 5: Jumps & Occupancy (Middle Middle)"""
    # Plot occupancy for this class (already converted to numpy)
    ax.plot(thresholds, class_occupancy, color='blue', label='Occupancy', linewidth=2)
    ax.set_ylabel("Occupancy Rate (%)", color='blue', fontsize=16)
    ax.set_title("Occupancy & Jump Events", fontsize=20)
    ax.grid(alpha=0.3)

    # Second axis for jump density
    ax_twin = ax.twinx()
    jump_hist = np.zeros(len(thresholds))
    t_min = thresholds[0]
    t_step = thresholds[1] - thresholds[0]
    for j_t, j_c, _, _, _ in jump_events:
        if j_c == display_idx:
            idx = int((j_t - t_min) / t_step + 0.5)
            if 0 <= idx < len(jump_hist):
                jump_hist[idx] += 1

    ax_twin.fill_between(thresholds, 0, jump_hist, color='crimson', alpha=0.4, label='Jumps')
    ax_twin.set_ylabel("Jump Intensity", color='crimson', fontsize=16)
    ax.set_xlabel("Threshold (\u0394)", fontsize=16)


def _plot_horizon_heatmap(ax, thresholds, occupancy_rates, num_classes):
    """PANEL 6: Horizon Heatmap (Middle Right)"""
    # Sample multiple classes to show variety
    sample_size = min(num_classes, 10)
    heatmap_data = occupancy_rates[:, :sample_size].cpu().numpy().T
    im = ax.imshow(
        heatmap_data,
        aspect='auto',
        extent=[thresholds[0], thresholds[-1], sample_size - 0.5, -0.5],
        cmap='magma'
    )
    ax.set_title("Multi-Class Horizon Heatmap", fontsize=20)
    ax.set_ylabel("Class ID", fontsize=16)
    ax.set_xlabel("Threshold (\u0394)", fontsize=16)
    plt.colorbar(im, ax=ax, shrink=0.8)


def _plot_topological_entropy(ax, thresholds, class_occupancy):
    """PANEL 7: Entropy Analysis (Bottom Left)"""
    # Simplified Shannon Entropy: p*log(p) + (1-p)*log(1-p)
    p = np.clip(class_occupancy / 100.0, 1e-7, 1.0 - 1e-7)
    entropy = -(p * np.log2(p) + (1.0 - p) * np.log2(1.0 - p))
    ax.plot(thresholds, entropy, color='green', linewidth=2.5)
    ax.fill_between(thresholds, 0, entropy, color='green', alpha=0.2)
    ax.set_title("Topological Entropy", fontsize=20)
    ax.set_xlabel("Threshold (\u0394)", fontsize=16)
    ax.set_ylabel("Bits", fontsize=16)
    ax.grid(alpha=0.3)
    return entropy


def _plot_gradient_stress(ax, delta_image):
    """PANEL 8: Gradient Stress Map (Bottom Middle)"""
    grad_mag = compute_gradient_magnitude(delta_image)
    im = ax.imshow(grad_mag, cmap='inferno')
    ax.set_title("Gradient Stress Map", fontsize=20)
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.axis('off')


def _plot_info_metadata(ax, data, configuration, label, thresholds, class_occupancy, jump_events, display_idx, entropy,
                        w, h):
    """PANEL 9: Info & Metadata (Bottom Right)"""
    ax.axis('off')
    info_text = (
        f"DATA SOURCE: {data.get('source_name', 'Unknown').upper()}\n"
        f"CLASS: {label}\n"
        f"IMAGE SIZE: {w}x{h}\n\n"
        f"SWEEP RANGE: [{thresholds[0]:.3f}, {thresholds[-1]:.3f}]\n"
        f"SWEEP STEPS: {len(thresholds):,}\n"
        f"JUMP THRESHOLD: {configuration.get('jump_threshold', 1.0)}%\n"
        f"TOTAL JUMPS: {len([j for j in jump_events if j[1] == display_idx])}\n\n"
        f"COLOR SPACE: {data.color_space}\n"
        f"DEVICE: {data.device}\n\n"
        f"--- TOPOLOGY OVERVIEW ---\n"
        f"Maximum Entropy: {np.max(entropy):.4f} bits\n"
        f"Peak Occupancy: {np.max(class_occupancy):.1f}%\n"
        f"T-Zero Occupancy: {class_occupancy[np.argmin(np.abs(thresholds))]:.1f}%"
    )
    ax.text(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=18,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.2))


def render(data, sweep, out_dir):
    """
    Render the "Beauty Vision" summary visualization.

    Args:
        data: Dictionary containing loaded data and configuration
        sweep: Dictionary containing threshold sweep results
        out_dir: Output directory for saving the figure
    """
    configuration = data["config"]
    symbols = data["symbol_delta_fields"]
    num_classes = data["number_of_classes"]
    thresholds = sweep.thresholds
    occupancy_rates = sweep.occupancy_rates
    jump_events = sweep.jump_events
    is_color = data.is_color

    # Selection: pick first few classes for detailed view
    display_idx = 0
    label = get_symbol_label(display_idx, data)
    delta_image = symbols[display_idx].cpu().numpy()

    # Get occupancy for this class and convert to numpy for calculations
    class_occupancy = occupancy_rates[:, display_idx].cpu().numpy()
    channel_colors, channel_colormaps = get_channel_config(data, configuration)

    # Create a large figure with GridSpec
    fig = plt.figure(figsize=(24, 18))
    fig.suptitle(f"Topological Analysis Summary: {label.upper()}", fontsize=32, fontweight='bold', y=0.98)

    gs = gridspec.GridSpec(3, 3, figure=fig)

    # --- PANEL 1: Original Delta Field (Top Left) ---
    _plot_delta_field(fig.add_subplot(gs[0, 0]), delta_image, is_color, channel_colors, display_idx, configuration)

    # --- PANEL 2: Binary Mask (Top Middle) ---
    _plot_binary_mask(fig.add_subplot(gs[0, 1]), delta_image, is_color, channel_colors, display_idx, configuration)

    # --- PANEL 3: 3D Surface (Top Right) ---
    _plot_3d_landscape(fig.add_subplot(gs[0, 2], projection='3d'), delta_image, channel_colormaps, display_idx)

    # --- PANEL 4: Persistence Skeleton (Middle Left) ---
    _plot_persistence_skeleton(fig.add_subplot(gs[1, 0], projection='3d'), delta_image, configuration)

    # --- PANEL 5: Jumps & Occupancy (Middle Middle) ---
    _plot_occupancy_jumps(fig.add_subplot(gs[1, 1]), thresholds, class_occupancy, jump_events, display_idx)

    # --- PANEL 6: Horizon Heatmap (Middle Right) ---
    _plot_horizon_heatmap(fig.add_subplot(gs[1, 2]), thresholds, occupancy_rates, num_classes)

    # --- PANEL 7: Entropy Analysis (Bottom Left) ---
    entropy = _plot_topological_entropy(fig.add_subplot(gs[2, 0]), thresholds, class_occupancy)

    # --- PANEL 8: Gradient Stress Map (Bottom Middle) ---
    _plot_gradient_stress(fig.add_subplot(gs[2, 1]), delta_image)

    # --- PANEL 9: Info & Metadata (Bottom Right) ---
    h, w = delta_image.shape
    _plot_info_metadata(fig.add_subplot(gs[2, 2]), data, configuration, label, thresholds, class_occupancy, jump_events,
                        display_idx, entropy, w, h)

    description = (
        "Beauty Vision: An artistic representation of the topological features. "
        "Uses colored masks to highlight regions above significant thresholds. "
        "Demonstrates the complexity and structural richness of the symbols' Delta fields."
    )
    save_visualization("16_beauty_vision.png", out_dir, configuration, "dpi_high", description=description)


if __name__ == "__main__":
    # Test stub
    pass
