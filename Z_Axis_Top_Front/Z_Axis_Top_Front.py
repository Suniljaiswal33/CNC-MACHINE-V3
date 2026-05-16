from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import numpy as np

# ============================================================================
# Z AXIS TOP FRONT
# ============================================================================

# ============================================================================
# FEATURE 1: Base profile extrude (40mm)
# ----------------------------------------------------------------------------
# 8 points on XZ plane at Y = 32.17 (front face, closed boundary):
#   Vertex     (249.15, 32.17, 222.90)  ← bottom-left of stepped bottom
#   Vertex     (310.11, 32.17, 222.90)  ← step inner corner (low)
#   Vertex     (310.11, 32.18, 229.77)  ← step inner corner (high)
#   Vertex     (429.15, 32.18, 229.77)  ← bottom-right of upper bottom
#   Vertex     (429.15, 32.18, 249.77)  ← right side, before top chamfer
#   Vertex     (427.15, 32.18, 251.77)  ← top-right corner (after 2mm chamfer)
#   Vertex     (251.15, 32.18, 251.77)  ← top-left corner (before 2mm chamfer)
#   Sketch Pt  (249.15, 32.18, 249.77)  ← left side, after top chamfer
#
# Profile dims:
#   X width   : 180.00 mm (249.15 → 429.15)
#   Z height  : 28.87 mm  (222.90 → 251.77) on the right portion
#               20.00 mm  on the right-most portion
#   Bottom    : stepped — drops 6.87 mm between X=310.11 and X=249.15
#   Top       : 2×2 mm chamfers at both upper corners
#
# Plane: XZ plane at Y = 32.17 (front face)
# Extrude: 40 mm in +Y direction (into part)
# ============================================================================
feature1_plane = Plane(
    origin=(339.15, 32.17, 237.335),    # center of profile bb
    x_dir=(1, 0, 0),                     # sketch X = world X
    z_dir=(0, 1, 0),                     # sketch normal = world +Y
)
# Right-handed: sketch Y = z_dir × x_dir = (0,1,0) × (1,0,0) = (0,0,-1) = world -Z
# Sketch coord conversion:
#   sketch_X = world_X - 339.15
#   sketch_Y = -(world_Z - 237.335)  =  237.335 - world_Z
feature1_pts = [
    (-90.00,  14.435),   # world (249.15, 222.90) - bottom-left low
    (-29.04,  14.435),   # world (310.11, 222.90) - step low
    (-29.04,   7.565),   # world (310.11, 229.77) - step high
    ( 90.00,   7.565),   # world (429.15, 229.77) - bottom-right
    ( 90.00, -12.435),   # world (429.15, 249.77) - right before chamfer
    ( 88.00, -14.435),   # world (427.15, 251.77) - top-right chamfer end
    (-88.00, -14.435),   # world (251.15, 251.77) - top-left chamfer start
    (-90.00, -12.435),   # world (249.15, 249.77) - left after chamfer
]

