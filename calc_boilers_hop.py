# Здесь уже присутствуют исходные данные и формулы расчётов, т.е.
# по сути можно сделать БД с расчитанными ХОП для котлов
# А также возможность добавлять новые

# Исходные данные для ХОП тп-170
tp170data = {
    'load': [75, 77.5, 80, 85, 89.4, 90, 95, 100, 101.4],
    'efficiency': [87.3, 87.5, 87.65, 87.85, 87.96, 87.97, 88.03, 88.05, 88.06]
}

# Функция для определния исходнных данных для расчёта ХОП
# потом будет сетевой запрос к БД
def getInputData(boiler_mark):
    if boiler_mark == 'ТП-170':
        return tp170data

# 1. Расчёт потерь тепла
# Qпот = Qi * ( (100 - Ni) / Ni )
# Где Qi - значение нагрузки из исходных данных
# Ni - значение КПД из исходных данных
def calc_heat_loss(input_data):
    # Кол-во значений нагрузки и кпд должно совпадать
    if len(input_data['load']) != len(input_data['efficiency']):
        raise ValueError("Load and efficiency len are not equal!")

    # Потери тепла
    heat_loss = []

    # Проходимся по массиву load
    for i in range(len(input_data['load'])):
        # Рассчитываем потери тепла и добавляем в heatLoss
        heat_loss_value = (input_data['load'][i] *
                           ((100 - input_data['efficiency'][i]) / input_data['efficiency'][i]))
        heat_loss.append(heat_loss_value)

    return heat_loss

# 2. Вычисление средних значений нагрузок
# Qср = (Qi + Qi+1)/2
def calc_average_load_values(load_values):
    average_load_values = []

    for i in range(len(load_values) - 1):
        average_load = (load_values[i] + load_values[i+1]) / 2
        average_load_values.append(average_load)

    return average_load_values

# 3. Вычисление абсолютных приростов потерь
# deltaQпот = Qпот(i+1) - Qпот(i)
def calc_absolute_increases_losses(heat_loss):
    absolute_increases_losses = []

    for i in range(len(heat_loss) - 1):
        abs_increases_losses_value = heat_loss[i+1] - heat_loss[i]
        absolute_increases_losses.append(abs_increases_losses_value)

    return absolute_increases_losses

# 4. Расчёт относительного прироста потерь
# Qпот.отн = deltaQпот(i) / (Q(i+1) - Q(i))
def calc_relative_increase_losses(absolute_increases_losses, load):
    relative_increase_losses = []

    for i in range(len(absolute_increases_losses)):
        rel_increases_losses_value = absolute_increases_losses[i] / (load[i+1] - load[i])
        relative_increase_losses.append(rel_increases_losses_value)

    return relative_increase_losses

# 5. Расчёт ОПРТ котла
def calc_hop(relative_increase_losses):
    hop = []

    for i in range(len(relative_increase_losses)):
        hop_value = (1 + relative_increase_losses[i]) * 0.143
        hop.append(hop_value)

    return hop

def calc_boiler_hop(boiler_mark):
    # Получение исходных данных по марке котла
    inputData = getInputData(boiler_mark)
    # расчёт потерь тепла Qпот
    heat_loss = calc_heat_loss(inputData)
    # Средние значения нагрузок Qср
    average_load_values = calc_average_load_values(inputData['load'])
    # Абсолютный прирост потерь
    absolute_increases_losses = calc_absolute_increases_losses(heat_loss)
    # Относительный приорст потерь
    relative_increase_losses = calc_relative_increase_losses(absolute_increases_losses, inputData['load'])
    # Результирующий ОПРТ
    hop = calc_hop(relative_increase_losses)
