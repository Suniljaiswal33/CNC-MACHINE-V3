from build123d import *
from ocp_vscode import show_object
from pathlib import Path
import numpy as np

# =========================
# HOSE CLAMP BOTTOM 90 DEGREE
# =========================

profile_points_1 = [
    (315.8972, 112.8254),
    (315.8972, 179.8254),
    (295.6472, 179.8254),
    (295.6472, 130.3834),
    (293.8972, 128.6793),
    (293.8972, 112.8254),
]

profile_points_2 = [
    (293.8972, 112.8254),
    (295.8972, 112.8254),
    (295.8972, 127.8254),
    (297.6472, 129.5446),
    (297.6472, 179.8254),
    (295.6472, 179.8254),
    (295.6472, 130.3834),
    (293.8972, 128.6793),
]

new_points = [
    (262.3305, -1.886),
    (269.4645, 5.2481),
    (270.7306, 4.2129),
    (271.9785, 3.2866),
    (273.4562, 2.5784),
    (274.9022, 1.8855),
    (276.5444, 1.2485),
    (277.9236, 0.8167),
    (279.4837, 0.4464),
    (281.5882, 0.1031),
    (283.1958, -0.0174),
    (284.2662, 0.0123),
    (285.8675, 0.0957),
    (293.8835, -7.8955),
    (295.6535, -7.8955),
    (295.6472, 2.0092),
    (300.9283, 2.0092),
    (300.9283, 7.8057),
    (302.9136, 10.483),
    (304.4815, 13.4242),
    (305.0979, 14.9738),
    (305.779, 16.9217),
    (305.9785, 18.1885),
    (306.2378, 19.8358),
    (306.4363, 22.0667),
    (306.4363, 24.3085),
    (306.0439, 26.4808),
    (305.6889, 28.1102),
    (305.0042, 30.0491),
    (304.5817, 31.2741),
    (303.9168, 32.779),
    (303.1011, 34.2336),
    (302.2372, 35.405),
    (301.6027, 36.1989),
    (301.1584, 36.9419),
    (308.2924, 44.076),
    (306.8782, 45.4811),
    (298.3929, 37.0049),
    (299.5123, 35.7915),
    (300.5305, 34.4919),
    (301.4407, 33.1147),
    (302.2372, 31.6686),
    (302.9148, 30.1631),
    (303.5089, 28.5336),
    (303.9168, 26.8058),
    (304.2752, 24.8764),
    (304.3931, 22.0964),
    (304.2934, 20.4485),
    (304.0394, 18.7854),
    (303.6987, 17.2034),
    (303.2076, 15.6273),
    (302.5175, 14.0476),
    (301.8535, 12.6188),
    (300.9995, 11.206),
    (299.5359, 9.2978),
    (298.3482, 8.0334),
    (297.7975, 7.4416),
    (296.54, 6.372),
    (294.5933, 5.0448),
    (292.6009, 4.0103),
    (290.7235, 3.244),
    (288.846, 2.6693),
    (287.4284, 2.345),
    (285.9579, 2.1131),
    (284.347, 2.0057),
    (282.8726, 2.0057),
    (281.6805, 2.1413),
    (280.5066, 2.304),
    (279.3931, 2.5102),
    (277.7984, 2.9375),
    (276.5254, 3.3974),
    (275.5833, 3.8062),
    (274.7379, 4.1692),
    (273.2918, 4.9657),
    (272.0876, 5.7625),
    (270.883, 6.6716),
    (270.0649, 7.3534),
    (269.4016, 8.0135),
    (260.9163, -0.4717),
]

def make_angled_hole_plane(pa, pb):
    direction = (pb - pa).normalized()
    hd = np.array([direction.X, direction.Y, direction.Z])
    arb = np.array([0, 1, 0]) if abs(hd[1]) < 0.9 else np.array([1, 0, 0])
    xd = np.cross(hd, arb)
    xd = xd / np.linalg.norm(xd)
    plane = Plane(
        origin=(pa.X, pa.Y, pa.Z),
        x_dir=(xd[0], xd[1], xd[2]),
        z_dir=(direction.X, direction.Y, direction.Z)
    )
    depth = (pb - pa).length
    return plane, depth

