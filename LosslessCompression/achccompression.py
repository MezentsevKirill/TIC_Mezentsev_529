import collections
import math
import matplotlib.pyplot as plt


original_sequences = []
sequences_list = []
N_sequence = 10


def main():
    f = open('results_AC_CH.txt', 'w')
    f.close()
    global original_sequences
    results = []
    with open("sequence.txt", "r", encoding="UTF-8") as file:
        for i in range(8):
            original_sequence = file.readline()[27:]
            original_sequences.append(original_sequence)
        original_sequences = [line.rstrip() for line in original_sequences]
    number = 0

    for sequence in original_sequences:
        number += 1
        sequence = sequence[:10]
        sequence_length = len(sequence)
        unique_chars = set(sequence)
        sequence_alphabet_size = len(unique_chars)
        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probability.values())

        encoded_data_ac, encoded_sequence_ac = encode_ac(unique_chars, probability, sequence_alphabet_size, sequence)
        bps_ac = len(encoded_sequence_ac) / sequence_length

        decoded_sequence = decode_ac(encoded_data_ac, sequence_length)

        encoded_data_ch, encoded_sequence_ch = encode_ch(unique_chars, probability, sequence)
        bps_ch = len(encoded_sequence_ch) / sequence_length

        decoded_sequence_2 = decode_ch(encoded_data_ch)

        with open("results_AC_CH.txt", "a", encoding="UTF-8") as file:
            print("//////////////////////////////////////////////////////////", file=file)
            print("Оригінальна послідовність №" + str(number) + ": ", sequence, file=file)
            print("Ентропія: ", entropy, "\n", file=file)
            print("_________Арифметичне кодування_________", file=file)
            print("Дані закодованої АС послідовності: ", encoded_data_ac, file=file)
            print("Закодована АС послідовність: ", encoded_sequence_ac, file=file)
            print("Значення bps при кодуванні АС: ", bps_ac, file=file)
            print("Декодована АС послідовність: ", decoded_sequence, "\n", file=file)
            print("_________Кодування Хаффмана_________", file=file)
            print("Алфавіт    Код символу", file=file)
            for i in encoded_data_ch[1]:
                print("  ", i[0], "      ", i[1], file=file)
            print("Дані закодованої HС послідовності: ", encoded_data_ch, file=file)
            print("Закодована HС послідовність: ", encoded_sequence_ch, file=file)
            print("Значення bps при кодуванні HС: ", bps_ch, file=file)
            print("Декодована HС послідовність: ", decoded_sequence_2, "\n", file=file)
        results.append([round(entropy, 2), bps_ac, bps_ch])
        fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
        headers = ['Ентропія', 'bps AC', 'bps CH']
        row = []
        for j in range(number):
            row.append('Послідовність ' + str(j + 1))
        ax.axis('off')
        table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
        table.set_fontsize(14)
        table.scale(0.8, 2)
        fig.savefig("Результати стиснення методами AC та CH")


def float_bin(point, size_cod):
    binary_code = ''
    for x in range(size_cod):
        point = point * 2
        if point > 1:
            binary_code += str(1)
            x = int(point)
            point = point - x
        elif point < 1:
            binary_code += str(0)
        elif point == 1:
            binary_code += str(1)
            break
    return binary_code


def encode_ac(uniq_chars, probabilitys, alphabet_size, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]
    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range = probability_range + probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])
    for i in range(len(sequence) - 1):
        for j in range(len(unity)):
            if sequence[i] == unity[j][0]:
                probability_low = unity[j][1]
                probability_high = unity[j][2]
                diff = probability_high - probability_low
                for k in range(len(unity)):
                    unity[k][1] = probability_low
                    unity[k][2] = probability[k] * diff + probability_low
                    probability_low = unity[k][2]
    low = 0
    high = 0
    for i in range(len(unity)):
        if unity[i][0] == sequence[-1]:
            low = unity[i][1]
            high = unity[i][2]
    point = (low + high) / 2
    size_cod = math.ceil(math.log((1 / (high - low)), 2) + 1)
    bin_code = float_bin(point, size_cod)
    return [point, alphabet_size, alphabet, probability], bin_code


def decode_ac(encoded_data_ac, sequence_length):
    point = encoded_data_ac[0]
    alphabet_size = encoded_data_ac[1]
    alphabet = encoded_data_ac[2]
    probability = encoded_data_ac[3]
    unity = []
    probability_range = 0.0
    for i in range(alphabet_size):
        l = probability_range
        probability_range = probability_range + probability[i]
        u = probability_range
        unity.append([alphabet[i], l, u])
    decoded_sequence = ""
    for i in range(sequence_length):
        for j in range(len(unity)):
            if point > unity[j][1] and point < unity[j][2]:
                prob_low = unity[j][1]
                prob_high = unity[j][2]
                diff = prob_high - prob_low
                decoded_sequence = decoded_sequence + unity[j][0]
                for k in range(len(unity)):
                    unity[k][1] = prob_low
                    unity[k][2] = probability[k] * diff + prob_low
                    prob_low = unity[k][2]
                break
    return decoded_sequence


def encode_ch(uniq_chars, probabilitys, sequence):
    alphabet = list(uniq_chars)
    probability = [probabilitys[symbol] for symbol in alphabet]
    final = []
    for i in range(len(alphabet)):
        final.append([alphabet[i], probability[i]])
    final.sort(key=lambda x: x[1])
    tot = 0
    tree = []
    if 1 in probability and len(set(probability)) == 1:
        symbol_code = []
        for i in range(len(alphabet)):
            code = "1" * i + "0"
            symbol_code.append([alphabet[i], code])
        encode = "".join([symbol_code[alphabet.index(c)][1] for c in sequence])
    else:
        for i in range(len(final) - 1):
            i = 0
            left = final[i]
            final.pop(i)
            right = final[i]
            final.pop(i)
            tot += left[1] + right[1]
            tree.append([left[0], right[0]])
            final.append([left[0] + right[0], tot])
            final.sort(key=lambda x: x[1])
        symbol_code = []
        tree.reverse()
        alphabet.sort()
        for i in range(len(alphabet)):
            code = ""
            for j in range(len(tree)):
                if alphabet[i] in tree[j][0]:
                    code = code + '0'
                    if alphabet[i] == tree[j][0]:
                        break
                else:
                    code = code + '1'
                if alphabet[i] == tree[j][1]:
                    break
            symbol_code.append([alphabet[i], code])
        encode = ""
        for c in sequence:
            encode += [symbol_code[i][1] for i in range(len(alphabet)) if symbol_code[i][0] == c][0]
    return [encode, symbol_code], encode


def decode_ch(encoded_sequence):
    encode = list(encoded_sequence[0])
    symbol_code = encoded_sequence[1]
    sequence = ""
    count = 0
    flag = 0
    for i in range(len(encode)):
        for j in range(len(symbol_code)):
            if encode[i] == symbol_code[j][1]:
                sequence = sequence + str(symbol_code[j][0])
                flag = 1
        if flag == 1:
            flag = 0
        else:
            count = count + 1
            if count == len(encode):
                break
            else:
                encode.insert(i + 1, str(encode[i] + encode[i + 1]))
                encode.pop(i + 2)
    return sequence


if __name__ == '__main__':
    main()
