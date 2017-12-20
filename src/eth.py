from os import urandom
from collections import defaultdict

class Address():
    # addresses are 20 bytes = 160 bits
    # like in Ethereum
    def __init__(self, bytes=None):
        if bytes != None:
            self.bytes = bytes

        else:
            self.bytes = urandom(20)
    def __eq__(self, other):
        return self.bytes == other.bytes
    def __hash__(self):
        return int.from_bytes(self.bytes, byteorder='big')
        #return int(self.bytes)
    def __repr__(self):
        return self.bytes.hex()


class BalanceError(Exception):
    pass

class Token():
    # token lives in an environment
    def __init__(self, name):
        self.name = name
        # balances indexed by ids
        self.balances = defaultdict(lambda : 0.0)

    def balanceOf(self, src):
        return balances[src]

    def transferFrom(self, src, dst, amt):
        if amt < 0:
            raise ValueError
        if self.balanceOf(guy) < amt:
            raise BalanceError
        self.balances[src] -= amt
        self.balances[dst] += amt

    def mint(self, guy, amt):
        if amt < 0:
            raise ValueError
        self.balances[guy] += amt

    def burn(self, guy, amt):
        if amt < 0:
            raise ValueError
        if self.balanceOf(guy) < amt:
            raise BalanceError
        self.balances[guy] -= amt
    

class Vault():
    def __init__(self, address=None):
        if address != None:
            self.id = address
        else:
            self.id = Address()
