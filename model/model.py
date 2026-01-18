import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()

    def get_date_range(self):
        return DAO.get_date_range()

    def populate_dd(self):
        categorie = DAO.get_category()
        return categorie
    def build_graph(self, cat, start, end):
        prodotti = DAO.get_nodes(cat)
        for product in prodotti:
            self.G.add_node(product)
        prodotti_range_pesi = DAO.get_pesi(str(start), str(end))
        for v in self.G.nodes:
            for u in self.G.nodes:
                if v.id != u.id:
                    if v.id in prodotti_range_pesi and u.id in prodotti_range_pesi:
                        peso_arco = int(prodotti_range_pesi[v.id] + prodotti_range_pesi[u.id])
                        if prodotti_range_pesi[v.id] > prodotti_range_pesi[u.id]:
                            self.G.add_edge(v, u, peso=peso_arco)
                        elif prodotti_range_pesi[v.id] < prodotti_range_pesi[u.id]:
                            self.G.add_edge(u, v, peso=peso_arco)
                        elif prodotti_range_pesi[v.id] == prodotti_range_pesi[u.id]:
                            self.G.add_edge(v, u, peso=peso_arco)
                            self.G.add_edge(u, v, peso=peso_arco)

        return self.G.number_of_nodes(), self.G.number_of_edges()

    def best_prod(self):
        best_prodotti = {}
        for v in self.G.nodes:
            somma_in = 0
            somma_out = 0
            archi_in = self.G.in_edges(v)
            archi_out = self.G.out_edges(v)
            for arco in archi_in:
                somma_in += self.G[arco[0]][arco[1]]['peso']
            for arco in archi_out:
                somma_out += self.G[arco[0]][arco[1]]['peso']
            best_prodotti[v] = somma_out - somma_in
        lista_best_prodotti = sorted(best_prodotti.items(), key=lambda item: item[1], reverse=True)
        best_prodotti_ordinato = dict(lista_best_prodotti[0:5])
        return best_prodotti_ordinato

    def percorso(self, nodo_in, nodo_fin, lunghezza_cammino):
        
        self.vincolo_lunghezza = int(lunghezza_cammino)
        self.vincolo_fine = nodo_fin
        self.best_path = []
        self.best_score = 0

        parziale = [nodo_in]

        visitati = {nodo_in.id}

        peso_iniziale = 0

        self.ricorsione_percorso(parziale, visitati, peso_iniziale)

        return self.best_path, self.best_score

    def ricorsione_percorso(self, parziale, visitati, score_corrente):
        
        if self.vincolo_lunghezza <= len(parziale) and parziale[-1] == self.vincolo_fine and score_corrente > self.best_score:
            self.best_score = score_corrente
            self.best_path = list(parziale)

        for arco_out in self.G.out_edges(parziale[-1]):
            if arco_out[1].id in visitati:
                continue

            visitati.add(arco_out[1].id)

            parziale.append(arco_out[1])

            score = self.G[arco_out[0]][arco_out[1]]['peso']

            self.ricorsione_percorso(parziale, visitati, score_corrente + score)

            parziale.pop()
            visitati.remove(arco_out[1].id)
