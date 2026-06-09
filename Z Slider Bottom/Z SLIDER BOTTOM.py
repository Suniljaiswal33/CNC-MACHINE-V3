from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# Z SLIDER BOTTOM - COMPLETE WITH FRONT FACE CUT
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

profile_3_pts = [
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

profile_4_pts = [
    (262.83, 60.50),   (273.65, 49.68),   (262.83, 38.87),   (252.01, 49.68),
]

# FRONT FACE through cut - 35 points (X, Z) at Y=34.52
profile_5_pts = [
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

with BuildPart() as z_slider:
    # Step 1: Main extrude with sharp corners
    with BuildSketch(Plane.YZ.offset(249.15)):
        with BuildLine():
            for i in range(len(profile_1_pts)):
                p1 = profile_1_pts[i]
                p2 = profile_1_pts[(i + 1) % len(profile_1_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=53)

    # Step 2: Pocket cut on right face
    with BuildSketch(Plane.YZ.offset(302.15)):
        with BuildLine():
            for i in range(len(profile_2_pts)):
                p1 = profile_2_pts[i]
                p2 = profile_2_pts[(i + 1) % len(profile_2_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=-31.535, mode=Mode.SUBTRACT)

    # Step 3: Through hole on bottom face
    with BuildSketch(Plane.XY.offset(8.77)):
        with BuildLine():
            Spline(*profile_3_pts, periodic=True)
        make_face()
    extrude(amount=50, mode=Mode.SUBTRACT, both=True)

    # Step 4: Pocket on top face - 12mm deep
    with BuildSketch(Plane.XY.offset(22.27)):
        with BuildLine():
            for i in range(len(profile_4_pts)):
                p1 = profile_4_pts[i]
                p2 = profile_4_pts[(i + 1) % len(profile_4_pts)]
                Line(p1, p2)
        make_face()
    extrude(amount=-12, mode=Mode.SUBTRACT)

    # Step 5: Through cut on front face (Y=34.52) - 35 points
    with BuildSketch(Plane.XZ.offset(34.52)):
        with BuildLine():
            Spline(*profile_5_pts, periodic=True)
        make_face()
    extrude(amount=-100, mode=Mode.SUBTRACT)  # Through cut in negative Y

show_object(z_slider.part)

# =========================
# EXPORT
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_Slider_Bottom.stl"
export_stl(z_slider.part, str(stl_file))
print("✅ Z SLIDER BOTTOM - FINAL COMPLETE")
print(f"📁 {stl_file}")
print(f"✓ Main extrude: 53mm")
print(f"✓ Right pocket: 31.535mm")
print(f"✓ Bottom hole: Through elliptical")
print(f"✓ Top pocket: 12mm diamond")
print(f"✓ Front face: Through cut (35 pts)")