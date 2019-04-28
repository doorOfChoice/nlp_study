# coding=utf-8
class TrieNode(object):
    """
    Trie结点
    """

    def __init__(self, parent=None, transfer="", marked=False):
        """
        __init__
        :param parent:   父节点
        :param transfer: 转移状态
        """
        self.prev_em = parent
        self.children = {}
        self.count = 0
        self.transfer = transfer
        self.value = ("" if parent is None else parent.get_value()) + transfer
        self.marked = marked

    def find(self, value):
        """
        在某个节点的孩子里寻找某个字符
        :param value: 单个字符
        :return:
        """
        if value in self.children:
            return self.children[value]

        return None

    def add(self, value):
        """
        新增字符节点
        :param value: 单个字符
        :return:
        """
        if value not in self.children:
            self.children[value] = TrieNode(self, value)
            return self.children[value]

    def remove(self, value):
        """
        移除当前节点
        :param value: 匹配的字符值
        :return:
        """
        if self.transfer == value:
            if self.prev_em is not None:
                em = self.prev_em
                del em[value]

    def remove_self(self):
        if self.prev_em is not None and self.prev_em.prev_em is not None:
            self.prev_em.children.pop(self.transfer)

    def equal(self, value):
        """
        判断当前节点是否和value字符相等
        :param value:
        :return:
        """
        return self.transfer == value

    def mark(self):
        self.marked = True

    def get_value(self):
        return self.value


class TrieTree(object):
    """
    Trie树
    """

    def __init__(self):
        self.node = TrieNode()

    def add(self, string):
        """
        向trie树里面添加字符串
        :param string:
        :return:
        """
        prev = self.node
        for char in string:
            cur = prev.find(char)
            if cur is None:
                cur = prev.add(char)

            prev = cur
        prev.mark()

    def remove(self, string):
        """
        从trie树移除字符串
        :param string:
        :return:
        """
        node = self.find(string)
        prev = node
        while prev is not None:
            cur = prev
            prev = prev.prev_em
            cur.remove_self()

    def find(self, string):
        """
        在trie树中查找字符串
        :param string:
        :return:
        """
        prev = self.node
        for char in string:
            cur = prev.find(char)
            if cur is None:
                break
            prev = cur
        if prev.value == string:
            return prev
        return None

    def root(self):
        return self.node

    def show(self):
        """
        打印trie树
        :return:
        """
        self.__show(self.node)

    def __show(self, node):
        if node is None:
            return
        if node.marked:
            print(node.value, node.marked)
        for _, child in node.children.items():
            self.__show(child)


if __name__ == "__main__":
    tree = TrieTree()
    tree.add("Hello World")
    tree.add("Momo")
    tree.add("Mi")
    tree.add("Master")
    tree.remove("Mi")
    tree.show()
