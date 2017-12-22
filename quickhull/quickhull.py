class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to_line(self, line):
        return (line.begin.x - self.x) * (line.end.y - self.y) - \
               (line.end.x - self.x) * (line.begin.y - self.y)

    def is_right(self, line):
        return self.distance_to_line(line) < 0

    def __str__(self):
        return '{ ' + str(self.x) + ', ' + str(self.y) + ' }'

    @staticmethod
    def is_clockwise_order(a, b, c):
        return a.x * (b.y - c.y) + \
            b.x * (c.y - a.y) + \
            c.x * (a.y - b.y) < 0


class Line:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end


class QuickHull:

    def __init__(self, points, handler=None):
        self.points = points
        self.hull_size = 0
        self.handler = handler

    def _add_point_to_hull(self, point_index):
        self.points[point_index], self.points[self.hull_size] = \
            self.points[self.hull_size], self.points[point_index]
        if self.hull_size != 0:
            self._add_to_hull(self.points[self.hull_size - 1], self.points[self.hull_size])
        self.hull_size += 1
        return self.hull_size - 1

    def _find_lowest_point(self):
        lowest = 0
        for i in range(1, len(self.points)):
            distance_x = self.points[i].x - self.points[lowest].x
            distance_y = self.points[i].y - self.points[lowest].y
            if distance_y < 0 or distance_y == 0 and distance_x < 0:
                lowest = i
        return lowest

    def _find_furthest_point(self, begin, end, line):
        furthest_point_index = begin
        max_distance = 0
        for i in range(begin, end + 1):
            current_distance = -self.points[i].distance_to_line(line)
            if current_distance > max_distance or \
                    current_distance == max_distance and \
                    self.points[i].x > self.points[furthest_point_index].y:
                furthest_point_index = i
                max_distance = current_distance
        return furthest_point_index

    def _find_nearest_point(self, point):
        nearest_point_index = 1
        for i in range(2, len(self.points)):
            if not Point.is_clockwise_order(self.points[point],
                                            self.points[nearest_point_index],
                                            self.points[i]):
                nearest_point_index = i
        return nearest_point_index

    def _split(self, begin, end, line):
        while begin <= end:
            while begin <= end and self.points[begin].is_right(line):
                begin += 1
            while begin <= end and not self.points[end].is_right(line):
                end -= 1
            if begin <= end:
                self.points[begin], self.points[end] = \
                    self.points[end], self.points[begin]
                begin += 1
                end -= 1
        return begin

    def _add_to_hull(self, begin, end):
        if self.handler:
            self.handler.add_to_hull(begin, end)

    def _add_line(self, start, finish, comment):
        if self.handler:
            self.handler.add_line(start, finish, comment)

    def _remove_line(self, start, finish, comment):
        if self.handler:
            self.handler.remove_line(start, finish, comment)

    def _select_points(self, begin, end, comment):
        if self.handler:
            self.handler.select_points(self.points[begin:end+1], comment)

    def _deselect_points(self):
        if self.handler:
            self.handler.deselect_points()

    def _calculate(self, begin, end, line):
        if begin > end:
            return
        self._select_points(begin, end, "Selecting points range")
        self._add_line(line.begin, line.end, "Split into two parts (depending on line).")
        furthest_point_index = self._find_furthest_point(begin, end, line)
        first_line = Line(line.begin, self.points[furthest_point_index])
        second_line = Line(self.points[furthest_point_index], line.end)
        self._add_line(first_line.begin, first_line.end, "Find furthest point and draw new two lines.")
        self._add_line(second_line.begin, second_line.end, "Find furthest point and draw new two lines.")
        self._remove_line(line.begin, line.end, "Split into two parts (depending on line).")
        self._deselect_points()

        self.points[furthest_point_index], self.points[end] = \
            self.points[end], self.points[furthest_point_index]

        partition = self._split(begin, end - 1, first_line)
        self._calculate(begin, partition - 1, first_line)
        self._remove_line(first_line.begin, first_line.end, "")

        self.points[end], self.points[partition] = \
            self.points[partition], self.points[end]
        self._add_point_to_hull(partition)

        second_partition = self._split(partition + 1, end, second_line)
        self._calculate(partition + 1, second_partition - 1, second_line)
        self._remove_line(second_line.begin, second_line.end, "")

    def calculate(self):
        length = len(self.points)
        if length < 3:
            self.hull_size = length
            return
        lowest = self._find_lowest_point()
        lowest = self._add_point_to_hull(lowest)
        nearest = self._find_nearest_point(lowest)
        self._add_to_hull(self.points[lowest], self.points[nearest])
        self.points[nearest], self.points[length - 1] = \
            self.points[length - 1], self.points[nearest]
        self._calculate(1, length - 2, Line(
            self.points[lowest], self.points[length - 1]))
        self._add_point_to_hull(length - 1)


def _test():
    input = open('input.txt', 'r')
    output = open('output.txt', 'w')

    n = int(input.readline())
    points = []
    for i in range(n):
        x, y = map(int, input.readline().split())
        points.append(Point(x, y))

    q = QuickHull(points)
    q.calculate()

    output.writelines(str(q.hull_size) + '\n')
    for i in range(q.hull_size):
        output.writelines(str(int(q.points[i].x)) + ' ' +
                          str(int(q.points[i].y)) + '\n')

    input.close()
    output.close()

# _test()

