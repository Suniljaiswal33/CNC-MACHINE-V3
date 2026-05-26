from build123d import *
from ocp_vscode import *
import os

# =========================================================
# PART NAME
# =========================================================

PART_NAME = "dust collector bottom part - SHELL"

# =========================================================
# PARAMETERS
# =========================================================

WALL_THICKNESS = 2.27

# =========================================================
# HELPER FUNCTION: OFFSET PROFILE INWARD
# =========================================================

def offset_profile_inward(points, offset_distance=2.0):
    """
    Offset a closed profile inward by the specified distance.
    This approximation offsets each point toward the centroid.
    """
    # Calculate centroid
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    
    offset_points = []
    for x, y in points:
        # Vector from centroid to point
        dx = x - cx
        dy = y - cy
        
        # Distance from centroid
        dist = (dx**2 + dy**2)**0.5
        
        if dist > 0:
            # Normalize and move inward
            scale_factor = (dist - offset_distance) / dist
            new_x = cx + dx * scale_factor
            new_y = cy + dy * scale_factor
            offset_points.append((new_x, new_y))
        else:
            offset_points.append((x, y))
    
    return offset_points

# =========================================================
# TOP SECTION
# =========================================================

section1 = [
    (-47.0, 17.0),
    (30.7393, 34.6138),
    (37.8188, 35.4684),
    (43.9747, 34.6138),
    (50.3982, 32.3615),
    (57.0, 28.0),
    (62.0, 22.0),
    (65.0, 15.0),
    (66.4284, 8.4245),
    (66.4284, 2.6839),
    (65.0, -4.0),
    (62.0, -10.0),
    (58.0, -15.0),
    (54.0, -18.0),
    (48.6298, -21.2117),
    (43.0, -23.0),
    (-30.0, -34.0),
    (-35.0, -35.0),
    (-40.7539, -35.3201),
    (-47.7819, -34.0),
    (-54.3593, -31.0853),
    (-59.0, -27.0),
    (-63.2204, -21.507),
    (-66.0, -15.0),
    (-66.6514, -9.688),
    (-66.0, -4.0),
    (-64.5964, 1.2565),
    (-62.3763, 6.1079),
    (-58.0, 11.0),
    (-51.6834, 15.4395),
]

# =========================================================
# BOTTOM SECTION
# =========================================================

section2 = [
    (48.8315, -21.0602),
    (53.872, -18.3197),
    (58.0, -15.0),
    (62.0, -10.0),
    (65.0, -4.0),
    (66.1786, 1.5421),
    (66.5492, 7.9683),
    (65.0, 15.8783),
    (62.5051, 20.8961),
    (59.2173, 25.4483),
    (55.4238, 28.989),
    (48.5592, 33.1085),
    (42.0, 35.0),
    (34.0, 35.0),
    (29.0, 34.0),
    (24.0, 32.0),
    (19.0, 29.0),
    (14.0, 24.0),
    (9.0, 14.5625),
    (8.0, 9.3457),
    (8.0, 3.0),
    (9.0, -3.0),
    (11.4345, -8.4481),
    (14.5136, -12.9328),
    (18.0369, -16.4614),
    (22.3603, -19.6729),
    (26.7684, -21.6324),
    (32.0, -23.0),
    (37.1256, -23.4376),
    (43.4424, -22.8572),
]

# =========================================================
# OFFSET PROFILES FOR INNER SHELL
# =========================================================

section1_inner = offset_profile_inward(section1, WALL_THICKNESS)
section2_inner = offset_profile_inward(section2, WALL_THICKNESS)

# =========================================================
# BUILD PART
# =========================================================

with BuildPart() as bp:

    # =====================================================
    # OUTER TOP PROFILE
    # =====================================================

    with BuildSketch(Plane.XY.offset(27.5)) as top_sk:
        with BuildLine():
            Polyline(*section1, close=True)
        make_face()

    top_face = top_sk.sketch.face()

    # =====================================================
    # OUTER BOTTOM PROFILE
    # =====================================================

    with BuildSketch(Plane.XY.offset(-27.5)) as bottom_sk:
        with BuildLine():
            Polyline(*section2, close=True)
        make_face()

    bottom_face = bottom_sk.sketch.face()

    # =====================================================
    # OUTER LOFT (FULL SOLID)
    # =====================================================

    outer_loft = loft(
        sections=[top_face, bottom_face],
        ruled=False,
    )

# =========================================================
# BUILD INNER CAVITY
# =========================================================

with BuildPart() as bp_inner:

    # =====================================================
    # INNER TOP PROFILE
    # =====================================================

    with BuildSketch(Plane.XY.offset(27.5)) as top_inner_sk:
        with BuildLine():
            Polyline(*section1_inner, close=True)
        make_face()

    top_inner_face = top_inner_sk.sketch.face()

    # =====================================================
    # INNER BOTTOM PROFILE
    # =====================================================

    with BuildSketch(Plane.XY.offset(-27.5)) as bottom_inner_sk:
        with BuildLine():
            Polyline(*section2_inner, close=True)
        make_face()

    bottom_inner_face = bottom_inner_sk.sketch.face()

    # =====================================================
    # INNER LOFT (CAVITY)
    # =====================================================

    inner_loft = loft(
        sections=[top_inner_face, bottom_inner_face],
        ruled=False,
    )

# =========================================================
# CREATE HOLLOW SHELL (REMOVE TOP AND BOTTOM)
# =========================================================

outer_model = bp.part
inner_model = bp_inner.part

# Subtract inner from outer to create shell
hollow_shell = outer_model - inner_model

# Remove top face
try:
    top_face_3d = outer_model.faces().filter(lambda f: f.center.Z > 25)
    if top_face_3d:
        hollow_shell = hollow_shell.cut(top_face_3d[0])
except:
    pass

# Remove bottom face
try:
    bottom_face_3d = outer_model.faces().filter(lambda f: f.center.Z < -25)
    if bottom_face_3d:
        hollow_shell = hollow_shell.cut(bottom_face_3d[0])
except:
    pass

model = hollow_shell

# =========================================================
# EXPORT STL
# =========================================================

desktop_path = os.path.expanduser("~/Desktop")

stl_path = os.path.join(
    desktop_path,
    f"{PART_NAME}.stl"
)

export_stl(model, stl_path)

# =========================================================
# INFO
# =========================================================

print("\n" + "=" * 60)
print("PART:", PART_NAME)
print("=" * 60)

print(f"\nWall Thickness: {WALL_THICKNESS} mm")
print(f"\nSTL Exported:\n{stl_path}")

bbox = model.bounding_box()

print("\nBounding Box (mm):")
print(f"  X: {bbox.size.X:.2f}")
print(f"  Y: {bbox.size.Y:.2f}")
print(f"  Z: {bbox.size.Z:.2f}")

print(f"\nVolume (mm^3): {model.volume:.2f}")

# =========================================================
# OCP VIEWER
# =========================================================

show(
    model,
    reset_camera=True,
)

print("\nModel sent to OCP CAD Viewer.")