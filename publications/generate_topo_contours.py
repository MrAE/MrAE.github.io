#!/usr/bin/env python3
"""
Generate randomized topographic contour SVG backgrounds.
Uses Perlin noise or random seeding to create unique contour patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import argparse
from datetime import datetime
import os

# Try to import Perlin noise; if not available, use fallback
try:
    from perlin_noise import PerlinNoise
    HAS_PERLIN = True
except ImportError:
    HAS_PERLIN = False
    print("Warning: perlin_noise not installed. Using fallback random method.")
    print("Install with: pip install perlin-noise")


def generate_perlin_contours(seed=None, width=1200, height=800, octaves=4, scale=200, num_contours=15):
    """
    Generate contour map using Perlin noise.
    
    Args:
        seed: Random seed for reproducibility
        width: SVG width in pixels
        height: SVG height in pixels
        octaves: Perlin noise octaves (more = more detail)
        scale: Scale of the noise (smaller = more frequent features)
        num_contours: Number of contour lines to draw
    """
    if seed is not None:
        np.random.seed(seed)
    
    if not HAS_PERLIN:
        return generate_random_contours(seed, width, height, num_contours)
    
    # Create Perlin noise
    noise = PerlinNoise(octaves=octaves, seed=seed)
    
    # Generate elevation data
    elevations = []
    for y in range(height):
        row = []
        for x in range(width):
            nx = (x / width) * 2
            ny = (y / height) * 2
            value = noise([nx, ny])
            row.append(value)
        elevations.append(row)
    
    elevations = np.array(elevations)
    
    # Normalize to 0-1
    elevations = (elevations - elevations.min()) / (elevations.max() - elevations.min())
    
    return elevations


def generate_random_contours(seed=None, width=1200, height=800, num_contours=15):
    """
    Generate contour map using random radial basis functions.
    Fallback method if Perlin noise not available.
    
    Args:
        seed: Random seed for reproducibility
        width: SVG width
        height: SVG height
        num_contours: Number of random peaks to create
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Create a blank elevation grid
    elevations = np.zeros((height, width))
    
    # Generate random peaks with Gaussian falloff
    num_peaks = num_contours * 2
    for _ in range(num_peaks):
        cx = np.random.randint(0, width)
        cy = np.random.randint(0, height)
        strength = np.random.uniform(0.3, 1.0)
        radius = np.random.randint(100, 400)
        
        # Create meshgrid for this peak
        yy, xx = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
        dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        
        # Gaussian peak
        peak = strength * np.exp(-(dist ** 2) / (2 * radius ** 2))
        elevations += peak
    
    # Normalize
    elevations = (elevations - elevations.min()) / (elevations.max() - elevations.min() + 1e-6)
    
    return elevations


