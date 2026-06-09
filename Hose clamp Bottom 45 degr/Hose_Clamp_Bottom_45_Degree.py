from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import numpy as np

# =========================
# HOSE CLAMP BOTTOM 45 DEGREE
# =========================

profile_points_1 = [
    (315.8972, 112.8254),
    (315.8972, 179.8254),
    (295.6472, 179.8254),
    (295.6472, 130.3834),
    (293.8972, 128.6793),
    (293.8972, 112.8254),
]

profile_points_2 = [
    (293.8972, 112.8254),
    (295.8972, 112.8254),
    (295.8972, 127.8254),
    (297.6472, 129.5446),
    (297.6472, 179.8254),
    (295.6472, 179.8254),
    (295.6472, 130.3834),
    (293.8972, 128.6793),
]

new_points = [
    (262.3305, -1.886), (269.4645, 5.2481), (270.7306, 4.2129), (271.9785, 3.2866),
    (273.4562, 2.5784), (274.9022, 1.8855), (276.5444, 1.2485), (277.9236, 0.8167),
    (279.4837, 0.4464), (281.5882, 0.1031), (283.1958, -0.0174), (284.2662, 0.0123),
    (285.8675, 0.0957), (293.8835, -7.8955), (295.6535, -7.8955), (295.6472, 2.0092),
    (300.9283, 2.0092), (300.9283, 7.8057), (302.9136, 10.483), (304.4815, 13.4242),
    (305.0979, 14.9738), (305.779, 16.9217), (305.9785, 18.1885), (306.2378, 19.8358),
    (306.4363, 22.0667), (306.4363, 24.3085), (306.0439, 26.4808), (305.6889, 28.1102),
    (305.0042, 30.0491), (304.5817, 31.2741), (303.9168, 32.779), (303.1011, 34.2336),
    (302.2372, 35.405), (301.6027, 36.1989), (301.1584, 36.9419), (308.2924, 44.076),
    (306.8782, 45.4811), (298.3929, 37.0049), (299.5123, 35.7915), (300.5305, 34.4919),
    (301.4407, 33.1147), (302.2372, 31.6686), (302.9148, 30.1631), (303.5089, 28.5336),
    (303.9168, 26.8058), (304.2752, 24.8764), (304.3931, 22.0964), (304.2934, 20.4485),
    (304.0394, 18.7854), (303.6987, 17.2034), (303.2076, 15.6273), (302.5175, 14.0476),
    (301.8535, 12.6188), (300.9995, 11.206), (299.5359, 9.2978), (298.3482, 8.0334),
    (297.7975, 7.4416), (296.54, 6.372), (294.5933, 5.0448), (292.6009, 4.0103),
    (290.7235, 3.244), (288.846, 2.6693), (287.4284, 2.345), (285.9579, 2.1131),
    (284.347, 2.0057), (282.8726, 2.0057), (281.6805, 2.1413), (280.5066, 2.304),
    (279.3931, 2.5102), (277.7984, 2.9375), (276.5254, 3.3974), (275.5833, 3.8062),
    (274.7379, 4.1692), (273.2918, 4.9657), (272.0876, 5.7625), (270.883, 6.6716),
    (270.0649, 7.3534), (269.4016, 8.0135), (260.9163, -0.4717),
]

def make_angled_hole_plane(pa, pb):
    direction = (pb - pa).normalized()
    hd = np.array([direction.X, direction.Y, direction.Z])
    arb = np.array([0, 1, 0]) if abs(hd[1]) < 0.9 else np.array([1, 0, 0])
    xd = np.cross(hd, arb)
    xd = xd / np.linalg.norm(xd)
    plane = Plane(
        origin=(pa.X, pa.Y, pa.Z),
        x_dir=(xd[0], xd[1], xd[2]),
        z_dir=(direction.X, direction.Y, direction.Z)
    )
    depth = (pb - pa).length
    return plane, depth

def make_svd_plane_and_locs(points_list):
    pts = np.array([[p[0], p[1], p[2]] for p in points_list])
    centroid = pts.mean(axis=0)
    centered = pts - centroid
    _, _, Vt = np.linalg.svd(centered)
    normal = Vt[-1] / np.linalg.norm(Vt[-1])
    x_dir = Vt[0] / np.linalg.norm(Vt[0])
    plane = Plane(
        origin=(centroid[0], centroid[1], centroid[2]),
        x_dir=(x_dir[0], x_dir[1], x_dir[2]),
        z_dir=(normal[0], normal[1], normal[2]),
    )
    def project(pt):
        y_dir = np.cross(normal, x_dir)
        v = pt - centroid
        return (np.dot(v, x_dir), np.dot(v, y_dir))
    locs = [project(np.array([p[0], p[1], p[2]])) for p in points_list]
    return plane, locs

