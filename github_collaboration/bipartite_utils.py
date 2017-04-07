import networkx as nx
from networkx.drawing import draw


def create_graph_from_user_info(user_info):
    """
    Create a bipartie graph with User and Repos Nodes
    @user_info: dict with users as keys and repos as values
    """

    users = list(user_info.keys())
    repositories = set()
    for user_repos in user_info.itervalues():
        repositories.update(user_repos)

    graph = nx.Graph()
    graph.add_nodes_from(users, bipartite=0)
    graph.add_nodes_from(repositories, bipartite=1)


    for user, repos in user_info.iteritems():
        for repo in repos:
            graph.add_edge(user, repo)

    return graph


def _get_node_labels(graph):
    return {
       node: node if desc["bipartite"] == 0 else node.name
       for node, desc in graph.nodes(data=True)
    }


def show_graph(graph):
    colors  = [
        "red" if desc["bipartite"] == 0 else "green"
        for node, desc in graph.nodes(data=True)
    ]

    draw(
        graph,
        node_color=colors,
        labels=_get_node_labels(graph),
        node_size=200,
        font_size=10,
        with_labels=True,
    )
