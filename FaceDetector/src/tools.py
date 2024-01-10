
def limit_dict(dict_data, key, value, max_len = None):
    if key not in dict_data:
        dict_data[key] = [value]
    else:
        if len(dict_data[key]) > max_len-1:
            dict_data[key].pop(0)
        dict_data[key].append(value)


def delete_saftely(dict_data):
    print(dict_data)