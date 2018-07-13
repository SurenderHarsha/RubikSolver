from Rubik2x2 import *
from NeuroEvolve import *
import numpy as np


nn=NeuroES(72,4,sigmoid)
nn.add_layer(28,relu)
nn.completed_network()
#nn.draw()




pop_size = 100
cr_rate = 0.2
m_rate = 1



gene_size=nn.get_weight_count()
print gene_size
### DATA CREATION AND PROCESSING


training_data=[]
training_data_y=[]

def left_shift(arr,num):
    for i in range(num):
        a=arr[0]
        for j in range(len(arr)-1):
            arr[j]=arr[j+1]
        arr[-1]=a
    return arr

#def create_data():
limit=12
cube=Rubik()
cube.reset()
a=cube.get_binary_cube()
for i in range(5):

    training_data.append(a)
    training_data_y.append([0,0,0,0])
    #a=left_shift(a,12)
    break
count=0
for i in range(1,5):
    #print "Making"
    while True:
        c = '{0:04b}'.format(i)
        #print c
        cube.reset()
        cube.shuffle(i)
        a=cube.get_binary_cube()
        l=a

        if count<limit:
            if l not in training_data:
                training_data.append(l)
                training_data_y.append([int(c[0]),int(c[1]),int(c[2]),int(c[3])])
                count+=1
        else:
            count=0
            if limit<800:
                limit=limit*7
            break

print len(training_data)

length=len(training_data)

# Initialize population of weights values between (0,1)
def gen_pop():
    pop = []
    for i in range(pop_size):
        weights = (np.random.uniform(size=gene_size)*2-1)
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
            if m_rate > random.randint(0, 500):
                c[j] = c[j]+(np.random.uniform()*2-1)
                #print "Mutated"
    return po


pop = gen_pop()
gen=0

while True:
    gen+=1
    n_pop = []
    i = 0
    while i < pop_size:
        #print i
        cand = pop[i]
        nn.set_weights(cand)
        av = 0
        for j in range(length):
            o=nn.evaluate(training_data[j])
            correct=0
            for k in range(len(o)):
                if o[k]==training_data_y[j][k]:
                    correct+=1
            correct=(float(correct)/4)*100
            av+=correct
        av=av/length
        n_pop.append([cand, av])
        if av >= 95:
            # print "DONE"
            #shuffle_rate += 1
            #print "Breakthrough"
            print cand

            #print cand
            import sys

            sys.exit()
        i += 1
    n_pop = sorted(n_pop, key=lambda x: x[1])
    n_pop = n_pop[::-1]
    best = n_pop[0][1]
    avg = 0
    # Calculate average perfomance through the population.
    for i in range(len(n_pop)):
        avg += n_pop[i][1]
    avg = avg / float(pop_size)
    pop = crossover(n_pop)
    pop = mutation(pop)
    # print pop
    # if gen%50==0:
    print gen, best, avg

#print left_shift([1,2,3,4,5],5)