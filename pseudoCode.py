#Défintion des variables 
# s -> configuration actuelle du plateau (temps t)
# s0 -> configuration du plateau a t+1, lorsque l'action de déplacement a été faite = AFTER STATE
# s00 -> configuration du plteau a t+2, une nouvelle tuile est ajoutée 
# r -> reward : 
# a -> action réalisée (G/D/H/B)
# P(x) -> fonction de transition 
# R(x) -> fonction de reward 


def playGame() :
    score = 0
    s = INITIALIZE GAME STATE
    while (not IS TERMINAL STATE(s)):
        a =  arg maxa0∈A(s) EVALUATE(s, a0)
        r, s0, s00 = MAKE MOVE(s, a)
    if LEARNING ENABLED :
        LEARN EVALUATION(s, a, r, s0, s00)
    score = score + r
    s = s00
    return score

# for a given state s ∈ S and action a ∈ A(s) returns a received reward and an observed state transition
def makeMove(s,a):
    s0, r = COMPUTE AFTERSTATE(s, a)
    s00 = ADD RANDOM TILE(s0)
    return (r, s0, s00)

#Les couples de méthodes ne se basent pas sur les memes configurations de départ 

#EVALUATE 
# attempts to measure the utility of taking each possible action a ∈ A(s) in the current state s
# moves are selected to maximize the value returned by this function


# LEARN EVALUATE 
# adjusts the evaluation function on the basis of the observed experience represented by a tuple (s, a, r, s0, s00)


#The action evaluation function and Q-LEARNING ->  Evaluating actions
def evaluate(s,a):
    return Va(s)

def learnEvaluation(s, a, r, s0, s00):
    vnext = maxa0∈A(s00) Va0 (s00)
    Va(s) = Va(s) + α(r + vnext − Va(s))

#The state evaluation function and TD(0) ->  Evaluating states
#évaluer les états dans lesquels ils aboutissent avec la fonction de valeur d'état V (s)
#méthode plus lente car doit évaluer tous les coups possibles à chaque fois
def evaluate(s,a):
    s0, r = COMPUTE AFTERSTATE(s, a)
    S00 = ALL POSSIBLE NEXT STATES(s0)
    return r + (somme s00∈S00) P(s, a, s00)V (s00)

def learnEvaluation(s, a, r, s0, s00):
    V (s) = V (s) + α(r + V (s00) − V (s))

#The afterstate evaluation function ->  Evaluating afterstates
# evaluate moves can be regarded as a combination of the action evaluation and the state evaluation 
# updates the value of the recently observed afterstate
def evaluate(s,a):
    s0, r = COMPUTE AFTERSTATE(s, a)
    return r + V(s0)

def learnEvaluation(s, a, r, s0, s00):
    #determining the next action that would be taken
    anext = arg maxa0∈A(s00) EVALUATE(s00, a0)
    #compute the next reward and the new afterstate
    s0next, rnext = COMPUTE AFTERSTATE(s00, anext)
    V (s0) = V (s0) + α(rnext + V (s0next) − V (s0))

# n-tuple network
# For a given board state s, it calculates the sum of values returned by the individual n-tuples