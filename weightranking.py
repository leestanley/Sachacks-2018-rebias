import main

# has global dictionary that contains list of user ratings per source
def update_dict(dict, source, ratings):
    dict[source].append(ratings)

def highest_user_biases(dict):
    src_list = []
    for x in sorted(list(dict.items()), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
        src_list.append((x[0], sum(x[1])/len(x[1])))
    return src_list[:3]