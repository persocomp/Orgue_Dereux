from svgpathtools import svg2paths, Line
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.affinity import rotate
import matplotlib.pyplot as plt
import pandas as pd

def path_to_polygon(path_obj, resolution=1000):
    points = [path_obj.point(t / resolution) for t in range(resolution + 1)]
    coords = [(pt.real, pt.imag) for pt in points]
    coords = list(dict.fromkeys(coords))
    if len(coords) >= 3:
        return Polygon(coords)
    return None

def extract_polygons_from_svg(svg_file, resolution=1000):
    paths, _ = svg2paths(svg_file)
    polygons = []
    for path in paths:
        try:
            subpaths = path.continuous_subpaths()
        except Exception:
            continue
        for sub in subpaths:
            if sub.start != sub.end:
                sub.append(Line(sub.end, sub.start))
            poly = path_to_polygon(sub, resolution)
            if poly and poly.is_valid and not poly.is_empty:
                polygons.append(poly)
    return unary_union(polygons) if polygons else None

def convert_svg_area_to_pixels2(area_svg_units, dpi=600):
    scale = dpi / 96
    return area_svg_units * (scale ** 2)

def compute_intersections_over_rotation(shape1, shape2, step=0.01, dpi=600):
    results = []
    angle = 0.0
    while angle <= 360.0:
        rotated_shape2 = rotate(shape2, angle, origin=(268.635, 299.127), use_radians=False)
        intersection = shape1.intersection(rotated_shape2).buffer(0)
        area_svg = intersection.area if not intersection.is_empty else 0
        area_px = convert_svg_area_to_pixels2(area_svg, dpi)
        if int(angle * 100) % 1000 == 0:
            print(f"Angle {angle:.2f}° ➜ Aire intersection : {area_px:.2f} pixels²")
        results.append((round(angle, 2), area_px))
        angle += step
    return results

def plot_intersection_graph(results, dpi=600):
    angles = [r[0] for r in results]
    areas_px = [r[1] for r in results]
    plt.figure(figsize=(10, 5))
    plt.plot(angles, areas_px, marker='o', linestyle='-', linewidth=0.5)
    plt.title(f"Aire d'intersection (pixels²) à {dpi} DPI")
    plt.xlabel("Angle de rotation (°)")
    plt.ylabel("Aire d'intersection (pixels²)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def export_to_csv(results, output_path):
    df = pd.DataFrame(results, columns=["Angle", "IntersectionArea_Pixels²"])
    df.to_csv(output_path, index=False)
    print(f"📁 Données exportées vers {output_path}")

def plot_svg_shapes(shape1, shape2, title="Formes originales"):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))
    plt.title(title)
    plt.axis("equal")
    if shape1.geom_type == "Polygon":
        x, y = shape1.exterior.xy
        plt.fill(x, y, color='blue', alpha=0.4, label="Forme 1")
    elif shape1.geom_type == "MultiPolygon":
        for poly in shape1.geoms:
            x, y = poly.exterior.xy
            plt.fill(x, y, color='blue', alpha=0.4)
    if shape2.geom_type == "Polygon":
        x, y = shape2.exterior.xy
        plt.fill(x, y, color='green', alpha=0.4, label="Forme 2")
    elif shape2.geom_type == "MultiPolygon":
        for poly in shape2.geoms:
            x, y = poly.exterior.xy
            plt.fill(x, y, color='green', alpha=0.4)
    plt.legend()
    plt.grid(True)
    plt.show()

# === CONFIGURATION ===
svg_file1 = "C:\\Users\\pierr\\OneDrive\\Bureau\\2MMLEN-Cours\\Projet - Orgue\\Liste forme\\Forme2.svg"
svg_file2 = "C:\\Users\\pierr\\OneDrive\\Bureau\\2MMLEN-Cours\\Projet - Orgue\\Disque1.svg"
resolution = 1000
step = 0.01
dpi = 600
output_csv = "C:\\Users\\pierr\\OneDrive\\Bureau\\2MMLEN-Cours\\Projet - Orgue\\Liste forme\\SVGForme2.csv"

# === TRAITEMENT ===
shape1 = extract_polygons_from_svg(svg_file1, resolution)
shape2 = extract_polygons_from_svg(svg_file2, resolution)

plot_svg_shapes(shape1, shape2, title="Formes originales avant rotation")
results = compute_intersections_over_rotation(shape1, shape2, step, dpi)
plot_intersection_graph(results, dpi)
export_to_csv(results, output_csv)
