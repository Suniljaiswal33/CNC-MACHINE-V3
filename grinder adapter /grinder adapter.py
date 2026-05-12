from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# GRINDER ADAPTER
# =========================

hole_points = [
    (19.9674, -10.0078),
    (19.9674, 10.1839),
]

with BuildPart() as grinder_adapter:
    # Main outer cylinder - OD 65 - 0.5 = 64.5mm
    Cylinder(radius=64.5/2, height=5)
    # Inner bore cut
    Cylinder(radius=25/2, height=5, mode=Mode.SUBTRACT)
    # 3mm width cut on top (C-ring style)
    Box(
        length=64.5/2 + 10,
        width=3,
        height=5,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT
    )
    # 6mm dia through holes
    with BuildSketch(Plane.XY.offset(2.5)):
        for pt in hole_points:
            with Locations((pt[0], pt[1])):
                Circle(radius=3)
    extrude(amount=-10, mode=Mode.SUBTRACT)

show_object(grinder_adapter.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Grinder_Adapter.stl"
export_stl(grinder_adapter.part, str(stl_file))
print("GRINDER ADAPTER CREATED")
print(f"File : {stl_file}")