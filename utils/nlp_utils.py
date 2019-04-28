# coding=utf-8


def filter_stop_words(trie, text):
    """
    去除停词，分割成
    :param trie: 停词字典树
    :param text: 待分割文本
    :return: list
    """

    def find_text(trie, text, i):
        """
        寻找非停词文本段
        :param trie: 停词字典树
        :param text: 待寻找文本
        :param i:    起始下标
        :return:
        """
        root = trie.root()
        line = ""
        j = i
        can_append = False
        for j in range(i, len(text)):
            char = text[j]
            node = root.find(char)
            line += char
            if node is None:
                line = text[i]
                j = i + 1
                break
            elif node.marked:
                j += 1
                can_append = True
                break
            root = node
        return j, line, can_append

    result = []
    out_i = 0
    out_line = ""
    for i, char in enumerate(text):
        if i < out_i:
            continue
        out_i, line, can_append = find_text(trie, text, i)
        if can_append and out_line != "":
            result.append(out_line)
            out_line = ""
        else:
            out_line += line
    if out_line != "":
        result.append(out_line)
    return result
