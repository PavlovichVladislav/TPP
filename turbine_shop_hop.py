from matplotlib import pyplot as plt

hop1 = [{'interval': [30, 80], 'tangent': 2.0296}, {'interval': [80, 104.21662468513853], 'tangent': 2.2795454545454534}]
hop2 = [{'interval': [53.2640470069776, 85.5], 'tangent': 1.8676258992805754}, {'interval': [85.5, 97.58333333333333], 'tangent': 2.4413793103448307}]
hop3 = [{'interval': [63.852132049518566, 79.5], 'tangent': 1.8027777777777776}, {'interval': [79.5, 86.7906976744186], 'tangent': 2.670526315789481}]
hop4 = [{'interval': [30, 60], 'tangent': 1.7306666666666664}, {'interval': [60, 96.01481481481483], 'tangent': 2.012941176470589}]

def plot_hop(data):
    # инициализируем массивы для x и y
    x_values = []
    y_values = []

    # перебираем все словари из входных данных
    # по сути берём интервалы и их значения тангенсов
    # -----------------------------------------------
    # по сути чтобы построить график нужно одинаковое кол-во x и y
    # т.к. это координаты
    # в цикле мы кладём в x начало и конец интервала
    # а в y кладём соотвтетсвующих два значения тангенса для начала и конца интервала
    for entry in data:
        interval = entry['interval']
        tangent = entry['tangent']
        x_values.extend(interval)
        y_values.extend([tangent, tangent])

    plt.plot(x_values, y_values, marker='o')
    plt.xlabel('N, мвт')
    plt.ylabel('Гкал / мвт/ч')
    plt.title('хоп турбины')
    plt.show()

def process_turbines(turbines_hop):
    # Combine all dictionaries into one array
    temp_arr = []
    for turbine in turbines_hop:
        temp_arr.extend(turbine)

    # Sort temp_arr by 'tangent' in descending order
    temp_arr.sort(key=lambda x: x['tangent'], reverse=False)

    result_arr = [temp_arr[0]]  # Initialize result_arr with the first element of temp_arr

    # Iterate over temp_arr starting from the second element
    for i in range(1, len(temp_arr)):
        if temp_arr[i] == temp_arr[i - 1]:
            # If the current dictionary is equal to the previous one,
            # extend the interval of the previous dictionary
            result_arr[-1]['interval'][1] += temp_arr[i]['interval'][1] - temp_arr[i]['interval'][0]
        else:
            # Otherwise, create a new dictionary and append it to result_arr
            new_interval = [
                result_arr[-1]['interval'][1],
                result_arr[-1]['interval'][1] + (temp_arr[i]['interval'][1] - temp_arr[i]['interval'][0])
            ]
            result_arr.append({'interval': new_interval, 'tangent': temp_arr[i]['tangent']})

    return result_arr

hops = process_turbines([hop1, hop2, hop3, hop4])
print(hops)
plot_hop(hops)