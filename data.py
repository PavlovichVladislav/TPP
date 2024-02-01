import math


def distance_to_line(point, line_points):
    x0, y0 = point
    x1, y1 = line_points[0]
    x2, y2 = line_points[1]

    # Вычисляем коэффициенты A, B, C для уравнения прямой Ax + By + C = 0
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    print(A, B, C)

    # Вычисляем расстояние от точки до прямой
    distance = abs(A * x0 + B * y0 + C) / math.sqrt(A**2 + B**2)

    return distance


def find_min_distance_to_polyline(target_point, polyline):
    start_point = polyline['start']
    end_point = polyline['end']
    polyline_points = [start_point] + polyline.get('points', []) + [end_point]

    min_distance = float('inf')

    for i in range(len(polyline_points) - 1):
        line_start = polyline_points[i]
        line_end = polyline_points[i + 1]
        print(line_start)
        print(line_end)

        distance = distance_to_line(target_point, [line_start, line_end])
        print(distance)
        print('------')
        min_distance = min(min_distance, distance)

    return min_distance


# Пример использования
target_point = (94, 336)
polyline = {'start': (30, 146), 'points': [(80, 318)], 'end': (99, 403)}

result = find_min_distance_to_polyline(target_point, polyline)
print(f"Наименьшая длина перпендикуляра: {result}")