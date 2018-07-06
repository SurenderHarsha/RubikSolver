# Evolutionary Reinforcement Learning to solve a Rubik's Cube.


This project requires three parts to work,
* A Rubik's Cube API (Environment)
* A Neural Network API (Agent/Brain)
* The Main Algorithm

The Rubiks Cube API is contained in the Rubik2x2.py and Rubik3x3.py (Upcoming).

Features of the Rubik's Cube API (Made from Scratch)

* Dictionary of the Cube's representation with each of its face (0,5) as a key. Each color is represented by an integer (0,5)
* The number of actions on the Cube are 12 (0,11). Each move is a function 'm#' where # is the move number, each move is called by the move() function where the move number is given to it as a parameter.
* The cube can be set into a solved state by calling the Reset() function.
* The function get_cube() can be used to see the curent representation of the cube( This can later be extended to represent the cube graphically)
* The function get_reward() can be called to get the percentage of the cube currently solved. This is a better reward that win or lose. This reward tells the network how close we are to solving , so that learning becomes efficient and better.
* Since each color on the Cube is a category, it cannot be fed into the neural network directly, it has to be encoded into binary(one hot encoding), therefore (0,6) colors are represented in binary digits, with each color being 3 digits. The current state of the cube in binary format can be received by using get_binary_cube() function.
* The cube can be Shuffled 'n' number of times from its starting position or from any position using Shuffle().


The Neural Network API's usage and working is given [here](https://github.com/SurenderHarsha/NeuroEvolve). I made this package to help me create neural networks for my other reinforcement learning tasks. Since our problem is to solve a 2x2 cube. We have (2x2x6x3) inputs,(6 faces and 3 bits for each color), we have a total of 72 inputs, and since there are 12 possible moves for each state, there will be 12 outputs. There will be one hidden layer with 42 nodes(Can be adjusted). The activation function for the hidden layer is RELU, and the activation function for output layer is softmax( gives a probability of each move).


The Main Algorithm

Here we train the network using an Evolutionary Strategy rather than the standard Gradient descent. Bear in mind this is still reinforcement learning but with the addition of an Evolutionary strategy.

[Here](https://blog.openai.com/evolution-strategies/) is research which seemingly shows that Evolutionary strategies can perform better.

So, our task is to find optimized weights which can be fit into the neural network, which can solve a cube in minimum moves. Genetic Algorithms work well in finding optimized weights. 

* We create a population of collection of random weights. (Example 50 members in population i.e 50 sets of weights)
* Each member of the population plays 10 consecutive games, where the game starts from a random shuffled position and tries to solve it in under 20 moves, if 20 moves have been completed and the cube is still unsolved, we get the percentage of cube solved and we assign it as a reward/fitness. We take the average reward/fitness of the 10 games and assign it to the member of the population.
* We take the Top 40% (cr_rate) of the population (based on fitness of each member). We then perform 'crossover' on the population ( We do many different operations on the population mixing two members, taking average of two members etc). This gives us a chance to get better weights from the top members
* We then perform mutation where there is a probability of a weight being slightly changed(given by mut_rate), this keeps randomness and allows us to explore more solutions and prevents us from getting stuck in local minima.
* We repeat the process above until a set of weights is able to solve all cubes in the 10 consecutive games.

The above solution works but is Naive, it might take a long amount to arrive at a solution because the search space for weights is quite large, we need to have some method to arrive at the solutions faster.

After some research, I came around the topic of Replay Memory, this allowed me to make a modification on the way the agent learns by exploiting the features of the rubik's cube.

Here it is,

* Since the network is quite new and needs help to learn. Therefore, I decided first to teach it how to solve the cube in a single move, we reset the cube to bring it to a solved state and then shuffle it with 1 random move. We then start training the entire population to find this one move to solve the cube based on the presolved state, this eliminates a lot of other weight sets and gets us the best ones. After the population solves this one move, we arrive at a "Breakthrough". 
* Now we increase the shuffle size to 2, where the cube is shuffled with two random moves. If the network can figure out one move to go the presolved state, the network can then immediately solve the last move as it immediately knows how to solve it. Therefore, we train the population to solve a 2 shuffle cube until a breakthrough occurs.
* We then increase shuffle size again until a certain criteria is met. For example if the network is able to solve a 7 shuffle cube, then 2x2 is considered to be solved. There is a certain factor of luck and random mutation in learning.

All the numbers given in this document are parameters and can be changed to optimize learning and new features and parameters can be added as they work like API's.






