import random
import string
import collections
import math
import matplotlib.pyplot as plt


N_sequence = 100
chars_len_list = []
original_sequences = []
probabilities_list = []
probabilities_str_list = []
mean_probabilities_list = []
uniformity_list = []
entropy_list = []
source_excesses = []
results = []


def write_to_file(original_sequence, original_sequence_size, unique_chars, probability, mean_probability, uniformity,
                  entropy, source_excess):
    with open("results_sequence.txt", "w", encoding="UTF-8") as file:
        print("Тестова послідовність №1: ", original_sequence, file=file)
        print("Розмір послідовності: ", original_sequence_size, " byte", file=file)
        print("Розмір алфавіту: ", len(unique_chars), file=file)
        print("Ймовірність появи символів: ", probability, file=file)
        print("Середнє арифметичне ймовірностей: ", mean_probability, file=file)
        print("Ймовірность розподілу символів: ", uniformity, file=file)
        print("Ентропія: ", entropy, file=file)
        print("Надмірність джерела: ", source_excess, "\n", file=file)


def write_to_file2(original_sequence, original_sequence_size, unique_chars, n, probability, mean_probability,
                   uniformity, entropy, source_excess):
    with open("results_sequence.txt", "a", encoding="UTF-8") as file:
        print("Тестова послідовність №" + str(n) + ": ", original_sequence, file=file)
        print("Розмір послідовності: ", original_sequence_size, " byte", file=file)
        print("Розмір алфавіту: ", len(unique_chars), file=file)
        print("Ймовірність появи символів: ", probability, file=file)
        print("Середнє арифметичне ймовірностей: ", mean_probability, file=file)
        print("Ймовірность розподілу символів: ", uniformity, file=file)
        print("Ентропія: ", entropy, file=file)
        print("Надмірність джерела: ", source_excess, "\n", file=file)


def sequence_list(x):
    original_sequences.append(x)


def size(x):
    original_sequence_size = len(x)
    return original_sequence_size


def chars(y):
    unique_chars = set(y)
    chars_len_list.append(len(unique_chars))
    return unique_chars


def test_1(n1):
    list1 = []
    for i in range(n1):
        list1.append(1)
    n0 = N_sequence - n1
    list0 = []
    for j in range(n0):
        list0.append(0)
    list2 = list1 + list0
    random.shuffle(list2)
    original_sequence = "".join(map(str, list2))
    return original_sequence


def test_2(n1):
    list1 = []
    for char in n1:
        list1.append(char)
    n0 = N_sequence - len(n1)
    list0 = []
    for i in range(n0):
        list0.append(0)
    list2 = []
    for j in list1:
        list2.append(j)
    for k in list0:
        list2.append(k)
    original_sequence = "".join(map(str, list2))
    return original_sequence


def test_3(n1):
    list1 = []
    for char in n1:
        list1.append(char)
    n0 = N_sequence - len(n1)
    list0 = []
    for i in range(n0):
        list0.append(0)
    list2 = []
    for j in list1:
        list2.append(j)
    for k in list0:
        list2.append(k)
    random.shuffle(list2)
    original_sequence = "".join(map(str, list2))
    return original_sequence


def test_4(n1, n2):
    letters = []
    for char in n1:
        letters.append(char)
    for i in n2:
        letters.append(i)
    n_letters = len(letters)
    n_repeats = N_sequence // n_letters
    remainder = N_sequence % n_letters
    list0 = letters * n_repeats
    list0 += letters[:remainder]
    original_sequence = ''.join(map(str, list0))
    return original_sequence


def test_5(n1, n2):
    letters = []
    digits = []
    for char in n1:
        letters.append(char)
    for i in n2:
        digits.append(i)
    list_0 = []
    for i in letters:
        for j in range(20):
            list_0.append(i)
    for i in digits:
        for j in range(20):
            list_0.append(i)
    random.shuffle(list_0)
    original_sequence = "".join(map(str, list_0))
    return original_sequence


def test_6(n1, n2):
    letters = []
    digits = []
    for char in n1:
        letters.append(char)
    for i in n2:
        digits.append(i)
    n_letters = int(0.7 * N_sequence)
    n_digits = int(0.3 * N_sequence)
    list_100 = []
    for i in range(n_letters):
        list_100.append(random.choice(letters))
    for j in range(n_digits):
        list_100.append(random.choice(digits))
    random.shuffle(list_100)
    original_sequence = "".join(map(str, list_100))
    return original_sequence


def test_7():
    elements = string.ascii_lowercase + string.digits
    list_100 = [random.choice(elements) for _ in range(N_sequence)]
    original_sequence = "".join(map(str, list_100))
    return original_sequence


