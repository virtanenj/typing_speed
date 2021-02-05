import xml.etree.ElementTree as et
import random
import time

from datetime import date

import pandas as pd


def load_finnish():
    xtree = et.parse("kotus-sanalista_v1.xml")
    xroot = xtree.getroot()
    word_list = []
    for node in xroot:
        word = node.find("s").text
        word_list.append(word)
    return word_list


def load_english():
    pass


def update(correct, word_num, overall_time):
    wpm = correct / (overall_time / 60)
    this_date = date.today().strftime("%d/%m/%Y")
    new_row = pd.DataFrame({'correct words':[correct], 'written words':[word_num], 'time':[overall_time], 'WPM':[wpm], 'date':[this_date]})
    try:
        data = pd.read_pickle('data.csv')
        data_update = data.append(new_row, ignore_index=True)
        data_update.to_pickle('data.csv')
    except FileNotFoundError:
        data = new_row
        data.to_pickle('data.csv')


def run(word_num, word_list, update_data=True):
    correct = 0
    start_time = time.time()
    for i in range(word_num):
        word = word_list[random.randint(0, len(word_list))]
        print('-----\nWrite the word:  '+word)
        written_word = input('HERE: ')
        if word == written_word:
            print('Correct!')
            correct += 1
        else:
            print('Wrond!')
    end_time = time.time()
    overall_time = end_time - start_time

    if update_data:
        update(correct, word_num, overall_time)


def session():
    language = input('Language (English, Finnish): ')
    word_list = []
    if language == 'Finnish':
        word_list = load_finnish()
    keep_training = True
    while keep_training:
        word_num = int(input('Number of words: '))
        run(word_num, word_list)
        keep_training_choice = input('Keep training (yes, no): ')
        if keep_training_choice == 'no':
            keep_training = False
            print('Goodbye!')


def load_data():
    return pd.read_pickle('data.csv')


def key_data():
    import matplotlib.pyplot as plt
    data = load_data()
    print('Average WPM of all time', data['WPM'].mean())
    print('Average WPM of last 3 tries', data['WPM'].iloc[-3:].mean())
    print(data)
    plt.plot(data['WPM'])
    plt.ylabel('WPM')
    plt.xlabel('Some instance of a run')
    plt.show()
    
    



session()
key_data()
