import random

def mutate_weight(parent, child):
    # Copying parent weights and biases into children
    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
            for k in range (child.sizes[i]):
                child.weights[i][j][k] = parent.weights[i][j][k]
    
    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
            child.biases[i][j] = parent.biases[i][j]

    # Modifing weight genes slightly by random amount
    genWeights = []

    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i] * child.sizes[i+1]):
            genWeights.append(child.weights[i].item(j))
    
    randomGen = random.randint(0, len(genWeights) - 1)
    genWeights[randomGen] = genWeights[randomGen]*random.uniform(0.8, 1,2)
    counter = 0

    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
            for k in range (child.sizes[i]):
                child.weights[i][j][k] = genWeights[counter]
                counter += 1 

    return



def mutate_biases(parent, child):
    # Copying parent weights and biases into children
    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
            for k in range (child.sizes[i]):
                child.weights[i][j][k] = parent.weights[i][j][k]
    
    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
            child.biases[i][j] = parent.biases[i][j]

     # Modifing biases genes slightly by random amount
    genBiases = []

    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i] * child.sizes[i+1]):
            genBiases.append(child.biases[i].item(j))
    
    randomGen = random.randint(0, len(genBiases) - 1)
    genBiases[randomGen] = genBiases[randomGen]*random.uniform(0.8, 1,2)
    counter = 0

    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
                child.biases[i][j] = genBiases[counter]
                counter += 1 
    
    return