import numpy as np

"""
Some functions for using with the spectrum kernel
"""
def spectrum_dict(sequence, k):
    """Creates a spectrum dictionary from a given sequence"""
    d = dict()
    for i in range(len(sequence) - k + 1):
        s = sequence[i:i + k]
        if s in d:
            d[s] += 1
        else:
            d[s] = 1
    return d


def spectrum_dot_product(d1, d2):
    """Returns the dot product given two spectrum dicts"""

    prod = 0
    for seq in iter(d1):
        if seq in d2:
            prod += d1[seq] * d2[seq]
    return prod


def spectrum_gram_matrix(dicts1, dicts2=None):
    """
    Computes a Gram matrix from one or two spectrum dictionaries
    """
    if dicts2 is None:
        dicts2 = dicts1
    mat = np.empty([len(dicts2), len(dicts1)])

    for i in range(len(dicts1)):
        for j in range(len(dicts2)):
            dp = spectrum_dot_product(dicts1[i], dicts2[j])
            mat[j, i] = dp
    return mat


"""
Constants and functions for a amino acid distance based kernel
"""
_aa = list("ARNDCQEGHILKMFPSTWYVBZX-")

_blosum_90 = [[5, -2, -2, -3, -1, -1, -1, 0, -2, -2, -2, -1, -2, -3, -1, 1, 0, -4, -3, -1, -2, -1, -1, -6],
              [-2, 6, -1, -3, -5, 1, -1, -3, 0, -4, -3, 2, -2, -4, -3, -1, -2, -4, -3, -3, -2, 0, -1, -6],
              [-2, -1, 7, 1, -4, 0, -1, -1, 0, -4, -4, 0, -3, -4, -3, 0, 0, -5, -3, -4, 5, -1, -1, -6],
              [-3, -3, 1, 7, -5, -1, 1, -2, -2, -5, -5, -1, -4, -5, -3, -1, -2, -6, -4, -5, 5, 1, -1, -6],
              [-1, -5, -4, -5, 9, -4, -6, -4, -5, -2, -2, -4, -2, -3, -4, -2, -2, -4, -4, -2, -4, -5, -1, -6],
              [-1, 1, 0, -1, -4, 7, 2, -3, 1, -4, -3, 1, 0, -4, -2, -1, -1, -3, -3, -3, -1, 5, -1, -6],
              [-1, -1, -1, 1, -6, 2, 6, -3, -1, -4, -4, 0, -3, -5, -2, -1, -1, -5, -4, -3, 1, 5, -1, -6],
              [0, -3, -1, -2, -4, -3, -3, 6, -3, -5, -5, -2, -4, -5, -3, -1, -3, -4, -5, -5, -2, -3, -1, -6],
              [-2, 0, 0, -2, -5, 1, -1, -3, 8, -4, -4, -1, -3, -2, -3, -2, -2, -3, 1, -4, -1, 0, -1, -6],
              [-2, -4, -4, -5, -2, -4, -4, -5, -4, 5, 1, -4, 1, -1, -4, -3, -1, -4, -2, 3, -5, -4, -1, -6],
              [-2, -3, -4, -5, -2, -3, -4, -5, -4, 1, 5, -3, 2, 0, -4, -3, -2, -3, -2, 0, -5, -4, -1, -6],
              [-1, 2, 0, -1, -4, 1, 0, -2, -1, -4, -3, 6, -2, -4, -2, -1, -1, -5, -3, -3, -1, 1, -1, -6],
              [-2, -2, -3, -4, -2, 0, -3, -4, -3, 1, 2, -2, 7, -1, -3, -2, -1, -2, -2, 0, -4, -2, -1, -6],
              [-3, -4, -4, -5, -3, -4, -5, -5, -2, -1, 0, -4, -1, 7, -4, -3, -3, 0, 3, -2, -4, -4, -1, -6],
              [-1, -3, -3, -3, -4, -2, -2, -3, -3, -4, -4, -2, -3, -4, 8, -2, -2, -5, -4, -3, -3, -2, -1, -6],
              [1, -1, 0, -1, -2, -1, -1, -1, -2, -3, -3, -1, -2, -3, -2, 5, 1, -4, -3, -2, 0, -1, -1, -6],
              [0, -2, 0, -2, -2, -1, -1, -3, -2, -1, -2, -1, -1, -3, -2, 1, 6, -4, -2, -1, -1, -1, -1, -6],
              [-4, -4, -5, -6, -4, -3, -5, -4, -3, -4, -3, -5, -2, 0, -5, -4, -4, 11, 2, -3, -6, -4, -1, -6],
              [-3, -3, -3, -4, -4, -3, -4, -5, 1, -2, -2, -3, -2, 3, -4, -3, -2, 2, 8, -3, -4, -3, -1, -6],
              [-1, -3, -4, -5, -2, -3, -3, -5, -4, 3, 0, -3, 0, -2, -3, -2, -1, -3, -3, 5, -4, -3, -1, -6],
              [-2, -2, 5, 5, -4, -1, 1, -2, -1, -5, -5, -1, -4, -4, -3, 0, -1, -6, -4, -4, 5, 0, -1, -6],
              [-1, 0, -1, 1, -5, 5, 5, -3, 0, -4, -4, 1, -2, -4, -2, -1, -1, -4, -3, -3, 0, 5, -1, -6],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -6],
              [-6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, 1, 1]]

_blosum_62 = [[4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0, -2, -1, 0, -4],
              [-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3, -1, 0, -1, -4],
              [-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3, 3, 0, -1, -4],
              [-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3, 4, 1, -1, -4],
              [0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1, -3, -3, -2, -4],
              [-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2, 0, 3, -1, -4],
              [-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1, -4],
              [0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3, -1, -2, -1, -4],
              [-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3, 0, 0, -1, -4],
              [-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3, -3, -3, -1, -4],
              [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1, -4, -3, -1, -4],
              [-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2, 0, 1, -1, -4],
              [-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1, -3, -1, -1, -4],
              [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1, -3, -3, -1, -4],
              [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2, -2, -1, -2, -4],
              [1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2, 0, 0, 0, -4],
              [0, -1, 0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1, 5, -2, -2, 0, -1, -1, 0, -4],
              [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1, -4, -3, -2, 11, 2, -3, -4, -3, -2, -4],
              [-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1, -3, -2, -1, -4],
              [0, -3, -3, -3, -1, -2, -2, -3, -3, 3, 1, -2, 1, -1, -2, -2, 0, -3, -1, 4, -3, -2, -1, -4],
              [-2, -1, 3, 4, -3, 0, 1, -1, 0, -3, -4, 0, -3, -3, -2, 0, -1, -4, -3, -3, 4, 1, -1, -4],
              [-1, 0, 0, 1, -3, 3, 4, -2, 0, -3, -3, 1, -1, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1, -4],
              [0, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 0, 0, -2, -1, -1, -1, -1, -1, -4],
              [-4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, 1]]


def distance_matrix(X, Y, matrix=_blosum_90):
    gram = np.zeros((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            xi = list(X[i])
            yj = list(Y[j])
            score = 0
            for k in range(len(xi)):
                c1 = xi[k]
                c2 = yj[k]
                score += matrix[_aa.index(c1)][_aa.index(c2)]
            gram[i][j] = score
    return gram


"""
Used to generate input for a DictVectorizer
"""
def feature_dict(sequence):
    return dict(zip(range(len(sequence)), list(sequence)))


def feature_dict_list(sequences):
    return [feature_dict(sequence) for sequence in sequences]
