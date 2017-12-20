class LimitOrder():
    def __init__(self, lad, base, quote, sense, quantity, limit):
        self.lad = lad
        self.base = base
        self.quote = quote
        self.sense = sense
        self.quantity = quantity
        self.limit = limit


class LimitOrderMarket():
    # simple limit order book that trades all asset pairs (base/quote system), has order matching
    def __init__(self, vault):
        self.id = id
        self.vault = vault
        # buys will be kept in descending order
        self.buys = []
        # sells will be kept in ascending order
        self.sells = []
        return

    def escrow(self, lad, gem, amt):
        gem.transferFrom(lad, self.vault.id, amt)
        
    
    def _pos(self, sense, limit):
        if sense == "Buy":
            for (i, price) in enumerate([order.limit for order in self.buys]):
                if limit > price:
                    return i
            # reached back of the book:
            return len(self.buys)
        if sense == "Sell":
            for (i, price) in enumerate([order.limit for order in self.sells]):
                if limit < price:
                    return i
            # reached back of the book:
            return len(self.sells)
    
    def make(self, order):
        if order.sense == "Buy":
            self.escrow(order.lad, order.quote, order.quantity*order.limit)
            self.buys.insert(self._pos("Buy", order.limit), order)
        if order.sense == "Sell":
            self.escrow(order,lad, order.base, order.quantity)
            self.sells.insert(self._pos("Sell", order.limit), order)
        self._match()

    def _match(self):
        if self.buys[0] < self.sells[0]:
            return
        else:
            # match top buy to top sell:
        
        
