import collections
import math
import matplotlib.pyplot as plt


N_sequence = 100
original_sequences = []
ZLW_result = []


def write_to_file(number, sequence, original_sequence_size, entropy, encoded_sequence, encoded_sequence_size, cr,
                  decoded_sequence, decoded_sequence_size):
    with open("results_rle_lzw.txt", "a", encoding="UTF-8") as file_1:
        print("Оригінальна послідовність №" + str(number) + ": ", sequence, file=file_1)
        print("Розмір оригінальної послідовності: ", original_sequence_size, " bits", file=file_1)
        print("Ентропія: ", entropy, "\n", file=file_1)
        print("__________Кодування_RLE__________", file=file_1)
        print("Закодована RLE послідовність: ", encoded_sequence, file=file_1)
        print("Розмір закодованої RLE послідовності: ", encoded_sequence_size, " bits", file=file_1)
        print("Коефіцієнт стиснення RLE: ", cr, file=file_1)
        print("Декодована RLE послідовність: ", decoded_sequence, file=file_1)
        print("Розмір декодованої RLE послідовності: ", decoded_sequence_size, " bits", "\n", file=file_1)
        print("__________Кодування_LZW__________", file=file_1)
        print("_____________Словник_____________", file=file_1)


def counter(sequence):
    counts = collections.Counter(sequence)
    return counts


def calc_probability(counts):
    probability = {symbol: count / N_sequence for symbol, count in counts.items()}
    return probability


def calc_entropy(probability):
    entropy = -sum(p * math.log2(p) for p in probability.values())
    return entropy


def size(sequence):
    original_sequence_size = len(sequence) * 16
    return original_sequence_size


def encode_rle(sequence):
    count = 1
    result = []
    for j, item in enumerate(sequence):
        if j == 0:
            continue
        elif item == sequence[j - 1]:
            count += 1
        else:
            result.append((sequence[j - 1], count))
            count = 1
    result.append((sequence[len(sequence) - 1], count))
    encoded = []
    for j, item in enumerate(result):
        encoded.append(f"{item[1]}{item[0]}")
    return "".join(encoded), result


def decode_rle(sequence):
    result = []
    for item in sequence:
        result.append(item[0] * item[1])
    return "".join(result)


def encode_zlw(sequence, result_list, k):
    dictionary = {}
    result = []
    total_size = 0
    for j in range(65536):
        dictionary[chr(j)] = j
    current = ""
    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])
            dictionary[new_str] = len(dictionary)
            element_bits = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
            with open("results_rle_lzw.txt", "a", encoding="UTF-8") as file_2:
                print("Code: ", dictionary[current], " Element: ", current, " bits: ", element_bits, file=file_2)
            current = c
            total_size += element_bits
    last = 16 if dictionary[current] < 65536 else math.ceil(math.log2(len(dictionary)))
    total_size += last
    compression_ratio_lzw = round(len(sequence) * 16 / total_size, 2)
    if compression_ratio_lzw < 1:
        compression_ratio_lzw = '-'
    else:
        compression_ratio_lzw = compression_ratio_lzw
    with open("results_rle_lzw.txt", "a", encoding="UTF-8") as file_2:
        print("Code: ", dictionary[current], " Element: ", current, " Bits: ", last, "\n", file=file_2)
        result.append(dictionary[current])
        print("_________________________________", file=file_2)
        print("Закодована LZW послідовність: ", ''.join(map(str, result)), file=file_2)
        print("Розмір закодованої LZW послідовності: ", total_size, " bits", file=file_2)
        print("Коефіцієнт стиснення LZW: ", compression_ratio_lzw, file=file_2)
        ZLW_result.append(result)
        result_list[k].append(compression_ratio_lzw)


def decode_zlw(sequence):
    dictionary = {}
    result = ""
    previous = None
    for j in range(65536):
        dictionary[j] = chr(j)
    for code in sequence:
        if code in dictionary:
            current = dictionary[code]
            result += current
            if previous is not None:
                dictionary[len(dictionary)] = previous + current[0]
            previous = current
        else:
            current = previous + previous[0]
            result += current
            dictionary[len(dictionary)] = current
            previous = current
    return result


def create_table(results):
    n = 8
    fig, ax = plt.subplots(figsize=(14 / 1.54, n / 1.54))
    headers = ['Ентропія', 'КС RLE', 'КС LZW']
    row = []
    for j in range(n):
        row.append('Послідовність ' + str(j + 1))
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row,
                     loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig("Результати стиснення методами RLE та LZW")


with open("sequence.txt", "r", encoding="UTF-8") as file:
    for i in range(8):
        original_sequence = file.readline()[27:]
        original_sequences.append(original_sequence)
    original_sequences = [line.rstrip() for line in original_sequences]


def main():
    result = []
    f = open('results_rle_lzw.txt', 'w')
    f.close()
    for j in range(8):
        encoded_sequence, encoded = encode_rle(original_sequences[j])
        compression_ratio_rle = round((len(original_sequences[j]) / len(encoded_sequence)), 2)
        if compression_ratio_rle < 1:
            compression_ratio_rle = '-'
        else:
            compression_ratio_rle = compression_ratio_rle
        write_to_file(j + 1, original_sequences[j], size(original_sequences[j]),
                      calc_entropy(calc_probability(counter(original_sequences[j]))),  encoded_sequence,
                      size(encoded_sequence), compression_ratio_rle, decode_rle(encoded),
                      size(decode_rle(encoded)))
        entropy = calc_entropy(calc_probability(counter(original_sequences[j])))
        result.append([round(entropy, 2), compression_ratio_rle])
        encode_zlw(original_sequences[j], result, j)
        with open("results_rle_lzw.txt", "a", encoding="UTF-8") as file_2:
            print(f"Декодована LZW послідовність:{decode_zlw(ZLW_result[j])} \n"
                  f"Розмір декодованої LZW послідовності: {len(decode_zlw(ZLW_result[j])) * 16} bits \n\n",
                  file=file_2)
    create_table(result)


main()