def create_svg_from_contours(elevations, width=1200, height=800, num_contours=20, 
                             line_color="#e0e0e0", bg_color="#1a1a1a", line_width=0.8):
    """
    Convert elevation data to SVG contour lines.
    
    Args:
        elevations: 2D numpy array of elevation values
        width: SVG width
        height: SVG height
        num_contours: Number of contour levels to draw
        line_color: Color of contour lines (hex)
        bg_color: Background color (hex)
        line_width: Width of contour lines
    """
    # Create matplotlib figure in memory
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw contours
    contours = ax.contour(elevations.T, levels=num_contours, colors=line_color, 
                          linewidths=line_width, alpha=0.6)
    
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    # Save to SVG
    svg_path = f"topo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.svg"
    plt.savefig(svg_path, format='svg', facecolor=bg_color, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return svg_path


def create_svg_from_contours_manual(elevations, width=1200, height=800, num_contours=20,
                                   line_color="e0e0e0", bg_color="1a1a1a", line_width=0.8):
    """
    Create SVG manually using contour extraction (more control over output).
    Uses matplotlib's contour finding but manually constructs SVG.
    """
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    
    # Create figure
    fig = Figure(figsize=(width/100, height/100), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw contours
    contour_set = ax.contour(elevations.T, levels=num_contours, 
                              colors=f"#{line_color}", linewidths=line_width, alpha=0.7)
    
    fig.patch.set_facecolor(f"#{bg_color}")
    ax.set_facecolor(f"#{bg_color}")
    
    # Extract SVG manually from paths
    svg_lines = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>']
    svg_lines.append(f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
    svg_lines.append(f'<rect width="{width}" height="{height}" fill="#{bg_color}"/>')
    
    # Add contour paths - handle both old and new matplotlib API
    try:
        # Try newer API (matplotlib >= 3.8)
        collections = contour_set.collections
    except AttributeError:
        # Fall back to older API
        collections = [contour_set]
    
    for collection in collections:
        try:
            paths = collection.get_paths()
            alpha = collection.get_alpha() or 0.7
        except AttributeError:
            # If collection doesn't have get_paths, iterate directly
            paths = collection
            alpha = 0.7
        
        for path in paths:
            try:
                vertices = path.vertices
            except AttributeError:
                # If path doesn't have vertices, skip
                continue
                
            if len(vertices) > 1:
                # Flip Y coordinates (matplotlib vs SVG)
                vertices = vertices.copy()
                vertices[:, 1] = height - vertices[:, 1]
                
                path_str = f"M {vertices[0, 0]:.1f} {vertices[0, 1]:.1f}"
                for vertex in vertices[1:]:
                    path_str += f" L {vertex[0]:.1f} {vertex[1]:.1f}"
                
                svg_lines.append(
                    f'<path d="{path_str}" stroke="#{line_color}" stroke-width="{line_width}" '
                    f'fill="none" opacity="{alpha}"/>'
                )
    
    svg_lines.append('</svg>')
    
    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    svg_path = f"topo_contours_{timestamp}.svg"
    
    with open(svg_path, 'w') as f:
        f.write('\n'.join(svg_lines))
    
    return svg_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate randomized topographic contour SVG backgrounds"
    )
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducibility (default: random)')
    parser.add_argument('--width', type=int, default=1920,
                        help='SVG width in pixels (default: 1920)')
    parser.add_argument('--height', type=int, default=1080,
                        help='SVG height in pixels (default: 1080)')
    parser.add_argument('--contours', type=int, default=20,
                        help='Number of contour lines (default: 20)')
    parser.add_argument('--octaves', type=int, default=4,
                        help='Perlin noise octaves, more = more detail (default: 4)')
    parser.add_argument('--scale', type=int, default=200,
                        help='Noise scale, smaller = more features (default: 200)')
    parser.add_argument('--line-color', default='e0e0e0',
                        help='Line color in hex without # (default: e0e0e0 - light gray)')
    parser.add_argument('--bg-color', default='1a1a1a',
                        help='Background color in hex without # (default: 1a1a1a - dark)')
    parser.add_argument('--line-width', type=float, default=0.8,
                        help='Contour line width (default: 0.8)')
    parser.add_argument('--method', choices=['perlin', 'random'], default='perlin',
                        help='Generation method: perlin or random (default: perlin)')
    parser.add_argument('--output', default=None,
                        help='Output filename (default: auto-generated with timestamp)')
    
    args = parser.parse_args()
    
    print(f"Generating topographic contours...")
    print(f"  Seed: {args.seed if args.seed else 'random'}")
    print(f"  Size: {args.width}x{args.height}")
    print(f"  Contours: {args.contours}")
    print(f"  Method: {args.method}")
    
    # Generate elevation data
    if args.method == 'perlin':
        if HAS_PERLIN:
            elevations = generate_perlin_contours(
                seed=args.seed,
                width=args.width,
                height=args.height,
                octaves=args.octaves,
                scale=args.scale,
                num_contours=args.contours
            )
        else:
            print("  (Falling back to random method - perlin_noise not installed)")
            elevations = generate_random_contours(
                seed=args.seed,
                width=args.width,
                height=args.height,
                num_contours=args.contours
            )
    else:
        elevations = generate_random_contours(
            seed=args.seed,
            width=args.width,
            height=args.height,
            num_contours=args.contours
        )
    
    # Create SVG
    svg_path = create_svg_from_contours_manual(
        elevations,
        width=args.width,
        height=args.height,
        num_contours=args.contours,
        line_color=args.line_color,
        bg_color=args.bg_color,
        line_width=args.line_width
    )
    
    print(f"\n✓ Generated: {svg_path}")
    print(f"\nTo use this in your HTML, embed it as:")
    print(f'  <svg class="topo-svg" data-src="{svg_path}"></svg>')
    
    return svg_path


if __name__ == '__main__':
    main()
