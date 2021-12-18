DIGIT_SIZE = 12


def main1() -> int:
    summary = [{0: 0, 1: 1} for _ in range(DIGIT_SIZE)]
    try:
        while value := input():
            for i, bit in enumerate(value):
                summary[i][int(bit)] += 1
    except EOFError:
        pass

    epsilon = ""
    gamma = ""
    for bit_counter in summary:
        if bit_counter[0] > bit_counter[1]:
            epsilon += "1"
            gamma += "0"
        else:
            epsilon += "0"
            gamma += "1"
    return int(gamma, 2) * int(epsilon, 2)


def main2() -> int:
    values = []
    try:
        while value := input():
            values.append(value)
    except EOFError:
        pass

    nb_bits = len(values[0])
    co2_filtered_values = values[:]
    o2_filtered_values = values[:]
    o2_result, co2_result = "", ""

    for position in range(nb_bits):
        nb_0, nb_1 = 0, 0
        for value in o2_filtered_values:
            if value[position] == "0":
                nb_0 += 1
            else:
                nb_1 += 1
        o2_filtered_values = [
            value
            for value in o2_filtered_values
            if value[position] == ("1" if nb_1 >= nb_0 else "0")
        ]
        if len(o2_filtered_values) == 1:
            o2_result = o2_filtered_values.pop()
            break

    for position in range(nb_bits):
        nb_0, nb_1 = 0, 0
        for value in co2_filtered_values:
            if value[position] == "0":
                nb_0 += 1
            else:
                nb_1 += 1
        co2_filtered_values = [
            value
            for value in co2_filtered_values
            if value[position] == ("0" if nb_0 <= nb_1 else "1")
        ]
        if len(co2_filtered_values) == 1:
            co2_result = co2_filtered_values.pop()
            break
    return int(o2_result, 2) * int(co2_result, 2)
