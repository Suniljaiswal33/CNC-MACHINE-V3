from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# BEARING BELT GUIDENER
# =========================

points = [
    (0.0, -143.2991, -2160.8723),
    (0.0, -111.5635, -2160.8723),
    (0.0, -111.5635, -2051.5972),
    (0.0, -143.2991, -2051.5972),
    (0.0, -143.2991, -2060.758),
    (0.0, -133.5541, -2060.758),
    (0.0, -128.164, -2062.2116),
    (0.0, -124.6866, -2064.2981),
    (0.0, -121.5569, -2067.08),
    (0.0, -119.9921, -2070.2097),
    (0.0, -118.6011, -2075.0781),
    (0.0, -118.6011, -2135.9333),
    (0.0, -119.1932, -2139.7039),
    (0.0, -120.3945, -2143.0304),
    (0.0, -122.5197, -2146.1721),
    (0.0, -124.467, -2147.9032),
    (0.0, -126.5085, -2149.2347),
    (0.0, -129.4376, -2150.5661),
    (0.0, -132.1892, -2151.1874),
    (0.0, -134.8521, -2151.1874),
    (0.0, -143.5517, -2151.1874),
]

with BuildPart() as bearing_belt_guidener:

    # Sketch on YZ Plane
    with BuildSketch(Plane.YZ):

        yz_points = [(y, z) for x, y, z in points]

        Polygon(*yz_points)

    # Revolve about Z Axis
    revolve(axis=Axis.Z)

# =========================
# SCALE 0.1
# =========================

scaled_part = scale(bearing_belt_guidener.part, by=0.1)

# Show model
show_object(scaled_part)

# =========================
# EXPORT STL
# =========================

desktop = Path.home() / "Desktop"
stl_file = desktop / "BEARING_BELT_GUIDENER.stl"

export_stl(scaled_part, str(stl_file))

print("\n============================")
print("BEARING BELT GUIDENER CREATED")
print("============================")
print(f"File : {stl_file}")
print("============================")