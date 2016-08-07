import matplotlib.pyplot as plt


def get_rid_unchanged(df):
    graph = df.reset_index()
    i = 0
    n = 1
    length = len(graph)
    #print(graph)
    while i < length:
        # print(len(graph))
        while graph.equity[i] == graph.equity[n]:
            # print(graph.equity[i],graph.equity[n])
            graph = graph.drop(n)
            n += 1
            if n >= length: break
            # print(i)
            # print(n)
        i = n
        n += 1
        if n >= length: break
        # print(i)
    graph = graph.set_index('date')
    return graph


def plot_return_beta(df):
    df.plot(y = ['return', 'beta'])
    plt.show()