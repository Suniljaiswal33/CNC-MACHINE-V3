from build123d import *
from pathlib import Path

part_name = "z carriage back"

base_pts = [
    (574.88, 61.13),
    (587.52, 48.75),
    (587.77, 43.44),
    (575.89, 31.31),
    (473.84, 31.47),
    (461.71, 43.26),
    (461.80, 48.75),
    (473.97, 61.09),
]

with BuildPart() as final_part:

    with BuildSketch():
        Polygon(*base_pts)
    extrude(amount=90)

    cut_pts = [
        (496.70, 90.04),
        (496.51, 84.71),
        (515.54, 84.72),
        (515.54, 79.76),
        (533.79, 79.74),
        (533.79, 84.72),
        (552.75, 84.72),
        (552.75, 90.24),
    ]
    with BuildSketch(Plane.XZ.offset(31.33)):
        Polygon(*cut_pts)
    extrude(amount=-200, mode=Mode.SUBTRACT)

    left_holes = [(464.84, 38.27, 11.07), (464.91, 38.38, 64.23)]
    left_x_dir  = Vector(473.84 - 461.80, 31.47 - 48.75, 0).normalized()
    left_normal = left_x_dir.cross(Vector(0, 0, 1))
    left_cut    = -left_normal

    for x, y, z in left_holes:
        hole_plane = Plane(origin=(x, y, z), x_dir=left_x_dir, z_dir=left_normal)
        with BuildSketch(hole_plane):
            Circle(radius=4)
        extrude(amount=150, dir=left_cut, mode=Mode.SUBTRACT)

    left_offset_inward = -left_normal
    for x, y, z in left_holes:
        offset_pos = Vector(x, y, z) + left_offset_inward * 5
        hex_plane = Plane(origin=(offset_pos.X, offset_pos.Y, offset_pos.Z), x_dir=left_x_dir, z_dir=left_normal)
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.801, side_count=6)
        extrude(amount=150, dir=left_cut, mode=Mode.SUBTRACT)

    right_holes = [(584.46, 38.45, 11.27), (584.43, 38.41, 64.27)]
    right_x_dir  = Vector(587.52 - 575.89, 48.75 - 31.31, 0).normalized()
    right_normal = right_x_dir.cross(Vector(0, 0, 1))
    right_cut    = -right_normal

    for x, y, z in right_holes:
        hole_plane = Plane(origin=(x, y, z), x_dir=right_x_dir, z_dir=right_normal)
        with BuildSketch(hole_plane):
            Circle(radius=4)
        extrude(amount=150, dir=right_cut, mode=Mode.SUBTRACT)

    right_offset_inward = -right_normal
    for x, y, z in right_holes:
        offset_pos = Vector(x, y, z) + right_offset_inward * 5
        hex_plane = Plane(origin=(offset_pos.X, offset_pos.Y, offset_pos.Z), x_dir=right_x_dir, z_dir=right_normal)
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.801, side_count=6)
        extrude(amount=150, dir=right_cut, mode=Mode.SUBTRACT)

    top_holes_5p5 = [(504.70, 46.18), (544.77, 46.13)]
    top_plane_z90 = Plane.XY.offset(90)
    with BuildSketch(top_plane_z90):
        for x, y in top_holes_5p5:
            with Locations((x, y)):
                Circle(radius=2.75)
    extrude(amount=-200, mode=Mode.SUBTRACT)

    pocket_18 = (524.69, 46.07)
    top_plane_pocket = Plane.XY.offset(80.74)
    with BuildSketch(top_plane_pocket):
        with Locations(pocket_18):
            Circle(radius=9)
    extrude(amount=-24.50, mode=Mode.SUBTRACT)

    hole_12mm = (524.69, 46.07)
    top_plane_hole = Plane.XY.offset(90)
    with BuildSketch(top_plane_hole):
        with Locations(hole_12mm):
            Circle(radius=6)
    extrude(amount=-200, mode=Mode.SUBTRACT)

    holes_3p5mm = [(519.20, 51.73), (530.30, 51.80), (529.96, 40.75), (519.20, 40.75)]
    holes_plane_z79 = Plane.XY.offset(80.74)
    with BuildSketch(holes_plane_z79):
        for x, y in holes_3p5mm:
            with Locations((x, y)):
                Circle(radius=1.75)
    extrude(amount=-24.5, mode=Mode.SUBTRACT)

    new_plane_pts = [(584.70, 51.52, 10.62), (576.99, 59.07, 10.62), (577.23, 58.83, 59.29), (584.70, 51.52, 59.61)]
    np1 = Vector(*new_plane_pts[0])
    np2 = Vector(*new_plane_pts[1])
    np3 = Vector(*new_plane_pts[2])
    nv1 = (np2 - np1).normalized()
    nv2 = (np3 - np1).normalized()
    n_normal = nv1.cross(nv2).normalized()
    n_z_dir = n_normal.cross(nv1).normalized()
    new_slant_plane = Plane(origin=np1, x_dir=nv1, z_dir=n_z_dir)
    new_slant_holes = [(582.39, 53.78, 26.07), (582.39, 53.78, 78.88)]
    n_cut = -n_normal
    for x, y, z in new_slant_holes:
        hole_plane = Plane(origin=(x, y, z), x_dir=nv1, z_dir=n_normal)
        with BuildSketch(hole_plane):
            Circle(radius=4)
        extrude(amount=150, dir=n_cut, mode=Mode.SUBTRACT)

    n_offset_inward = -n_normal
    for x, y, z in new_slant_holes:
        offset_pos = Vector(x, y, z) + n_offset_inward * 5
        hex_plane = Plane(origin=(offset_pos.X, offset_pos.Y, offset_pos.Z), x_dir=nv1, z_dir=n_normal)
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.6015, side_count=6)
        extrude(amount=150, dir=n_cut, mode=Mode.SUBTRACT)

    third_plane_pts = [(464.45, 51.44, 79.69), (471.52, 58.60, 79.69), (471.52, 58.60, 19.62), (464.45, 51.44, 19.62)]
    tp1 = Vector(*third_plane_pts[0])
    tp2 = Vector(*third_plane_pts[1])
    tp3 = Vector(*third_plane_pts[2])
    tv1 = (tp2 - tp1).normalized()
    tv2 = (tp3 - tp1).normalized()
    t_normal = tv1.cross(tv2).normalized()
    t_z_dir = t_normal.cross(tv1).normalized()
    third_slant_plane = Plane(origin=tp1, x_dir=tv1, z_dir=t_z_dir)
    third_slant_holes = [(466.86, 53.88, 79.33), (466.86, 53.88, 26.25)]
    t_cut = -t_normal
    for x, y, z in third_slant_holes:
        hole_plane = Plane(origin=(x, y, z), x_dir=tv1, z_dir=t_normal)
        with BuildSketch(hole_plane):
            Circle(radius=4)
        extrude(amount=150, dir=t_cut, mode=Mode.SUBTRACT)

    t_offset_inward = -t_normal
    for x, y, z in third_slant_holes:
        offset_pos = Vector(x, y, z) + t_offset_inward * 5
        hex_plane = Plane(origin=(offset_pos.X, offset_pos.Y, offset_pos.Z), x_dir=tv1, z_dir=t_normal)
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.601, side_count=6)
        extrude(amount=150, dir=t_cut, mode=Mode.SUBTRACT)

    # =================================================
    # BACK FACE - 20MM DIA CIRCLE CUT, 9MM DEPTH
    # =================================================
    with BuildSketch(Plane.XZ.offset(61.11)):
        with Locations((524.18, 37.12)):
            Circle(radius=10)
    
    extrude(amount=-9, mode=Mode.SUBTRACT)

    front_plane_z = Plane.XZ.offset(31.40)
    with BuildSketch(front_plane_z):
        for x, z in [(506.59, 63.62), (506.59, 10.64), (541.96, 10.64), (542.14, 63.62)]:
            with Locations((x, z)):
                Circle(radius=4)
    extrude(amount=-200, mode=Mode.SUBTRACT)

desktop_path = Path.home() / "Desktop"
stl_path = desktop_path / f"{part_name}.stl"
export_stl(final_part.part, str(stl_path))
print(f"STL exported successfully:\n{stl_path}")
print(f"Volume (mm^3) : {final_part.part.volume:.2f}")

try:
    from ocp_vscode import show
    show(final_part.part)
    print("Sent to OCP CAD Viewer.")
except Exception:
    print("OCP Viewer skipped - STL saved.")