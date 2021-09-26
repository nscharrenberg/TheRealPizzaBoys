class Pizza:
    def __init__(self, id: str, name: str, isVeggy: bool, price: float):
        self.id = id
        self.name = name
        self.isVeggy = isVeggy
        self.price = price

    @staticmethod
    def deserialize(pizza_d: dict):
        return Pizza(**pizza_d)

    def __repr__(self):
        return f"Pizza {self.name}, {self.price}"
