# import main

# has global dictionary that contains list of user ratings per source
def update_dict(srcdict, source, rating):
    new_dict = srcdict.copy()
    if source in new_dict:
        new_dict[source].append(int(rating))
    else:
        new_dict[source] = [int(rating)]
    return new_dict

def source_user_biases(srcdict):
    src_list = []
    # for x in sorted(list(dict.items()), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
    for x in srcdict:
        src_list.append((x, sum(srcdict[x])/len(srcdict[x])))
    return src_list