import numpy as np
from sklearn import svm


def read_files(pos_file, neg_file):
    """Reads training data"""

    poslines = read_file(pos_file)
    neglines = read_file(neg_file)

    poslabels = np.ones_like(poslines, dtype=np.int)
    neglabels = np.zeros_like(neglines, dtype=np.int)

    lines = poslines + neglines
    labels = np.concatenate((poslabels, neglabels))
    return lines, labels


def read_file(filename):
    """Reads a file, returns lines"""
    f = open(filename, 'r')
    ls = f.read().splitlines()
    f.close()
    return ls


def remove_gaps(sequences):
    """Removes gaps (-) from a set of strings"""

    return map(lambda seq: seq.replace('-', ''), sequences)


def spectrum_dict(sequence, k):
    """Creates a spectrum dictionary from a given sequence"""

    d = dict()
    for i in range(len(sequence)-k+1):
        s = sequence[i:i+k]
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
    if dicts2 is None:
        dicts2 = dicts1
    mat = np.empty([len(dicts2), len(dicts1)])

    for i in range(len(dicts1)):
        for j in range(len(dicts2)):
            dp = spectrum_dot_product(dicts1[i], dicts2[j])
            mat[j,i] = dp
    return mat


if __name__ == "__main__":
    f1 = "training1"
    f2 = "training2"
    f3 = "testing"

    (lines, labels) = read_files(f1, f2)


    testlines = read_file(f3)
    testseqs = remove_gaps(testlines)
    testdicts = map (lambda seq: spectrum_dict(seq, 3), testseqs)

    seqs = remove_gaps(lines)
    dicts = list(map(lambda seq: spectrum_dict(seq, 3), seqs))

    gram = spectrum_gram_matrix(dicts)
    clf = svm.SVC(kernel='precomputed')
    clf.fit(gram, labels)
    gram2 = spectrum_gram_matrix(dicts, testdicts)
    ans = clf.predict(gram2)
    print(ans)
    print(gram2.shape)
