
def flatten_tuple_of_keys(data):
    """
    Method to transform keys of a dictionary from tuple into separated keys with the same values.
    """
    flatten_dict = {}
    for key, value in data.items():
        if isinstance(key, tuple):
            for action in key:
                flatten_dict[action] = value
        else:
            flatten_dict[key] = value
    return flatten_dict
