"""
Router Mount - build123d + OCP CAD Viewer
Steps 1-9: body, plate, boss, holes, hex pockets, bore, slot, deep hex
Step 10: 2x2 chamfer on top face outer edges (collar top rim)
STL output: ~/Desktop/router_mount.stl
"""

import os
from build123d import (
    BuildPart, BuildSketch, BuildLine,
    Plane, Polyline, make_face, extrude, export_stl,
    Axis, Mode, RectangleRounded, Circle, RegularPolygon, Locations,
)
from ocp_vscode import show, set_port

set_port(3939)

profile_pts = [
    (301.56,  17.18), (377.06,  17.18), (376.94, -28.67),
    (375.92, -34.79), (373.92, -40.66), (370.98, -46.12),
    (369.19, -48.65), (367.19, -51.03), (365.01, -53.23),
    (362.65, -55.25), (360.13, -57.06), (357.48, -58.67),
    (354.70, -60.05), (351.81, -61.19), (348.85, -62.10),
    (345.81, -62.76), (345.81, -78.32), (332.81, -78.32),
    (332.81, -62.76), (329.78, -62.10), (326.81, -61.19),
    (323.93, -60.05), (321.15, -58.67), (318.49, -57.06),
    (315.98, -55.25), (313.62, -53.23), (311.44, -51.03),
    (309.44, -48.65), (307.64, -46.12), (306.06, -43.45),
    (304.71, -40.66), (303.59, -37.77), (302.71, -34.79),
    (302.07, -31.75), (301.69, -28.67),
]

SKETCH_Z, FIRST_EXTRUDE = 58.39, 90.0
PLATE_EXTRUDE, TAPER_DEG = 10.0, 45.0
BOSS_Y, BOSS_THICK, BOSS_W, BOSS_H, BOSS_FILLET = 34.76, 16.619, 101.39, 90.0, 2.0
BOSS_CX, BOSS_CZ = 339.315, 148.39
HOLE_DIA, HOLE_DEPTH = 8.0, 60.0
HOLE_CENTERS = [(321.64,114.39),(321.56,167.38),(357.06,167.38),(356.98,114.37)]
SIDE_X, SIDE_DIA, SIDE_DEPTH = 345.81, 5.0, 30.0
SIDE_CENTERS = [(-70.54,138.42),(-70.54,103.39),(-70.49,68.40)]
HEX_AC, HEX_DEPTH = 13.3, 6.0
HEX_CENTERS = [(321.56,167.38),(357.06,167.38)]
BORE_Z, BORE_DIA, BORE_DEPTH = 58.39, 65.0, 100.0
BORE_CENTER = (339.23, -25.62)
SLOT_Z, SLOT_DEPTH = 58.39, 100.0
SLOT_PTS = [(337.81,-78.32),(340.81,-78.32),(340.81,-58.29),(337.81,-58.29)]
HEX2_Y, HEX2_AC, HEX2_DEPTH = 23.18, 13.3, 40.0
HEX2_CENTERS = [(321.54,114.13),(357.05,114.13)]

# Step 10: chamfer params
CHAMFER       = 2.0     # mm - chamfer size (2 x 2)
TOP_Z         = SKETCH_Z + FIRST_EXTRUDE   # 148.39 - top face height

with BuildPart() as router_mount:
    # Step 1: main 90 mm body
    with BuildSketch(Plane.XY.offset(SKETCH_Z)):
        with BuildLine(): Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=FIRST_EXTRUDE)

    # Step 2: tapered plate on back face (+Y)
    back_face = router_mount.faces().sort_by(Axis.Y)[-1]
    extrude(to_extrude=back_face, amount=PLATE_EXTRUDE, taper=TAPER_DEG, mode=Mode.ADD)

    # Step 3: rounded rectangle boss on plane Y = 34.76
    with BuildSketch(Plane.XZ.offset(-BOSS_Y)):
        with Locations((BOSS_CX, BOSS_CZ)):
            RectangleRounded(BOSS_W, BOSS_H, BOSS_FILLET)
    extrude(amount=BOSS_THICK, dir=(0,-1,0), mode=Mode.ADD)

    # Step 4: 4 thru holes (M8) on plate
    with BuildSketch(Plane.XZ.offset(-BOSS_Y)):
        with Locations(*HOLE_CENTERS):
            Circle(radius=HOLE_DIA/2)
    extrude(amount=HOLE_DEPTH, dir=(0,-1,0), mode=Mode.SUBTRACT)

    # Step 5: 3 thru holes (M5) on right face
    with BuildSketch(Plane.YZ.offset(SIDE_X)):
        with Locations(*SIDE_CENTERS):
            Circle(radius=SIDE_DIA/2)
    extrude(amount=SIDE_DEPTH, dir=(-1,0,0), mode=Mode.SUBTRACT)

    # Step 6: 2 hex pockets on plate (counterbore)
    with BuildSketch(Plane.XZ.offset(-BOSS_Y)):
        with Locations(*HEX_CENTERS):
            RegularPolygon(radius=HEX_AC/2, side_count=6)
    extrude(amount=HEX_DEPTH, dir=(0,-1,0), mode=Mode.SUBTRACT)

    # Step 7: 65 mm thru bore (router collar)
    with BuildSketch(Plane.XY.offset(BORE_Z)):
        with Locations(BORE_CENTER):
            Circle(radius=BORE_DIA/2)
    extrude(amount=BORE_DEPTH, dir=(0,0,1), mode=Mode.SUBTRACT)

    # Step 8: clamping slot, thru cut on bottom
    with BuildSketch(Plane.XY.offset(SLOT_Z)):
        with BuildLine(): Polyline(*SLOT_PTS, close=True)
        make_face()
    extrude(amount=SLOT_DEPTH, dir=(0,0,1), mode=Mode.SUBTRACT)

    # Step 9: 2 deep hex pockets at Y = 23.18
    with BuildSketch(Plane.XZ.offset(-HEX2_Y)):
        with Locations(*HEX2_CENTERS):
            RegularPolygon(radius=HEX2_AC/2, side_count=6)
    extrude(amount=HEX2_DEPTH, dir=(0,-1,0), mode=Mode.SUBTRACT)

    # ----- Step 10: 2 x 2 chamfer on top face outer edges -----
    # Native chamfer() fails on the small polyline segments. Instead:
    # 1) ADD a "cap": profile extruded UP 2 mm above the body (Z=148.39 -> 150.39)
    # 2) SUBTRACT a tapered solid: same profile at Z=148.39 extruded UP 2 mm
    #    with -45 deg taper (flares outward), which removes everything OUTSIDE
    #    the chamfered surface. Net effect = 2x2 chamfer on top rim.
    with BuildSketch(Plane.XY.offset(TOP_Z)):
        with BuildLine(): Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=CHAMFER, dir=(0,0,1), mode=Mode.ADD)

    with BuildSketch(Plane.XY.offset(TOP_Z)):
        with BuildLine(): Polyline(*profile_pts, close=True)
        make_face()
    extrude(amount=CHAMFER, dir=(0,0,1), taper=-45, mode=Mode.SUBTRACT)

# show in OCP CAD Viewer
show(router_mount.part, names=["router_mount"])

# export STL to Desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
os.makedirs(desktop, exist_ok=True)
stl_path = os.path.join(desktop, "router_mount.stl")
export_stl(router_mount.part, stl_path)

print(f"STL written to : {stl_path}")
print(f"Volume (mm^3)  : {router_mount.part.volume:.2f}")
print(f"Num solids     : {len(router_mount.part.solids())}")