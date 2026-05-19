# Topographic Contour Generator

Generate custom, randomized topographic contour map backgrounds for your publications page.

## Installation

First, install the required packages:

```bash
pip install numpy matplotlib perlin-noise
```

(If you don't want to install `perlin-noise`, the script will fall back to a random generation method.)

## Usage

### Basic Usage

Generate a random topographic contour SVG with default settings:

```bash
python generate_topo_contours.py
```

This creates a file like `topo_contours_20240519_143022.svg` in your current directory.

### With a Specific Seed (for Reproducibility)

If you find a contour map you like, use the seed to regenerate it later:

```bash
python generate_topo_contours.py --seed 42
```

This uses seed `42`, so you'll always get the same contour pattern.

### Adjusting Parameters

**Number of contours (default: 20):**
```bash
python generate_topo_contours.py --contours 30  # More contours = denser
python generate_topo_contours.py --contours 10  # Fewer = sparser
```

**Line width (default: 0.8):**
```bash
python generate_topo_contours.py --line-width 1.2  # Thicker lines
python generate_topo_contours.py --line-width 0.5  # Thinner lines
```

**Line color (default: e0e0e0, light gray):**
```bash
python generate_topo_contours.py --line-color "a0a0a0"  # Darker gray
python generate_topo_contours.py --line-color "00d4d4"  # Teal (LCARS!)
python generate_topo_contours.py --line-color "ff9d42"  # Orange (LCARS!)
```

**Background color (default: 1a1a1a, dark):**
```bash
python generate_topo_contours.py --bg-color "0a0a0a"  # Even darker
```

**Noise detail (Perlin method only, default octaves: 4):**
```bash
python generate_topo_contours.py --octaves 6  # More fractal detail
python generate_topo_contours.py --octaves 2  # Smoother, larger features
```

**Generation method (default: perlin):**
```bash
python generate_topo_contours.py --method random   # Use random peaks instead
```

### Full Example with All Options

```bash
python generate_topo_contours.py \
  --seed 123 \
  --contours 25 \
  --line-width 0.9 \
  --line-color "a8a8a8" \
  --octaves 5 \
  --method perlin
```

## Iteration Workflow

Here's how to find a contour pattern you like:

1. **Generate several random variations:**
   ```bash
   python generate_topo_contours.py --seed 1
   python generate_topo_contours.py --seed 2
   python generate_topo_contours.py --seed 3
   ```

2. **View the SVGs** — Open them in your browser or image viewer to see the patterns

3. **Once you find one you like, note the seed:**
   - If you like `topo_contours_...svg` generated with `--seed 42`, save that seed

4. **Fine-tune parameters** with that seed:
   ```bash
   python generate_topo_contours.py --seed 42 --contours 22 --line-width 1.0
   ```

5. **Try different colors:**
   ```bash
   python generate_topo_contours.py --seed 42 --line-color "00d4d4"  # Teal
   ```

6. **Test with different octaves** (for Perlin):
   ```bash
   python generate_topo_contours.py --seed 42 --octaves 3  # Smoother
   python generate_topo_contours.py --seed 42 --octaves 6  # More detail
   ```

## Using the SVG in Your HTML

Once you've found a contour map you like:

1. **Copy the SVG file** to your publications folder:
   ```bash
   cp topo_contours_XXXXXX.svg /path/to/publications/images/topo-bg.svg
   ```

2. **Update your HTML** to use it instead of the inline SVG:
   
   Replace this:
   ```html
   <svg class="topo-svg" viewBox="0 0 1200 800">
     <!-- inline SVG content -->
   </svg>
   ```
   
   With this:
   ```html
   <svg class="topo-svg" data-src="/publications/images/topo-bg.svg"></svg>
   ```

   Or embed it directly:
   ```html
   <object class="topo-svg" data="/publications/images/topo-bg.svg" type="image/svg+xml"></object>
   ```

3. **Update the CSS parallax script** — the existing script in `publications-index-final.html` will work with both inline and external SVGs

## Parameter Recommendations

### For a Subtle, Professional Look:
```bash
python generate_topo_contours.py --seed YOURNUM --contours 15 --line-width 0.6 --line-color "c0c0c0"
```

### For a Bold, Dramatic Look:
```bash
python generate_topo_contours.py --seed YOURNUM --contours 30 --line-width 1.2 --line-color "a0a0a0"
```

### For LCARS Color Palette:
```bash
python generate_topo_contours.py --seed YOURNUM --line-color "00d4d4"  # Teal
# or
python generate_topo_contours.py --seed YOURNUM --line-color "ff9d42"  # Orange
```

### For High Detail (Perlin):
```bash
python generate_topo_contours.py --seed YOURNUM --octaves 6 --contours 25
```

### For Smooth, Large Features (Perlin):
```bash
python generate_topo_contours.py --seed YOURNUM --octaves 2 --contours 15
```

## Troubleshooting

**"perlin_noise not installed"**
- Install it: `pip install perlin-noise`
- Or use the fallback: `--method random`

**Lines are too thick/thin**
- Adjust `--line-width` (range 0.5-2.0 is usually good)

**Too many or too few contours**
- Adjust `--contours` (try 10-40)

**Pattern looks too uniform/random**
- For Perlin: adjust `--octaves` (2-6 range)
- For random: that's the nature of it; try a different seed

**Colors not showing up**
- Make sure you're using hex colors *without* the `#` symbol
- Example: `--line-color "ff0000"` (not `#ff0000`)

## Example Use Case

You want a subtle teal-tinted topographic background:

```bash
# Generate with seed 777, 18 contours, thin lines, teal color
python generate_topo_contours.py --seed 777 --contours 18 --line-width 0.7 --line-color "00a8a8"

# View topo_contours_XXXXXX.svg in browser
# Like it? Copy to your repo:
cp topo_contours_XXXXXX.svg publications/images/topo-bg.svg

# Update your HTML to use it
# Done!
```

---

## Advanced: Tweaking the Generator

If you want to modify the generation logic itself, edit `generate_topo_contours.py`:

- **`generate_perlin_contours()`** — Uses Perlin noise for organic-looking terrain
- **`generate_random_contours()`** — Uses random Gaussian peaks; simpler, faster
- **`create_svg_from_contours_manual()`** — Converts elevation data to SVG paths

The Perlin method generally produces smoother, more natural-looking contours. The random method produces more jagged, mountain-peak style patterns.
