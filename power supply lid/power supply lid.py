from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# POWER SUPPLY LID
# =========================

profile_points = [
    (63.00, 13.60),
    (61.40, 13.60),
    (61.40, 3.60),
    (61.20, 2.73),
    (60.96, 2.35),
    (60.65, 2.04),
    (60.27, 1.80),
    (59.40, 1.60),
    (0.00, 1.60),
    (0.00, 0.00),
    (63.00, 0.00),
]

top_cut_points = [
    (13.00, 63.00),
    (13.00, 52.00),
    (13.20, 51.13),
    (13.75, 50.44),
    (14.55, 50.05),
    (86.00, 50.00),
    (86.87, 50.20),
    (87.56, 50.75),
    (87.95, 51.55),
    (88.00, 52.00),
    (88.00, 63.00),
]

hole_points = [
    (6.52,  6.80),
    (99.11, 6.80),
]

# Top face cut - Z=1.60 constant, X aur Y use karenge
top_cut_2_points = [
    (0.00,    1.97),
    (0.05,    1.55),
    (0.20,    1.13),
    (0.44,    0.75),
    (0.75,    0.44),
    (1.13,    0.20),
    (1.55,    0.05),
    (2.00,    0.00),
    (108.00, -0.00),
    (108.45,  0.05),
    (108.87,  0.20),
    (109.25,  0.44),
    (109.56,  0.75),
    (109.80,  1.13),
    (109.95,  1.55),
    (110.01,  1.99),
    (110.01, -7.10),
    (0.00,   -7.10),
]

with BuildPart() as power_supply_lid:
    with BuildSketch(Plane.YZ):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
    extrude(amount=110)

    # Top face thru cut 1
    with BuildSketch(Plane.XY.offset(13.60)):
        with BuildLine():
            Polyline(*top_cut_points, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    # Front face holes
    with BuildSketch(Plane.XZ.offset(61.40)):
        for x, z in hole_points:
            with Locations((x, z)):
                Circle(radius=1.5)
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    # Top face thru cut 2 - Z=1.60 par
    with BuildSketch(Plane.XY.offset(1.60)):
        with BuildLine():
            Polyline(*top_cut_2_points, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

show_object(power_supply_lid.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Power_Supply_Lid.stl"
export_stl(power_supply_lid.part, str(stl_file))
print("POWER SUPPLY LID CREATED")
print(f"File : {stl_file}")