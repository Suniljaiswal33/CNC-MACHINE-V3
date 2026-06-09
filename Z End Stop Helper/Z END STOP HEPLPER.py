from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# Z END STOP HELPER
# =========================

length = 200
width = 450
height = 12

with BuildPart() as z_end_stop_helper:

    # Create rectangular cube
    Box(length, width, height)

# =========================
# SCALE 0.1
# =========================

scaled_part = scale(z_end_stop_helper.part, by=0.1)

# Show model
show_object(scaled_part)

# =========================
# EXPORT STL TO DESKTOP
# =========================

desktop = Path.home() / "Desktop"
stl_file = desktop / "Z_END_STOP_HELPER.stl"

export_stl(scaled_part, str(stl_file))

print("\n============================")
print("Z END STOP HELPER CREATED")
print("============================")
print(f"File : {stl_file}")
print("============================")