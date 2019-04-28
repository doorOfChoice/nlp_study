# coding=utf-8
"""
新词发现算法
参考:
    http://www.matrix67.com/blog/archives/5044
"""
import math
import re

from dawndevil.data_structure.trie import TrieTree
from dawndevil.utils.io_utils import read_file_as_string, read_file_as_set
from dawndevil.utils.nlp_utils import filter_stop_words


class WordDiscovery(object):
    def __init__(self):
        self.mi = 100
        self.left_entropy = 0.5
        self.right_entropy = 0.5
        self.words = {}
        self.entropy = {}
        self.words_count = 0
        self.symbol = ""
        self.stop_words = TrieTree()

    def set_threshold(self, mi, left_entropy, right_entropy):
        """
        设置基本阈值
        :param mi:              凝固度
        :param left_entropy:    左邻熵
        :param right_entropy:   右邻熵
        :return:
        """
        self.mi = mi
        self.left_entropy = left_entropy
        self.right_entropy = right_entropy

    def set_dict(self, symbol="", stop_words=""):
        """
        加载各类词典
        :param stop_words:  停词表
        :param symbol: 标点符号文件
        :return:
        """
        self.symbol = read_file_as_string(symbol)
        stop_words = read_file_as_set(stop_words)
        for stop_word in stop_words:
            self.stop_words.add(stop_word)

    def append(self, text):
        """
        将文本拆分为词，计算出现次数
        :param text:
        :return:
        """
        for line in self.split_text(text):
            size = len(line)
            if size == 0:
                continue
            for i in range(size + 1):
                for j in range(i + 1, size + 1):
                    word = line[i: j]
                    self.words[word] = self.words.get(word, 0) + 1
                    self.words_count += 1

    def p(self, word):
        """
        求单词概率
        :param word:
        :return:
        """
        return self.words[word] / self.words_count

    def split_text(self, text):
        """
        分割文本
        :param text:
        :return:
        """
        pattern = "[\\s\n" + self.symbol + "]"
        filtered_list = re.split(pattern, text)
        result = []

        for filtered_text in filtered_list:
            result.extend(filter_stop_words(self.stop_words, filtered_text))
        return result

    def get_mi(self, word):
        """
        求凝固度
        :param word: 单词
        :return:
        """
        if len(word) <= 1:
            return 0
        word_prob = self.p(word)
        min_mi = 1e8
        for i in range(1, len(word)):
            left_string = word[:i]
            right_string = word[i:]
            left_prob = self.p(left_string)
            right_prob = self.p(right_string)
            mi = word_prob / left_prob / right_prob
            min_mi = min(min_mi, mi)
        return min_mi

    def load_entropy(self):
        """
        计算左右邻熵
        :return:
        """
        for word in self.words:
            if len(word) > 1:
                # 计算左邻
                left_word = word[1:]
                if left_word not in self.entropy:
                    self.entropy[left_word] = {"left": [], "right": []}
                self.entropy[left_word]["left"].append(self.words[word])
                # 计算右邻

                right_word = word[:-1]
                if right_word not in self.entropy:
                    self.entropy[right_word] = {"left": [], "right": []}
                self.entropy[right_word]["right"].append(self.words[word])

    def get_entropy(self, word, direct=0):
        """
        求信息熵
        :param word:   单词
        :param direct: 0 left, 1 right
        :return:
        """
        if word not in self.entropy:
            return 0
        entropy_list = self.entropy[word]["left"] \
            if direct == 0 else self.entropy[word]["right"]
        total = sum(entropy_list)
        result = 0
        for v in entropy_list:
            prob = v / total
            result += -prob * math.log(prob)

        return result

    def run(self):

        """
        ① 计算mi凝固值, MIN(p(电影院)/(p(电影)*p(院)), p(电影院)/(p(电)*p(影院院)))
        ② 计算左邻信息熵
        ③ 计算右邻信息熵
        :return: 结果集
        """
        result = []
        self.entropy.clear()
        self.load_entropy()
        for word in self.words:
            mi = self.get_mi(word)

            left_entropy = self.get_entropy(word)

            right_entropy = self.get_entropy(word, direct=1)

            if left_entropy < self.left_entropy:
                continue

            if right_entropy < self.right_entropy:
                continue

            if mi < self.mi:
                continue

            result.append({
                "word": word,
                "mi": mi,
                "le": left_entropy,
                "re": right_entropy
            })
        return result
