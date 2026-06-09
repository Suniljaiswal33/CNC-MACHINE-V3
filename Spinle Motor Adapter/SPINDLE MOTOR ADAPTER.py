from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# SPINDLE MOTOR ADAPTER
# =========================

with BuildPart() as spindle_motor_adapter:
    # Main outer cylinder - 100mm height
    Cylinder(radius=650/2, height=100)
    # Inner bore cut
    Cylinder(radius=525/2, height=100, mode=Mode.SUBTRACT)
    # 30mm GAP cut through wall thickness (C-ring style)
    Box(
        length=650/2 + 10,
        width=30,
        height=100,
        align=(Align.MIN, Align.CENTER, Align.CENTER),
        mode=Mode.SUBTRACT
    )

# =========================
# SCALE 0.1
# =========================
scaled_part = scale(spindle_motor_adapter.part, by=0.1)
show_object(scaled_part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Spindle_Motor_Adapter.stl"
export_stl(scaled_part, str(stl_file))
print("SPINDLE MOTOR ADAPTER CREATED")
print(f"File : {stl_file}")