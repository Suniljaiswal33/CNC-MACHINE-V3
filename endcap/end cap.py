from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import math

# =========================
# END CAP
# =========================

loft_profile_1 = [
    (7.9754, -10.0216),
    (8.6341, -9.8754),
    (9.0836, -9.6756),
    (9.4332, -9.3759),
    (9.7578, -8.9639),
    (9.9576, -8.4145),
    (10.0121, -7.9704),
    (10.0137, 8.0225),
    (9.942, 8.5014),
    (9.6809, 9.0816),
    (9.178, 9.6232),
    (8.4674, 9.949),
    (7.9079, 9.9926),
    (-7.9374, 10.0017),
    (-8.7311, 9.848),
    (-9.3279, 9.5137),
    (-9.8144, 8.8418),
    (-9.9998, 7.9845),
    (-10.0, -8.0),
    (-9.8396, -8.7433),
    (-9.5328, -9.2546),
    (-8.9874, -9.7318),
    (-8.4931, -9.9364),
    (-7.9476, -10.0216),
]

loft_profile_2 = [
    (-7.68, 9.6),
    (-8.3696, 9.459),
    (-8.9291, 9.1316),
    (-9.3794, 8.5448),
    (-9.5967, 7.6752),
    (-9.6, -7.68),
    (-9.4591, -8.3474),
    (-9.1733, -8.8611),
    (-8.64, -9.3404),
    (-8.1769, -9.5346),
    (-7.68, -9.6),
    (7.658, -9.6),
    (8.3372, -9.4733),
    (8.7713, -9.2562),
    (9.0934, -8.9762),
    (9.3791, -8.5889),
    (9.5485, -8.0729),
    (9.5948, 7.6863),
    (9.5334, 8.1733),
    (9.3399, 8.6475),
    (9.0389, 9.0284),
    (8.6442, 9.3367),
    (8.1878, 9.5259),
]

# Loft profile A (first cross section) - 3 boundaries
loft_A1 = [(-2.1345, -8.0975), (-3.0132, -7.7994), (-2.5949, -6.4905), (-1.7085, -6.7512)]
loft_A2 = [(0.496, -8.3642), (-0.4556, -8.3642), (-0.4832, -6.9467), (0.4814, -6.9467)]
loft_A3 = [(3.0499, -7.7994), (2.1362, -8.1055), (1.7067, -6.7772), (2.6061, -6.4905)]

# Loft profile B (second cross section) - 3 boundaries
loft_B1 = [(-3.2205, -8.3805), (-2.3081, -8.6934), (-1.7085, -6.7512), (-2.5949, -6.4905)]
loft_B2 = [(0.4814, -8.9541), (0.4814, -6.9467), (-0.4832, -6.9467), (-0.4832, -8.9541)]
loft_B3 = [(2.2933, -8.6543), (3.2318, -8.3675), (2.6061, -6.4905), (1.7067, -6.7772)]

def rotate_points(points, angle_deg):
    angle = math.radians(angle_deg)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return [
        (x * cos_a - y * sin_a, x * sin_a + y * cos_a)
        for x, y in points
    ]

def make_loft_feature(part, a1, a2, a3, b1, b2, b3):
    """Teen loft features banao - har boundary ke liye ek loft"""
    for pa, pb in [(a1, b1), (a2, b2), (a3, b3)]:
        with BuildPart() as loft_tool:
            with BuildSketch(Plane.XY.offset(10)):
                with BuildLine():
                    Polyline(*pa, close=True)
                make_face()
            with BuildSketch(Plane.XY.offset(0)):
                with BuildLine():
                    Polyline(*pb, close=True)
                make_face()
            loft()
        part.part = part.part.fuse(loft_tool.part)

with BuildPart() as end_cap:
    # Main loft feature
    with BuildSketch(Plane.XY.offset(0)):
        with BuildLine():
            Polyline(*loft_profile_1, close=True)
        make_face()

    with BuildSketch(Plane.XY.offset(-2)):
        with BuildLine():
            Polyline(*loft_profile_2, close=True)
        make_face()

    loft()

    # Tube loft
    with BuildSketch(Plane.XY.offset(0)):
        Circle(radius=15/2)
        Circle(radius=15/2 - 2, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(10)):
        Circle(radius=13.95/2)
        Circle(radius=13.95/2 - 1.47, mode=Mode.SUBTRACT)

    loft()

# 4 instances - 0, 90, 180, 270 degree
for angle in [0, 90, 180, 270]:
    a1 = rotate_points(loft_A1, angle)
    a2 = rotate_points(loft_A2, angle)
    a3 = rotate_points(loft_A3, angle)
    b1 = rotate_points(loft_B1, angle)
    b2 = rotate_points(loft_B2, angle)
    b3 = rotate_points(loft_B3, angle)

    make_loft_feature(end_cap, a1, a2, a3, b1, b2, b3)

show_object(end_cap.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "End_Cap.stl"
export_stl(end_cap.part, str(stl_file))
print("END CAP CREATED")
print(f"File : {stl_file}")