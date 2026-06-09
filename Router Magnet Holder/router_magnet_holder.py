from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# ROUTER MAGNET HOLDER
# =========================

cut_points_1 = [
    (0.1645, -68.667),
    (-17.1889, -50.1983),
    (-15.678, -48.7763),
    (-14.3449, -47.5321),
    (-12.4786, -46.2878),
    (-10.5234, -45.2213),
    (-8.4793, -44.3326),
    (-6.9684, -43.6216),
    (-4.1244, -43.1772),
    (-0.8361, -42.7329),
    (1.2969, -42.7329),
    (3.0435, -42.8591),
    (5.1132, -43.2371),
    (7.1917, -43.8106),
    (9.7967, -44.8125),
    (12.3015, -46.1484),
    (14.0048, -47.2505),
    (15.7081, -48.6866),
    (17.1776, -50.1561),
]

cut_points_2 = [
    (-37.4829, -37.6588),
    (-37.3156, 37.9106),
    (-80.5383, 38.0608),
    (-80.5383, -37.801),
]

add_points = [
    (-42.7268, -37.6588),
    (-37.4829, -37.6588),
    (-37.3156, 37.9106),
    (-42.7268, 37.8491),
]

# Bottom face hole locations (X, Y only)
hole_points = [
    (-34.8273, 22.6432),
    (-34.8273, -22.7358),
    (-20.9973, -38.3007),
    (22.8927, -36.5174),
    (39.447, -17.8556),
    (39.447, 17.8408),
    (22.9217, 36.4763),
    (1.1473, 42.5569),
    (-20.9973, 37.9515),
]

with BuildPart() as router_magnet_holder:
    # Main outer cylinder
    Cylinder(radius=106.4/2, height=5)
    # Inner bore cut
    Cylinder(radius=65.52/2, height=5, mode=Mode.SUBTRACT)
    # 3mm GAP cut through wall (C-ring style)
    Box(
        length=106.4/2 + 10,
        width=3,
        height=5,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT
    )
    # Cut 1 - Curved profile through cut
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*cut_points_1, close=True)
        make_face()
    extrude(amount=5, both=True, mode=Mode.SUBTRACT)

    # Cut 2 - Rectangle through cut
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*cut_points_2, close=True)
        make_face()
    extrude(amount=5, both=True, mode=Mode.SUBTRACT)

    # ADD MATERIAL
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*add_points, close=True)
        make_face()
    extrude(amount=2.5, both=True, mode=Mode.ADD)

    # HOLES on bottom face - Dia 8mm, Depth 1.5mm
    with BuildSketch(Plane.XY.offset(-2.5)):  # bottom face
        for pt in hole_points:
            with Locations((pt[0], pt[1])):
                Circle(radius=4)  # 8mm dia = 4mm radius
    extrude(amount=1.5, mode=Mode.SUBTRACT)

show_object(router_magnet_holder.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Router_Magnet_Holder.stl"
export_stl(router_magnet_holder.part, str(stl_file))
print("ROUTER MAGNET HOLDER CREATED")
print(f"File : {stl_file}")