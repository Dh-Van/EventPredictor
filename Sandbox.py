from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

T176 = [2.0, 0,0]
T4909 = [1.3333333333333333, 0.4714045207910317]
T88 = [1.3333333333333333, 0.4714045207910317]

def get_prob(data, lower, upper):
    upper_limit = norm(loc = T4909[0], scale = T4909[1]).cdf(upper)
    lower_limit = norm(loc = T4909[0], scale = T4909[1]).cdf(lower)
    prob = upper_limit - lower_limit
    if(prob < 0.001): prob = 0
    return prob

counter = 0
for i in range(8):
    prob = get_prob(T4909, counter, counter + 1)
    print("week ", counter, ": ", prob * 100)
    counter += 1


