from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# END STOP RIGHT
# =========================

profile_points = [
    (-1.0, -20.1421),
    (-1.0, -13.1421),
    (-14.1421, 0.0),
    (-1.0, 13.1421),
    (-1.0, 20.1421),
    (-20.0, 20.1421),
    (-20.0, -20.1421),
]

hole_points = [
    (-1.0, -17.1469, 4.9636),
    (-1.0, 17.229, 4.9636),
]

with BuildPart() as end_stop_right:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
    extrude(amount=10)

    # Right face (YZ plane at x=-1) par through holes
    with BuildSketch(Plane.YZ.offset(-1)):
        for pt in hole_points:
            with Locations((pt[1], pt[2])):
                Circle(radius=2)  # 4mm dia = 2mm radius
    extrude(amount=-20, mode=Mode.SUBTRACT)

show_object(end_stop_right.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "End_Stop_Right.stl"
export_stl(end_stop_right.part, str(stl_file))
print("END STOP RIGHT CREATED")
print(f"File : {stl_file}")