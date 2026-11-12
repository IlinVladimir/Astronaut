def number_to_dac(number):
    return [int(element) for element in bin(number)[2:].zfill(8)]

print(number_to_dac(1))