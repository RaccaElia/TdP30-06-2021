import copy

import networkx as nx

from database.DAO import DAO
from database.DB_connect import DBConnect


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.soluzioneBest = []
        self.costoBest = 0
        localizzazioni = DAO.getLocalizzazioni()
        self.grafo.add_nodes_from(localizzazioni.keys())

        for arco in DAO.getArchi():
            self.grafo.add_edge(arco[0], arco[1], weight=arco[2])

    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def nodi(self):
        return self.grafo.nodes

    def getAdiacenti(self, nodo):
        ris = []
        for vicino in self.grafo.neighbors(nodo):
            ris.append((vicino, self.grafo[nodo][vicino]["weight"]))
        return ris

    def cercaPercorso(self, nodo):
        self.soluzioneBest = []
        self.costoBest = 0
        for vicino in self.grafo.neighbors(nodo):
            self.ricorsione([(nodo, vicino)])
        return self.soluzioneBest, self.costoBest

    def ricorsione(self, parziale):
        vicini = self.nodiVisitabili(parziale)
        if vicini == []:
            if self.calcolaCosto(parziale):
                print("best")
                self.soluzioneBest = copy.deepcopy(parziale)
        else:
            for nodo in vicini:
                last = parziale[-1][1]
                parziale.append((last, nodo))
                self.ricorsione(parziale)
                parziale.pop()

    def nodiVisitabili(self, lista):         #no archi ripetuti
        ris = []
        print(lista)
        ultimoNodo = lista[-1][1]
        for vicino in self.grafo.neighbors(ultimoNodo):
            if (ultimoNodo, vicino) not in lista:
                ris.append(vicino)
        print(ris)
        return ris

    def calcolaCosto(self, parziale):
        costo = 0
        for arco in parziale:
            costo += self.grafo[arco[0]][arco[1]]["weight"]
        if costo > self.costoBest:
            self.costoBest = costo
            return True
        return False