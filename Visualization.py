import matplotlib.pyplot as plt


def get_rid_unchanged_equity(df):
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

def get_rid_unchanged(df,fuckoff):
    assert type(fuckoff) is str
    graph = df.reset_index()
    i = 0
    n = 1
    length = len(graph)
    #print(graph)
    while i < length:
        # print(len(graph))
        while graph[fuckoff][i] == graph[fuckoff][n]:
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
    graph = graph.set_index('index')
    return graph

def get_rid_Zero(df,fuckoff_column):
    assert type(fuckoff_column) is str
    df = df.reset_index()
    ll = []
    for i in range(len(df)-1):
        if df[fuckoff_column][i] == 0:
            ll.append(i)
    df = df.drop(ll)
    df = df.set_index('index')
    return df

def plot_return_beta(df):
    df.plot(y = ['return', 'beta'])
    plt.show()