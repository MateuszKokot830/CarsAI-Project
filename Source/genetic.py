import random

def mutate_weights(parent, child):
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
    genWeights[randomGen] = genWeights[randomGen]*random.uniform(0.8, 1.2)
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
        for j in range(child.sizes[i+1]):
            genBiases.append(child.biases[i].item(j))
    
    randomGen = random.randint(0, len(genBiases) - 1)
    genBiases[randomGen] = genBiases[randomGen]*random.uniform(0.8, 1.2)
    counter = 0

    for i in range(len(child.sizes)-1):
        for j in range(child.sizes[i+1]):
                child.biases[i][j] = genBiases[counter]
                counter += 1 
    
    return


def crossover_weights(parent1, parent2, child1, child2):
    # Copying parent weights into children
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            for k in range (child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]
    
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            for k in range (child1.sizes[i]):
                child2.weights[i][j] = parent2.weights[i][j]

    # Copying parent biases into children
    for i in range(len(child1.sizes)-1):
        for j in range(child2.sizes[i+1]):
            child1.biases[i][j] = parent1.biases[i][j]
    
    for i in range(len(child1.sizes)-1):
        for j in range(child2.sizes[i+1]):
            child2.biases[i][j] = parent2.biases[i][j]
    
    # Containers for all weights for child1 and child2
    gen1 = []
    gen2 = []

    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i]*child1.sizes[i+1]):
            gen1.append(child1.weights[i].item(j))
    
    for i in range(len(child1.sizes)-1):
        for j in range(child2.sizes[i]*child2.sizes[i+1]):
            gen2.append(child2.weights[i].item(j))

    check = True

    # Crossover on weights
    for i in range(len(gen1)):
        if check == True:
            x = gen1[i]
            gen1[i] = gen2[i]
            gen2[i] = x
            check = False
        else:
            check = True

    # Going back from genome list to weights on children
    counter = 0
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            for k in range (child1.sizes[i]):
                child1.weights[i][j][k] = gen1[counter]
                counter += 1
    
    counter = 0
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            for k in range (child1.sizes[i]):
                child2.weights[i][j][k] = gen2[counter]
                counter+=1

    return


def crossover_biases(parent1, parent2, child1, child2):
    # Copying parent weights into children
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            for k in range (child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]
    
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            for k in range (child1.sizes[i]):
                child2.weights[i][j] = parent2.weights[i][j]

    # Copying parent biases into children
    for i in range(len(child1.sizes)-1):
        for j in range(child2.sizes[i+1]):
            child1.biases[i][j] = parent1.biases[i][j]
    
    for i in range(len(child1.sizes)-1):
        for j in range(child2.sizes[i+1]):
            child2.biases[i][j] = parent2.biases[i][j]
    
    # Containers for all weights for child1 and child2
    gen1 = []
    gen2 = []

    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            gen1.append(child1.biases[i].item(j))
    
    for i in range(len(child1.sizes)-1):
        for j in range(child2.sizes[i+1]):
            gen2.append(child2.biases[i].item(j))

    # Crossover on weights
    check = True
    for i in range(len(gen1)):
        if check == True:
            x = gen1[i]
            gen1[i] = gen2[i]
            gen2[i] = x
            check = False
        else:
            check = True

    # Going back from genome list to weights on children
    counter = 0
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            child1.biases[i][j] = gen1[counter]
            counter += 1
    
    counter = 0
    for i in range(len(child1.sizes)-1):
        for j in range(child1.sizes[i+1]):
            child2.biases[i][j] = gen2[counter]
            counter +=1

    return
