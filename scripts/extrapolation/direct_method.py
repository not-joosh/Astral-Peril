class Direct_Method:
    # def __init__(self, game, vsisted):
    #     self.game = game
    #     self.visited = []
    def __init__(self) -> None:
        pass
    def interpolate_next(self, dataset, x):
        # Extract x and y values from the dataset
        xs = [data[0] for data in dataset]
        ys = [data[1] for data in dataset]

        # Solve for A and B using Cramer's Rule
        n = len(dataset)
        det = n * sum([x ** 2 for x in xs]) - sum(xs) ** 2
        det_a = sum([xs[i] * ys[i] for i in range(n)]) * n - sum(xs) * sum(ys)
        det_b = sum([x ** 2 for x in xs]) * sum(ys) - sum(xs) * sum([xs[i] * ys[i] for i in range(n)])

        A = det_a / det
        B = det_b / det

        # Calculate the extrapolated point
        y = A * x + B

        return x, y
    def plot(self):
        pass


Direct_Sample = [
    (0, 7.5),
    (2.5, 10.5),
    (5, 12.5),
    (10, 15.8),
    (15, 17.9),
    (20.0, 19.4),
]

Trial = Direct_Method()
print(Trial.interpolate_next(Direct_Sample, 3)) 