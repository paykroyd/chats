"""
Basic utilities that aren't stats related.
"""

def keys_and_values(d):
  """Returns a list of keys and a list of values corresponding the kv pairs in the dict.

  Params:
    d: a dict
  
  Returns:
    a tuple containing 2 lists of equal length
  """
  keys = []
  vals = []
  for k, v in d.items():
    keys.append(k)
    vals.append(v)
  return keys, vals
