import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self._list_rifugi = []
        self.get_all_rifugi()

        self._dict_rifugi = {}
        for r in self._list_rifugi:
            self._dict_rifugi[r.id] = r

        self.G = None

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G = nx.Graph()

        connessioni = DAO.readAllConnessioni(self._dict_rifugi, year)

        for c in connessioni:
            self.G.add_node(c.r1)
            self.G.add_node(c.r2)
            self.G.add_edge(c.r1, c.r2)

        #print(self.G)

    def get_all_rifugi(self):
        self._list_rifugi = DAO.readAllRifugi()

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        return self.G.nodes()

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        num_meighbors = len(list(self.G.neighbors(node)))
        return num_meighbors

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        num = len(list(nx.connected_components(self.G)))
        return num

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        result_bfs = self.get_reachable_bfs_tree(start)

        return result_bfs


    def get_reachable_bfs_tree(self, start):
        bfs_tree = nx.bfs_tree(self.G, start)
        list_visited = list(bfs_tree.nodes())
        list_visited.remove(start)

        return list_visited