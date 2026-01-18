from dataclasses import dataclass

@dataclass
class Product:
    id : int
    product_name : str
    list_price : float


    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.product_name < other.product_name

    def __str__(self):
        return f"id: {self.id} | nome: {self.product_name} | prezzo: {self.list_price}"

    def __hash__(self):
        return hash(self.id)