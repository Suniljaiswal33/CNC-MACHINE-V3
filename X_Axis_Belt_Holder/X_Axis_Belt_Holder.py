from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# X AXIS BELT HOLDER
# =========================

# Profile points on XZ plane at Y=-126.27 (Plane.XZ normal is -Y)
belt_holder_points = [
    (745.00, 132.14),
    (748.00, 135.14),
    (764.50, 135.14),
    (766.00, 136.64),
    (766.00, 145.14),
    (780.00, 145.14),
    (780.00, 110.14),
    (766.00, 110.14),
    (766.00, 118.64),
    (764.50, 120.14),
    (748.00, 120.14),
    (745.00, 123.14),
]

# 8 mm dia thru hole (X, Z) - cuts along Y
hole_points_xz = [
    (752.50, 127.68),
]

# 4 mm dia thru holes on right face (Y, Z) on YZ plane at X=780
# Part Y range is -126.27 to -136.27, so Y must be negative
hole_points_yz = [
    (-131.19, 115.14),
    (-131.19, 140.21),
]

with BuildPart() as x_axis_belt_holder:
    with BuildSketch(Plane.XZ.offset(126.27)):
        with BuildLine():
            Polyline(*belt_holder_points, close=True)
        make_face()
    extrude(amount=10)

    # 8 mm dia thru hole (along Y)
    with BuildSketch(Plane.XZ.offset(126.27)):
        for x, z in hole_points_xz:
            with Locations((x, z)):
                Circle(radius=4.0)
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    # 4 mm dia thru holes on right face (along X)
    with BuildSketch(Plane.YZ.offset(780.00)):
        for y, z in hole_points_yz:
            with Locations((y, z)):
                Circle(radius=2.0)
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

show_object(x_axis_belt_holder.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "X_Axis_Belt_Holder.stl"
export_stl(x_axis_belt_holder.part, str(stl_file))
print("X AXIS BELT HOLDER CREATED")
print(f"File : {stl_file}")