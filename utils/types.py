# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum


class Dataset(Enum):
    CMC = 'cmc'
    MGM = 'mgm'
    ADULT = 'adult'
    CAHOUSING = 'cahousing'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return str(other) == self.value


class AnonMethod(Enum):

    #Optimal Lattice Anonymization
    OLA = 'ola'

    # Basic Mondrian
    MONDRIAN = 'mondrian'

    # Top-Down Greedy
    TOPDOWN = 'topdown'

    # Cluster-based
    CLUSTER = 'cluster'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return str(other) == self.value