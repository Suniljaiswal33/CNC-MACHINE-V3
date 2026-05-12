from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# END STOP LEFT
# =========================

profile_points = [
    (25.0, -20.1421),
    (1.0, -20.1421),
    (1.0, -13.1421),
    (14.1421, 0.0),
    (1.0, 13.1421),
    (1.0, 20.1421),
    (25.0, 20.1421),
]

hole_points = [
    (25.0, -17.1015, 5.0197),
    (25.0, 17.1707, 5.0197),
]

with BuildPart() as end_stop_left:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
    extrude(amount=10)

    # Right face (YZ plane at x=25) par through holes
    with BuildSketch(Plane.YZ.offset(25)):
        for pt in hole_points:
            with Locations((pt[1], pt[2])):
                Circle(radius=1.5)
    extrude(amount=-25, mode=Mode.SUBTRACT)

show_object(end_stop_left.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "End_Stop_Left.stl"
export_stl(end_stop_left.part, str(stl_file))
print("END STOP LEFT CREATED")
print(f"File : {stl_file}")