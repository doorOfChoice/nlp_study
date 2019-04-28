# coding=utf-8
def read_file_as_string(filename):
    """
    读入文件为字符串
    :param filename:
    :return:
    """
    s = ""
    with open(filename, 'r') as f:
        for line in f:
            s += line
    return s


def read_file_as_list(filename):
    result = []
    with open(filename, 'r') as f:
        for line in f:
            result.append(line.strip(" ").strip("\n"))
    return result


def read_file_as_set(filename):
    return set(read_file_as_list(filename))
