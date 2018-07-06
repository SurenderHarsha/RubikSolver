from Rubik2x2 import *
import numpy as np
import random
import time
import math
from NeuroEvolve import *

nn=NeuroES(72,12,softmax)
nn.add_layer(42,relu)
#nn.add_layer(12,relu)
nn.completed_network()
#nn.draw()
#nn.init_rand_weights()


pop_size = 50
cr_rate = 0.4
m_rate = 1
consecutive=10
shuffle_rate=1

cube=Rubik()
cube.reset()
#cube.shuffle(30)


gene_size=nn.get_weight_count()
print gene_size
# Initialize population of weights values between (0,1)
def gen_pop():
    pop = []
    for i in range(pop_size):
        weights = (np.random.uniform(size=gene_size)*2-1)*2
        pop.append(weights)

    return pop


# The crossover of Top members, can be anything as long as new variations of best genes are available.
def crossover(po):
    pop = []
    topp = int(cr_rate * len(po))
    top = [po[x][0] for x in range(0, topp)]
    for i in range(0, topp):
        pop.append(top[i])
    j = 0
    s_topp = topp + (topp) / 2
    for i in range(topp, s_topp):
        a = top[j]
        b = top[j + 1]
        c = []
        for k in range(len(a)):
            c.append((a[k] + b[k]) / 2)
        j = j + 2
        pop.append(c)
    j = 0
    #print s_topp
    for i in range(pop_size - s_topp):
        k=random.randint(1,topp-1)

        j=random.randint(1,topp-1)
        s=[x for x in top[k]]      # x can be multiplied with some noise.
        b=[x for x in top[j]]      # x can be multiplied with some noise.
        r=[]
        sw=0
        for l in range(len(s)):
            if sw==0:
                r.append(s[l])
                sw=1
            else:
                r.append(b[l])
                sw=0
        pop.append(r)
    return pop


# Mutation , slightly mutate weights of some members.
def mutation(po):
    for i in range(len(po)):
        c = po[i]
        for j in range(len(c)):
            if m_rate > random.randint(0, 2000):
                c[j] = c[j]+(np.random.uniform()*2-1)
                #print "Mutated"
    return po


pop = gen_pop()
gen=0
i=0
while True:


    gen+=1
    n_pop = []
    i=0
    while i<pop_size:
        cand=pop[i]
        nn.set_weights(cand)
        av=0
        for j in range(consecutive):
            cube.reset()
            cube.shuffle(shuffle_rate)
            mvs=0
            while mvs<=20:
                a=cube.get_binary_cube()
                o=nn.evaluate(a)
                t=np.argmax(o)
                cube.move(t)
                k=cube.get_reward()

                if k>=100:
                    #print "DONE",i
                    #hello=nn.get_weights()
                    #print "Got one!"
                    break
                mvs+=1
            av+=k
        av=av/float(consecutive)
        n_pop.append([cand,av])
        if av>=99:
            #print "DONE"
            shuffle_rate+=1
            print "Breakthrough"
            if shuffle_rate>=12:
                print "DONE"
                print cand
                import sys
                sys.exit()
        i+=1
    n_pop = sorted(n_pop, key=lambda x: x[1])
    n_pop = n_pop[::-1]
    best=n_pop[0][1]
    avg = 0
    # Calculate average perfomance through the population.
    for i in range(len(n_pop)):
        avg += n_pop[i][1]
    avg = avg / float(pop_size)
    pop = crossover(n_pop)
    pop = mutation(pop)
    #print pop
    #if gen%50==0:
    print shuffle_rate,gen,best,avg
            #nn.clear_weights()
