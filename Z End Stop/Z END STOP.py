from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# Z END STOP
# =========================

points = [
    (3810.0, 400.0, 2100.0),
    (3810.0, 400.0, 2280.0),
    (3810.0, 600.0, 2280.0),
    (3810.0, 600.0, 2300.0),
    (3810.0, 380.0, 2300.0),
    (3810.0, 380.0, 2100.0),
]

extrude_length = 200

with BuildPart() as z_end_stop:

    # Create sketch on YZ plane
    with BuildSketch(Plane.YZ):

        # Convert 3D points to YZ 2D points
        poly_points = [(y, z) for x, y, z in points]

        # Create closed boundary
        Polygon(*poly_points)

    # Extrude in X direction
    extrude(amount=extrude_length)

# =========================
# SCALE 0.1
# =========================

scaled_part = scale(z_end_stop.part, by=0.1)

# Show model
show_object(scaled_part)

# =========================
# EXPORT STL TO DESKTOP
# =========================

desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_END_STOP.stl"

export_stl(scaled_part, str(stl_file))

print("\n============================")
print("Z END STOP CREATED")
print("============================")
print(f"File : {stl_file}")
print("============================")