import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import cascaded_union

def plot_polygon(polygon, ax, color='black'):
    x, y = polygon.exterior.xy
    ax.plot(x, y, color)

def plot_line(line, ax, color='r'):
    x, y = line.xy
    ax.plot(x, y, color)

def is_point_inside_polygon(point, polygon):
    return polygon.contains(Point(point))

def is_line_inside_polygon(line, polygon):
    return polygon.contains(line)

# Ограничивающий контур
boundary_points = [(105, 470), (78.5, 470), (72, 444), (50, 296), (37.5, 226), (30, 174), (30, 132), (60, 220), (94, 336)]
boundary_polygon = Polygon(boundary_points)

# Ломаные внутри контура
lines = [
    {'start': (61.5, 372), 'points': [(79.5, 427)], 'end': (89, 470)},
    {'start': (30, 146), 'points': [(80, 318)], 'end': (99, 403)}
]

# Построение ограничивающего контура
fig, ax = plt.subplots()
plot_polygon(boundary_polygon, ax)

# Построение ломаных внутри контура
for line_data in lines:
    line_points = [line_data['start']] + line_data['points'] + [line_data['end']]
    line = LineString(line_points)

    for point in line_data['points']:
        plt.scatter(point[0], point[1], color='green', marker='o')

    # Проверка, что ломаная не выходит за границы контура
    if is_line_inside_polygon(line, boundary_polygon):
        plot_line(line, ax)

plt.axis('equal')
plt.gca().set_aspect(0.25)
plt.show()