with BuildPart() as z_axis_top_front:
    # ------------------------------------------------------------------------
    # FEATURE 1: Base profile extrude (40 mm)
    # ------------------------------------------------------------------------
    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*feature1_pts, close=True)
        make_face()
    extrude(amount=40, mode=Mode.ADD)
    # ------------------------------------------------------------------------
    # END FEATURE 1
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 2: Two 8mm DIA through holes on front face (Y = 32.18)
    # ------------------------------------------------------------------------
    # 2 sketch points on front face:
    #   (274.18, 32.18, 240.72)  ← left hole
    #   (404.27, 32.18, 240.84)  ← right hole
    #
    # Hole diameter : 8 mm  →  radius 4 mm
    # Cut depth     : through 40 mm part thickness (using 100mm both=True)
    # ========================================================================
    hole2_centers_world = [
        (274.18, 240.72),   # 1 - left
        (404.27, 240.84),   # 2 - right
    ]
    # Convert world (X, Z) → sketch (X, Y) using feature1_plane origin
    # sketch_X = world_X - 339.15
    # sketch_Y = 237.335 - world_Z
    hole2_centers_sketch = [
        (x - 339.15, 237.335 - z) for (x, z) in hole2_centers_world
    ]

    with BuildSketch(feature1_plane):
        with Locations(*hole2_centers_sketch):
            Circle(radius=4.0)   # 8 mm diameter / 2 = 4 mm radius
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 2
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 3: Slot/stadium-shape through cut on front face (Y = 32.17)
    # ------------------------------------------------------------------------
    # 28 points define a closed boundary forming a horizontal slot:
    #   - Right semicircle (CCW from top to bottom) at center ~(294.77, 230.9)
    #   - Bottom straight edge from (294.77, 227.90) to (288.94, 227.90)
    #   - Left semicircle (CCW from bottom to top) at center ~(288.95, 230.9)
    #   - Top straight edge from (288.96, 233.90) to (294.77, 233.90)
    #
    # Slot dimensions:
    #   Total length (X) : ~11.80 mm
    #   Total height (Z) :  6.00 mm
    #   Corner radius    : ~3.00 mm
    #
    # Cut: through 40mm part thickness (using 100mm both=True for safety)
    # ========================================================================
    slot_pts_world = [
        (294.77, 233.90), (295.50, 233.81), (296.18, 233.55), (296.78, 233.13),
        (297.26, 232.58), (297.59, 231.93), (297.76, 231.21), (297.74, 230.48),
        (297.55, 229.77), (297.21, 229.15), (296.73, 228.63), (296.14, 228.23),
        (295.47, 227.99), (294.77, 227.90), (288.94, 227.90), (288.18, 228.00),
        (287.47, 228.29), (286.86, 228.75), (286.41, 229.30), (286.11, 229.94),
        (285.96, 230.64), (285.98, 231.35), (286.17, 232.03), (286.52, 232.66),
        (287.00, 233.18), (287.59, 233.58), (288.25, 233.82), (288.96, 233.90),
    ]
    # Convert world (X, Z) → sketch (X, Y)
    slot_pts_sketch = [
        (x - 339.15, 237.335 - z) for (x, z) in slot_pts_world
    ]

    with BuildSketch(feature1_plane):
        with BuildLine():
            Polyline(*slot_pts_sketch, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 3
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 4: Hexagon extrude cut on BACK face (Y = 72.18)
    # ------------------------------------------------------------------------
    # 6 points form a hexagon on the back face (one listed as "Sketch Point",
    # rest as "Vertex" — all part of the closed boundary):
    #   Sketch Pt  (283.10, 72.18, 230.90)  ← left vertex
    #   Vertex     (286.10, 72.18, 225.71)  ← bottom-left
    #   Vertex     (297.77, 72.17, 225.71)  ← bottom-right
    #   Vertex     (300.76, 72.18, 230.90)  ← right vertex
    #   Vertex     (297.81, 72.18, 236.01)  ← top-right
    #   Vertex     (286.05, 72.18, 236.01)  ← top-left
    #
    # Hexagon dimensions:
    #   X width  : ~17.66 mm (283.10 → 300.76, point-to-point)
    #   Z height : ~10.30 mm (225.71 → 236.01, flat-to-flat)
    #   Center   : (~291.93, ~230.86)
    #
    # Plane: XZ plane at Y = 72.18 (back face)
    # Cut depth: 5.2 mm in -Y direction (into the part toward front)
    # ========================================================================
    feature4_plane = Plane(
        origin=(291.93, 72.18, 230.86),    # hexagon center
        x_dir=(1, 0, 0),                    # sketch X = world X
        z_dir=(0, -1, 0),                   # sketch normal = world -Y (into part)
    )
    # Right-handed: sketch Y = z_dir × x_dir = (0,-1,0) × (1,0,0) = (0,0,1) = world +Z
    # Sketch coord conversion:
    #   sketch_X = world_X - 291.93
    #   sketch_Y = world_Z - 230.86
    feature4_pts_world = [
        (283.10, 230.90),   # left vertex
        (286.10, 225.71),   # bottom-left
        (297.77, 225.71),   # bottom-right
        (300.76, 230.90),   # right vertex
        (297.81, 236.01),   # top-right
        (286.05, 236.01),   # top-left
    ]
    feature4_pts_sketch = [
        (x - 291.93, z - 230.86) for (x, z) in feature4_pts_world
    ]

    with BuildSketch(feature4_plane):
        with BuildLine():
            Polyline(*feature4_pts_sketch, close=True)
        make_face()
    extrude(amount=5.2, mode=Mode.SUBTRACT)   # 5.2 mm deep pocket
    # ------------------------------------------------------------------------
    # END FEATURE 4
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 5: Slot/stadium-shape through cut on TOP face (Z = 251.77)
    # ------------------------------------------------------------------------
    # 28 points form a closed slot boundary on the top face:
    #   - Top semicircle around (262.79, 49.68) → curves up to Y=53.68
    #   - Right straight edge from (265.79, 53.68) ... wait it's vertical slot
    #   - Two semicircles (top & bottom in Y), connected by short X straights
    #
    # Slot dimensions:
    #   X width  : ~13.95 mm (255.82 → 269.77)
    #   Y height :  8.00 mm  (45.68 → 53.68)
    #   Corner radius : ~4.0 mm
    #   Center   : (~262.79, 49.68)
    #
    # Plane: XY plane at Z = 251.77 (top face)
    # Cut: through 28.87 mm part height (using 100mm both=True for safety)
    # ========================================================================
    feature5_plane = Plane(
        origin=(262.79, 49.68, 251.77),    # slot center on top face
        x_dir=(1, 0, 0),                    # sketch X = world X
        z_dir=(0, 0, -1),                   # sketch normal = world -Z (into part)
    )
    # Right-handed: sketch Y = z_dir × x_dir = (0,0,-1) × (1,0,0) = (0,-1,0) = world -Y
    # Sketch coord conversion:
    #   sketch_X = world_X - 262.79
    #   sketch_Y = -(world_Y - 49.68)  =  49.68 - world_Y
    feature5_pts_world = [
        (259.79, 53.68), (258.84, 53.56), (257.94, 53.22), (257.14, 52.67),
        (256.50, 51.95), (256.05, 51.10), (255.82, 50.16), (255.82, 49.19),
        (256.05, 48.26), (256.50, 47.40), (257.14, 46.68), (257.94, 46.14),
        (258.84, 45.79), (259.79, 45.68), (265.79, 45.68), (266.75, 45.79),
        (267.65, 46.14), (268.45, 46.68), (269.09, 47.40), (269.53, 48.26),
        (269.77, 49.19), (269.77, 50.16), (269.53, 51.10), (269.09, 51.95),
        (268.45, 52.67), (267.65, 53.22), (266.75, 53.56), (265.79, 53.68),
    ]
    feature5_pts_sketch = [
        (x - 262.79, 49.68 - y) for (x, y) in feature5_pts_world
    ]

    with BuildSketch(feature5_plane):
        with BuildLine():
            Polyline(*feature5_pts_sketch, close=True)
        make_face()
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 5
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 6: Counterbore on TOP face — 22mm DIA pocket + 18mm DIA through
    # ------------------------------------------------------------------------
    # Center point: (339.20, 49.79, 251.77) on top face (Z = 251.77)
    #
    # Step A: 22 mm DIA extrude cut from top face, 7 mm deep
    #         (creates a flat counterbore face at Z = 244.77)
    # Step B: 18 mm DIA concentric circle, through cut
    #         (from the counterbore face all the way down through part)
    #
    # Plane: XY plane at Z = 251.77 (top face), normal -Z (into part)
    # ========================================================================
    feature6_plane = Plane(
        origin=(339.20, 49.79, 251.77),    # cut center on top face
        x_dir=(1, 0, 0),                    # sketch X = world X
        z_dir=(0, 0, -1),                   # sketch normal = world -Z (into part)
    )
    # Cut is centered on the sketch plane origin → sketch coords for both
    # circles are (0, 0).

    # ---- Step A: 22 mm DIA pocket, 7 mm deep ----
    with BuildSketch(feature6_plane):
        Circle(radius=11.0)   # 22 mm DIA / 2 = 11 mm radius
    extrude(amount=7, mode=Mode.SUBTRACT)

    # ---- Step B: 18 mm DIA concentric through cut ----
    with BuildSketch(feature6_plane):
        Circle(radius=9.0)    # 18 mm DIA / 2 = 9 mm radius
    extrude(amount=100, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 6
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 7: 8mm DIA through hole on TOP face (Z = 251.77)
    # ------------------------------------------------------------------------
    # Single sketch point: (415.47, 49.68, 251.77)
    #
    # Hole diameter : 8 mm  →  radius 4 mm
    # Cut depth     : through part (using 100mm both=True for safety)
    # ========================================================================
    feature7_plane = Plane(
        origin=(415.47, 49.68, 251.77),
        x_dir=(1, 0, 0),
        z_dir=(0, 0, -1),
    )
    with BuildSketch(feature7_plane):
        Circle(radius=4.0)   # 8 mm DIA / 2 = 4 mm radius
    extrude(amount=100, both=True, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 7
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 8: T-slot / dogbone extrude cut on LEFT face (X = 249.15)
    # ------------------------------------------------------------------------
    # 12 points form a closed boundary on the left face (YZ plane at X=249.15):
    #   The shape is a horizontal rectangle with two small tabs protruding
    #   left/right at mid-height — classic T-slot profile for sliding T-nuts.
    #
    # Main rectangle:
    #   Y range : 35.85 → 64.17  (width 28.32 mm)
    #   Z range : 222.90 → 236.90 (height 14.00 mm)
    # Side tabs (middle Z = 227.90→233.90, height 6 mm):
    #   Left tab  : Y 34.01 → 35.85 (sticks out 1.84 mm to -Y)
    #   Right tab : Y 64.17 → 66.01 (sticks out 1.84 mm to +Y)
    #
    # Plane: YZ plane at X = 249.15 (left face)
    # Cut depth: 56 mm in +X direction (into the part)
    # ========================================================================
    feature8_plane = Plane(
        origin=(249.15, 50.01, 229.90),    # bb center of the profile
        x_dir=(0, 1, 0),                    # sketch X = world Y
        z_dir=(1, 0, 0),                    # sketch normal = world +X (into part)
    )
    # Right-handed: sketch Y = z_dir × x_dir = (1,0,0) × (0,1,0) = (0,0,1) = world +Z
    # Sketch coord conversion:
    #   sketch_X = world_Y - 50.01
    #   sketch_Y = world_Z - 229.90
    feature8_pts_world = [
        (64.17, 236.90),   #  1 SP - top-right
        (64.17, 233.90),   #  2 V  - right side, above tab
        (66.01, 233.90),   #  3 V  - right tab top-outer
        (66.01, 227.90),   #  4 V  - right tab bottom-outer
        (64.17, 227.90),   #  5 V  - right side, below tab
        (64.17, 222.90),   #  6 V  - bottom-right
        (35.85, 222.90),   #  7 V  - bottom-left
        (35.85, 227.90),   #  8 V  - left side, below tab
        (34.01, 227.90),   #  9 V  - left tab bottom-outer
        (34.01, 233.90),   # 10 V  - left tab top-outer
        (35.85, 233.90),   # 11 V  - left side, above tab
        (35.85, 236.90),   # 12 SP - top-left
    ]
    feature8_pts_sketch = [
        (y - 50.01, z - 229.90) for (y, z) in feature8_pts_world
    ]

    with BuildSketch(feature8_plane):
        with BuildLine():
            Polyline(*feature8_pts_sketch, close=True)
        make_face()
    extrude(amount=56, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 8
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 9: Asymmetric T-slot extension cut on plane X = 273.61
    # ------------------------------------------------------------------------
    # 12 points form an asymmetric closed boundary on plane X = 273.61.
    # The depth (31.535mm) takes the cut from X=273.61 to X=305.145, which
    # exactly matches the back wall of Feature 8's T-slot — so this is a
    # stepped continuation of that cut creating a narrower channel.
    #
    # Profile dims:
    #   Y range : 59.17 → 66.01 (width 6.84 mm)
    #   Z range : 222.90 → 236.81 (height 13.91 mm)
    # Asymmetric shape:
    #   Left side  (Y=59.17): has INWARD notch from Z=227.90 to Z=233.90
    #                         (tab extends to Y=61.01)
    #   Right side (Y=64.17): has OUTWARD bump from Z=227.90 to Z=233.90
    #                         (tab extends to Y=66.01)
    #
    # Plane: YZ plane at X = 273.61
    # Cut depth: 31.535 mm in +X direction
    # ========================================================================
    feature9_plane = Plane(
        origin=(273.61, 62.59, 229.855),    # bb center of profile
        x_dir=(0, 1, 0),                     # sketch X = world Y
        z_dir=(1, 0, 0),                     # sketch normal = world +X
    )
    # sketch_X = world_Y - 62.59
    # sketch_Y = world_Z - 229.855
    feature9_pts_world = [
        (59.17, 236.81),   #  1 SP - top-left
        (59.17, 233.90),   #  2 SP - left side above notch
        (61.01, 233.90),   #  3 SP - notch top-inner
        (61.01, 227.90),   #  4 SP - notch bottom-inner
        (59.17, 227.90),   #  5 SP - left side below notch
        (59.17, 222.90),   #  6 V  - bottom-left
        (64.17, 222.90),   #  7 SP - bottom-right
        (64.17, 227.90),   #  8 V  - right side below tab
        (66.01, 227.90),   #  9 V  - right tab bottom-outer
        (66.01, 233.90),   # 10 SP - right tab top-outer
        (64.17, 233.90),   # 11 SP - right side above tab
        (64.17, 236.81),   # 12 SP - top-right
    ]
    feature9_pts_sketch = [
        (y - 62.59, z - 229.855) for (y, z) in feature9_pts_world
    ]

    with BuildSketch(feature9_plane):
        with BuildLine():
            Polyline(*feature9_pts_sketch, close=True)
        make_face()
    extrude(amount=31.535, mode=Mode.SUBTRACT)
    # ------------------------------------------------------------------------
    # END FEATURE 9
    # ------------------------------------------------------------------------

    # ========================================================================
    # FEATURE 10: Diamond annulus (ring) protrusion below bottom face
    # ------------------------------------------------------------------------
    # Two concentric diamonds on plane Z = 224.77, both centered at
    # (415.50, 49.68). The AREA BETWEEN them (annular ring) is extruded.
    #
    # OUTER diamond (4 vertices):
    #   (401.85, 49.68)  ← left
    #   (415.50, 36.03)  ← bottom
    #   (429.15, 49.68)  ← right
    #   (415.50, 63.32)  ← top
    #   → Half-diagonal: 13.65 mm
    #
    # INNER diamond (4 vertices):
    #   (415.50, 38.86)  ← bottom
    #   (426.32, 49.68)  ← right
    #   (415.50, 60.50)  ← top
    #   (404.68, 49.68)  ← left
    #   → Half-diagonal: 10.82 mm
    #
    # Ring wall thickness : 2.83 mm
    # Z=224.77 is exactly 5 mm below the bottom face (Z=229.77) at this X
    # region, so extruding 5 mm in +Z fills up to the existing bottom,
    # creating a protrusion that hangs below the part's main body.
    #
    # Plane     : XY plane at Z = 224.77
    # Extrude   : 5 mm in +Z direction (toward existing part bottom)
    # ========================================================================
    feature10_plane = Plane(
        origin=(415.50, 49.68, 224.77),
        x_dir=(1, 0, 0),                    # sketch X = world X
        z_dir=(0, 0, 1),                    # sketch normal = world +Z (upward)
    )
    # sketch_X = world_X - 415.50
    # sketch_Y = world_Y - 49.68

    # Outer diamond points
    outer_diamond_world = [
        (401.85, 49.68),   # left
        (415.50, 36.03),   # bottom
        (429.15, 49.68),   # right
        (415.50, 63.32),   # top
    ]
    outer_diamond_sketch = [
        (x - 415.50, y - 49.68) for (x, y) in outer_diamond_world
    ]

    # Inner diamond points
    inner_diamond_world = [
        (415.50, 38.86),   # bottom
        (426.32, 49.68),   # right
        (415.50, 60.50),   # top
        (404.68, 49.68),   # left
    ]
    inner_diamond_sketch = [
        (x - 415.50, y - 49.68) for (x, y) in inner_diamond_world
    ]

    with BuildSketch(feature10_plane):
        # Outer diamond — added to sketch
        with BuildLine():
            Polyline(*outer_diamond_sketch, close=True)
        make_face()
        # Inner diamond — subtracted from sketch (creates the hole in the ring)
        with BuildLine():
            Polyline(*inner_diamond_sketch, close=True)
        make_face(mode=Mode.SUBTRACT)
    extrude(amount=5, mode=Mode.ADD)
    # ------------------------------------------------------------------------
    # END FEATURE 10
    # ------------------------------------------------------------------------

    # ========================================================================
    # NEXT FEATURE GOES HERE — paste below this line
    # ========================================================================



show_object(z_axis_top_front.part)

# ============================================================================
# EXPORT STL
# ============================================================================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_Axis_Top_Front.stl"
export_stl(z_axis_top_front.part, str(stl_file))

print("=" * 70)
print("Z AXIS TOP FRONT")
print("=" * 70)
print(f"📁 File : {stl_file}")
print(f"✓ Feature 1 — Base profile extrude: 40mm in +Y direction")
print(f"✓ Feature 2 — 2x 8mm DIA through holes on front face")
print(f"✓ Feature 3 — Slot/stadium through cut (28-pt boundary) on front face")
print(f"✓ Feature 4 — Hexagon pocket (5.2mm deep) on BACK face Y=72.18")
print(f"✓ Feature 5 — Slot/stadium through cut (28-pt boundary) on TOP face")
print(f"✓ Feature 6 — Counterbore: 22mm DIA (7mm deep) + 18mm DIA through")
print(f"✓ Feature 7 — 8mm DIA through hole on TOP face at (415.47, 49.68)")
print(f"✓ Feature 8 — T-slot extrude cut (56mm deep) on LEFT face X=249.15")
print(f"✓ Feature 9 — Asymmetric T-slot extension cut (31.535mm) at X=273.61")
print(f"✓ Feature 10 — Diamond annulus protrusion (5mm) below bottom face ✅")
print("=" * 70)