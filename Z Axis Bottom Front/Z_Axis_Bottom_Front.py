from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import numpy as np

# ============================================================================
# Z AXIS BOTTOM FRONT
# ----------------------------------------------------------------------------
# This part is the MIRROR of "Z_Axis_Top_Front" about the XY plane (Z=0),
# with one important difference: the counterbore hole is placed on the
# OPPOSITE face (compared to where it would land after a plain mirror).
#
# Strategy:
#   1. Build source = Top Front WITHOUT the counterbore (Feature 6 skipped)
#   2. Mirror source about XY plane
#   3. Add counterbore on the opposite face of the mirrored part
# ============================================================================

# ============================================================================
# SOURCE: Z Axis Top Front (Features 1-10 except Feature 6 counterbore)
# ============================================================================

# Feature 1 — Base profile extrude plane
feature1_plane = Plane(
    origin=(339.15, 32.17, 237.335),
    x_dir=(1, 0, 0),
    z_dir=(0, 1, 0),
)
feature1_pts = [
    (-90.00,  14.435),
    (-29.04,  14.435),
    (-29.04,   7.565),
    ( 90.00,   7.565),
    ( 90.00, -12.435),
    ( 88.00, -14.435),
    (-88.00, -14.435),
    (-90.00, -12.435),
]

