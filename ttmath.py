from operator import mul
from functools import cache, reduce

def probability(k,p):
  """Calculates the probality of having k successful Bernoulli trials out of a total of n based on a recursive formula for the Poisson binomial distribution.
  
  Keyword arguments:
    k -- the number of necessary successful trials
    p -- the list of probabilities for success of each Bernoulli distributed random variable; each probability has to be in the interval [0,1)
  """
  def _t_pb(i,p):
    pdemphi=[(aP/(1-aP))**i for aP in p]
    #print(p)
    #print(pdemphi)  
    return sum(pdemphi)

  if k == 0:
    emp = [1 - aP for aP in p]
    return reduce(mul, emp, 1)
  else:
    prb_sum = 0
    for i in range(1,k+1):      
      prb_sum = prb_sum + ((-1)**(i-1)) * probability(k-i,p) * _t_pb(i,p)
    return prb_sum/k

def calculateExpectedValue(densityGraph):
  return sum([k*p for k,p in densityGraph])
  
if __name__ == "__main__":
  pass