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
    