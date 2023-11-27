import matplotlib.pyplot as plt
class Lagrange:
    # def __init__(self, game, visited):
    #     self.game = game
    #     self.visited = visited
    def __init__(self):
        pass
    def extrapolate_next(self, x, data_points):
        needs_sum = []   # mutable list of Li(x0)(), Li(x1)(), Li(x2)(), Li(x3)()
        for i in range(data_points.__len__()):
            prodOfLi_n = 1
            temp = 1
            for j in range(data_points.__len__()):
                if i != j: 
                    prodOfLi_n *= (x - data_points[j][0]) / (data_points[i][0] - data_points[j][0])
                    temp = prodOfLi_n * data_points[i][1] # Li * fx
            needs_sum.append(temp)
        fx = 0
        for i in range(needs_sum.__len__()):
            fx += needs_sum[i]
        result = (int(x), int(fx))
        return result
    def plot(self, data_points, extrapolated_point):
        x_values = [point[0] for point in data_points]
        y_values = [point[1] for point in data_points]

        plt.scatter(x_values, y_values, color='blue', label='Data Points')
        plt.scatter(extrapolated_point[0], extrapolated_point[1], color='red', label='Extrapolated Point')

        # Plotting the line connecting the data points
        x_range = max(x_values) - min(x_values)
        x_min = min(x_values) - 0.1 * x_range
        x_max = max(x_values) + 0.1 * x_range
        x_values_line = [x_min + i * (x_max - x_min) / 100 for i in range(101)]
        y_values_line = [self.extrapolate_next(x, data_points)[1] for x in x_values_line]
        plt.plot(x_values_line, y_values_line, color='green', label='Extrapolation Line')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Lagrange Extrapolation')
        plt.legend()
        plt.show()