def make_svd_plane_and_locs(points_list):
    pts = np.array([[p[0], p[1], p[2]] for p in points_list])
    centroid = pts.mean(axis=0)
    centered = pts - centroid
    _, _, Vt = np.linalg.svd(centered)
    normal = Vt[-1] / np.linalg.norm(Vt[-1])
    x_dir = Vt[0] / np.linalg.norm(Vt[0])
    plane = Plane(
        origin=(centroid[0], centroid[1], centroid[2]),
        x_dir=(x_dir[0], x_dir[1], x_dir[2]),
        z_dir=(normal[0], normal[1], normal[2]),
    )
    def project(pt):
        y_dir = np.cross(normal, x_dir)
        v = pt - centroid
        return (np.dot(v, x_dir), np.dot(v, y_dir))
    locs = [project(np.array([p[0], p[1], p[2]])) for p in points_list]
    return plane, locs

# Hole 1
pa1 = Vector(265.9891, 155.2927, 1.7726)
pb1 = Vector(264.5294, 155.2791, 3.1414)
plane1, depth1 = make_angled_hole_plane(pa1, pb1)

# Hole 2
pa2 = Vector(303.4258, 155.1699, 42.0324)
pb2 = Vector(304.8363, 155.1699, 40.6204)
plane2, depth2 = make_angled_hole_plane(pa2, pb2)

# SVD thru cut 1
svd_pts_1 = [
    (308.1927, 160.1064, 46.7941),
    (305.49,   160.1064, 44.0944),
    (306.9001, 158.1133, 45.503),
    (306.9001, 152.0676, 45.503),
    (305.49,   150.0746, 44.0944),
    (308.1927, 150.0746, 46.7941),
]
svd_plane_1, locs_1 = make_svd_plane_and_locs(svd_pts_1)

# SVD thru cut 2
svd_pts_2 = [
    (259.4583, 160.1138, -1.8879),
    (262.2953, 160.1138,  0.946),
    (260.9258, 158.0742, -0.4221),
    (260.9258, 152.0592, -0.4221),
    (262.2953, 150.0888,  0.946),
    (259.4583, 150.0888, -1.8879),
]
svd_plane_2, locs_2 = make_svd_plane_and_locs(svd_pts_2)

with BuildPart() as hose_clamp_bottom:
    # Feature 1
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points_1, close=True)
        make_face()
    extrude(amount=2)

    # Feature 2
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points_2, close=True)
        make_face()
    extrude(amount=-18.25)

    # Feature 3
    with BuildSketch(Plane.XZ.offset(-150.1044)):
        with BuildLine():
            Polyline(*new_points, close=True)
        make_face()
    extrude(amount=-10)

    # 8mm dia thru hole
    with BuildSketch(Plane.XY.offset(2.0092)):
        with Locations((305.6698, 121.8217)):
            Circle(radius=4)
    extrude(amount=-30, mode=Mode.SUBTRACT)

    # 5mm angled hole 1
    with BuildSketch(plane1):
        Circle(radius=2.5)
    extrude(amount=depth1, mode=Mode.SUBTRACT)

    # 5mm angled hole 2
    with BuildSketch(plane2):
        Circle(radius=2.5)
    extrude(amount=depth2, mode=Mode.SUBTRACT)

    # SVD thru cut 1
    with BuildSketch(svd_plane_1):
        with BuildLine():
            Polyline(*locs_1, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

    # SVD thru cut 2
    with BuildSketch(svd_plane_2):
        with BuildLine():
            Polyline(*locs_2, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

show_object(hose_clamp_bottom.part)

# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Hose_Clamp_Bottom_90_Degree.stl"
export_stl(hose_clamp_bottom.part, str(stl_file))
print("HOSE CLAMP BOTTOM 90 DEGREE CREATED")
print(f"File : {stl_file}")