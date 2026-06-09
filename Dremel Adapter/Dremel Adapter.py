from build123d import *
from pathlib import Path
from ocp_vscode import show_object, set_port, reset_show
import math

# ======================
# OCP VIEWER
# ======================
set_port(3939)
reset_show()

# ======================
# PARAMETERS
# ======================
RING_OD = 650
RING_ID = 475
RING_H = 250

# Slit Cut (30 mm width, full height, through wall)
SLIT_WIDTH = 30

# 30 MM Through Holes at ±20° from vertical (bottom side)
HOLE_DIA = 30
HOLE_ANGLE = 20      # degrees from vertical (Y-axis), both sides
HOLE_PCD = (RING_OD + RING_ID) / 2  # mid-radius of wall = 562.5

# ======================
# CREATE DREMEL ADAPTER
# ======================
with BuildPart() as adapter:

    # ------ Main Ring (OD 650, ID 475, H 250) ------
    with BuildSketch(Plane.XY):
        Circle(RING_OD / 2)
        Circle(RING_ID / 2, mode=Mode.SUBTRACT)
    extrude(amount=RING_H)

    # ------ 30 MM WIDTH SLIT CUT THROUGH WALL (bottom side, -Y) ------
    wall_thickness = (RING_OD - RING_ID) / 2
    cut_length = wall_thickness + 10

    with BuildSketch(Plane.XY):
        with Locations((0, -(RING_ID / 2 - 5))):  # bottom side, start inside ID
            Rectangle(
                SLIT_WIDTH,
                cut_length,
                align=(Align.CENTER, Align.MAX),
            )
    extrude(amount=RING_H, mode=Mode.SUBTRACT)

    # ------ 2 THROUGH HOLES (30 dia) AT ±20° FROM VERTICAL ------
    # Vertical line is along -Y direction (bottom)
    # Hole centers on PCD (mid-wall radius), symmetric about Y-axis
    pcd_radius = HOLE_PCD / 2

    hole_points = []
    for sign in [-1, +1]:  # left side (-X) and right side (+X)
        angle_from_neg_y = math.radians(sign * HOLE_ANGLE)
        # -Y direction is base; rotate by ±20°
        x = pcd_radius * math.sin(angle_from_neg_y)
        y = -pcd_radius * math.cos(angle_from_neg_y)
        hole_points.append((x, y))

    with BuildSketch(Plane.XY):
        with Locations(*hole_points):
            Circle(HOLE_DIA / 2)
    extrude(amount=RING_H, mode=Mode.SUBTRACT)

# ======================
# FINAL PART
# ======================
final_part = adapter.part

# ======================
# SHOW IN OCP VIEWER (original size)
# ======================
show_object(final_part)

# ======================
# SCALE DOWN BY 0.1 BEFORE EXPORT
# ======================
SCALE_FACTOR = 0.1
scaled_part = final_part.scale(SCALE_FACTOR)

# ======================
# EXPORT STL (scaled)
# ======================
desktop = Path.home() / "Desktop"
stl_path = desktop / "Dremel-Adapter.stl"

mesher = Mesher()
mesher.add_shape(scaled_part)
mesher.write(str(stl_path))

# ======================
# INFO
# ======================
bb_original = final_part.bounding_box()
bb_scaled = scaled_part.bounding_box()

print("=" * 60)
print("DREMEL ADAPTER CREATED")
print("=" * 60)
print(f"File : {stl_path}")
print(f"Size : {stl_path.stat().st_size / 1024:.1f} KB")
print(f"Scale Factor : {SCALE_FACTOR}")
print()
print(f"Ring : OD = {RING_OD} mm, ID = {RING_ID} mm, H = {RING_H} mm")
print(f"Slit : {SLIT_WIDTH} mm width, full height through wall (bottom side)")
print(f"Holes : 2 x Ø{HOLE_DIA} mm at ±{HOLE_ANGLE}° from vertical, PCD {HOLE_PCD:.1f} mm")
print("Hole Locations (X, Y) :")
for i, (x, y) in enumerate(hole_points):
    print(f"  Hole {i+1} : ({x:.2f}, {y:.2f})")
print()
print("Original Dimensions :")
print(
    f"  {bb_original.max.X - bb_original.min.X:.1f} x "
    f"{bb_original.max.Y - bb_original.min.Y:.1f} x "
    f"{bb_original.max.Z - bb_original.min.Z:.1f} mm"
)
print()
print("Scaled Dimensions (exported) :")
print(
    f"  {bb_scaled.max.X - bb_scaled.min.X:.2f} x "
    f"{bb_scaled.max.Y - bb_scaled.min.Y:.2f} x "
    f"{bb_scaled.max.Z - bb_scaled.min.Z:.2f} mm"
)
print()
print(f"Original Volume : {final_part.volume:,.0f} mm³")
print(f"Scaled Volume   : {scaled_part.volume:,.2f} mm³")
print("=" * 60)