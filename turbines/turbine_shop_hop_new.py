from turbines.turbine_hop_new import calc_turbine_hop

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

# Расчёт ХОП турбинного цеха
def calc_turbines_shop_hop(turbines):
    turbines_hops = []
    flow_chars = []

    for turbine in turbines:
        print(turbine)
        turbine_hop = calc_turbine_hop(turbine['type'], turbine['steam_consuption'])
        turbines_hops.append(turbine_hop['hop'])
        flow_chars.append({'mark': turbine_hop['mark'], 'flow_char': turbine_hop['flow_char']})

    turbine_shop_hop = process_turbines(turbines_hops)

    return flow_chars, turbine_shop_hop

