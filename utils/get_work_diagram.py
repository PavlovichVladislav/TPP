def get_work_diagram(turbine_mark):
    contour = []
    lines = []

    if (turbine_mark == 'ПТ-80/100-130/13'):
        # contour = [(110, 470), (78.5, 470), (72, 444), (50, 296), (37.5, 226), (30, 174), (30, 132), (60, 220), (94, 336)]
        contour = [(110, 277.3), (78.5, 277.3), (72, 261.96), (50, 174.64), (37.5, 133.34), (30, 102.66), (30, 77.88),
                   (60, 129.8), (94, 198.24)]

        # lines = [
        #     {'collection_point': 150, 'start': (72, 444), 'points': [], 'end': (78.5, 470)},
        #     {'collection_point': 120, 'start': (61.5, 372), 'points': [(79.5, 427)], 'end': (89, 470)},
        #     {'collection_point': 90, 'start': (50.75, 300), 'points': [(85.5, 410)], 'end': (100, 470)},
        #     {'collection_point': 60, 'start': (37.5, 228), 'points': [(77, 346), (100, 426)],
        #      'end': (108.5, 470)},
        #     {'collection_point': 30, 'start': (30, 166), 'points': [(80, 318)], 'end': (102, 403)},
        #     {'collection_point': 0, 'start': (30, 132), 'points': [(60, 220)], 'end': (94, 336)}
        # ]

        lines = [
            {'collection_point': 150, 'start': (72, 261.96), 'end': (78.5, 277.3), 'points': []},
            {'collection_point': 120, 'start': (61.5, 219.48), 'end': (89, 277.3), 'points': [(79.5, 251.93)]},
            {'collection_point': 90, 'start': (50.75, 177.0), 'end': (100, 277.3), 'points': [(85.5, 241.9)]},
            {'collection_point': 60, 'start': (37.5, 134.52), 'end': (108.5, 277.3),
             'points': [(77, 204.14), (100, 251.34)]},
            {'collection_point': 30, 'start': (30, 97.94), 'end': (102, 237.77), 'points': [(80, 187.62)]},
            {'collection_point': 0, 'start': (30, 77.88), 'end': (94, 198.24), 'points': [(60, 129.8)]}
        ]

    if (turbine_mark == 'Т-20-90'):
        # contour = [(18.3, 170), (24.9, 170), (21.5, 133), (5, 44), (5, 65), (7.3, 83), (8.93, 94)]
        contour = [(18.3, 100.3), (24.9, 100.3), (21.5, 78.47), (5, 25.96), (5, 38.35), (7.3, 48.97), (8.93, 55.46)]

        # lines = [
        #     {'collection_point': 100, 'start': (15.9, 149), 'points': [], 'end': (19.3, 170)},
        #     {'collection_point': 90, 'start': (13.9, 134), 'points': [], 'end': (20.2, 170)},
        #     {'collection_point': 80, 'start': (11.8, 117), 'points': [], 'end': (21, 170)},
        #     {'collection_point': 70, 'start': (9.8, 102), 'points': [], 'end': (21.8, 170)},
        #     {'collection_point': 60, 'start': (7.7, 86), 'points': [], 'end': (22.7, 170)},
        #     {'collection_point': 50, 'start': (5.7, 70), 'points': [], 'end': (23.5, 170)},
        #     {'collection_point': 40, 'start': (5, 61.5), 'points': [], 'end': (24.3, 170)},
        #     {'collection_point': 30, 'start': (5, 57), 'points': [], 'end': (24.5, 164)},
        #     {'collection_point': 20, 'start': (5, 52.5), 'points': [], 'end': (23.6, 154)},
        #     {'collection_point': 10, 'start': (5, 49), 'points': [], 'end': (22.6, 144)},
        #     {'collection_point': 0, 'start': (5, 44), 'points': [], 'end': (21.5, 133)}
        # ]
        lines = [{'collection_point': 100, 'start': (15.9, 87.91), 'end': (19.3, 100.3), 'points': []},
                 {'collection_point': 90, 'start': (13.9, 79.06), 'end': (20.2, 100.3), 'points': []},
                 {'collection_point': 80, 'start': (11.8, 69.03), 'end': (21, 100.3), 'points': []},
                 {'collection_point': 70, 'start': (9.8, 60.18), 'end': (21.8, 100.3), 'points': []},
                 {'collection_point': 60, 'start': (7.7, 50.74), 'end': (22.7, 100.3), 'points': []},
                 {'collection_point': 50, 'start': (5.7, 41.3), 'end': (23.5, 100.3), 'points': []},
                 {'collection_point': 40, 'start': (5, 36.285), 'end': (24.3, 100.3), 'points': []},
                 {'collection_point': 30, 'start': (5, 33.63), 'end': (24.5, 96.76), 'points': []},
                 {'collection_point': 20, 'start': (5, 30.975), 'end': (23.6, 90.86), 'points': []},
                 {'collection_point': 10, 'start': (5, 28.91), 'end': (22.6, 84.96), 'points': []},
                 {'collection_point': 0, 'start': (5, 25.96), 'end': (21.5, 78.47), 'points': []}]

    if (turbine_mark == 'ПТ-65/75-130/13'):
        # contour = [(110, 470), (78.5, 470), (72, 444), (50, 296), (37.5, 226), (30, 174), (30, 132), (60, 220), (94, 336)]
        contour = [(110, 277.3), (78.5, 277.3), (72, 261.96), (50, 174.64), (37.5, 133.34), (30, 102.66), (30, 77.88),
                   (60, 129.8), (94, 198.24)]

        # lines = [
        #     {'collection_point': 150, 'start': (72, 444), 'points': [], 'end': (78.5, 470)},
        #     {'collection_point': 120, 'start': (61.5, 372), 'points': [(79.5, 427)], 'end': (89, 470)},
        #     {'collection_point': 90, 'start': (50.75, 300), 'points': [(85.5, 410)], 'end': (100, 470)},
        #     {'collection_point': 60, 'start': (37.5, 228), 'points': [(77, 346), (100, 426)],
        #      'end': (108.5, 470)},
        #     {'collection_point': 30, 'start': (30, 166), 'points': [(80, 318)], 'end': (102, 403)},
        #     {'collection_point': 0, 'start': (30, 132), 'points': [(60, 220)], 'end': (94, 336)}
        # ]

        lines = [
            {'collection_point': 150, 'start': (72, 261.96), 'end': (78.5, 277.3), 'points': []},
            {'collection_point': 120, 'start': (61.5, 219.48), 'end': (89, 277.3), 'points': [(79.5, 251.93)]},
            {'collection_point': 90, 'start': (50.75, 177.0), 'end': (100, 277.3), 'points': [(85.5, 241.9)]},
            {'collection_point': 60, 'start': (37.5, 134.52), 'end': (108.5, 277.3),
             'points': [(77, 204.14), (100, 251.34)]},
            {'collection_point': 30, 'start': (30, 97.94), 'end': (102, 237.77), 'points': [(80, 187.62)]},
            {'collection_point': 0, 'start': (30, 77.88), 'end': (94, 198.24), 'points': [(60, 129.8)]}
        ]

    return contour, lines