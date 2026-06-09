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
# Bottom Ring (Flange)
RING1_OD = 760
RING1_ID = 600
RING1_H = 20

# Top Ring
RING2_OD = 640
RING2_ID = 600
RING2_H = 20

# PCD Holes on Bottom Flange
PCD = 700
HOLE_DIA = 30
NUM_HOLES = 4  # 4 quadrants: 0°, 90°, 180°, 270°

# ======================
# CREATE VACUUM HOSE ADAPTER
# ======================
with BuildPart() as adapter:

    # ------ Bottom Ring (OD 760, ID 600, H 20) ------
    with BuildSketch(Plane.XY):
        Circle(RING1_OD / 2)
        Circle(RING1_ID / 2, mode=Mode.SUBTRACT)
    extrude(amount=RING1_H)

    # ------ Top Ring (OD 640, ID 600, H 20) ------
    with BuildSketch(Plane(origin=(0, 0, RING1_H))):
        Circle(RING2_OD / 2)
        Circle(RING2_ID / 2, mode=Mode.SUBTRACT)
    extrude(amount=RING2_H)

    # ------ 4 THROUGH HOLES ON PCD 700 (BOTTOM FLANGE) ------
    pcd_radius = PCD / 2
    hole_points = []
    for i in range(NUM_HOLES):
        angle = math.radians(i * (360 / NUM_HOLES))  # 0°, 90°, 180°, 270°
        x = pcd_radius * math.cos(angle)
        y = pcd_radius * math.sin(angle)
        hole_points.append((x, y))

    with BuildSketch(Plane.XY):
        with Locations(*hole_points):
            Circle(HOLE_DIA / 2)
    extrude(amount=RING1_H, mode=Mode.SUBTRACT)

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
stl_path = desktop / "Vacuum-hose-adapter.stl"

mesher = Mesher()
mesher.add_shape(scaled_part)
mesher.write(str(stl_path))

# ======================
# INFO
# ======================
bb_original = final_part.bounding_box()
bb_scaled = scaled_part.bounding_box()

print("=" * 60)
print("VACUUM HOSE ADAPTER CREATED")
print("=" * 60)
print(f"File : {stl_path}")
print(f"Size : {stl_path.stat().st_size / 1024:.1f} KB")
print(f"Scale Factor : {SCALE_FACTOR}")
print()
print("Ring 1 (Bottom Flange) :")
print(f"  OD = {RING1_OD} mm, ID = {RING1_ID} mm, H = {RING1_H} mm")
print("Ring 2 (Top) :")
print(f"  OD = {RING2_OD} mm, ID = {RING2_ID} mm, H = {RING2_H} mm")
print()
print(f"PCD Holes : {NUM_HOLES} x Ø{HOLE_DIA} mm on PCD {PCD} mm")
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