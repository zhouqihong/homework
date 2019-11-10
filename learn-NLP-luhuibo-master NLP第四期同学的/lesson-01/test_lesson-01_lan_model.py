#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/7/5 23:42
@Desc   ：
2. 使用新数据源完成语言模型的训练
按照我们上文中定义的prob_2函数，我们更换一个文本数据源，获得新的Language Model:

下载文本数据集（你可以在以下数据集中任选一个，也可以两个都使用）
可选数据集1，保险行业问询对话集： https://github.com/Computing-Intelligence/insuranceqa-corpus-zh/raw/release/corpus/pool/train.txt.gz
可选数据集2：豆瓣评论数据集：https://github.com/Computing-Intelligence/datasource/raw/master/movie_comments.csv
修改代码，获得新的2-gram语言模型
进行文本清洗，获得所有的纯文本
将这些文本进行切词
送入之前定义的语言模型中，判断文本的合理程度
=================================================='''
import pandas as pd
import re
import jieba
import random
from collections import Counter

data_bank_chat_file = 'train.txt'
data_movie_commonent_file = 'train_movie_comments.csv'
data_article_9k = 'train_article_9k.txt'
data_sqlResult = 'train_sqlResult_1558435.csv'

good = """
good = 对象 状态 加油
对象 = 你们 | 我们 | 他们 | 你 | 我 | 他
状态 = 要 | 必须
加油 = 元气满满 | 加油鸭 | 努力努力
"""


def token(string):
    """
    # 只保留中文、数字、英文
    # 将常用方法写到自己的wiki中：
    # https://github.com/Valuebai/learn-NLP-luhuibo/wiki
    :param string:
    :return:保留中文、数字、英文后的
    """
    return re.findall('[a-zA-Z0-9\u4e00-\u9fa5]', string)


def jieba_cut(string):
    """
    进行jieba中文分词
    :param string:
    :return: 返回列表
    """
    return list(jieba.cut(string))


def prob_1(word):
    """
    计算1-gram，1个词的概率
    :param word:
    :return:float
    """
    return words_count[word] / len(TOKEN)


def prob_2(word_1, word_2):
    """
    计算2-gram，2个词的概率
    :param word:
    :return:float
    """
    if word_1 + word_2 in words_count_2:
        # 这个地方的计算不能用课堂上老师讲的，得用https://zhuanlan.zhihu.com/p/52061158 中的公式
        return (words_count_2[word_1 + word_2] / len(TOKEN_2_GRAM)) / prob_1(word_2)
    else:
        return 1 / len(TOKEN_2_GRAM)


def prob_sentence(sentence):
    """
    计算1个句子的概率
        P(w1 w2 w3 w4)
        = P(w1|w2w3w4) P(w2|w3w4) P(w3|w4) P(w4)
        ≈ P(w1|w2) P(w2|w3) P(w3|w4) P(w4)
        = P(w1w2)/P(w2) * P(w2w3)/P(w3) * P(w3w4)/P(w4) * P(w4)
    :param word:
    :return:float
    """
    words = jieba_cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probability = prob_2(word, next_)
        sentence_pro *= probability
    return sentence_pro


def create_grammar(grammar_str, line_split='=', value_split=('|')):
    """
    主要将输入的文本转为字典中
    :param grammar:
    :return: grammar
    """
    grammar = {}
    # 读取文本的每一行，按照\n来进行切分，如果有空的行，即不进行处理
    for line in grammar_str.split('\n'):
        if not line.strip(): continue
        key, value = line.split(line_split)
        grammar[key.strip()] = [s.split() for s in value.split(value_split)]
    return grammar


def generate(gram_dict, target_str):
    # 1.从字典中的key中对应的value随机取出一个值，
    # 2.如果这个值还是字典的key的话，继续上一步的随机取值 如果target不在字典的key中，则返回target
    if target_str not in gram_dict: return target_str
    expand = []
    for t in random.choice(gram_dict[target_str]):
        expand.append(generate(gram_dict, t))
    # expaned = [generate(gram_dict, t) for t in random.choice(gram_dict[target])]
    # 一开始返回expand列表，会得到一个列表[[['这个'], [['蓝色的'], [['蓝色的'], ['null']]], ['女人']], [['坐在'], [['这个'], ['null'], ['女人']]]],我们可以使用''.join将列表中的字符串连接起来
    # ''.join(expand)打印出来的结果中带有null，再处理下
    return ''.join([e for e in expand if e != 'null'])


def generate_best(gram, string, n):  # you code here
    sentences_pro_list = []
    for i in range(n):
        sentence = generate(gram, string)
        sentence_pro = prob_sentence(sentence)
        sentence_pro_list = (sentence, sentence_pro)
        sentences_pro_list.append(sentence_pro_list)
    print('===随机生成的句子及概率：')
    print(sentences_pro_list)
    return sorted(sentences_pro_list, key=lambda x: x[1], reverse=True)[0]


if __name__ == "__main__":
    # 1.读取文本，进行文本清洗，获得所有的纯文本
    movie_comment = pd.read_csv(data_movie_commonent_file, encoding='utf-8', low_memory=False)
    movie_comment_list = movie_comment['comment'].tolist()
    print('打印评论列表的长度:', len(movie_comment_list))
    # 清除列表每一行的多余符号，只保留中文、数字、英文
    clean_comment_list = []
    for line in movie_comment_list:
        clean_comment_list.append(''.join(token(str(line))))
    # print('-' * 20 + 'After clean')
    # print('打印清洗过数据的列表:', clean_comment_list)

    # 2.将这些文本进行切词
    TOKEN = []
    count = 0
    for i in clean_comment_list:
        if count % 20000 == 0:
            print(count)
        if count > 100000:
            break
        count += 1
        TOKEN += jieba_cut(i)
    print('打印jieba分词后TOKEN列表的前10个：', TOKEN[:10])
    words_count = Counter(TOKEN)
    print('打印Counter后前100个：', words_count.most_common(100))

    # 3. 送入之前定义的语言模型中，判断文本的合理程度
    print('1个词的概率===========')
    print('TOKEN--的长度为:', len(TOKEN))
    print('一个词的概率【的】:', prob_1('的'))
    print('一个词的概率【我】:', prob_1('的'))
    print('一个词的概率【我们】:', prob_1('的'))

    print('2个词的概率===========')
    TOKEN = [str(t) for t in TOKEN]
    TOKEN_2_GRAM = [''.join(TOKEN[i:i + 2]) for i in range(len(TOKEN[:-2]))]
    print('TOKEN_2_GRAM--的长度为:', len(TOKEN_2_GRAM))
    words_count_2 = Counter(TOKEN_2_GRAM)
    print('一个词的概率【吴京，傻】:', prob_2('吴京', '傻'))
    print('一个词的概率【中国，人】:', prob_2('中国', '人'))
    print('一个词的概率【我们，爱】:', prob_2('我们', '爱'))

    print('句子的概率===========')
    print('句子：小明去背景的概率为', prob_sentence('小明去背景'))
    print('句子：我们去上班的概率为', prob_sentence('中国人爱看电影'))
    print('句子：我们去上班的概率为', prob_sentence('中国人爱看电影'))

    need_compared = [
        "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
        "真事一只好看的小猫 真是一只好看的小猫",
        "今晚我去吃火锅 今晚火锅去吃我",
        "洋葱奶昔来一杯 养乐多绿来一杯"
    ]

    for s in need_compared:
        s1, s2 = s.split()
        p1, p2 = prob_sentence(s1), prob_sentence(s2)

    better = s1 if p1 > p2 else s2

    # 用generate_best()来
    # 获得最优质的的语言
    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probility {}'.format(s1, p1))
    print('-' * 4 + ' {} with probility {}'.format(s2, p2))
    gram_good = create_grammar(grammar_str=good)
    print('\n获得最优质的的语言是：', generate_best(gram_good, 'good', n=5))
