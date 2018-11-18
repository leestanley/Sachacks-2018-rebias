from datascience import Table
bias = Table().read_table("bias.csv").select("News Source", "Horizontal Rank")
# print(bias)
userweight = 50


def weighter(currweight, source, rating):
    horirank = bias.where("News Source", source).column("Horizontal Rank").item(0)
    # print(horirank)
    return currweight + (((rating - 5) / 10) * horirank)


#userweight = weighter("LA Times", 2)
#userweight = weighter("LA Times", 10)
# print(userweight)