with BuildPart() as source_top_front_no_cb:
    # ------------------------------------------------------------------------
    # FEATURE 1: Base profile extrude (40mm)
    # ------------------------------------------------------------------------
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature1_pts, close=True)
        make_face()
    extrude(amount=40, mode=Mode.ADD)

    # ------------------------------------------------------------------------
    # FEATURE 2: 2x 8mm DIA through holes on front face
    # ------------------------------------------------------------------------
    hole2_centers_world = [(274.18, 240.72), (404.27, 240.84)]
    hole2_centers_sketch = [(x - 339.15, 237.335 - z) for (x, z) in hole2_centers_world]
    with BuildSketch(feature1_plane):
        with Locations(*hole2_centers_sketch):
            Circle(radius=4.0)
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 3: Slot through cut on front face
    # ------------------------------------------------------------------------
    slot_pts_world = [
        (294.77, 233.90), (295.50, 233.81), (296.18, 233.55), (296.78, 233.13),
        (297.26, 232.58), (297.59, 231.93), (297.76, 231.21), (297.74, 230.48),
        (297.55, 229.77), (297.21, 229.15), (296.73, 228.63), (296.14, 228.23),
        (295.47, 227.99), (294.77, 227.90), (288.94, 227.90), (288.18, 228.00),
        (287.47, 228.29), (286.86, 228.75), (286.41, 229.30), (286.11, 229.94),
        (285.96, 230.64), (285.98, 231.35), (286.17, 232.03), (286.52, 232.66),
        (287.00, 233.18), (287.59, 233.58), (288.25, 233.82), (288.96, 233.90),
    ]
    slot_pts_sketch = [(x - 339.15, 237.335 - z) for (x, z) in slot_pts_world]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*slot_pts_sketch, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 4: Hexagon pocket (5.2mm deep) on BACK face Y=72.18
    # ------------------------------------------------------------------------
    feature4_plane = Plane(
        origin=(291.93, 72.18, 230.86),
        x_dir=(1, 0, 0),
        z_dir=(0, -1, 0),
    )
    feature4_pts_world = [
        (283.10, 230.90), (286.10, 225.71), (297.77, 225.71),
        (300.76, 230.90), (297.81, 236.01), (286.05, 236.01),
    ]
    feature4_pts_sketch = [(x - 291.93, z - 230.86) for (x, z) in feature4_pts_world]
    with BuildSketch(feature4_plane):
        with BuildLine():
            Polyline(*feature4_pts_sketch, close=True)
        make_face()
    extrude(amount=5.2, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 5: Slot through cut on TOP face Z=251.77
    # ------------------------------------------------------------------------
    feature5_plane = Plane(
        origin=(262.79, 49.68, 251.77),
        x_dir=(1, 0, 0),
        z_dir=(0, 0, -1),
    )
    feature5_pts_world = [
        (259.79, 53.68), (258.84, 53.56), (257.94, 53.22), (257.14, 52.67),
        (256.50, 51.95), (256.05, 51.10), (255.82, 50.16), (255.82, 49.19),
        (256.05, 48.26), (256.50, 47.40), (257.14, 46.68), (257.94, 46.14),
        (258.84, 45.79), (259.79, 45.68), (265.79, 45.68), (266.75, 45.79),
        (267.65, 46.14), (268.45, 46.68), (269.09, 47.40), (269.53, 48.26),
        (269.77, 49.19), (269.77, 50.16), (269.53, 51.10), (269.09, 51.95),
        (268.45, 52.67), (267.65, 53.22), (266.75, 53.56), (265.79, 53.68),
    ]
    feature5_pts_sketch = [(x - 262.79, 49.68 - y) for (x, y) in feature5_pts_world]
    with BuildSketch(feature5_plane):
        with BuildLine():
            Polyline(*feature5_pts_sketch, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 6 SKIPPED — counterbore will be added AFTER mirror on opposite face
    # ------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # FEATURE 7: 8mm DIA through hole on TOP face at (415.47, 49.68)
    # ------------------------------------------------------------------------
    feature7_plane = Plane(
        origin=(415.47, 49.68, 251.77),
        x_dir=(1, 0, 0),
        z_dir=(0, 0, -1),
    )
    with BuildSketch(feature7_plane):
        Circle(radius=4.0)
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 8: T-slot extrude cut (56mm) on LEFT face X=249.15
    # ------------------------------------------------------------------------
    feature8_plane = Plane(
        origin=(249.15, 50.01, 229.90),
        x_dir=(0, 1, 0),
        z_dir=(1, 0, 0),
    )
    feature8_pts_world = [
        (64.17, 236.90), (64.17, 233.90), (66.01, 233.90), (66.01, 227.90),
        (64.17, 227.90), (64.17, 222.90), (35.85, 222.90), (35.85, 227.90),
        (34.01, 227.90), (34.01, 233.90), (35.85, 233.90), (35.85, 236.90),
    ]
    feature8_pts_sketch = [(y - 50.01, z - 229.90) for (y, z) in feature8_pts_world]
    with BuildSketch(feature8_plane):
        with BuildLine():
            Polyline(*feature8_pts_sketch, close=True)
        make_face()
    extrude(amount=56, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 9: Asymmetric T-slot extension cut (31.535mm) at X=273.61
    # ------------------------------------------------------------------------
    feature9_plane = Plane(
        origin=(273.61, 62.59, 229.855),
        x_dir=(0, 1, 0),
        z_dir=(1, 0, 0),
    )
    feature9_pts_world = [
        (59.17, 236.81), (59.17, 233.90), (61.01, 233.90), (61.01, 227.90),
        (59.17, 227.90), (59.17, 222.90), (64.17, 222.90), (64.17, 227.90),
        (66.01, 227.90), (66.01, 233.90), (64.17, 233.90), (64.17, 236.81),
    ]
    feature9_pts_sketch = [(y - 62.59, z - 229.855) for (y, z) in feature9_pts_world]
    with BuildSketch(feature9_plane):
        with BuildLine():
            Polyline(*feature9_pts_sketch, close=True)
        make_face()
    extrude(amount=31.535, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 10: Diamond annulus protrusion (5mm) below bottom face
    # ------------------------------------------------------------------------
    feature10_plane = Plane(
        origin=(415.50, 49.68, 224.77),
        x_dir=(1, 0, 0),
        z_dir=(0, 0, 1),
    )
    outer_diamond_world = [
        (401.85, 49.68), (415.50, 36.03), (429.15, 49.68), (415.50, 63.32),
    ]
    outer_diamond_sketch = [(x - 415.50, y - 49.68) for (x, y) in outer_diamond_world]
    inner_diamond_world = [
        (415.50, 38.86), (426.32, 49.68), (415.50, 60.50), (404.68, 49.68),
    ]
    inner_diamond_sketch = [(x - 415.50, y - 49.68) for (x, y) in inner_diamond_world]
    with BuildSketch(feature10_plane):
        with BuildLine():
            Polyline(*outer_diamond_sketch, close=True)
        make_face()
        with BuildLine():
            Polyline(*inner_diamond_sketch, close=True)
        make_face(mode=Mode.SUBTRACT)
    extrude(amount=5, mode=Mode.ADD)

# ============================================================================
# MIRROR: Reflect source (no counterbore) about XY plane (Z = 0)
# ============================================================================
mirrored = mirror(source_top_front_no_cb.part, about=Plane.XY)

# ============================================================================
# BUILD FINAL PART: Mirrored part + Counterbore on OPPOSITE face
# ----------------------------------------------------------------------------
# In the mirrored coordinate system:
#   - Original TOP face (Z=251.77) is now at Z=-251.77 (became BOTTOM)
#   - Original BOTTOM face at X≈339 (Z=229.77) is now at Z=-229.77 (became TOP)
#
# Counterbore goes on the OPPOSITE face from where it would have landed
# after a plain mirror — i.e., on the new TOP face (Z = -229.77).
# Direction: into the part (-Z direction in mirrored coords).
# ============================================================================
with BuildPart() as z_axis_bottom_front:
    add(mirrored)

    # ------------------------------------------------------------------------
    # FEATURE 6 (relocated): Counterbore on OPPOSITE face
    # 22 mm DIA pocket (7 mm deep) + 18 mm DIA concentric through hole
    # Center: (339.20, 49.79) on new top face at Z = -229.77
    # ------------------------------------------------------------------------
    cb_plane = Plane(
        origin=(339.20, 49.79, -229.77),
        x_dir=(1, 0, 0),
        z_dir=(0, 0, -1),   # normal -Z = into the mirrored part
    )
    # Step A: 22mm DIA pocket, 7mm deep
    with BuildSketch(cb_plane):
        Circle(radius=11.0)
    extrude(amount=7, mode=Mode.SUBTRACT)
    # Step B: 18mm DIA through hole, concentric
    with BuildSketch(cb_plane):
        Circle(radius=9.0)
    extrude(amount=100, mode=Mode.SUBTRACT)

show_object(z_axis_bottom_front.part)

# ============================================================================
# EXPORT STL
# ============================================================================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_Axis_Bottom_Front.stl"
export_stl(z_axis_bottom_front.part, str(stl_file))

print("=" * 70)
print("Z AXIS BOTTOM FRONT")
print("=" * 70)
print(f"📁 File : {stl_file}")
print(f"✓ Source: Top Front built with Features 1-10 (Feature 6 skipped)")
print(f"✓ Mirrored about XY plane (Z=0)")
print(f"✓ Counterbore added on OPPOSITE face: Z=-229.77 (was original bottom)")
print(f"   - 22mm DIA pocket, 7mm deep")
print(f"   - 18mm DIA concentric through hole ✅")
print("=" * 70)