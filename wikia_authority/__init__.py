class MinMaxScaler:
    """
    Scales values from 0 to 1 by default
    """

    def __init__(self, vals, enforced_min=0, enforced_max=1):
        self.min = min(vals)
        self.max = max(vals)
        self.enforced_min = enforced_min
        self.enforced_max = enforced_max
        print 'min', str(self.min)
        print 'max', str(self.max)
        print 'enforced_min', str(self.enforced_min)
        print 'enforced_max', str(self.enforced_max)

    def scale(self, val):
        denominator = self.max - self.min
        if denominator == 0:
            denominator = 1.0
        return (((self.enforced_max - self.enforced_min) * (val - self.min)) /
                denominator) + self.enforced_min


def log(*args):
    """TODO: Use a real logger"""
    print ' '.join([str(arg) for arg in args])
