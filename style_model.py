import numpy as np
from keras import utils
from keras.models import Sequential
import os
from keras.models import load_model
from keras.preprocessing.text import Tokenizer

mymodel = load_model('StylisticModel.h5')

text_train = []

for file_name in ['Artistic.txt', 'Official.txt',
                  'Publicistic.txt', 'Scientific.txt']:
    with open(f'Stylistics/{file_name}', 'r', encoding="utf-8") as f:
        file_text = f.read()
        file_text = file_text.replace('\n', ' ').split(' ')
        text_train.append(' '.join(file_text[:int(len(file_text) * 0.8)]))


VOCAB_SIZE = 10000                        # Объем словаря для токенизатора
WIN_SIZE = 100                          # Длина отрезка текста (окна) в словах
WIN_HOP = 20                            # Шаг окна разбиения текста на векторы

tokenizer = Tokenizer(
    num_words=VOCAB_SIZE,
    filters='!"#$%&()*+,-–—./…:;<=>?@[\\]^_`‘’\'{|}~«»\t\n\xa0\ufeff',
    lower=True,
    split=' ',
    oov_token='неизвестное_слово',
    char_level=False
)
tokenizer.fit_on_texts(text_train)


def pred(file):
    input_text = open(file, 'r', encoding="utf-8")
    input_text = input_text.read()  # Загрузим содержимое файла в строку
    input_text = input_text.replace('\n', ' ').replace('‘', '').replace('’', '').replace("'", '')

    input_text = input_text.lower()
    print(input_text)

    cyr_lat_dict = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'yo',
        'ж': 'j',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'x',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sh',
        'ъ': '',
        'ы': 'i',
        'ь': '',
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
        'ғ' : 'g',
        'ҳ' : 'h',
        'ў' : 'o'
    }

    for cl in cyr_lat_dict:
        input_text = input_text.replace(cl, cyr_lat_dict[cl])
    while len(input_text.split(' ')) < 100:
        input_text += ' ' + input_text

    seq_val = tokenizer.texts_to_sequences([input_text])[0]
    print(seq_val)
    print('len(seq_val): ', len(seq_val))


    x_val_list = []

    vectors = [seq_val[i:i + WIN_SIZE] for i in range(0, len(seq_val) - WIN_SIZE + 1, WIN_HOP)]
    x_val_list+=vectors
    print(x_val_list)

    x_val = np.array(x_val_list)
    print("shape: ", x_val.shape)

    y_pred = mymodel.predict(x_val)

    r = np.argmax(y_pred, axis=1)  # Найдем индексы писателя
    unique, counts = np.unique(r, return_counts=True)  # Найдем полученые индексы и их количество
    counts = counts / y_pred.shape[0] * 100  # Считаем долю каждного полученного индекса
    print(unique, counts)  # Выведем полученые индексы и их доли

    styles_list = ["Badiiy", "Rasmiy", "Publitsistik", "Ilmiy"]
    for i in range(0, len(unique)):
        print(styles_list[unique[i]], counts[i])

    return unique, counts


# pred('test.txt')