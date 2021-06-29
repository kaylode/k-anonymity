# -*- coding: utf-8 -*-

# Range for numeric type


class NumRange(object):

    """Class for Generalization hierarchies (Taxonomy Tree).
    Store numeric node in instances.
    self.sort_value: sorted values, which may help get the normalized width
    self.value: node value, e.g. '10,20'
    self.support: support (frequency) of all values, dict
    self.range: (max-min), used for normalized width
    self.cover: leaves nodes of current node
    """

    def __init__(self, sort_value, support):
        self.sort_value = list(sort_value)
        self.support = support.copy()
        # sometimes the values may be str
        self.range = float(sort_value[-1]) - float(sort_value[0])
        self.dict = {}
        for i, v in enumerate(sort_value):
            self.dict[v] = i
        self.value = sort_value[0] + ',' + sort_value[-1]

    def __len__(self):
        """
        return |max-min|
        """
        return self.range
