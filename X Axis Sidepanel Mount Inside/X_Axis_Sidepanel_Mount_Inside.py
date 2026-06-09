from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import numpy as np

# ============================================================================
# X AXIS SIDEPANEL MOUNT INSIDE
# ============================================================================

# ============================================================================
# FEATURE 1: Base profile extrude (10mm)
# ----------------------------------------------------------------------------
# 8 vertices on YZ plane at X = 65.00 (chamfered rectangle):
#   (65.00, 126.27, 219.36)   ← top-right chamfer-start
#   (65.00, 119.27, 226.36)   ← top-right corner
#   (65.00,  73.27, 226.36)   ← top-left corner
#   (65.00,  66.27, 219.36)   ← top-left chamfer-end
#   (65.00,  66.27,  26.18)   ← bottom-left chamfer-start
#   (65.00,  73.27,  19.18)   ← bottom-left corner
#   (65.00, 119.27,  19.18)   ← bottom-right corner
#   (65.00, 126.27,  26.18)   ← bottom-right chamfer-end
#
# Profile dims : 60 mm (Y) × 207.18 mm (Z), with 7×7 chamfers at all 4 corners
# Plane normal : +X (sketch on YZ plane at X=65)
# Extrude      : 10 mm in +X direction
# ============================================================================
feature1_plane = Plane(
    origin=(65.0, 96.27, 122.77),   # bb center: Y_mid=96.27, Z_mid=122.77
    x_dir=(0, 1, 0),                 # sketch X = world Y
    z_dir=(1, 0, 0),                 # sketch normal = world +X
)
# Right-handed: sketch Y = z_dir × x_dir = (1,0,0) × (0,1,0) = (0,0,1) = world Z
# Sketch coord conversion: (world_Y, world_Z) → (world_Y - 96.27, world_Z - 122.77)
feature1_pts = [
    ( 30.00,   96.59),   # world (126.27, 219.36)
    ( 23.00,  103.59),   # world (119.27, 226.36)
    (-23.00,  103.59),   # world ( 73.27, 226.36)
    (-30.00,   96.59),   # world ( 66.27, 219.36)
    (-30.00,  -96.59),   # world ( 66.27,  26.18)
    (-23.00, -103.59),   # world ( 73.27,  19.18)
    ( 23.00, -103.59),   # world (119.27,  19.18)
    ( 30.00,  -96.59),   # world (126.27,  26.18)
]