# Angled holes
pa1 = Vector(266.9891, 155.2927, 1.7726)
pb1 = Vector(264.5294, 155.2791, 4.1414)
plane1, depth1 = make_angled_hole_plane(pa1, pb1)

pa2 = Vector(303.4258, 155.1699, 43.0324)
pb2 = Vector(305.8363, 155.1699, 40.6204)
plane2, depth2 = make_angled_hole_plane(pa2, pb2)

# SVD cuts
svd_pts_1 = [
    (308.1927, 160.1064, 46.7941), (305.49, 160.1064, 44.0944),
    (306.9001, 158.1133, 45.503),  (306.9001, 152.0676, 45.503),
    (305.49,   150.0746, 44.0944), (308.1927, 150.0746, 46.7941),
]
svd_plane_1, locs_1 = make_svd_plane_and_locs(svd_pts_1)

svd_pts_2 = [
    (259.4583, 160.1138, -1.8879), (262.2953, 160.1138, 0.946),
    (260.9258, 158.0742, -0.4221), (260.9258, 152.0592, -0.4221),
    (262.2953, 150.0888,  0.946),  (259.4583, 150.0888, -1.8879),
]
svd_plane_2, locs_2 = make_svd_plane_and_locs(svd_pts_2)

# NEW FEATURE - 4 vertices
new_vertices = [
    (297.34, 169.75, 9.92),
    (302.62, 169.75, 9.92),
    (302.62, 176.82, 2.85),
    (297.34, 176.82, 2.85),
]

# Create SVD plane for new vertices (normal direction extrude)
new_feature_plane, new_feature_locs = make_svd_plane_and_locs(new_vertices)

