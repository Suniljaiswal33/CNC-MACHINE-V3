from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import numpy as np

# ============================================================================
# X AXIS SIDEPANEL MOUNT OUTSIDE
# ----------------------------------------------------------------------------
# This part is the MIRROR of "X_Axis_Sidepanel_Mount_Inside" about the
# XY plane (Z=0 plane). The construction below first builds the inside
# part as a source object, then mirrors it. The source object is NOT
# shown/exported — only the mirrored "Outside" part is.
# ============================================================================

# ============================================================================
# FEATURE 1: Base profile extrude (10mm)
# ============================================================================
feature1_plane = Plane(
    origin=(65.0, 96.27, 122.77),
    x_dir=(0, 1, 0),
    z_dir=(1, 0, 0),
)
feature1_pts = [
    ( 30.00,   96.59),
    ( 23.00,  103.59),
    (-23.00,  103.59),
    (-30.00,   96.59),
    (-30.00,  -96.59),
    (-23.00, -103.59),
    ( 23.00, -103.59),
    ( 30.00,  -96.59),
]

with BuildPart() as source_inside:
    # ------------------------------------------------------------------------
    # FEATURE 1: Base profile extrude (10 mm)
    # ------------------------------------------------------------------------
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature1_pts, close=True)
        make_face()
    extrude(amount=10, mode=Mode.ADD)

    # ------------------------------------------------------------------------
    # FEATURE 2: Diamond through cut at top (Y=96.27, Z=196.36)
    # ------------------------------------------------------------------------
    feature2_pts = [
        ( 14.32,  73.59),
        (  0.00,  87.91),
        (-14.32,  73.59),
        (  0.00,  59.27),
    ]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature2_pts, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 3: Diamond through cut at bottom (Y=96.27, Z=49.18)
    # ------------------------------------------------------------------------
    feature3_pts = [
        (  0.00, -87.91),
        ( 14.32, -73.59),
        (  0.00, -59.27),
        (-14.32, -73.59),
    ]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature3_pts, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 4: 8x 6mm DIA through holes
    # ------------------------------------------------------------------------
    hole_centers_world = [
        (116.31,  29.14),
        ( 76.22,  29.13),
        ( 76.12,  69.22),
        (116.22,  69.27),
        ( 76.20, 176.47),
        (116.32, 176.37),
        ( 76.24, 216.47),
        (116.27, 216.42),
    ]
    Y_ORIGIN = 96.27
    Z_ORIGIN = 122.77
    hole_centers_sketch = [
        (y - Y_ORIGIN, z - Z_ORIGIN) for (y, z) in hole_centers_world
    ]
    with BuildSketch(feature1_plane):
        with Locations(*hole_centers_sketch):
            Circle(radius=3.0)
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 5: Slot through cut on LEFT face (Y=66.27)
    # ------------------------------------------------------------------------
    feature5_plane = Plane(
        origin=(70.0, 66.27, 122.77),
        x_dir=(1, 0, 0),
        z_dir=(0, 1, 0),
    )
    feature5_pts = [
        (5.00,  43.59),
        (0.00,  38.59),
        (0.00, -38.59),
        (5.00, -43.59),
    ]
    with BuildSketch(feature5_plane):
        with BuildLine():
            Polyline(*feature5_pts, close=True)
        make_face()
    extrude(amount=200, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 6: Structural rib on TOP face (28-pt boundary): 10mm extrude
    # ------------------------------------------------------------------------
    feature6_plane = Plane(
        origin=(75.0, 96.27, 122.77),
        x_dir=(0, 1, 0),
        z_dir=(1, 0, 0),
    )
    feature6_pts = [
        (-30.00,  76.09),
        (-18.89,  76.09),
        ( -2.50,  92.48),
        ( -2.50, 103.59),
        (  2.50, 103.59),
        (  2.50,  92.48),
        ( 18.89,  76.09),
        ( 30.00,  76.09),
        ( 30.00,  71.09),
        ( 18.89,  71.09),
        (  2.50,  54.70),
        (  2.50, -54.70),
        ( 18.89, -71.09),
        ( 30.00, -71.09),
        ( 30.00, -76.09),
        ( 18.89, -76.09),
        (  2.50, -92.48),
        (  2.50, -103.59),
        ( -2.50, -103.59),
        ( -2.50, -92.48),
        (-18.89, -76.09),
        (-30.00, -76.09),
        (-30.00, -71.09),
        (-18.89, -71.09),
        ( -2.50, -54.70),
        ( -2.50,  54.70),
        (-18.89,  71.09),
        (-30.00,  71.09),
    ]
    with BuildSketch(feature6_plane):
        with BuildLine():
            Polyline(*feature6_pts, close=True)
        make_face()
    extrude(amount=10, mode=Mode.ADD)

    # ------------------------------------------------------------------------
    # FEATURE 7: Central column extension on back face: 18mm extrude
    # ------------------------------------------------------------------------
    feature7_plane = Plane(
        origin=(85.0, 96.27, 122.77),
        x_dir=(0, 1, 0),
        z_dir=(1, 0, 0),
    )
    feature7_pts = [
        (-2.50,  54.70),
        (-2.50, -54.70),
        ( 2.50, -54.70),
        ( 2.50,  54.70),
    ]
    with BuildSketch(feature7_plane):
        with BuildLine():
            Polyline(*feature7_pts, close=True)
        make_face()
    extrude(amount=-15, mode=Mode.ADD)

    # ------------------------------------------------------------------------
    # FEATURE 8: 8x Hex pockets (R5, 5mm deep) on BACK face X=75
    # ------------------------------------------------------------------------
    hex_centers_world = [
        (116.23, 216.37),
        ( 76.25, 216.37),
        ( 76.26, 176.31),
        (116.27, 176.31),
        ( 76.26,  69.08),
        ( 76.26,  29.06),
        (116.27,  29.06),
        (116.27,  69.08),
    ]
    hex_centers_sketch = [
        (y - 96.27, z - 122.77) for (y, z) in hex_centers_world
    ]
    hex_pocket_plane = feature1_plane.offset(10)   # plane at X = 75
    with BuildSketch(hex_pocket_plane):
        with Locations(*hex_centers_sketch):
            RegularPolygon(radius=5.0, side_count=6)
    extrude(amount=-5, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # Re-apply diamond cuts to ensure through-cut after Feature 6/7
    # ------------------------------------------------------------------------
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature2_pts, close=True)
        make_face()
    extrude(amount=200, both=True, mode=Mode.SUBTRACT)

    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature3_pts, close=True)
        make_face()
    extrude(amount=200, both=True, mode=Mode.SUBTRACT)

    # ------------------------------------------------------------------------
    # FEATURE 9: 6.5×6.5 chamfer on 6 selected edges
    # ------------------------------------------------------------------------
    target_edges = []
    for edge in source_inside.edges():
        v_start = edge @ 0
        v_end = edge @ 1
        if abs(v_start.X - 85.0) > 0.1 or abs(v_end.X - 85.0) > 0.1:
            continue
        is_top_horizontal = (abs(v_start.Z - 226.36) < 0.1 and
                             abs(v_end.Z   - 226.36) < 0.1)
        is_bot_horizontal = (abs(v_start.Z -  19.18) < 0.1 and
                             abs(v_end.Z   -  19.18) < 0.1)
        same_y = abs(v_start.Y - v_end.Y) < 0.1
        is_outer_y = ((abs(v_start.Y -  66.27) < 0.1) or
                      (abs(v_start.Y - 126.27) < 0.1))
        z_min = min(v_start.Z, v_end.Z)
        z_max = max(v_start.Z, v_end.Z)
        is_top_ear = (abs(z_min - 193.86) < 0.1 and abs(z_max - 198.86) < 0.1)
        is_bot_ear = (abs(z_min -  46.68) < 0.1 and abs(z_max -  51.68) < 0.1)
        is_corner_ear_vertical = same_y and is_outer_y and (is_top_ear or is_bot_ear)
        if is_top_horizontal or is_bot_horizontal or is_corner_ear_vertical:
            target_edges.append(edge)

    chamfer_sizes_to_try = [6.5, 5.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.0]
    applied_chamfer = None
    if target_edges:
        for sz in chamfer_sizes_to_try:
            try:
                chamfer(target_edges, length=sz, length2=sz)
                applied_chamfer = sz
                break
            except Exception:
                continue
    print(f"[Source build] Chamfer applied at {applied_chamfer}mm on "
          f"{len(target_edges)} edge(s)")

# ============================================================================
# MIRROR: Reflect the source (Inside) part about the XY plane (Z = 0)
# to create the OUTSIDE part. The source object is not shown or exported.
# ============================================================================
sidepanel_mount_outside = mirror(source_inside.part, about=Plane.XY)

# Show ONLY the mirrored Outside part (source is discarded)
show_object(sidepanel_mount_outside)

# ============================================================================
# EXPORT STL
# ============================================================================
desktop = Path.home() / "Desktop"
stl_file = desktop / "X_Axis_Sidepanel_Mount_Outside.stl"
export_stl(sidepanel_mount_outside, str(stl_file))

print("=" * 70)
print("X AXIS SIDEPANEL MOUNT OUTSIDE")
print("=" * 70)
print(f"📁 File : {stl_file}")
print(f"✓ Source: Inside mount built with 9 features")
print(f"✓ Mirrored about XY plane (Z=0) to create Outside variant")
print(f"✓ Source object discarded — only mirrored part exported ✅")
print("=" * 70)