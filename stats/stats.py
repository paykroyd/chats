"""
My statistics package.
"""


def mean(values):
    """
    Computes the mean of the set of values.

    Params:
        values: a sequence of numbers

    Returns:
        float
    """
    return float(sum(values)) / len(values)

def variance(values, mu=None):
    """
    Computes the variance of the values.

    v^2 = 1/n * sum(v[1..n] - mean)

    Args:
            values: sequence of numbers
            mu: optionally the mean can be passed in to improve efficiency
    """
    if mu is None:
        mu = mean(values)
    return sum([(x - mu)**2 for x in values]) / float(len(values))

def std_dev(values, mu=None):
    """
    Computes the standard deviation of the values.

    This is just the square root of the variance.

    Args:
            values: sequence of numbers
            mu: optionally the mean can be passed in for efficiency
    """
    return variance(values, mu)**.5

def hist(values):
    """
    Creates a histogram for the values passed in.

    The histogram is represented by a dict with the value for key mapped to the count.
    Args:
        values: a sequence of numbers

    Returns:
        dict
    """
    hist = {}
    for val in values:
        hist[val] = hist.get(val, 0) + 1
    return hist

def pmf(values):
    """
    Creates a pmf of the values which is a normalized histogram.

    Args:
        values: a sequence of numbers

    Returns:
        dict
    """
    h = hist(values)
    n = len(values)
    for val, cnt in h.items():
        h[val] = float(cnt) / n
    return h

def renormalize(pmf):
  """
  Given a pmf, this function will renormalize it so that it's probablities sum to 1.0

  Params:
    pmf: a dict representing a pmf

  Returns:
    dict
  """
  # determine how much to muliply each entry's probablity by to re-normalize
  total = sum(pmf.values())
  mult = 1 / total
  return dict([(key, prob * mult) for key, prob in pmf.items()])


def mode(pmf):
    """
    Returns the mode of the distribution. 

    The mode is the value which appears most frequently.

    Args:
        pmf: a valid pmf dict object for the distribution

    Returns:
        number
    """
    if not pmf:
        raise ValueError, 'Must be some values in the pmf'
    return allmodes(pmf)[0]

def allmodes(pmf):
    """
    Returns the values in order by how often they appear in the distribution.

    Args:
        pmf: a valid pmf dict object for the distribution

    Returns:
        sequence of numbers
    """
    s = sorted(pmf.items(), cmp=lambda v1, v2: int(v1[1] * 100 - v2[1] * 100), reverse=True)
    return [i[0] for i in s]

