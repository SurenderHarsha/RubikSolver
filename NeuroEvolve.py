
'''
Created by Surender Harsha.
June 24 2018
https://github.com/SurenderHarsha
'''


#Import Statements
import numpy
import math
import matplotlib.pyplot as plt


########################################################################################################################
# This function is created by @author: craffel
def draw_neural_net(ax, left, right, bottom, top, layer_sizes, layer_text=None):
    '''
    Draw a neural network cartoon using matplotilb.

    :usage:
        >>> fig = plt.figure(figsize=(12, 12))
        >>> draw_neural_net(fig.gca(), .1, .9, .1, .9, [4, 7, 2], ['x1', 'x2','x3','x4'])

    :parameters:
        - ax : matplotlib.axes.AxesSubplot
            The axes on which to plot the cartoon (get e.g. by plt.gca())
        - left : float
            The center of the leftmost node(s) will be placed here
        - right : float
            The center of the rightmost node(s) will be placed here
        - bottom : float
            The center of the bottommost node(s) will be placed here
        - top : float
            The center of the topmost node(s) will be placed here
        - layer_sizes : list of int
            List of layer sizes, including input and output dimensionality
        - layer_text : list of str
            List of node annotations in top-down left-right order
    '''
    n_layers = len(layer_sizes)
    v_spacing = (top - bottom) / float(max(layer_sizes))
    h_spacing = (right - left) / float(len(layer_sizes) - 1)
    ax.axis('off')
    # Nodes
    for n, layer_size in enumerate(layer_sizes):
        layer_top = v_spacing * (layer_size - 1) / 2. + (top + bottom) / 2.
        for m in range(layer_size):
            x = n * h_spacing + left
            y = layer_top - m * v_spacing
            circle = plt.Circle((x, y), v_spacing / 4.,
                                color='w', ec='k', zorder=4)
            ax.add_artist(circle)
            # Node annotations
            if layer_text:
                text = layer_text.pop(0)
                plt.annotate(text, xy=(x, y), zorder=5, ha='center', va='center')

    # Edges
    for n, (layer_size_a, layer_size_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        layer_top_a = v_spacing * (layer_size_a - 1) / 2. + (top + bottom) / 2.
        layer_top_b = v_spacing * (layer_size_b - 1) / 2. + (top + bottom) / 2.
        for m in range(layer_size_a):
            for o in range(layer_size_b):
                line = plt.Line2D([n * h_spacing + left, (n + 1) * h_spacing + left],
                                  [layer_top_a - m * v_spacing, layer_top_b - o * v_spacing], c='k')


                ax.add_artist(line)

########################################################################################################################




# You can add your own activation functions here
def relu(x):
    return max(0,x)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def softmax(inputs):
    return numpy.exp(inputs) / float(sum(numpy.exp(inputs)))




# The class of Neural Network, rest of it will be explained in Readme
class NeuroES(object):
    def __init__(self,input,output,out_fun):
        self.weights=[]
        self.input=input
        self.output=output
        self.completed=0
        self.node_list=[]
        self.layer_count=0
        self.weight_count=0
        self.out_f=out_fun
    def add_layer(self,nodes,act_f):
        if nodes<=0:
            print("Nodes should be atleast one or more than one!")
            return
        if self.completed==1:
            print("Error, Network not in edit mode")
            return
        self.layer_count+=1
        self.node_list.append([nodes,act_f])
    def completed_network(self):
        ini=self.input
        for i in range(len(self.node_list)):
            k=self.node_list[i][0]
            self.weight_count+=k*ini+k
            ini=k
        self.weight_count+=self.output*ini+self.output
        self.completed=1
    def set_weights(self,wg):
        if len(wg)==self.weight_count:
            self.weights=wg
        else:
            print("ERROR: Given weights are not enough or too much!")
            return
    def get_weights(self):
        return self.weights
    def get_weight_count(self):
        return self.weight_count
    def clear_weights(self):
        self.weights=[]

    def init_rand_weights(self):
        for i in range(self.weight_count):
            self.weights.append(float(numpy.random.uniform(size=1)*2-1))
        return self.weights

    def edit_mode(self):
        self.weights=[]
        self.weight_count=0
        self.completed=0
        return

    def add_node(self,layer_no):
        if self.completed==1:
            print("Put the networking in edit mode first")
            return
        self.node_list[layer_no][0]+=1


    def remove_node(self,layer_no):
        if self.completed==1:
            print("Put the networking in edit mode first")
            return
        self.node_list[layer_no][0]-=1
        if self.node_list[layer_no]<=0:
            del self.node_list[layer_no]

    def remove_layer(self,layer_no):
        if self.completed==1:
            print("Put the networking in edit mode first")
            return
        del self.node_list[layer_no]

    def change_input(self,inp_num):
        if self.completed==1:
            print("Put the networking in edit mode first")
            return
        self.input=inp_num
        return
    def change_output(self,out_num):
        if self.completed==1:
            print("Put the networking in edit mode first")
            return
        self.output=out_num
        return

    def draw(self):
        if self.completed!=1:
            print("Please complete the network before drawing")
            return
        fig=plt.figure(figsize=(12,12))
        lyr=[self.input]
        for i in self.node_list:
            lyr.append(i[0])
        lyr.append(self.output)
        print lyr
        draw_neural_net(fig.gca(), .1, .9, .1, .9, lyr)
        plt.show()

    def evaluate(self,inputs):
        if self.completed!=1:
            print("Please complete the network before evaluation")
            return

        if self.input!=len(inputs):
            print("Input size is not correct")
            return
        out=[]
        prev=inputs
        w_i=0
        for i in range(self.layer_count):
            current=[]
            f=self.node_list[i][1]
            l=self.node_list[i][0]
            for j in range(l):
                w_array=self.weights[w_i:w_i+len(prev)]
                arg2=numpy.array(w_array)
                arg1=numpy.array(prev)
                w_i+=len(prev)
                arg3=numpy.matmul(arg1,arg2)+self.weights[w_i]
                w_i+=1
                #print arg3
                arg3=f(arg3)
                current.append(arg3)
            prev=current
        for i in range(self.output):
            w_array=self.weights[w_i:w_i+len(prev)]
            arg2 = numpy.array(w_array)
            arg1 = numpy.array(prev)
            w_i += len(prev)
            arg3 = numpy.matmul(arg1, arg2)+self.weights[w_i]
            w_i+=1

            out.append(arg3)

        out=self.out_f(out)
        return out









