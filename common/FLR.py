import numpy as np
from pyFTS.common import FuzzySet

"""
This module implements functions for Fuzzy Logical Relationship generation 
"""

class FLR(object):
    """Fuzzy Logical Relationship"""
    def __init__(self, LHS, RHS):
        """
        Creates a Fuzzy Logical Relationship
        :param LHS: Left Hand Side fuzzy set
        :param RHS: Right Hand Side fuzzy set
        """
        self.LHS = LHS
        self.RHS = RHS

    def __str__(self):
        return self.LHS.name + " -> " + self.RHS.name


class IndexedFLR(FLR):
    """Season Indexed Fuzzy Logical Relationship"""
    def __init__(self, index, LHS, RHS):
        """
        Create a Season Indexed Fuzzy Logical Relationship
        :param index: seasonal index 
        :param LHS: Left Hand Side fuzzy set
        :param RHS: Right Hand Side fuzzy set
        """
        super(IndexedFLR, self).__init__(LHS, RHS)
        self.index = index

    def __str__(self):
        return str(self.index) + ": "+ self.LHS.name + " -> " + self.RHS.name


def generateNonRecurrentFLRs(fuzzyData):
    """
    Create a ordered FLR set from a list of fuzzy sets without recurrence
    :param fuzzyData: ordered list of fuzzy sets
    :return: ordered list of FLR 
    """
    flrs = {}
    for i in range(2,len(fuzzyData)):
        tmp = FLR(fuzzyData[i-1],fuzzyData[i])
        flrs[str(tmp)] = tmp
    ret = [value for key, value in flrs.items()]
    return ret


def generateRecurrentFLRs(fuzzyData):
    """
    Create a ordered FLR set from a list of fuzzy sets with recurrence
    :param fuzzyData: ordered list of fuzzy sets
    :return: ordered list of FLR 
    """
    flrs = []
    for i in np.arange(1,len(fuzzyData)):
        flrs.append(FLR(fuzzyData[i-1],fuzzyData[i]))
    return flrs


def generateIndexedFLRs(sets, indexer, data, transformation=None):
    """
    Create a season-indexed ordered FLR set from a list of fuzzy sets with recurrence
    :param sets: fuzzy sets
    :param indexer: seasonality indexer 
    :param data: original data
    :return: ordered list of FLR 
    """
    flrs = []
    index = indexer.get_season_of_data(data)
    ndata = indexer.get_data(data)
    if transformation is not None:
        ndata = transformation.apply(ndata)
    for k in np.arange(1,len(ndata)):
        lhs = FuzzySet.getMaxMembershipFuzzySet(ndata[k-1],sets)
        rhs = FuzzySet.getMaxMembershipFuzzySet(ndata[k], sets)
        season = index[k]
        flr = IndexedFLR(season,lhs,rhs)
        flrs.append(flr)
    return flrs