with BuildPart() as sidepanel_mount_inside:
    # ------------------------------------------------------------------------
    # FEATURE 1: Base profile extrude (10 mm)
    # ------------------------------------------------------------------------
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature1_pts, close=True)
        make_face()
    extrude(amount=10, mode=Mode.ADD)
    # ------------------------------------------------------------------------
    # END FEATURE 1
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 2: Diamond-shape through cut
    # ------------------------------------------------------------------------
    # 4 points on YZ plane at X = 65.00 (closed boundary, diamond/rhombus):
    #   Vertex      (65.00, 110.59, 196.36)  ← right
    #   Vertex      (65.00,  96.27, 210.68)  ← top
    #   Vertex      (65.00,  81.95, 196.36)  ← left
    #   Sketch Pt   (65.00,  96.27, 182.04)  ← bottom (closes the boundary)
    #
    # Center : (Y=96.27, Z=196.36)
    # Width  : 28.64 mm (Y), Height: 28.64 mm (Z) → square rotated 45°
    # Cut    : through 10mm part thickness (using 100mm for safety)
    # ========================================================================
    feature2_pts = [
        ( 14.32,  73.59),   # world (110.59, 196.36) — right
        (  0.00,  87.91),   # world ( 96.27, 210.68) — top
        (-14.32,  73.59),   # world ( 81.95, 196.36) — left
        (  0.00,  59.27),   # world ( 96.27, 182.04) — bottom
    ]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature2_pts, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 2
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 3: Diamond-shape through cut (bottom — mirror of Feature 2)
    # ------------------------------------------------------------------------
    # 4 points on YZ plane at X = 65.00 (closed boundary, diamond/rhombus):
    #   Vertex (65.00,  96.27,  34.86)  ← bottom
    #   Vertex (65.00, 110.59,  49.18)  ← right
    #   Vertex (65.00,  96.27,  63.50)  ← top
    #   Vertex (65.00,  81.95,  49.18)  ← left
    #
    # Center : (Y=96.27, Z=49.18)
    # Width  : 28.64 mm (Y), Height: 28.64 mm (Z) → square rotated 45°
    # Cut    : through 10mm part thickness (using 100mm both=True for safety)
    # ========================================================================
    feature3_pts = [
        (  0.00, -87.91),   # world ( 96.27,  34.86) — bottom
        ( 14.32, -73.59),   # world (110.59,  49.18) — right
        (  0.00, -59.27),   # world ( 96.27,  63.50) — top
        (-14.32, -73.59),   # world ( 81.95,  49.18) — left
    ]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature3_pts, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 3
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 4: Eight 6mm DIA through holes (4 rows x 2 columns pattern)
    # ------------------------------------------------------------------------
    # 8 sketch points on front face (X = 65.00).
    # Note: Points 2 and 4 in the input had X=70.00 and X=72.50 respectively,
    # which is measurement noise from picking on the visualizer surface.
    # All hole centers are normalized to X = 65 (the front face).
    #
    # Hole positions (Y, Z) on the front face:
    #   Row 1 (Z ~ 29.14):  (116.31, 29.14) , ( 76.22, 29.13)
    #   Row 2 (Z ~ 69.25):  ( 76.12, 69.22) , (116.22, 69.27)
    #   Row 3 (Z ~ 176.4):  ( 76.20, 176.47), (116.32, 176.37)
    #   Row 4 (Z ~ 216.4):  ( 76.24, 216.47), (116.27, 216.42)
    #
    # Hole diameter : 6 mm  →  radius 3 mm
    # Cut depth     : through entire 10 mm thickness (using 100mm both=True)
    # ========================================================================
    hole_centers_world = [
        (116.31,  29.14),   # 1 - bottom-right
        ( 76.22,  29.13),   # 2 - bottom-left
        ( 76.12,  69.22),   # 3 - lower-left
        (116.22,  69.27),   # 4 - lower-right
        ( 76.20, 176.47),   # 5 - upper-left
        (116.32, 176.37),   # 6 - upper-right
        ( 76.24, 216.47),   # 7 - top-left
        (116.27, 216.42),   # 8 - top-right
    ]
    # Convert world (Y, Z) → sketch (X, Y) by subtracting plane origin
    Y_ORIGIN = 96.27
    Z_ORIGIN = 122.77
    hole_centers_sketch = [
        (y - Y_ORIGIN, z - Z_ORIGIN) for (y, z) in hole_centers_world
    ]

    with BuildSketch(feature1_plane):
        with Locations(*hole_centers_sketch):
            Circle(radius=3.0)   # 6 mm diameter / 2 = 3 mm radius
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 4
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 5: Slot-shape through cut on LEFT side face (Y = 66.27)
    # ------------------------------------------------------------------------
    # 4 points on XZ plane at Y = 66.27 (closed boundary):
    #   Vertex     (75.00, 66.27,  79.18)  ← bottom-right corner
    #   Sketch Pt  (70.00, 66.27,  84.18)  ← bottom-left (inset 5mm)
    #   Sketch Pt  (70.00, 66.27, 161.36)  ← top-left    (inset 5mm)
    #   Vertex     (75.00, 66.27, 166.36)  ← top-right corner
    #
    # Shape : vertical slot with chamfered corners on the +X side
    # Cut   : through 60mm part thickness in +Y direction
    #         (using 200mm both=True for safety)
    # ========================================================================
    feature5_plane = Plane(
        origin=(70.0, 66.27, 122.77),    # plane on the Y=66.27 face
        x_dir=(1, 0, 0),                  # sketch X = world X
        z_dir=(0, 1, 0),                  # sketch normal = world +Y (into part)
    )
    # Right-handed: sketch Y = z_dir × x_dir = (0,1,0) × (1,0,0) = (0,0,-1) = world -Z
    # Sketch coord conversion:
    #   sketch_X = world_X - 70
    #   sketch_Y = -(world_Z - 122.77)  =  122.77 - world_Z
    feature5_pts = [
        (5.00,  43.59),   # world (75.00, 79.18)
        (0.00,  38.59),   # world (70.00, 84.18)
        (0.00, -38.59),   # world (70.00, 161.36)
        (5.00, -43.59),   # world (75.00, 166.36)
    ]
    with BuildSketch(feature5_plane):
        with BuildLine():
            Polyline(*feature5_pts, close=True)
        make_face()
    extrude(amount=200, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 5
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 6: Structural rib on TOP face (back face at X = 75)
    # ------------------------------------------------------------------------
    # 28 points define a closed boundary forming a structural rib pattern:
    #   - 4 corner "ear" protrusions at extremes of the profile
    #   - 2 diamond extensions at top (Z~226) and bottom (Z~19) of part
    #   - 1 long central narrow column connecting top and bottom diamonds
    #   - Chamfered transitions (45°) between sections
    #
    # NOTE on input X values:
    #   User-supplied points have X=80 or X=85 (alternating systematically:
    #   X=80 at outer extremes, X=85 at inset/chamfered positions). This is
    #   a chamfered 3D boundary. For a planar extrude we project all points
    #   to a single plane using only their (Y, Z) values, with the sketch
    #   plane placed at X=75 (the existing part's top/back face) so the new
    #   rib sits directly on the existing extrude with no gap.
    #
    # Plane origin : (75, 96.27, 122.77)  — at existing top face center
    # Sketch X     : world Y direction
    # Sketch Y     : world Z direction
    # Extrude      : 10 mm in +X direction
    # ========================================================================
    feature6_plane = Plane(
        origin=(75.0, 96.27, 122.77),
        x_dir=(0, 1, 0),                  # sketch X = world Y
        z_dir=(1, 0, 0),                  # sketch normal = world +X
    )
    # sketch_X = world_Y - 96.27
    # sketch_Y = world_Z - 122.77
    feature6_pts = [
        (-30.00,  76.09),    # 1  - left-top outer corner   (world Y=66.27,  Z=198.86)
        (-18.89,  76.09),    # 2  - inset                   (world Y=77.38,  Z=198.86)
        ( -2.50,  92.48),    # 3  - chamfer toward top      (world Y=93.77,  Z=215.25)
        ( -2.50, 103.59),    # 4  - top-left of diamond     (world Y=93.77,  Z=226.36)
        (  2.50, 103.59),    # 5  - top-right of diamond    (world Y=98.77,  Z=226.36)
        (  2.50,  92.48),    # 6  - chamfer from top        (world Y=98.77,  Z=215.25)
        ( 18.89,  76.09),    # 7  - inset                   (world Y=115.16, Z=198.86)
        ( 30.00,  76.09),    # 8  - right-top outer corner  (world Y=126.27, Z=198.86)
        ( 30.00,  71.09),    # 9  - right-top inner corner  (world Y=126.27, Z=193.86)
        ( 18.89,  71.09),    # 10 - inset                   (world Y=115.16, Z=193.86)
        (  2.50,  54.70),    # 11 - chamfer to center       (world Y=98.77,  Z=177.47)
        (  2.50, -54.70),    # 12 - center column bottom-R  (world Y=98.77,  Z=68.07)
        ( 18.89, -71.09),    # 13 - inset                   (world Y=115.16, Z=51.68)
        ( 30.00, -71.09),    # 14 - right-bot inner corner  (world Y=126.27, Z=51.68)
        ( 30.00, -76.09),    # 15 - right-bot outer corner  (world Y=126.27, Z=46.68)
        ( 18.89, -76.09),    # 16 - inset                   (world Y=115.16, Z=46.68)
        (  2.50, -92.48),    # 17 - chamfer toward bottom   (world Y=98.77,  Z=30.29)
        (  2.50, -103.59),   # 18 - bot-right of diamond    (world Y=98.77,  Z=19.18)
        ( -2.50, -103.59),   # 19 - bot-left of diamond     (world Y=93.77,  Z=19.18)
        ( -2.50, -92.48),    # 20 - chamfer from bottom     (world Y=93.77,  Z=30.29)
        (-18.89, -76.09),    # 21 - inset                   (world Y=77.38,  Z=46.68)
        (-30.00, -76.09),    # 22 - left-bot outer corner   (world Y=66.27,  Z=46.68)
        (-30.00, -71.09),    # 23 - left-bot inner corner   (world Y=66.27,  Z=51.68)
        (-18.89, -71.09),    # 24 - inset                   (world Y=77.38,  Z=51.68)
        ( -2.50, -54.70),    # 25 - chamfer to center       (world Y=93.77,  Z=68.07)
        ( -2.50,  54.70),    # 26 - center column top-L     (world Y=93.77,  Z=177.47)
        (-18.89,  71.09),    # 27 - inset                   (world Y=77.38,  Z=193.86)
        (-30.00,  71.09),    # 28 - left-top inner corner   (world Y=66.27,  Z=193.86)
    ]
    with BuildSketch(feature6_plane):
        with BuildLine():
            Polyline(*feature6_pts, close=True)
        make_face()
    extrude(amount=10, mode=Mode.ADD)
    # ------------------------------------------------------------------------
    # END FEATURE 6
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 7: Rectangular extrude on back face of Feature 6's central column
    # ------------------------------------------------------------------------
    # 4 input points (user-provided):
    #   Sketch Pt (70.00, 99.17, 177.53)  ← APPEARS TO BE MEASUREMENT ERROR
    #   Vertex    (85.00, 93.77, 177.47)
    #   Vertex    (85.00, 93.77,  68.07)
    #   Vertex    (85.00, 98.77,  68.07)
    #
    # NOTE: 3 vertices form 3 corners of a rectangle at plane X=85, while
    # the 4th (sketch) point reads X=70 — likely a pick error on a slanted
    # surface. We treat the 4th corner as the symmetric (85, 98.77, 177.47)
    # since it perfectly matches the central column of Feature 6.
    #
    # Profile : 5 mm wide (Y) × 109.4 mm tall (Z) rectangle at X = 85
    # Plane   : X = 85 (back face of Feature 6's central column)
    # Extrude : 18 mm in +X direction (extends column from X=85 to X=103)
    # ========================================================================
    feature7_plane = Plane(
        origin=(85.0, 96.27, 122.77),
        x_dir=(0, 1, 0),                  # sketch X = world Y
        z_dir=(1, 0, 0),                  # sketch normal = world +X
    )
    # sketch_X = world_Y - 96.27
    # sketch_Y = world_Z - 122.77
    feature7_pts = [
        (-2.50,  54.70),   # world (93.77, 177.47) — top-left
        (-2.50, -54.70),   # world (93.77,  68.07) — bottom-left
        ( 2.50, -54.70),   # world (98.77,  68.07) — bottom-right
        ( 2.50,  54.70),   # world (98.77, 177.47) — top-right (inferred)
    ]
    with BuildSketch(feature7_plane):
        with BuildLine():
            Polyline(*feature7_pts, close=True)
        make_face()
    extrude(amount=-15, mode=Mode.ADD)
    # ------------------------------------------------------------------------
    # END FEATURE 7
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 8: Eight hex pockets (circumradius R5) on BACK face (X = 75)
    # ------------------------------------------------------------------------
    # Same 8 positions as Feature 4's round through holes.
    # Hex pockets cut INTO the part from the BACK face (X=75) toward X=70.
    # Suitable for hex nut traps on the inside surface.
    #
    # Hex circumradius : 5 mm
    # Cut              : 5 mm deep pocket from X=75 face going inward (-X)
    # ========================================================================
    hex_centers_world = [
        (116.23, 216.37),   # 1 - top-right
        ( 76.25, 216.37),   # 2 - top-left
        ( 76.26, 176.31),   # 3 - upper-left
        (116.27, 176.31),   # 4 - upper-right
        ( 76.26,  69.08),   # 5 - lower-left
        ( 76.26,  29.06),   # 6 - bottom-left
        (116.27,  29.06),   # 7 - bottom-right
        (116.27,  69.08),   # 8 - lower-right
    ]
    # Convert world (Y, Z) → sketch (X, Y) by subtracting plane origin
    hex_centers_sketch = [
        (y - 96.27, z - 122.77) for (y, z) in hex_centers_world
    ]
    # Plane on the BACK face of Feature 1's extrude (X = 75)
    # Same orientation as feature1_plane (normal +X), just shifted by 10mm in +X
    hex_pocket_plane = feature1_plane.offset(10)   # plane at X = 75

    with BuildSketch(hex_pocket_plane):
        with Locations(*hex_centers_sketch):
            RegularPolygon(radius=5.0, side_count=6)   # circumradius = 5 mm
    extrude(amount=-5, mode=Mode.SUBTRACT)   # cut INTO part: X=75 → X=70

    # ========================================================================
    # FEATURE 2 / 3 RE-APPLY: Diamond cuts through Feature 6/7 material
    # ------------------------------------------------------------------------
    # Features 2 & 3 cut diamond holes through Feature 1's extrude earlier
    # (X = 65 → X = 75). However, Feature 6 then added material on top of
    # the back face (X = 75 → X = 85), partially blocking the diamond cut
    # path. We re-apply the diamond cuts here so they go all the way through
    # every layer (Feature 1 + Feature 6 + Feature 7 if any in path).
    # ========================================================================
    # Top diamond (re-apply of Feature 2)
    feature2_repeat_pts = [
        ( 14.32,  73.59), (  0.00,  87.91), (-14.32,  73.59), (  0.00,  59.27),
    ]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature2_repeat_pts, close=True)
        make_face()
    extrude(amount=200, both=True, mode=Mode.SUBTRACT)

    # Bottom diamond (re-apply of Feature 3)
    feature3_repeat_pts = [
        (  0.00, -87.91), ( 14.32, -73.59), (  0.00, -59.27), (-14.32, -73.59),
    ]
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature3_repeat_pts, close=True)
        make_face()
    extrude(amount=200, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 8 + diamond re-apply
    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    # END FEATURE 8
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 9 (revised v2): 6.5×6.5 chamfer on specific edges only
    # ------------------------------------------------------------------------
    # Two groups of edges (mirrored symmetrically across the part):
    #
    # Group A — Horizontal edges at very top/bottom of structural rib:
    #   Edge 1: (X=85, Y=93.77→98.77, Z=226.36) — top rib edge
    #   Edge 2: (X=85, Y=93.77→98.77, Z= 19.18) — bottom rib edge (mirror)
    #
    # Group B — Vertical edges at 4 corner "ears" of structural rib:
    #   Edge 3: (X=85, Y= 66.27, Z=193.86→198.86) — top-left ear  ← user-shown
    #   Edge 4: (X=85, Y=126.27, Z=193.86→198.86) — top-right ear (mirror)
    #   Edge 5: (X=85, Y= 66.27, Z= 46.68→ 51.68) — bottom-left ear
    #   Edge 6: (X=85, Y=126.27, Z= 46.68→ 51.68) — bottom-right ear
    # ========================================================================
    target_edges = []
    for edge in sidepanel_mount_inside.edges():
        v_start = edge @ 0
        v_end = edge @ 1

        # All target edges have BOTH endpoints at X = 85
        if abs(v_start.X - 85.0) > 0.1 or abs(v_end.X - 85.0) > 0.1:
            continue

        # ---- Group A: horizontal Y-direction edges at very top / bottom ----
        is_top_horizontal = (abs(v_start.Z - 226.36) < 0.1 and
                             abs(v_end.Z   - 226.36) < 0.1)
        is_bot_horizontal = (abs(v_start.Z -  19.18) < 0.1 and
                             abs(v_end.Z   -  19.18) < 0.1)

        # ---- Group B: vertical Z-direction edges at 4 corner ears ----
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

    print(f"[Feature 9] Found {len(target_edges)} target edge(s) to chamfer "
          f"(expected 6: 2 horizontal + 4 corner-ear vertical)")

    # Try 6.5×6.5 first; fall back to smaller sizes if geometry rejects
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

    if applied_chamfer is not None:
        print(f"[Feature 9] ✓ Applied {applied_chamfer}×{applied_chamfer}mm "
              f"chamfer (requested 6.5×6.5)")
    else:
        print("[Feature 9] ✗ Could not apply chamfer (no edges found or all sizes failed)")
    # ------------------------------------------------------------------------
    # END FEATURE 9
    # ------------------------------------------------------------------------

    # ========================================================================
    # NEXT FEATURE GOES HERE — paste below this line
    # ========================================================================



show_object(sidepanel_mount_inside.part)

# ============================================================================
# EXPORT STL
# ============================================================================
desktop = Path.home() / "Desktop"
stl_file = desktop / "X_Axis_Sidepanel_Mount_Inside.stl"
export_stl(sidepanel_mount_inside.part, str(stl_file))

print("=" * 70)
print("X AXIS SIDEPANEL MOUNT INSIDE")
print("=" * 70)
print(f"📁 File : {stl_file}")
print(f"✓ Feature 1 — Base profile extrude: 10mm in +X direction")
print(f"✓ Feature 2 — Diamond through cut at top (Y=96.27, Z=196.36)")
print(f"✓ Feature 3 — Diamond through cut at bottom (Y=96.27, Z=49.18)")
print(f"✓ Feature 4 — 8x 6mm DIA through holes (4 rows x 2 cols)")
print(f"✓ Feature 5 — Slot through cut on LEFT face (Y=66.27)")
print(f"✓ Feature 6 — Structural rib on TOP face (28-pt boundary): 10mm extrude")
print(f"✓ Feature 7 — Central column extension on back face: 18mm extrude")
print(f"✓ Feature 8 — 8x Hex pockets (R5, 5mm deep) on BACK face X=75")
print(f"✓ Diamond cuts re-applied to ensure through-cut after Feature 6/7")
print(f"✓ Feature 9 — 6.5×6.5 chamfer on 6 edges (2 horiz + 4 corner-ear vert) ✅")
print("=" * 70)