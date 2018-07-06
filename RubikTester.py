from Rubik2x2 import *
import numpy as np
import random
import time
import math
from NeuroEvolve import *


nn=NeuroES(72,12,softmax)
nn.add_layer(42,relu)
nn.completed_network()
#nn.draw()

winner=[]
winner=[float(x) for x in winner]

nn.set_weights(winner)

cube=Rubik()
cube.reset()
print cube.shuffle(1)
i=0
while True:
    a = cube.get_binary_cube()
    o = nn.evaluate(a)
    t = np.argmax(o)
    cube.move(t)
    k = cube.get_reward()
    print k
    if k>=99:
        print "solved in",i
        break

    i+=1