# =========================
# Step 1 - Build U-clamp + all cuts in original orientation
# =========================
with BuildPart() as u_clamp_builder:
    with BuildSketch(Plane.XZ.offset(-150.1044)):
        with BuildLine():
            Polyline(*new_points, close=True)
        make_face()
    extrude(amount=-10)

    with BuildSketch(plane1):
        Circle(radius=2.5)
    extrude(amount=depth1, mode=Mode.SUBTRACT)

    with BuildSketch(plane2):
        Circle(radius=2.5)
    extrude(amount=depth2, mode=Mode.SUBTRACT)

    with BuildSketch(svd_plane_1):
        with BuildLine():
            Polyline(*locs_1, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    with BuildSketch(svd_plane_2):
        with BuildLine():
            Polyline(*locs_2, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

# =========================
# Step 2 - Tilt 45° about X axis
# =========================
tilt_pivot = Axis((0, 150.1044, 0), (1, 0, 0))
u_clamp_tilted = u_clamp_builder.part.rotate(tilt_pivot, -45)

# =========================
# Step 2b - Translate to align with original position
# =========================
TRANSLATE_X = 1.696
TRANSLATE_Y = 18.227
TRANSLATE_Z = 8.5

u_clamp_aligned = u_clamp_tilted.translate((TRANSLATE_X, TRANSLATE_Y, TRANSLATE_Z))

# =========================
# Step 3 - Main assembly
# =========================
with BuildPart() as hose_clamp_bottom:
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points_1, close=True)
        make_face()
    extrude(amount=2)

    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points_2, close=True)
        make_face()
    extrude(amount=-18.25)

    # Add the rotated + translated U-clamp
    add(u_clamp_aligned)

    # 8mm dia thru hole on base plate
    with BuildSketch(Plane.XY.offset(2.0092)):
        with Locations((305.6698, 121.8217)):
            Circle(radius=4)
    extrude(amount=-30, mode=Mode.SUBTRACT)

    # NEW FEATURE - Rectangular extrude in normal direction
    with BuildSketch(new_feature_plane):
        with BuildLine():
            Polyline(*new_feature_locs, close=True)
        make_face()
    extrude(amount=9.8, mode=Mode.ADD)

    # =========================================================================
    # ADDED FEATURE: Triangular Extrude-Cut on face at X = 302.620
    # ---------------------------------------------------------------------------
    # Face properties from screenshot:
    #   - At X = 302.620 (face perpendicular to X-axis, bb size X = 0)
    #   - Area = 16.644 mm²  → exactly half of bb rect (8.159 × 4.080)
    #     → confirms face is a TRIANGLE (not full rectangle)
    #   - bb Y: 165.811 → 173.970 (width 8.159)
    #   - bb Z: -4.080 → 0.000   (height 4.080)
    #
    # Derived triangle vertices (isoceles, apex points down in -Z):
    #   - Base L : (302.620, 165.811,  0.000)
    #   - Base R : (302.620, 173.970,  0.000)
    #   - Apex   : (302.620, 169.890, -4.080)
    #
    # Cut depth: 4.973 mm into the part (along -X direction).
    # =========================================================================
    cut_face_plane = Plane(
        origin=(302.620, 169.890, -2.040),   # bb center of the triangular face
        x_dir=(0, 1, 0),                      # sketch X = world Y
        z_dir=(-1, 0, 0),                     # sketch normal = world -X (into part)
    )
    # Right-handed: sketch Y direction = z_dir × x_dir = (0, 0, -1) = world -Z
    # So in sketch coords:
    #   World Z = 0      → sketch Y = -2.040   (bottom)
    #   World Z = -4.080 → sketch Y = +2.040   (top)
    #   World Y = 165.811 → sketch X = -4.0795 (left)
    #   World Y = 173.970 → sketch X = +4.0795 (right)
    #   World Y = 169.890 → sketch X =  0      (center)
    with BuildSketch(cut_face_plane):
        with BuildLine():
            Polyline(
                (-4.0795, -2.040),   # base-left  → world (302.620, 165.811,  0.000)
                ( 4.0795, -2.040),   # base-right → world (302.620, 173.970,  0.000)
                ( 0.0000,  2.040),   # apex       → world (302.620, 169.890, -4.080)
                close=True,
            )
        make_face()
    extrude(amount=4.973, mode=Mode.SUBTRACT)

    # =========================================================================
    # ADDED FEATURE: "Extrude Up To Next Face" on tilted face
    # ---------------------------------------------------------------------------
    # Face properties from screenshot:
    #   - bb min : (297.340, 162.820, 2.000)
    #   - bb max : (302.620, 163.811, 2.990)
    #   - bb size: (5.280, 0.990, 0.990)
    #   - area   : 7.382 mm²
    #   - angle to XY : 135°  → normal ≈ (0, -1/√2, -1/√2)
    #
    # This is the exposed portion of the new feature's CAP parallelogram
    # which sticks out above the base plate (Z=2).
    #
    # NOTE: build123d has no native "up to next face" operator. We find the
    # face via bounding-box match and extrude it by EXTRUDE_AMOUNT in its
    # natural normal direction. Tune EXTRUDE_AMOUNT until it lands on the
    # desired next face.
    # =========================================================================
    EXTRUDE_AMOUNT = 5.0   # mm — adjust as needed; use negative to flip direction

    target_face = None
    for face in hose_clamp_bottom.faces():
        fbb = face.bounding_box()
        if (abs(fbb.min.X - 297.340) < 0.1 and abs(fbb.max.X - 302.620) < 0.1 and
            abs(fbb.min.Y - 162.820) < 0.1 and abs(fbb.max.Y - 163.811) < 0.1 and
            abs(fbb.min.Z -   2.000) < 0.1 and abs(fbb.max.Z -   2.990) < 0.1):
            target_face = face
            break

    if target_face is not None:
        face_normal = target_face.normal_at(target_face.center())
        print(f"[Feature 13] ✓ Target face found")
        print(f"[Feature 13]   Face center : {target_face.center()}")
        print(f"[Feature 13]   Face normal : {face_normal}")
        print(f"[Feature 13]   Extruding {EXTRUDE_AMOUNT}mm in normal direction")
        extrude(target_face, amount=EXTRUDE_AMOUNT, mode=Mode.ADD)
    else:
        print("[Feature 13] ✗ Target face NOT found — check bb tolerances")

    # =========================================================================
    # ADDED FEATURE 14: "Extrude Up To Next Face" on corresponding -X side face
    # ---------------------------------------------------------------------------
    # Face properties from screenshot:
    #   - bb min : (295.580, 162.748, -4.154)
    #   - bb max : (297.349, 169.820,  2.917)
    #   - bb size: (1.770, 7.071, 7.071)
    #   - area   : 2.885 mm²
    #   - angle to XY : 135°  (same tilt as Feature 13's face)
    #
    # This is the corresponding face on the -X side of the new feature,
    # created/exposed after Feature 13's extrusion.
    # =========================================================================
    EXTRUDE_AMOUNT_14 = 5.0   # mm — adjust as needed; use negative to flip

    target_face_14 = None
    for face in hose_clamp_bottom.faces():
        fbb = face.bounding_box()
        if (abs(fbb.min.X - 295.580) < 0.1 and abs(fbb.max.X - 297.349) < 0.1 and
            abs(fbb.min.Y - 162.748) < 0.1 and abs(fbb.max.Y - 169.820) < 0.1 and
            abs(fbb.min.Z - (-4.154)) < 0.1 and abs(fbb.max.Z -   2.917) < 0.1):
            target_face_14 = face
            break

    if target_face_14 is not None:
        face_normal_14 = target_face_14.normal_at(target_face_14.center())
        print(f"[Feature 14] ✓ Target face found")
        print(f"[Feature 14]   Face center : {target_face_14.center()}")
        print(f"[Feature 14]   Face normal : {face_normal_14}")
        print(f"[Feature 14]   Extruding {EXTRUDE_AMOUNT_14}mm in normal direction")
        extrude(target_face_14, amount=EXTRUDE_AMOUNT_14, mode=Mode.ADD)
    else:
        print("[Feature 14] ✗ Target face NOT found — check bb tolerances")

    # =========================================================================
    # ADDED FEATURE 15: Rectangular extrude-cut on RIGHT face at X = 315.8972
    # ---------------------------------------------------------------------------
    # 4 input points (closed boundary, all at X = 315.8972):
    #   (315.8972, 144.9455,   0.0000)
    #   (315.8972, 179.2349,   0.0000)
    #   (315.8972, 179.2349, -12.9093)
    #   (315.8972, 144.9455, -12.9093)
    #
    # Rectangle dimensions:
    #   Y-width  : 179.2349 - 144.9455 = 34.2894 mm
    #   Z-height : 0.0000 - (-12.9093) = 12.9093 mm
    #
    # Cut depth: 18.25 mm in -X direction (into the part).
    # =========================================================================
    right_face_plane = Plane(
        origin=(315.8972, 162.0902, -6.45465),  # bb center of the 4 input points
        x_dir=(0, 1, 0),     # sketch X = world Y
        z_dir=(-1, 0, 0),    # sketch normal = world -X (into part)
    )
    # Right-handed: sketch Y direction = z_dir × x_dir = (0, 0, -1) = world -Z
    # Sketch coords for each input point (relative to plane origin):
    #   (315.8972, 144.9455,   0.0000) → (-17.1447, -6.45465)
    #   (315.8972, 179.2349,   0.0000) → ( 17.1447, -6.45465)
    #   (315.8972, 179.2349, -12.9093) → ( 17.1447,  6.45465)
    #   (315.8972, 144.9455, -12.9093) → (-17.1447,  6.45465)
    with BuildSketch(right_face_plane):
        with BuildLine():
            Polyline(
                (-17.1447, -6.45465),
                ( 17.1447, -6.45465),
                ( 17.1447,  6.45465),
                (-17.1447,  6.45465),
                close=True,
            )
        make_face()
    extrude(amount=18.25, mode=Mode.SUBTRACT)

show_object(hose_clamp_bottom.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Hose_Clamp_Bottom_45_Degree.stl"
export_stl(hose_clamp_bottom.part, str(stl_file))
print("✅ HOSE CLAMP BOTTOM 45 DEGREE - UPDATED")
print(f"📁 File : {stl_file}")
print(f"✓ Rectangular feature: 9.8mm normal extrude added")
print(f"✓ Triangular cut on face X=302.620: 4.973mm deep")
print(f"✓ Feature 13 — Face extrude (+X side): 5.0mm in normal direction")
print(f"✓ Feature 14 — Face extrude (-X side): 5.0mm in normal direction")
print(f"✓ Feature 15 — Rect cut on RIGHT face X=315.8972: 18.25mm deep ✅")