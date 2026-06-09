from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# Z SLIDER TOP - ALL 8 FEATURES (FINAL)
# =========================

profile_1_pts = [
    (63.68, 8.77),    (63.68, 12.27),   (65.52, 12.27),   (65.52, 17.27),
    (63.68, 17.27),   (63.68, 22.27),   (36.36, 22.27),   (36.36, 17.27),
    (34.52, 17.27),   (34.52, 12.27),   (36.36, 12.27),   (36.36, 8.77),
]

profile_2_pts = [
    (63.68, 22.27),   (63.68, 17.27),   (65.52, 17.27),   (65.52, 12.27),
    (63.68, 12.27),   (63.68, 8.77),    (58.68, 8.77),    (58.68, 12.27),
    (60.52, 12.27),   (60.52, 17.27),   (58.68, 17.27),   (58.68, 22.27),
]

profile_3_ellipse_pts = [
    (265.8795, 45.6983),  (266.8462, 45.8448),  (267.6156, 46.0767),  (268.32, 46.574),
    (268.8675, 47.1044),  (269.3947, 47.9246),  (269.6475, 48.6201),  (269.757, 49.1605),
    (269.7862, 50.0026),  (269.6475, 50.6939),  (269.2875, 51.6498),  (268.6171, 52.5065),
    (267.7729, 53.1272),  (266.9395, 53.51),    (265.8326, 53.6785),  (260.0285, 53.6785),
    (259.3527, 53.6526),  (258.6813, 53.4905),  (257.9636, 53.2127),  (257.2691, 52.7728),
    (256.8177, 52.3561),  (256.4241, 51.7889),  (256.1116, 51.2217),  (255.8916, 50.5337),
    (255.796, 49.8354),   (255.8394, 49.0341),  (256.0013, 48.3864),  (256.3021, 47.7386),
    (256.6723, 47.1602),  (257.0887, 46.7206),  (257.5745, 46.3505),  (258.0835, 46.0497),
    (258.685, 45.8415),   (259.3097, 45.7027),
]

profile_4_top_pts = [
    (302.15, 36.36),  (249.15, 36.36),  (249.15, 63.68),  (271.61, 63.68),
    (271.61, 58.68),  (302.15, 58.68),
]

profile_5_bottom_pts = [
    (302.15, 36.36),  (302.15, 58.68),  (270.61, 58.68),  (270.61, 63.68),
    (249.15, 63.68),  (249.15, 36.36),
]

diamond_pts = [
    (252.0846, 49.653),   (262.7851, 38.8855),  (273.5335, 49.653),   (262.7851, 60.483),
]

profile_7_pts = [
    (288.81, 17.77),  (288.37, 17.74),  (287.94, 17.65),  (287.53, 17.49),
    (287.15, 17.27),  (286.81, 17.01),  (286.47, 16.73),  (286.19, 16.40),
    (285.96, 16.03),  (285.79, 15.63),  (285.69, 15.21),  (285.65, 14.77),
    (285.69, 14.34),  (285.79, 13.92),  (285.96, 13.52),  (286.19, 13.15),
    (286.47, 12.82),  (286.81, 12.54),  (287.15, 12.27),  (287.53, 12.06),
    (287.94, 11.90),  (288.37, 11.81),  (288.81, 11.77),  (294.81, 11.77),
    (295.24, 11.81),  (295.67, 11.90),  (296.08, 12.06),  (296.46, 12.27),
    (296.82, 12.55),  (297.13, 12.88),  (297.39, 13.26),  (297.59, 13.66),
    (297.73, 14.10),  (297.80, 14.55),  (297.80, 15.00),
]

