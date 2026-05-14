from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# Z CARRIAGE TOP
# =========================

# Profile points on XZ plane at Y=31.33, (X, Z) coordinates
z_carriage_top_points = [
    (336.03, 183.39),
    (336.03, 188.39),
    (317.03, 188.39),
    (317.03, 193.39),
    (372.26, 193.39),
    (372.26, 188.39),
    (353.26, 188.39),
    (353.26, 183.39),
]

# 7 mm dia thru holes on top face (X, Y) on XY plane at Z=193.39
hole_points_7mm = [
    (324.71, -46.16),
    (364.71, -46.16),
]

# 3 mm dia thru holes on top face (4 corner points)
hole_points_3mm = [
    (338.99, -40.51),
    (350.31, -40.47),
    (338.98, -51.79),
    (350.30, -51.77),
]

# 12 mm dia thru hole on top face (center point)
hole_points_12mm = [
    (344.62, -46.04),
]

with BuildPart() as z_carriage_top:
    with BuildSketch(Plane.XZ.offset(31.33)):
        with BuildLine():
            Polyline(*z_carriage_top_points, close=True)
        make_face()
    extrude(amount=29.698)

    # 7 mm dia thru holes (along Z)
    with BuildSketch(Plane.XY.offset(193.39)):
        for x, y in hole_points_7mm:
            with Locations((x, y)):
                Circle(radius=3.5)
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    # 3 mm dia thru holes (along Z)
    with BuildSketch(Plane.XY.offset(193.39)):
        for x, y in hole_points_3mm:
            with Locations((x, y)):
                Circle(radius=1.5)
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    # 12 mm dia thru hole (along Z)
    with BuildSketch(Plane.XY.offset(193.39)):
        for x, y in hole_points_12mm:
            with Locations((x, y)):
                Circle(radius=6.3)
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

show_object(z_carriage_top.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_Carriage_Top.stl"
export_stl(z_carriage_top.part, str(stl_file))
print("Z CARRIAGE TOP CREATED")
print(f"File : {stl_file}")