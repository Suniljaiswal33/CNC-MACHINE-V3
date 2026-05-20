from build123d import *
from pathlib import Path

# =====================================================
# PART NAME
# =====================================================
part_name = "Carriage_Back_spindle_2"

# =====================================================
# BASE PROFILE
# =====================================================
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

# =====================================================
# BUILD PART
# =====================================================
with BuildPart() as final_part:

    # -------------------------------------------------
    # BASE EXTRUSION
    # -------------------------------------------------
    with BuildSketch():
        Polygon(*base_pts)

    extrude(amount=90)

    # -------------------------------------------------
    # ANGLED THROUGH CUT (top slot)
    # -------------------------------------------------
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

    # -------------------------------------------------
    # FRONT FACE 7 mm DIA HOLES
    # -------------------------------------------------
    front_holes = [
        (489.72, 46.38),
        (559.75, 46.31),
        (489.82, 26.19),
        (559.75, 26.25),
    ]

    front_plane = Plane.XZ.offset(90)

    with BuildSketch(front_plane):
        for x, z in front_holes:
            with Locations((x, z)):
                Circle(radius=3.5)

    extrude(amount=-200, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # LEFT SLANTED FACE - 8 mm DIA THRU HOLES
    # Plane defined by corners:
    #   (461.80, 48.75, 0), (473.84, 31.47, 0),
    #   (473.84, 31.47, 90), (461.80, 48.75, 90)
    # -------------------------------------------------
    left_holes = [
        (464.84, 38.27, 11.07),
        (464.91, 38.38, 64.23),
    ]

    left_x_dir  = Vector(473.84 - 461.80, 31.47 - 48.75, 0).normalized()
    left_normal = left_x_dir.cross(Vector(0, 0, 1))
    left_cut    = -left_normal

    for x, y, z in left_holes:
        hole_plane = Plane(
            origin=(x, y, z),
            x_dir=left_x_dir,
            z_dir=left_normal,
        )
        with BuildSketch(hole_plane):
            Circle(radius=4)
        extrude(amount=150, dir=left_cut, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # LEFT SLANTED FACE - HEXAGON HOLES (5mm offset inward)
    # Circumscribed diameter 13.602 mm, thru cut
    # -------------------------------------------------
    left_offset_inward = -left_normal   # 5mm inward direction
    left_hex_holes = [
        (464.84, 38.27, 11.07),
        (464.91, 38.38, 64.23),
    ]

    for x, y, z in left_hex_holes:
        # Offset position 5mm inward
        offset_pos = Vector(x, y, z) + left_offset_inward * 5
        
        hex_plane = Plane(
            origin=(offset_pos.X, offset_pos.Y, offset_pos.Z),
            x_dir=left_x_dir,
            z_dir=left_normal,
        )
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.801, side_count=6)  # 13.602 mm circumscribed
        extrude(amount=150, dir=left_cut, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # RIGHT SLANTED FACE - 8 mm DIA THRU HOLES
    # Plane defined by corners:
    #   (575.89, 31.31, 0), (587.52, 48.75, 0),
    #   (587.52, 48.75, 90), (575.89, 31.31, 90)
    # -------------------------------------------------
    right_holes = [
        (584.46, 38.45, 11.27),
        (584.43, 38.41, 64.27),
    ]

    right_x_dir  = Vector(587.52 - 575.89, 48.75 - 31.31, 0).normalized()
    right_normal = right_x_dir.cross(Vector(0, 0, 1))
    right_cut    = -right_normal

    for x, y, z in right_holes:
        hole_plane = Plane(
            origin=(x, y, z),
            x_dir=right_x_dir,
            z_dir=right_normal,
        )
        with BuildSketch(hole_plane):
            Circle(radius=4)
        extrude(amount=150, dir=right_cut, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # RIGHT SLANTED FACE - HEXAGON HOLES (5mm offset inward)
    # Circumscribed diameter 13.602 mm, thru cut
    # -------------------------------------------------
    right_offset_inward = -right_normal   # 5mm inward direction
    right_hex_holes = [
        (584.46, 38.45, 11.27),
        (584.43, 38.41, 64.27),
    ]

    for x, y, z in right_hex_holes:
        # Offset position 5mm inward
        offset_pos = Vector(x, y, z) + right_offset_inward * 5
        
        hex_plane = Plane(
            origin=(offset_pos.X, offset_pos.Y, offset_pos.Z),
            x_dir=right_x_dir,
            z_dir=right_normal,
        )
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.801, side_count=6)  # 13.602 mm circumscribed
        extrude(amount=150, dir=right_cut, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # TOP FACE - 5.5 mm DIA THRU HOLES (drilled top-down, -Z direction)
    # Both holes on top face (Z = 90), cut all the way through.
    # -------------------------------------------------
    top_holes_5p5 = [
        (504.70, 46.18),   # (X, Y) - first hole
        (544.77, 46.13),   # (X, Y) - second hole
    ]

    top_plane_z90 = Plane.XY.offset(90)

    with BuildSketch(top_plane_z90):
        for x, y in top_holes_5p5:
            with Locations((x, y)):
                Circle(radius=2.75)   # 5.5 mm dia

    extrude(amount=-200, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # TOP FACE - 18 mm DIA POCKET, 24.50 mm DEPTH
    # Cut into the top surface at (524.69, 46.07), down 24.50 mm
    # -------------------------------------------------
    pocket_18 = (524.69, 46.07)

    top_plane_pocket = Plane.XY.offset(80.74)

    with BuildSketch(top_plane_pocket):
        with Locations(pocket_18):
            Circle(radius=9)   # 18 mm dia

    extrude(amount=-24.50, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # TOP FACE - 12 mm DIA THRU HOLE
    # Hole at (524.69, 46.07), drilled top-down all the way through
    # -------------------------------------------------
    hole_12mm = (524.69, 46.07)

    top_plane_hole = Plane.XY.offset(90)

    with BuildSketch(top_plane_hole):
        with Locations(hole_12mm):
            Circle(radius=6)   # 12 mm dia

    extrude(amount=-200, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # 4 HOLES - 3.5 mm DIA, 24.5 mm DEPTH
    # At Z = 79.74-79.76
    # -------------------------------------------------
    holes_3p5mm = [
        (519.20, 51.73),
        (530.30, 51.80),
        (529.96, 40.75),
        (519.20, 40.75),
    ]

    holes_plane_z79 = Plane.XY.offset(80.74)

    with BuildSketch(holes_plane_z79):
        for x, y in holes_3p5mm:
            with Locations((x, y)):
                Circle(radius=1.75)   # 3.5 mm dia

    extrude(amount=-24.5, mode=Mode.SUBTRACT)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #1 - 6-point boundary at Y = 61.12
    # Extrude perpendicular to plane (Y direction, inward)
    # -------------------------------------------------
    hex_boundary_pts = [
        (554.89, 58.37),   # (X, Z) on Y=-61.12 plane
        (544.25, 58.38),
        (538.30, 64.24),
        (544.02, 70.20),
        (555.18, 70.16),
        (540.65, 64.27),
    ]

    hex_extrude_plane = Plane.XZ.offset(-61.12)

    with BuildSketch(hex_extrude_plane):
        with BuildLine():
            Polyline(*hex_boundary_pts, close=True)
        make_face()

    # Extrude inward (toward body center, -Y direction)
    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #2 - 6-point boundary at Y = 61.12
    # Second hexagon feature, lower Z position
    # -------------------------------------------------
    hex_boundary_pts_2 = [
        (554.94, 5.38),    # (X, Z) on Y=61.12 plane
        (544.34, 5.38),
        (538.21, 11.27),
        (544.34, 17.16),
        (555.11, 17.13),
        (540.69, 11.24),
    ]

    hex_extrude_plane_2 = Plane.XZ.offset(-61.12)

    with BuildSketch(hex_extrude_plane_2):
        with BuildLine():
            Polyline(*hex_boundary_pts_2, close=True)
        make_face()

    # Extrude inward (toward body center, -Y direction)
    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #3 - 6-point boundary at Y = 61.10
    # Third hexagon feature
    # -------------------------------------------------
    hex_boundary_pts_3 = [
        (493.82, 5.18),    # (X, Z) on Y=61.10 plane
        (503.56, 5.18),
        (509.51, 11.07),
        (503.56, 16.96),
        (494.68, 16.96),
        (508.60, 11.24),
    ]

    hex_extrude_plane_3 = Plane.XZ.offset(-61.10)

    with BuildSketch(hex_extrude_plane_3):
        with BuildLine():
            Polyline(*hex_boundary_pts_3, close=True)
        make_face()

    # Extrude inward (toward body center, -Y direction)
    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #4 - 6-point boundary at Y = 61.10
    # Fourth hexagon feature, higher Z position
    # -------------------------------------------------
    hex_boundary_pts_4 = [
        (494.20, 58.34),   # (X, Z) on Y=61.10 plane
        (503.47, 58.34),
        (509.42, 64.23),
        (503.47, 70.12),
        (494.28, 70.09),
        (508.60, 64.24),
    ]

    hex_extrude_plane_4 = Plane.XZ.offset(-61.10)

    with BuildSketch(hex_extrude_plane_4):
        with BuildLine():
            Polyline(*hex_boundary_pts_4, close=True)
        make_face()

    # Extrude inward (toward body center, -Y direction)
    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # =================================================
    # MIRROR PLANE - from 4 points
    # =================================================
    mirror_pts = [
        (456.81, 46.29, 1.87),
        (459.69, 46.29, 89.05),
        (586.93, 46.21, 89.05),
        (586.93, 46.21, 1.87),
    ]
    
    # Calculate plane from 4 points
    p1 = Vector(*mirror_pts[0])
    p2 = Vector(*mirror_pts[1])
    p3 = Vector(*mirror_pts[2])
    
    v1 = (p2 - p1).normalized()  # x_dir
    v2 = (p3 - p1).normalized()
    v3 = v1.cross(v2).normalized()  # normal
    z_dir = v3.cross(v1).normalized()  # z_dir perpendicular to both
    
    mirror_plane = Plane(origin=p1, x_dir=v1, z_dir=z_dir)

    # =================================================
    # MIRRORED HEXAGON FEATURES (About mirror plane)
    # =================================================

    # -------------------------------------------------
    # HEXAGON EXTRUSION #1 MIRROR
    # -------------------------------------------------
    hex_boundary_pts_m1 = [
        (554.89, 58.37),
        (544.25, 58.38),
        (538.30, 64.24),
        (544.02, 70.20),
        (555.18, 70.16),
        (540.65, 64.27),
    ]

    hex_extrude_plane_m1 = Plane.XZ.offset(-61.12)

    with BuildSketch(hex_extrude_plane_m1):
        with BuildLine():
            Polyline(*hex_boundary_pts_m1, close=True)
        make_face()

    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #2
    # -------------------------------------------------
    hex_boundary_pts_2 = [
        (554.94, 5.38),
        (544.34, 5.38),
        (538.21, 11.27),
        (544.34, 17.16),
        (555.11, 17.13),
        (540.69, 11.24),
    ]

    hex_extrude_plane_2 = Plane.XZ.offset(-61.12)

    with BuildSketch(hex_extrude_plane_2):
        with BuildLine():
            Polyline(*hex_boundary_pts_2, close=True)
        make_face()

    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #3
    # -------------------------------------------------
    hex_boundary_pts_3 = [
        (493.82, 5.18),
        (503.56, 5.18),
        (509.51, 11.07),
        (503.56, 16.96),
        (494.68, 16.96),
        (508.60, 11.24),
    ]

    hex_extrude_plane_3 = Plane.XZ.offset(-61.10)

    with BuildSketch(hex_extrude_plane_3):
        with BuildLine():
            Polyline(*hex_boundary_pts_3, close=True)
        make_face()

    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)

    # -------------------------------------------------
    # HEXAGON EXTRUSION #4
    # -------------------------------------------------
    hex_boundary_pts_4 = [
        (494.20, 58.34),
        (503.47, 58.34),
        (509.42, 64.23),
        (503.47, 70.12),
        (494.28, 70.09),
        (508.60, 64.24),
    ]

    hex_extrude_plane_4 = Plane.XZ.offset(-61.10)

    with BuildSketch(hex_extrude_plane_4):
        with BuildLine():
            Polyline(*hex_boundary_pts_4, close=True)
        make_face()

    extrude(amount=26, dir=(0, -1, 0), mode=Mode.ADD)


    # =================================================
    # NEW SLANTED FACE - SVD PLANE from 4 points
    # =================================================
    new_plane_pts = [
        (584.70, 51.52, 10.62),
        (576.99, 59.07, 10.62),
        (577.23, 58.83, 59.29),
        (584.70, 51.52, 59.61),
    ]
    
    # Calculate plane from 4 points
    np1 = Vector(*new_plane_pts[0])
    np2 = Vector(*new_plane_pts[1])
    np3 = Vector(*new_plane_pts[2])
    
    nv1 = (np2 - np1).normalized()
    nv2 = (np3 - np1).normalized()
    n_normal = nv1.cross(nv2).normalized()
    n_z_dir = n_normal.cross(nv1).normalized()
    
    new_slant_plane = Plane(origin=np1, x_dir=nv1, z_dir=n_z_dir)
    
    # 8mm dia thru holes on new slanted face
    new_slant_holes = [
        (582.39, 53.78, 26.07),
        (582.39, 53.78, 78.88),
    ]
    
    n_cut = -n_normal
    
    for x, y, z in new_slant_holes:
        hole_plane = Plane(
            origin=(x, y, z),
            x_dir=nv1,
            z_dir=n_normal,
        )
        with BuildSketch(hole_plane):
            Circle(radius=4)  # 8mm dia
        extrude(amount=150, dir=n_cut, mode=Mode.SUBTRACT)

    # =================================================
    # HEXAGON CUTS ON NEW SLANTED FACE - 5mm offset inward
    # Circumscribed diameter 13.203 mm (radius = 6.6015)
    # =================================================
    n_offset_inward = -n_normal  # 5mm inward direction
    
    for x, y, z in new_slant_holes:
        # Offset position 5mm inward
        offset_pos = Vector(x, y, z) + n_offset_inward * 5
        
        hex_plane = Plane(
            origin=(offset_pos.X, offset_pos.Y, offset_pos.Z),
            x_dir=nv1,
            z_dir=n_normal,
        )
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.6015, side_count=6)  # 13.203 mm circumscribed
        extrude(amount=150, dir=n_cut, mode=Mode.SUBTRACT)

    # =================================================
    # THIRD SLANTED FACE - SVD PLANE from 4 points
    # =================================================
    third_plane_pts = [
        (464.45, 51.44, 79.69),
        (471.52, 58.60, 79.69),
        (471.52, 58.60, 19.62),
        (464.45, 51.44, 19.62),
    ]
    
    # Calculate plane from 4 points
    tp1 = Vector(*third_plane_pts[0])
    tp2 = Vector(*third_plane_pts[1])
    tp3 = Vector(*third_plane_pts[2])
    
    tv1 = (tp2 - tp1).normalized()
    tv2 = (tp3 - tp1).normalized()
    t_normal = tv1.cross(tv2).normalized()
    t_z_dir = t_normal.cross(tv1).normalized()
    
    third_slant_plane = Plane(origin=tp1, x_dir=tv1, z_dir=t_z_dir)
    
    # 8mm dia thru holes on third slanted face
    third_slant_holes = [
        (466.86, 53.88, 79.33),
        (466.86, 53.88, 26.25),
    ]
    
    t_cut = -t_normal
    
    for x, y, z in third_slant_holes:
        hole_plane = Plane(
            origin=(x, y, z),
            x_dir=tv1,
            z_dir=t_normal,
        )
        with BuildSketch(hole_plane):
            Circle(radius=4)  # 8mm dia
        extrude(amount=150, dir=t_cut, mode=Mode.SUBTRACT)

    # =================================================
    # HEXAGON CUTS ON THIRD SLANTED FACE - 5mm offset inward
    # Circumscribed diameter 13.202 mm (radius = 6.601)
    # =================================================
    t_offset_inward = -t_normal  # 5mm inward direction
    
    for x, y, z in third_slant_holes:
        # Offset position 5mm inward
        offset_pos = Vector(x, y, z) + t_offset_inward * 5
        
        hex_plane = Plane(
            origin=(offset_pos.X, offset_pos.Y, offset_pos.Z),
            x_dir=tv1,
            z_dir=t_normal,
        )
        with BuildSketch(hex_plane):
            RegularPolygon(radius=6.601, side_count=6)  # 13.202 mm circumscribed
        extrude(amount=150, dir=t_cut, mode=Mode.SUBTRACT)


# =====================================================
# EXPORT STL
# =====================================================
desktop_path = Path.home() / "Desktop"
stl_path = desktop_path / f"{part_name}.stl"

export_stl(final_part.part, str(stl_path))

print(f"STL exported successfully:\n{stl_path}")
print(f"Volume (mm^3) : {final_part.part.volume:.2f}")

# =====================================================
# OCP VIEW (optional - won't crash if viewer broken)
# =====================================================
try:
    from ocp_vscode import show
    show(final_part.part)
    print("Sent to OCP CAD Viewer.")
except Exception:
    print("OCP Viewer skipped - STL saved, open in Preview app.")