# Feature 8: TOP ELLIPTICAL CUT - 35 points at Z=20.3
profile_8_top_ellipse = [
    (265.8385, 45.675),   (266.4698, 45.736),   (266.942, 45.8434),  (267.3766, 45.999),
    (267.8113, 46.2244),  (268.2007, 46.4996),  (268.6577, 46.8867),  (269.0681, 47.381),
    (269.3747, 47.9021),  (269.7435, 48.8668),  (269.7941, 49.6385),  (269.7435, 50.2868),
    (269.5541, 51.0286),  (269.2858, 51.5968),  (268.907, 52.1493),   (268.465, 52.686),
    (267.881, 53.0806),   (267.2496, 53.3805),  (266.5236, 53.6057),  (265.735, 53.6057),
    (259.8825, 53.6057),  (258.9535, 53.6057),  (258.1656, 53.2723),  (257.408, 52.9087),
    (256.8928, 52.3329),  (256.4079, 51.6965),  (256.014, 50.9995),   (255.8322, 50.0904),
    (255.8322, 49.1813),  (256.0443, 48.2116),  (256.4988, 47.52),    (257.014, 46.7873),
    (257.6807, 46.3024),  (258.3852, 45.963),   (259.4205, 45.7033),
]

with BuildPart() as z_slider_top:
    # Feature 1: Main extrude (53mm)
    with BuildSketch(Plane.YZ.offset(249.15)):
        with BuildLine():
            for i in range(len(profile_1_pts)):
                p1 = profile_1_pts[i]
                p2 = profile_1_pts[(i + 1) % len(profile_1_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=53)

    # Feature 2: Pocket on right face (31.535mm)
    with BuildSketch(Plane.YZ.offset(302.15)):
        with BuildLine():
            for i in range(len(profile_2_pts)):
                p1 = profile_2_pts[i]
                p2 = profile_2_pts[(i + 1) % len(profile_2_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=-31.535, mode=Mode.SUBTRACT)

    # Feature 3: Elliptical hole on BOTTOM (through)
    with BuildSketch(Plane.XY.offset(8.77)):
        with BuildLine():
            Spline(*profile_3_ellipse_pts, periodic=True)
        make_face()
    extrude(amount=-13.5, mode=Mode.SUBTRACT)

    # Feature 4: TOP FACE CUT (1.97mm)
    with BuildSketch(Plane.XY.offset(22.27)):
        with BuildLine():
            for i in range(len(profile_4_top_pts)):
                p1 = profile_4_top_pts[i]
                p2 = profile_4_top_pts[(i + 1) % len(profile_4_top_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=-1.97, mode=Mode.SUBTRACT)

    # Feature 5: BOTTOM FACE MATERIAL (1.97mm add)
    with BuildSketch(Plane.XY.offset(8.77)):
        with BuildLine():
            for i in range(len(profile_5_bottom_pts)):
                p1 = profile_5_bottom_pts[i]
                p2 = profile_5_bottom_pts[(i + 1) % len(profile_5_bottom_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=-1.97)

    # Feature 6: DIAMOND CUT (12mm)
    with BuildSketch(Plane.XY.offset(18.8)):
        with BuildLine():
            for i in range(len(diamond_pts)):
                p1 = diamond_pts[i]
                p2 = diamond_pts[(i + 1) % len(diamond_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=-12, mode=Mode.SUBTRACT)

    # Feature 7: FRONT FACE SLOT CUT (through)
    with BuildSketch(Plane.XZ.offset(34.52)):
        with BuildLine():
            Spline(*profile_7_pts, periodic=True)
        make_face()
    extrude(amount=-100, mode=Mode.SUBTRACT)

    # Feature 8: TOP ELLIPTICAL CUT (through) [NEW]
    with BuildSketch(Plane.XY.offset(20.3)):
        with BuildLine():
            Spline(*profile_8_top_ellipse, periodic=True)
        make_face()
    extrude(amount=-20, mode=Mode.SUBTRACT)

show_object(z_slider_top.part)

# =========================
# EXPORT
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_Slider_Top.stl"
export_stl(z_slider_top.part, str(stl_file))
print("✅ Z SLIDER TOP - ALL 8 FEATURES FINAL")
print(f"📁 {stl_file}")
print(f"1. ✓ Main extrude: 53mm")
print(f"2. ✓ Right pocket: 31.535mm")
print(f"3. ✓ Elliptical hole: Through (13.5mm)")
print(f"4. ✓ Top face cut: 1.97mm")
print(f"5. ✓ Bottom face material: 1.97mm")
print(f"6. ✓ Diamond cut: 12mm")
print(f"7. ✓ Front slot cut: Through")
print(f"8. ✓ Top elliptical cut: Through ✅ [NEW]")