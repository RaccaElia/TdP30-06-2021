import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        nodi = self._model.nodi()
        self._view._ddlocalizzazione.options = list(map(lambda x: ft.dropdown.Option(x), nodi))
        self._view.txtOut.controls.append(ft.Text(f"nodi: {self._model.grafoDetails()[0]}, archi: {self._model.grafoDetails()[1]}"))

    def handle_dettagli(self, e):
        vicini = self._model.getAdiacenti(self._view._ddlocalizzazione.value)
        self._view.txtOut.controls.append(ft.Text(f"nodi adiacenti a {self._view._ddlocalizzazione.value}"))
        for nodo in vicini:
            self._view.txtOut.controls.append(ft.Text(f"{nodo[0]}\t\t{nodo[1]}"))
        self._view.update_page()

    def handle_search(self, e):
        sol, costo = self._model.cercaPercorso(self._view._ddlocalizzazione.value)
        self._view.txtOut2.controls.append(ft.Text(f"Percorso massimo ha il costo {costo}"))
        for arco in sol:
            self._view.txtOut2.controls.append(ft.Text(f"{arco[0]} --> {arco[1]}"))
        self._view.update_page()
