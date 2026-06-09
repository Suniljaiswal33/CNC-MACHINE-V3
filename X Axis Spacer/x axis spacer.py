from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# X AXIS SPACER
# =========================

outer_dia = 120
inner_dia = 85
height = 80

with BuildPart() as spacer:

    # Outer cylinder
    Cylinder(
        radius=outer_dia / 2,
        height=height
    )

    # Inner hole
    Cylinder(
        radius=inner_dia / 2,
        height=height + 2,
        mode=Mode.SUBTRACT
    )

# =========================
# SCALE 0.1
# =========================

scaled_part = scale(spacer.part, by=0.1)

# Show model
show_object(scaled_part)

# =========================
# EXPORT STL TO DESKTOP
# =========================

desktop = Path.home() / "Desktop"
stl_file = desktop / "X_AXIS_SPACER.stl"

export_stl(scaled_part, str(stl_file))

print("\n============================")
print("X AXIS SPACER CREATED")
print("============================")
print(f"File : {stl_file}")
print("============================")