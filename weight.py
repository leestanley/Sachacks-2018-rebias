from datascience import Table
bias = Table().read_table("bias.csv").select("News Source", "Horizontal Rank")


def weighter(currweight, source, rating):
    horirank = bias.where("News Source", source).column("Horizontal Rank").item(0)
    return currweight + (((rating - 5) / 10) * horirank)
