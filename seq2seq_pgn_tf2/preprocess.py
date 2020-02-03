import numpy as np
import pandas as pd
import re
from jieba import posseg
import jieba
from utils.tokenizer import segment


REMOVE_WORDS = ['|', '[', ']', '语音', '图片']


def read_stopwords(path):
    lines = set()
    with open(path, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            lines.add(line)
    return lines


def remove_words(words_list):
    words_list = [word for word in words_list if word not in REMOVE_WORDS]
    return words_list


def parse_data(train_path, test_path):
    train_df = pd.read_csv(train_path, encoding='utf-8')
    train_df.dropna(subset=['Question', 'Dialogue', 'Report'], how='any', inplace=True)
    train_x = train_df.Question.str.cat(train_df.Dialogue)
    train_y = []
    if 'Report' in train_df.columns:
        train_y = train_df.Report

    test_df = pd.read_csv(test_path, encoding='utf-8')
    test_df.dropna(subset=['Question', 'Dialogue'], how='any', inplace=True)
    test_x = test_df.Question.str.cat(test_df.Dialogue)
    test_y = []
    print('train_x is ', len(train_x))
    print('train_y is ', len(train_y))
    print('test_x is ', len(test_x))
    return train_x, train_y, test_x, test_y


def save_data(data_1, data_2, data_3, data_path_1, data_path_2, data_path_3, stop_words_path=''):
    stopwords = read_stopwords(stop_words_path)
    with open(data_path_1, 'w', encoding='utf-8') as f1:
        count_1 = 0
        for line in data_1:
            # print(line)
            if isinstance(line, str):
                seg_list = segment(line.strip(), cut_type='word')
                seg_list = remove_words(seg_list)
                # seg_words = []
                # for j in seg_list:
                #     if j in stopwords:
                #         continue
                #     seg_words.append(j)
                if len(seg_list) > 0:
                    seg_line = ' '.join(seg_list)
                    f1.write('%s' % seg_line)
                    f1.write('\n')
                    count_1 += 1
        print('train_x_length is ', count_1)

    with open(data_path_2, 'w', encoding='utf-8') as f2:
        count_2 = 0
        for line in data_2:
            if isinstance(line, str):
                seg_list = segment(line.strip(), cut_type='word')
                seg_list = remove_words(seg_list)
                # seg_words = []
                # for j in seg_list:
                #     if j in stopwords:
                #         continue
                #     seg_words.append(j)
                if len(seg_list) > 0:
                    seg_line = ' '.join(seg_list)
                    f2.write('%s' % seg_line)
                    f2.write('\n')
                    count_2 += 1
        print('train_y_length is ', count_2)

    with open(data_path_3, 'w', encoding='utf-8') as f3:
        count_3 = 0
        for line in data_3:
            if isinstance(line, str):
                seg_list = segment(line.strip(), cut_type='word')
                seg_list = remove_words(seg_list)
                if len(seg_list) > 0:
                    seg_line = ' '.join(seg_list)
                    f3.write('%s' % seg_line)
                    f3.write('\n')
                    count_3 += 1
        print('test_y_length is ', count_3)


def preprocess_sentence(sentence):
    seg_list = segment(sentence.strip(), cut_type='word')
    seg_line = ' '.join(seg_list)
    return seg_line


if __name__ == '__main__':
    train_list_src, train_list_trg, test_list_src, _ = parse_data('../datasets/AutoMaster_TrainSet.csv',
                                                                  '../datasets/AutoMaster_TestSet.csv')
    save_data(train_list_src,
              train_list_trg,
              test_list_src,
              '../datasets/train_set.seg_x.txt',
              '../datasets/train_set.seg_y.txt',
              '../datasets/test_set.seg_x.txt',
              stop_words_path='../datasets/stop_words.txt')


