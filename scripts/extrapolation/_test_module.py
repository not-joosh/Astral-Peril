from lagrange_method import Lagrange
from direct_method import Direct_Method

#-:-:-:-:---:-:--:-:-:-:---:-:--:-:-:-:---:-:-
#
# Control Samples
#
Control_Sample = [
    (0, 7.5),
    (2.5, 10.5),
    (5, 12.5),
    (10, 15.8),
    (15, 17.9),
    (20.0, 19.4),
]
#
# Lagrange Samples
#
Lagrange_Sample1 = [
    (-24, 272), (-15, 267), (-6, 262),
    (2, 257), (10, 252), (18, 247),
    (26, 242), (34, 237), (42, 232),
    (50, 227), (58, 222), (66, 217),
    (74, 212), (82, 207), (90, 202),
    (98, 197), (106, 192), (114, 187),
    (122, 182), (130, 177), (138, 172),
    (146, 167), (154, 162), (162, 157),
    (170, 152), (178, 147), (186, 142),
    (194, 137), (202, 132), (210, 127),
    (218, 122), (226, 117), (234, 112),
    (242, 107), (250, 102), (258, 97),
    (266, 92), (274, 87), (282, 82),
    (290, 77), (298, 72), (306, 67),
    (314, 62), (322, 57), (330, 52),
    (338, 47), (346, 42), (354, 37),
    (362, 32), (370, 27), (378, 22),
    (386, 17), (394, 12), (402, 7),
    (410, 2), (418, -2)
]
#-:-:-:-:---:-:--:-:-:-:---:-:--:-:-:-:---:-:-
class TestModule:
    def __init__(self) -> None:
        pass
    def lagrange_test_extrapolation(weight1, weight2, dataset):
            filtered_data = dataset[weight1:weight2]
            lagrange_test_obj = Lagrange()
            predicted_coordinate = lagrange_test_obj.extrapolate_next(dataset[-1][0], filtered_data)
            print("\nCHOSEN DATA POINTS: \t", filtered_data)
            print("\nPREDICTION: \t", predicted_coordinate)
            print("\nEXPECTED: \t", dataset[-1], "\n\n\n")
        
    def lagrange_test_interpolation(weight1, weight2, dataset):
            print("Interpolation not supported...")
    def direct_test_extrapolation(weight1, weight2, dataset):
            print("Extrapolation not supported...")
    def direct_test_interpolation(dataset, target):
        # Find the two data points that surround the target value
        filtered_data = []
        for i in range(len(dataset) - 1):
            if dataset[i][0] <= target <= dataset[i+1][0]:
                filtered_data = [dataset[i], dataset[i+1]]
                break
        print(filtered_data)
        # Perform interpolation to predict the y value of the target
        # x1, y1 = filtered_data[0]
        # x2, y2 = filtered_data[1]
        # predicted_coordinate = y1 + (target - x1) * (y2 - y1) / (x2 - x1)
        
        print("\nCHOSEN DATA POINTS: \t", filtered_data)
        # print("\nPREDICTION: \t", predicted_coordinate)

TestingModule = TestModule()
TestModule.lagrange_test_extrapolation(25, -5, Lagrange_Sample1)
# TestingModule.direct_test_interpolation(Control_Sample, 3)

# lagrange_test_extrapolation(self, weight1, weight2, dataset):
# difficulty = {
#     "very_easy": (-25, 21),
#     "easy": (-25, -20),
#     "medium": (-25, -15),
#     "hard": (-20, -10),
#     "very_hard": (-10, -5),
# }
# TestModule.lagrange_test(difficulty["easy"][0], difficulty["easy"][1], Lagrange_Sample)
