from build123d import *
from ocp_vscode import show_object
from pathlib import Path

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

ring_center_mirror = (-0.211, -66.40)

new_points = [
    (-30.6976, -66.1783),
    (-30.4737, -63.2583),
    (-30.1809, -61.3896),
    (-29.8535, -59.0978),
    (-29.3203, -57.3058),
    (-28.7626, -55.7847),
    (-28.0527, -54.0609),
    (-27.2922, -52.7426),
    (-26.7345, -51.323),
    (-25.7135, -49.9033),
    (-24.9599, -48.6358),
    (-23.9111, -47.2811),
    (-25.7135, -46.2512),
    (-27.3687, -45.258),
    (-29.0607, -44.2649),
    (-30.863, -43.0511),
]

new_points_mirror = [(-x, y) for (x, y) in new_points]

new_points_2 = [
    (-30.9826, -66.2448),
    (-30.888, -63.4993),
    (-30.5569, -61.3925),
    (-29.961, -59.0941),
    (-29.3203, -57.3058),
    (-29.5354, -57.2213),
    (-28.9395, -55.7741),
    (-28.0527, -54.0609),
    (-27.2369, -52.2839),
    (-25.7135, -49.9033),
    (-24.9599, -48.6358),
    (-23.917, -47.091),
    (-25.7135, -46.2512),
    (-27.3687, -45.258),
    (-29.0607, -44.2649),
    (-30.863, -43.0511),
]

new_points_2_mirror = [(-x, y) for (x, y) in new_points_2]

with BuildPart() as dust_collector_top_part:

    # MAIN BODY
    Cylinder(radius=106.4/2, height=5)

    Cylinder(radius=65.52/2, height=5, mode=Mode.SUBTRACT)

    Box(
        length=106.4/2 + 10,
        width=3,
        height=5,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT
    )

    # CUT FEATURE 1
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*cut_points_1, close=True)
        make_face()

    extrude(amount=5, both=True, mode=Mode.SUBTRACT)

    # CUT FEATURE 2
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*cut_points_2, close=True)
        make_face()

    extrude(amount=5, both=True, mode=Mode.SUBTRACT)

    # SIDE ADD FEATURE
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*add_points, close=True)
        make_face()

    extrude(amount=2.5, both=True, mode=Mode.ADD)

    # HOLES
    with BuildSketch(Plane.XY.offset(2.5)):
        for pt in hole_points:
            with Locations((pt[0], pt[1])):
                Circle(radius=4)

    extrude(amount=-1.5, mode=Mode.SUBTRACT)

    # CENTER RING
    with Locations((ring_center_mirror[0], ring_center_mirror[1], 2.5)):
        Cylinder(radius=61.581/2, height=10, mode=Mode.ADD)
        Cylinder(radius=47.252/2, height=10, mode=Mode.SUBTRACT)

    # LOWER FEATURE MIRROR
    with BuildSketch(Plane.XY.offset(-2.5)):
        with BuildLine():
            Polyline(*new_points_mirror, close=True)
        make_face()

    extrude(amount=10, mode=Mode.ADD)

    # TOP CUT
    with BuildSketch(Plane.XY.offset(2.5)):
        Circle(radius=105.624/2)

    extrude(amount=5, mode=Mode.SUBTRACT)

    # NEW FEATURE ORIGINAL
    with BuildSketch(Plane.XY.offset(-2.5)):
        with BuildLine():
            Polyline(
                *new_points_2,
                new_points_2[0],
                close=True
            )
        make_face()

    extrude(amount=5, mode=Mode.ADD)

        # NEW FEATURE ORIGINAL 01
    with BuildSketch(Plane.XY.offset(2.5)):
        with BuildLine():
            Polyline(
                *new_points_2,
                new_points_2[0],
                close=True
            )
        make_face()

    extrude(amount=5, mode=Mode.ADD)

 

# SHOW PART
show_object(dust_collector_top_part.part)

# EXPORT STL
desktop = Path.home() / "Desktop"
stl_file = desktop / "Dust_Collector_Top_Part.stl"

export_stl(dust_collector_top_part.part, str(stl_file))

print("DUST COLLECTOR TOP PART CREATED")
print(f"File : {stl_file}")