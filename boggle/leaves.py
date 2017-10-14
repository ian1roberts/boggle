'''
Created on 14 Oct 2017

@author: ian
'''
class Leaves(object):
    def __init__(self, tier, parent, loc, moves):
        self.tier = tier
        self.parent = parent
        self.loc = loc
        self.moves = moves
        
        # record paths that leaf is in
        self.paths = set()
        
    def __hash__(self):
        return hash((self.tier, self.loc))
        
    def __str__(self):
        return "T:{} P:{} L:{} M:{}".format(self.tier, repr(self.parent), self.loc, self.moves)
        
    def __contains__(self, pk):
        return True if pk in self.paths else False
    
    def __eq__(self, leaf):
        if isinstance(leaf, Leaves):
            return self.parent == leaf.parent and self.loc == leaf.loc
        
    def __lt__(self, leaf):
        if isinstance(self, leaf):
            return self.tier < leaf.tier
    
    @property
    def is_root(self):
        return True if self.tier==0 and self.parent==0 else False
    
    @property
    def is_valid(self, pk):
        return False if pk in self else True
    
