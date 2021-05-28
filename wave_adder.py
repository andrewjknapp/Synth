# Code written by 18alantom
# Full repo can be viewed at
# https://github.com/18alantom/synth

class WaveAdder:
    def __init__(self, *oscillators):
        self.oscillators = oscillators
        self.n = len(oscillators)
    
    def __iter__(self):
        [iter(osc) for osc in self.oscillators]
        return self
    
    def __next__(self):
        sum = 0
        for x in range(self.n):
            sum += next(self.oscillators[0][x])
        return sum / self.n    
        #return sum(next(osc) for osc in self.oscillators) / self.n