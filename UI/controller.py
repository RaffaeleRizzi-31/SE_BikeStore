from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_cat = None
        self._current_prod_in = None
        self._current_prod_fin = None

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        if self._current_cat is None:
            self._view.show_alert("Selezionare prima una categoria")
            return
        n_nodi, n_archi = self._model.build_graph(self._current_cat, self._view.dp1.value, self._view.dp2.value)
        self.populate_dd_prod()
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {self._view.dp1.value}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {self._view.dp2.value}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {n_archi}"))
        self._view.update()
    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        best_prodotti = self._model.best_prod()
        self._view.txt_risultato.controls.append(ft.Text(f""))
        self._view.txt_risultato.controls.append(ft.Text(f"I cinque prodotti più venduti sono:"))
        for prodotto, score in best_prodotti.items():
            self._view.txt_risultato.controls.append(ft.Text(f"{prodotto.product_name} with score {score}"))
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        if self._view.txt_lunghezza_cammino.value == "":
            self._view.show_alert("Selezionare prima la lunghezza del cammino")
            return
        elif self._current_prod_in is None:
            self._view.show_alert("Selezionare prima il prodotto iniziale")
            return
        elif self._current_prod_fin is None:
            self._view.show_alert("Selezionare prima il prodotto finale")
            return
        best_path, best_score = self._model.percorso(self._current_prod_in, self._current_prod_fin, self._view.txt_lunghezza_cammino.value)
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Cammino migliore:"))
        for prod in best_path:
            self._view.txt_risultato.controls.append(ft.Text(f"{prod.product_name}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Score: {best_score}:"))
        self._view.update()

    def populate_dd_category(self):
        categorie = self._model.populate_dd()
        self._view.dd_category.options.clear()
        for id,nome in categorie.items():
            option = ft.dropdown.Option(text=str(nome), data=id)
            self._view.dd_category.options.append(option)
        self._view.update()

    def get_selected_cat(self,e):
        selected_option = e.control.value
        if selected_option is None:
            self._current_cat = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_cat = found

    def populate_dd_prod(self):
        prodotti = self._model.G.nodes
        self._view.dd_category.options.clear()
        for prod in sorted(prodotti):
            option = ft.dropdown.Option(text=prod.product_name, data=prod)
            self._view.dd_prodotto_iniziale.options.append(option)
            self._view.dd_prodotto_finale.options.append(option)
        self._view.update()

    def get_selected_prod_in(self,e):
        selected_option = e.control.value
        if selected_option is None:
            self._current_prod_in = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_prod_in = found

    def get_selected_prod_fin(self,e):
        selected_option = e.control.value
        if selected_option is None:
            self._current_prod_fin = None
            return
        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break
        self._current_prod_fin = found
