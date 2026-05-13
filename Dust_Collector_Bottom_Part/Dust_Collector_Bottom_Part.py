from build123d import *
from ocp_vscode import show_object
from pathlib import Path

# =========================
# DUST COLLECTOR BOTTOM PART
# =========================

profile_points = [
    (3770.0949, 172.1712),
    (3797.1508, 162.5701),
    (3821.6012, 147.828),
    (3844.2537, 126.6137),
    (3861.1533, 100.725),
    (3871.2211, 77.3534),
    (3874.0251, 64.2788),
    (3888.1376, -2.8488),
    (3909.3942, -128.189),
    (3917.553, -167.3457),
    (3920.788, -195.1666),
    (3923.9803, -230.3854),
    (3924.5817, -264.3418),
    (3922.7948, -299.1516),
    (3918.9536, -333.1912),
    (3912.416, -367.8288),
    (3908.128, -386.3347),
    (3904.1465, -401.4311),
    (3895.3649, -429.5433),
    (3879.1779, -470.0435),
    (3866.8569, -496.636),
    (3849.3453, -528.5459),
    (3828.6338, -560.3292),
    (3795.919, -603.197),
    (3745.1714, -654.1583),
    (3681.5579, -702.7359),
    (3653.3519, -719.7762),
    (3610.13, -740.5665),
    (3565.2667, -759.1683),
    (3524.2332, -771.7519),
    (3482.6526, -779.9586),
    (3456.3912, -783.7884),
    (3407.6981, -783.7884),
    (3378.2707, -783.6352),
    (3327.9714, -783.6352),
    (3253.2386, -769.7686),
    (2678.3284, -567.95),
    (2628.6871, -548.4851),
    (2590.6082, -532.0275),
    (2544.4046, -503.1125),
    (2501.4743, -465.7472),
    (2468.879, -422.8168),
    (2445.0287, -379.8864),
    (2425.063, -318.6793),
    (2418.9642, -266.8399),
    (2425.063, -203.8194),
    (2448.4416, -125.5521),
    (2480.9682, -68.6304),
    (2526.7089, -20.8568),
    (2597.0459, 28.678),
    (2680.2212, 73.2793),
    (2777.8619, 115.4697),
    (2881.5297, 146.8112),
    (2945.418, 161.2765),
    (3002.76, 172.1712),
]

new_feature_points = [
    (3202.6847, -688.0214),
    (2704.4568, -510.2103),
    (2615.2882, -477.4643),
    (2573.4792, -449.7879),
    (2538.1478, -415.0453),
    (2510.354, -374.4546),
    (2487.7259, -315.7706),
    (2480.4182, -248.4161),
    (2487.7259, -194.8262),
    (2506.4011, -146.9202),
    (2541.3157, -93.3304),
    (2584.291, -53.555),
    (2676.5717, 2.5034),
    (2749.8789, 38.7257),
    (2833.5352, 69.7734),
    (2920.6413, 93.9217),
    (3012.653, 111.2111),
    (3075.7056, 111.7022),
    (3075.6839, 93.0077),
    (3053.0956, 70.1196),
    (3033.4668, 48.9085),
    (3014.833, 25.7847),
    (3004.5828, 11.0026),
    (2995.8152, -2.2003),
    (2993.9078, -4.9912),
    (2985.2991, -13.794),
    (2978.3427, -20.7015),
    (2717.7222, -20.7015),
    (2685.6366, -24.9391),
    (2657.1274, -32.3763),
    (2635.4285, -41.0164),
    (2618.6422, -49.2805),
    (2603.5344, -58.1902),
    (2573.769, -81.2125),
    (2553.9943, -100.7894),
    (2539.0989, -119.781),
    (2526.0416, -139.7336),
    (2517.1169, -157.9197),
    (2508.5291, -178.6316),
    (2499.0275, -215.3671),
    (2496.0093, -243.1296),
    (2496.0093, -268.5322),
    (2498.1515, -289.6817),
    (2503.1239, -314.2137),
    (2512.9649, -343.7367),
    (2537.2775, -388.268),
    (2568.2904, -424.1052),
    (2611.0193, -458.564),
    (2662.9237, -479.2307),
    (2716.2, -490.3299),
    (2978.1422, -490.3299),
    (2997.4903, -509.4263),
    (3025.9895, -553.1251),
    (3075.3882, -607.2736),
    (3139.0365, -652.8724),
]

new_feature_points_2 = [
    (3847.8153, -134.4897),
    (3829.637, -79.3683),
    (3802.6394, -24.7635),
    (3773.5519, 21.9843),
    (3710.6314, 92.8362),
    (3710.6314, 111.7731),
    (3755.1797, 111.2111),
    (3780.0488, 102.9214),
    (3797.8125, 88.7105),
    (3811.4314, 65.0255),
    (3817.1209, 41.66),
    (3836.4745, -56.791),
]

thru_cut_points = [
    (3378.2707, -783.6352),
    (3407.6981, -783.7884),
    (3407.6981, -723.5364),
    (3378.2707, -723.246),
]

with BuildPart() as dust_collector_bottom:
    # Outer profile extrude
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
    extrude(amount=110)

    # Inner offset 60mm subtract - ring
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
        offset(amount=-60)
    extrude(amount=110, mode=Mode.SUBTRACT)



    # CAVITY - bottom face (z=0) se 80mm deep
    # Step 1: Outer -20mm offset area cut karo
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
        offset(amount=-20)  # outer se 20mm andar
    extrude(amount=80, mode=Mode.SUBTRACT)

    # Step 2: Inner -40mm offset area wapas ADD karo
    # (60mm inner wall - 20mm = 40mm offset = inner boundary +20mm bahar)
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
        offset(amount=-40)  # inner boundary se 20mm bahar
    extrude(amount=80, mode=Mode.ADD)

        # Inner offset 60mm subtract - ring
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*profile_points, close=True)
        make_face()
        offset(amount=-60)
    extrude(amount=110, mode=Mode.SUBTRACT)

        # THRU CUT
    with BuildSketch(Plane.XY):
        with BuildLine():
            Polyline(*thru_cut_points, close=True)
        make_face()
    extrude(amount=500, both=True, mode=Mode.SUBTRACT)

        # New feature 1
    with BuildSketch(Plane.XY.offset(110)):
        with BuildLine():
            Polyline(*new_feature_points, close=True)
        make_face()
    extrude(amount=-20)

    # New feature 2
    with BuildSketch(Plane.XY.offset(110)):
        with BuildLine():
            Polyline(*new_feature_points_2, close=True)
        make_face()
    extrude(amount=-20)

show_object(dust_collector_bottom.part)





# =========================
# EXPORT STL
# =========================
desktop = Path.home() / "Desktop"
stl_file = desktop / "Dust_Collector_Bottom_Part.stl"
export_stl(dust_collector_bottom.part, str(stl_file))
print("DUST COLLECTOR BOTTOM PART CREATED")
print(f"File : {stl_file}")