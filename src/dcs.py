

def sgn(value):
    if value == 0:
        return 0
    elif value > 0:
        return +1
    else:
        return -1

class Vat:
    # could also be called Vat I guess
    def __init__(self, how0):
        # labels tags by gem
        self.tags = dict()
        # labels ilks by identifiers
        self.ilks = dict()
        # labels urns by identifiers
        self.urns = dict()
        # add a vox
        self.vox = Vox(wut=1.0, par=1.0, way=1.0, how=how0, tau=0.0)
        # add a (stopped) timesource
        self.set_era(lambda : 0)

    def set_era(self, era):
        self.era = era
        # any component that uses era goes here:
        self.vox.era = era
        
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
        
        
        
    def form(self, ilk_id, gem):
        if ilk_id in self.ilks:
            raise ValueError("Ilk id already taken!")
        self.ilks[ilk_id] = Ilk(gem)

    def mark(self, gem, tag, zzz):
        self.tags[gem].tag = tag
        self.tags[gem].zzz = zzz

    def tell(self, wut):
        # update DAI/USD price
        self.vox.wut = wut
                              
    def _next_urn_id(self):
        return list(filter(lambda id: not id in self.urns.keys(), range(1, len(self.urns.keys())+2)))[0]
    
class Tag:
    def __init__(self):
        self.tag = 0
        self.zzz = 0
    
class Ilk:
    def __init__(self, gem):
        self.gem = gem
        self.lax = 0
        self.mat = 1.0
        self.axe = 1.0
        self.hat = 0.0
        self.tax = 1.0
        self.chi = 1.0
        self.rho = 0
        self.rum = 0.0
        # instead of using ilk.jar:
        self.balance = 0.0
            
class Urn:
    def __init__(self, ilk_id, lad):
        self.ilk = ilk_id
        self.lad = lad
        self.art = 0
        self.ink = 0
        # instead of cat, use rid to record whether or not riddance is triggered
        self.rid = False

class Vox:
    def __init__(self, wut, par, way, how, tau):
        self.wut = wut
        self._par = par
        self._way = way
        self.how = how
        self.tau = tau
        
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
        age = self.era() - self.tau
        wag = self.how * age

        self._par *= self._way**age
        self._way = self.inj(self.prj(self._way) + sgn(self._par - self.wut)*wag)

        self.tau = self.era()
        
    def par(self):
        self.prod()
        return self._par
    
    def way(self):
        self.prod()
        return self._way
 
