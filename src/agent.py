from collections import defaultdict

from dcs import Vat, Ilk, Urn, Tag

#TODO: work on liquidation (bite, auctions, etc.)
#TODO: work on "exogeneous signal" implementation
#TODO: work on market venue

class SimulationEnvironment:
    def __init__(self, vat, agents=dict()):
        # initialise basic environment
        # add a notion of time
        self._era = 0
        self.era = lambda : self._era
        # add a DCS:
        self.vat = vat
        self.vat.set_era(self.era)
        #
        # add exogeneous signals:
        # for every ilk in DCS.ilks, a time series for ILK/REF
        #
        #
        # add agents (indexed by id):
        self.agents = agents
        #
        # add venues:
        #
        #
    def let(self, agent_id):
        # lets the agent do everything he wants to do
        self.agents[agent_id].act(self)
    def step(self):
        # in a step, one by one let every agent do what they want to do
        for agent_id in self.agents:
            self.let(agent_id)
            # QUESTION: "synchronise" or not?
            self._era += 1
        

class Agent:
    def __init__(self, id):
        self.id = id
        # balances indexed by identifiers, default balance is 0.0
        self.balances = defaultdict(lambda : 0.0)
    def act(self, env):
        return

# now add classes for dcs agents, market agents (use multiple inheritance)
    

class DCSAgent(Agent):
    # any agent that can interact with the DCS
    # TODO fix inheritance signatures
    def __init__(self, id):
        super().__init__(id)
    
    def open(self, vat, urn_id, ilk_id):
        if urn_id in vat.urns:
            raise ValueError("Urn id is already taken!")
        if not ilk_id in vat.ilks:
            raise ValueError("No such ilk!")
        vat.urns[urn_id] = Urn(ilk_id, self.id)
        
        
    def lock(self, vat, urn_id, amt):
        if amt < 0:
            raise ValueError("Amount must be >= 0!")
        if not urn_id in vat.urns:
            raise ValueError("No such urn!")
        if vat.urns[urn_id].lad != self.id:
            raise ValueError("Not your urn!")
        if vat.feel(urn_id) in {"Grief", "Dread"}:
            raise ValueError("Cannot lock when riddance in process!")
        ilk_id = vat.urns[urn_id].ilk
        gem = vat.ilks[ilk_id].gem
        if self.balances[gem] < amt:
            raise ValueError("Not enough gem!")
        self.balances[gem] -= amt
        vat.ilks[ilk_id].balance += amt
        vat.urns[urn_id].ink += amt

    def free(self, vat, urn_id, amt):
        if amt < 0:
            raise ValueError("Amount must be >= 0!")
        if not urn_id in vat.urns:
            raise ValueError("No such urn!")
        if vat.urns[urn_id].lad != self.id:
            raise ValueError("Not your urn!")
        vat.urns[urn_id].ink -= amt
        if not vat.feel(urn_id) in {"Pride", "Anger"}:
            # roll back:
            vat.urns[urn_id].ink += amt
            raise ValueError("Urn is in a bad state!")
        ilk_id = vat.urns[urn_id].ilk
        gem = vat.ilks[ilk_id].gem
        vat.ilks[ilk_id].balance -= amt
        self.balances[gem] += amt

    def draw(self, vat, urn_id, amt):
        if amt < 0:
            raise ValueError("Amount must be >= 0!")
        if not urn_id in vat.urns:
            raise ValueError("No such urn!")
        if vat.urns[urn_id].lad != self.id:
            raise ValueError("Not your urn!")
        ilk_id = vat.urns[urn_id].ilk

        # PP calls it wad_chi, code calls it ink (ink/jam switch)
        huh = amt / vat.chi(ilk_id)
        
        vat.urns[urn_id].art += huh
        vat.ilks[ilk_id].rum += huh
        if not vat.feel(urn_id) == "Pride":
            # roll back:
            vat.urns[urn_id].art -= huh
            vat.ilks[ilk_id].rum -= huh
            raise ValueError("Urn is in a bad state!")
        # dai and sin get minted
        self.balances[vat.dai] += amt

    def wipe(self, vat, urn_id, amt):
        if amt < 0:
            raise ValueError("Amount must be >= 0!")
        if not urn_id in vat.urns:
            raise ValueError("No such urn!")
        if vat.urns[urn_id].lad != self.id:
            raise ValueError("Not your urn!")
        if vat.feel(urn_id) in {"Grief", "Dread"}:
            raise ValueError("Cannot lock when riddance in process!")
        if self.balances[vat.dai] < amt:
            raise ValueError("Not enough DAI!")
        ilk_id = vat.urns[urn_id].ilk

        # PP calls it wad_chi, code calls it ink (ink/jam switch)
        huh = amt / vat.chi(ilk_id)

        vat.urns[urn_id].art -= huh
        vat.ilks[ilk_id].rum -= huh
        if not vat.feel(urn_id) == "Pride":
            # roll back:
            vat.urns[urn_id].art += huh
            vat.ilks[ilk_id].rum += huh
            raise ValueError("Urn is in a bad state!")
        # dai and sin get minted
        self.balances[vat.dai] -= amt

    def shut(self, vat, urn_id):
        self.wipe(vat, urn_id, vat.tab(urn_id))
        self.free(vat, urn_id, vat.urns[urn_id].ink)
        del vat.urns[urn_id]

class Ernie(DCSAgent):
    # weird guy who tries to keep all of his gems locked in urns
    # he refrains from making too many urns though
    def __init__(self, id):
        super().__init__(id)

    def act(self, env):
        for gem in self.balances.keys():
            if self.balances[gem] > 0:
                possible_ilks = set(filter(lambda ilk_id: env.vat.ilks[ilk_id].gem == gem, env.vat.ilks.keys()))
                if possible_ilks != set():
                    ilk_id = possible_ilks.pop()
                    possible_urns = set(filter(lambda urn_id: env.vat.urns[urn_id].lad == self.id, env.vat.urns.keys()))
                    if possible_urns == set():
                        # must make a new urn for this gem
                        urn_id = env.vat._next_urn_id()
                        self.open(env.vat, urn_id, ilk_id)
                    else:
                        urn_id = possible_urns.pop()
                    self.lock(env.vat, urn_id, self.balances[gem])
        return
        
        
class LimitOrderMarket():
    # simple limit order book that trades all asset pairs, has order matching
    def __init__(self):
        return



eth = "ETH"
dai = "DAI"
vat1 = Vat(1.0)
vat1.dai = dai
vat1.form(1, eth)
vat1.tags[eth] = Tag()
# update eth price, expires in 1000 seconds
vat1.mark(eth, 300.0, 1000)

# make 3 Ernie agents each with the same balance
#balances1 = defaultdic(lambda : 0.0, {"ETH" : 5.0, "USD" : 100.0})
agents1 = {i: Ernie(i) for i in range(1,4)}
for agent_id in agents1:
    agents1[agent_id].balances["ETH"] = 5.0
    agents1[agent_id].balances["USD"] = 100.0

env1 = SimulationEnvironment(vat1, agents=agents1)
