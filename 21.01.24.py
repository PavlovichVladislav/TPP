import matplotlib.pyplot as plt
import numpy as np


def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def find_nearest_line(lines, entrance_collection_point):
    min_distance = float('inf')
    found_line = None

    for line in lines:
        collection_point = line['collection_point']
        dist = abs(collection_point - entrance_collection_point)

        if dist < min_distance:
            min_distance = dist
            found_line = line

    return found_line, min_distance


def intersect_with_contour(line, contour):
    start, end = line['start'], line['end']
    points = [start] + line['points'] + [end]

    # Find intersection with contour for the start and end points
    start_intersection = min(contour, key=lambda point: distance(point, start))
    end_intersection = min(contour, key=lambda point: distance(point, end))

    return start_intersection, end_intersection


def create_new_line(found_line, entrance_collection_point, dist):
    new_line = {
        'start': np.add(found_line['start'], dist),
        'points': [np.add(point, dist) for point in found_line['points']],
        'end': np.add(found_line['end'], dist)
    }
    return new_line


def adjust_line_to_contour(new_line, contour):
    start_intersection, end_intersection = intersect_with_contour(new_line, contour)
    new_line['start'] = start_intersection
    new_line['end'] = end_intersection

    return new_line


def plot_lines(lines, contour):
    plt.plot(*zip(*contour + [contour[0]]), marker='o', label='Contour')

    for line in lines:
        plt.plot(*zip(line['start'], *line['points'], line['end']), marker='o',)

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


def main():
    contour = [(105, 470), (78.5, 470), (72, 444), (50, 296), (37.5, 226), (30, 174), (30, 132), (60, 220), (94, 336)]

    lines = [
        {'collection_point': 120, 'start': (61.5, 372), 'points': [(79.5, 427)], 'end': (89, 470)},
        {'collection_point': 30, 'start': (30, 146), 'points': [(80, 318)], 'end': (99, 403)}
    ]

    entrance_collection_point = int(input('Введите entrance_collection_point: '))

    found_line, dist = find_nearest_line(lines, entrance_collection_point)
    print(found_line, dist)
    new_line = create_new_line(found_line, entrance_collection_point, dist)
    new_line = adjust_line_to_contour(new_line, contour)

    lines.append(new_line)
    plot_lines(lines, contour)


if __name__ == "__main__":
    main()