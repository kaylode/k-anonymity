# -*- coding: utf-8 -*-

# logic tree


class GenTree(object):

    """Class for Generalization hierarchies (Taxonomy Tree).
    Store tree node in instances.
    self.value: node value
    self.level: tree level (top is 0)
    self.leaf_num: number of leaf node covered
    self.parent: ancestor node list
    self.child: direct successor node list
    self.cover: all nodes covered by current node
    """

    def __init__(self, value=None, parent=None, isleaf=False):
        self.value = ''
        self.level = 0
        self.leaf_num = 0
        self.parent = []
        self.child = []
        self.cover = {}
        self.isleaf = isleaf
        self.leaf_list = []
        if value is not None:
            self.value = value
            self.cover[value] = self
        if parent is not None:
            self.parent = parent.parent[:]
            self.parent.insert(0, parent)
            parent.child.append(self)
            self.level = parent.level + 1
            for t in self.parent:
                t.cover[self.value] = self
                if isleaf:
                    t.leaf_num += 1
                    t.leaf_list.append(self.value)

    def node(self, value):
        """Search tree with value, return GenTree node.
        return point to that node, or None if not exists
        """
        try:
            return self.cover[value]
        except KeyError:
            return None

    def __len__(self):
        """
        return number of leaf node covered by current node
        """
        return self.leaf_num

    def get_leaves_names(self):
        return self.leaf_list
