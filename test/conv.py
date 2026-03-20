def dec_to_bin(dec):
    decimal = dec
    binary = []
    for i in range(len(str(abs(decimal)))):
        x = decimal / 2 ** i
        if x.is_integer():
            binary.append(1)
            decimal /= 2 ** i
        else:
            binary.append(0)
            decimal /= 2 ** i


    return binary


def bin_to_dec(bin):
    decimal = 0

    bin2 = bin[::-1]

    for i in range(len(bin2)):
        if bin2[i] == 1 or bin2[i] == True:
            decimal += 2 ** i
    return decimal



print(dec_to_bin(2000))
