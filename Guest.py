class Guest:
    def __init__(self, p_id):
        self._id = p_id
        self.cart = []

    def add_to_cart(self, good_id, name, price, count):
        if good_id not in list(map(lambda x: x[0], self.cart)):
            self.cart.append([good_id, name, price, count])
        else:
            for art in self.cart:
                if art[0] == good_id:
                    art[-1] = count + art[-1]

    def get_full_price(self):
        full_price = 0
        for art in self.cart:
            full_price += art[-1]*art[-2]
        return full_price

    def look_into_cart(self):
        return self.cart

    def remove_from_cart(self, good_id):
        for art in self.cart:
            if art[0] == good_id:
                self.cart.remove(art)


if __name__ == '__main__':
    g = Guest('000')
    g.add_to_cart(2, 'qqq', 20, 3)
    g.add_to_cart(1, 'www', 30, 1)
    g.remove_from_cart(1)
    print(g.look_into_cart())
