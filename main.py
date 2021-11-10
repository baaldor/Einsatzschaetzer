from operator import mul
from functools import reduce

def t_pb(i,p):
  pdemphi=[(aP/(1-aP))**i for aP in p]
  #print(p)
  #print(pdemphi)  
  return sum(pdemphi)

def probability(k,p):
  """Calculates the probality of having k successful Bernoulli trials out of a total of n based on a recursive formula for the Poisson binomial distribution.
  
  Keyword arguments:
    k -- the number of necessary successful trials
    p -- the list of probabilities for success of each Bernoulli distributed random variable
  """
  if k == 0:
    emp = [1 - aP for aP in p]
    return reduce(mul, emp, 1)
  else:
    prb_sum = 0
    for i in range(1,k+1):      
      prb_sum = prb_sum + ((-1)**(i-1)) * probability(k-i,p) * t_pb(i,p)
    return prb_sum/k


# Variante auf Basis von Schätzwerten der letzten Saison
#     Henry, Bully, Phil, Daniel, Maik, Niclas, Martin
#myPs=[0.9,  0.62,  0.54, 0.31,   0.46, 0.69,  0.77]

myPs=[
  #Lukas
  0.9,

  #Henry
  0.6,

  #Frank
  0.22,

  #Torsten
  0.1,
    
  #Maik
  0.5,
  
  #Niclas
  0.33,
  
  #Martin
  0.9,
  
  #Wolfgang
  0.66  
  ]

'''myPs=[
  #Lukas
  0.9,

  #Henry
  0.5,

  #Marco
  0.9,

  #Phil
  #0.2,
    
  #Maik
  0.5,
  
  #Niclas
  0.4,
  
  #Martin
  0.33,
  
  #Jonathan
  0.75,

  #Jarne
  0.75
 ]'''

#Variante mit Thommy und Theo (konservativ: Theo keine Auswärtsspiele)
#     Thommy, Henry, Bully, Phil, Daniel, Maik, Niclas, Martin, Theo
#myPs=[0.9,   0.9,   0.62,  0.54, 0.31,   0.46, 0.33,   0.2,    0.5]

mindestspielstaerke = 3
sollspielstaerke = 4
prb_sollspielstaerke_erreicht = 0
prb_mindestspielstaerke_erreicht = 0
prb = 0
erwartungswert = 0

print("los gehts...")
print("Wahrscheinlichkeit für das Ereignis, dass genau K Spieler Zeit haben;")

for k in range(0,len(myPs)+1):
  prb_of_k_successful_trials = probability(k,myPs)
  erwartungswert = erwartungswert + k*prb_of_k_successful_trials
  if k >= mindestspielstaerke:
    prb_mindestspielstaerke_erreicht = prb_mindestspielstaerke_erreicht + prb_of_k_successful_trials
  if k >= sollspielstaerke:
    prb_sollspielstaerke_erreicht = prb_sollspielstaerke_erreicht + prb_of_k_successful_trials
  print("P(K=" + str(k) + ")=" + str(round(100*prb_of_k_successful_trials, 1)) + " %")

print("Wahrscheinlichkeit, dass min. "+ str(sollspielstaerke) + " Spieler Zeit haben: " + str(round(100*prb_sollspielstaerke_erreicht, 1)) + " %")
print("Wahrscheinlichkeit, dass min. "+ str(mindestspielstaerke) + " Spieler Zeit haben: " + str(round(100*prb_mindestspielstaerke_erreicht, 1)) + " %")
print("Erwartungswert: " + str(round(erwartungswert, 1)))