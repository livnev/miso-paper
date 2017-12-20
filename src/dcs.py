from eth import Token, Vault
#from collections import defaultdict

def sgn(value):
    if value == 0:
        return 0
    elif value > 0:
        return +1
    else:
        return -1

class Vat:
    # could also be called Vat I guess
    def __init__(self, how0, dai, sin):
        self.dai = dai
        self.sin = sin
        # add a (stopped) timesource
        self.era = lambda : 0
        # labels tags by gem
        self.tags = dict()
        # labels ilks by identifiers
        self.ilks = dict()
        # labels urns by identifiers
        self.urns = dict()
        # add a vox
        self.vox = Vox(self, par=1.0, how=how0)
        # add a tap (or vow)
        self.tap = Tap(self, Vault())

        
    def drip(self, ilk_id):
        age = self.era() - self.ilks[ilk_id].rho
        chi = self.ilks[ilk_id].chi * (self.ilks[ilk_id].tax**age)
        dew = self.ilks[ilk_id].rum * (chi - self.ilks[ilk_id].chi)
        # dai and sin get minted...
        self.ilks[ilk_id].chi = chi
        self.ilks[ilk_id].rho = self.era()
        
    def chi(self, ilk_id):
        self.drip(ilk_id)
        return self.ilks[ilk_id].chi

    def din(self, ilk_id):
        return self.ilks[ilk_id].rum * self.chi(ilk_id)
    
    def tab(self, urn_id):
        return self.urns[urn_id].art * self.chi(self.urns[urn_id].ilk)
    
    def feel(self, urn_id):
        if not urn_id in self.urns:
            raise ValueError("No such urn!")
        ilk = self.ilks[self.urns[urn_id].ilk]
        tag = self.tags[ilk.gem]
        pro = self.urns[urn_id].ink * tag.tag
        con = self.tab(urn_id) * self.vox.par()
        # min is a python built in, so we use mon instead ;)
        mon = con * ilk.mat
        if self.urns[urn_id].rid and self.urns[urn_id].ink == 0:
            # Riddance triggered and started
            return "Dread"
        elif self.urns[urn_id].rid:
            # Riddance triggered
            return "Grief"
        elif (tag.zzz + ilk.lax < self.era()) or pro < mon:
            # Locked assetcoin value below issuance times riddance ratio
            return "Panic"
        elif tag.zzz < self.era():
            # Assetcoin price limbo exceeded limit
            return "Worry"
        elif self.din(self.urns[urn_id].ilk) > ilk.hat:
            # Issuance ceiling exceeded
            return "Anger"
        else:
            # No problems
            return "Pride"
        
        
        
    def form(self, ilk_id, jar, gem):
        if ilk_id in self.ilks:
            raise ValueError("Ilk id already taken!")
        self.ilks[ilk_id] = Ilk(gem, jar)
        self.ilks[ilk_id].jar = jar

    def mark(self, gem, tag, zzz):
        self.tags[gem].tag = tag
        self.tags[gem].zzz = zzz

    def tell(self, wut):
        # update DAI/USD price
        self.vox.wut = wut

    def bite(self, urn_id):
        # Sai-style bite, uses a tap
        # TODO: make generic, a la Dai
        if self.feel(urn_id) != "Panic":
            raise ValueError("Urn not fit for riddance!")

        self.urns[urn_id].rid = True
        
        rue = self.tab(urn_id)
        self.sin.mint(self.tap.vault.id, rue)
        #self.tap.balances[self.sin] += rue
        
        ilk = self.ilks[self.urns[urn_id].ilk]
        gem = ilk.gem
        axe = ilk.axe
        owe = (rue * axe * self.vox.par()) / self.tags[gem]

        if owe > self.urns[urn_id].ink:
            owe = self.urns[urn_id].ink

        self.urns[urn_id].ink -= owe
        gem.transferFrom(ilk.jar, self.tap.vault.id, owe)
        #ilk.balance -= owe
        #self.tap.balances[gem] += owe
        self.urns[urn_id].art = 0
                                      
    def _next_urn_id(self):
        return list(filter(lambda id: not id in self.urns.keys(), range(1, len(self.urns.keys())+2)))[0]

    
class Tag:
    def __init__(self):
        self.tag = 0
        self.zzz = 0
    
class Ilk:
    def __init__(self, gem, jar):
        self.gem = gem
        self.lax = 0
        self.mat = 1.0
        self.axe = 1.0
        self.hat = 0.0
        self.tax = 1.0
        self.chi = 1.0
        self.rho = 0
        self.rum = 0.0
        self.jar = jar
        # instead of using ilk.jar:
        #self.balance = 0.0
            
class Urn:
    def __init__(self, ilk_id, lad):
        self.ilk = ilk_id
        self.lad = lad
        self.art = 0
        self.ink = 0
        # instead of cat, use rid to record whether or not riddance is triggered
        self.rid = False

class Vox:
    def __init__(self, vat, par, how):
        # in Dai code vox doesn't know vat
        self.vat = vat
        self.wut = par
        self._par = par
        self._way = how
        self.how = how
        self.tau = self.vat.era()
        
    def inj(self, x):
        if x >= 0:
            return x + 1
        else:
            return 1/(1-x)
        return
    
    def prj(self, x):
        if x >= 1:
            return x - 1
        else:
            return 1 - 1/x
        
    def prod(self):
        age = self.vat.era() - self.tau
        wag = self.how * age

        self._par *= self._way**age
        self._way = self.inj(self.prj(self._way) + sgn(self._par - self.wut)*wag)

        self.tau = self.vat.era()
        
    def par(self):
        self.prod()
        return self._par
    
    def way(self):
        self.prod()
        return self._way
 
class Tap:
    # multi-gem tap
    def __init__(self, vat, vault):
        self.vat = vat
        self.vault = vault
        self.dai = self.vat.dai
        self.sin = self.vat.sin
        self.gap = 0
        #self.balances = defaultdict(lambda : 0.0)

    def joy(self):
        return self.dai.balanceOf(self.vault)
        #return self.balances[self.vat.dai]
    
    def woe(self):
        return self.sin.balanceOf(self.vault)
        #return self.balances[self.vat.sin]
    
    def fog(self, gem):
        return gem.balanceOf(self.vault)
        #return self.balances[gem]
        
    def heal(self):
        wad = min(self.joy(), self.woe())
        # annihilate:
        self.dai.burn(self, self.vault.id, wad)
        self.sin.burn(self, self.vault.id, wad)
        #self.balances[self.vat.dai] -= wad
        #self.balances[self.vat.sin] -= wad

        