def test_8():
    original_sequence = "1" * N_sequence
    return original_sequence


def calculation_probability(sequence):
    counts = collections.Counter(sequence)
    probability = {symbol: count / N_sequence for symbol, count in counts.items()}
    probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])
    probabilities_list.append(probability)
    probabilities_str_list.append(probability_str)


def calculation_mean_probability(probability):
    mean_probability = sum(probability.values()) / len(probability)
    mean_probabilities_list.append(mean_probability)


def probability_distribution(probability, mean_probability):
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
    if equal:
        uniformity = "рівна"
    else:
        uniformity = "нерівна"
    uniformity_list.append(uniformity)


def calculation_entropy(probability):
    entropy = -sum(p * math.log2(p) for p in probability.values())
    entropy_list.append(entropy)


def source_redundancy(entropy, sequence_alphabet_size):
    if sequence_alphabet_size > 1:
        source_excess = 1 - entropy / math.log2(sequence_alphabet_size)
    else:
        source_excess = 1
    source_excesses.append(source_excess)
    return source_excess


def main():
    sequence_list(test_1(8))
    sequence_list(test_2("мезенцев"))
    sequence_list(test_3("мезенцев"))
    sequence_list(test_4("мезенцев", "529"))
    sequence_list(test_5("ме", "529"))
    sequence_list(test_6("ме", "529"))
    sequence_list(test_7())
    sequence_list(test_8())

    with open("sequence.txt", "w", encoding="UTF-8") as file:
        for i in range(1, 9):
            print("Тестова послідовність №" + str(i) + ": ", original_sequences[i-1], file=file)

    for i in range(8):
        calculation_probability(original_sequences[i])
        calculation_mean_probability(probabilities_list[i])
        probability_distribution(probabilities_list[i], mean_probabilities_list[i])
        calculation_entropy(probabilities_list[i])

    # test 1
    write_to_file(test_1(8), size(test_1(8)), chars(test_1(8)), probabilities_str_list[0],
                  mean_probabilities_list[0], uniformity_list[0], entropy_list[0],
                  source_redundancy(entropy_list[0], chars_len_list[0]))

    # test 2
    write_to_file2(test_2("мезенцев"), size(test_2("мезенцев")), chars(test_2("мезенцев")), 2,
                   probabilities_str_list[1], mean_probabilities_list[1], uniformity_list[1], entropy_list[1],
                   source_redundancy(entropy_list[1], chars_len_list[1]))

    # test 3
    write_to_file2(test_3("мезенцев"), size(test_3("мезенцев")), chars(test_3("мезенцев")), 3,
                   probabilities_str_list[2], mean_probabilities_list[2], uniformity_list[2], entropy_list[2],
                   source_redundancy(entropy_list[2], chars_len_list[2]))

    # test 4
    write_to_file2(test_4("мезенцев", "529"), size(test_4("мезенцев", "529")), chars(test_4("мезенцев", "529")), 4,
                   probabilities_str_list[3], mean_probabilities_list[3], uniformity_list[3], entropy_list[3],
                   source_redundancy(entropy_list[3], chars_len_list[3]))

    # test 5
    write_to_file2(test_5("ме", "529"), size(test_5("ме", "529")), chars(test_5("ме", "529")), 5,
                   probabilities_str_list[4], mean_probabilities_list[4], uniformity_list[4], entropy_list[4],
                   source_redundancy(entropy_list[4], chars_len_list[4]))

    # test 6
    write_to_file2(test_6("ме", "529"), size(test_6("ме", "529")), chars(test_6("ме", "529")), 6,
                   probabilities_str_list[5], mean_probabilities_list[5], uniformity_list[5], entropy_list[5],
                   source_redundancy(entropy_list[5], chars_len_list[5]))

    # test 7
    write_to_file2(test_7(), size(test_7()), chars(test_7()), 7, probabilities_str_list[6], mean_probabilities_list[6],
                   uniformity_list[6], entropy_list[6], source_redundancy(entropy_list[6], chars_len_list[6]))

    # test 8
    write_to_file2(test_8(), size(test_8()), chars(test_8()), 8, probabilities_str_list[7], mean_probabilities_list[7],
                   uniformity_list[7], entropy_list[7], source_redundancy(entropy_list[7], chars_len_list[7]))

    for i in range(8):
        results.append([chars_len_list[i], round((entropy_list[i]), 2), round((source_excesses[i]), 2),
                        uniformity_list[i]])

    fig, ax = plt.subplots(figsize=(14 / 1.54, 8 / 1.54))
    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    row = []
    for i in range(1, 9):
        row.append("Послідовність " + str(i))
    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)
    fig.savefig("Характеристики сформованих послідовностей" + ".png", dpi=600)


main()
