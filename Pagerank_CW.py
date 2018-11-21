import random 
import numpy as np #Import numpy for array operations
import matplotlib.pyplot as plt #Import MATLAB plot library to plot graphs, specifically a histogram.

edges = [(0,2),(1,1),(1,2),(2,0),(2,2),(2,3),(3,3),(3,4),(4,6),(5,6),(5,5),(6,4),(6,6),(6,3)] #Store each edge as a tuple
pages = [0,1,2,3,4,5,6] #Array of distinct pages

def randomWalk(edges,probability,iters):
    
    walk = [] # Initialise array for storing pages visited on a walk
    counts = [0,0,0,0,0,0,0] # Represent the amount each page is visited
    
    currentPage = random.choice(pages) # Start the walk on a random page
    counts[pages.index(currentPage)] += 1 #Increment t
    walk.append(currentPage) # Add page to walk array
    
    teleport_percentage = probability*100 #Convert decimal percentage to a whole number for ease of use
    
    for i in range(iters): # Perform passed integer parameter (iters) steps in the walk
        if random.randint(1,100)<=teleport_percentage:  
            # Calculates a random integer, if this integer is within the range of the teleport integer value and 0 then teleport to a random page
             nextPage = random.choice(pages) # Randomly select a page to teleport to
             
             while nextPage==currentPage:
                 nextPage = random.choice(pages)
             currentPage = nextPage
             
             counts[pages.index(currentPage)] += 1 # Increment selected pages frequency bin 
             walk.append(currentPage) # Add teleport destination to walk

        else:
             possibleMoves = [] # Initialise array to store edges containing the current page in the walk
             for edge in edges: # Iterate over edges adding edges which start from the current page
                 if(edge[0]==currentPage): 
                     possibleMoves.append(edge)
             nextEdge = random.choice(possibleMoves) # Select a random possible move from the currentPage   
             currentPage = nextEdge[1] # Assign the next edge to follows destination to the current page
             counts[pages.index(currentPage)] += 1 # Increment current page's frequency bin
             walk.append(currentPage) # Add current page to walk
      
    plt.hist(walk,pages) #Creates a histogram from the walk array with the pre-defined pages array as the bins to use in histogram generation
    plt.title("Random walk Histogram") 
    plt.show() #Draw the resulting histogram
    
    return counts #Returns the frequency that each page was visited as an array, where index 0 is equal to the number of time page 0 was visited.


def pageRank(edges,probability,iters):
    
    transition = np.array([[0.00 for col in range(len(pages))] for row in range(len(pages))])
    # Initialise tranistion array with 0's, each distinct page has a corresponding array of probabilities

    for page in pages:
        connected_edges = [] # Create array to store potential moves from that page, including to itself. 
        for edge in edges: 
            if edge[0] == page: # If starting position in an edge is equal to this page
                connected_edges.append(edge) #Add to array
        
        remainder_probability = 1.00 - probability  
        # Calculte total probability of going to another page excluding teleporting
        edge_probability = remainder_probability/len(connected_edges) 
        # Assume each connected page has an equal probability of being selected
        
        for edge in connected_edges: 
            transition[page,edge[1]] = edge_probability 
            # Assign previously calculated equiprobability to the connected page in this pages transition array
        randomChance = probability/(len(pages)-1) # Calculate the probabilty of teleporting to any page, excluding the current page.

        for element in range(len(pages)): # Add the random teleporting probability to each page in this pages tranistion array
            if element != page: #Exclude the current page
                transition[page,element] += randomChance

    probability_vector = np.array([0.00 for i in range(len(pages))]) 
    #Initialise probability vector with 0s, where the probability vector represents the probability of being on a given page.
    for i in range(len(pages)): 
        probability_vector[i] = 1.00/len(pages) #Assign arbitrary equal probability to each element in probability vector
    
    for i in range(iters): #
        probability_vector = probability_vector.dot(transition)  #Multiply probability vector with tranistion matrix (dot product) by 'iters' times
    return probability_vector

print "Page rank probability vector (3 Iterations):"
probability_vector_3 = pageRank(edges,0.20,20)
print probability_vector_3
print ''

print "Page rank probability vector (5 Iterations):"
probability_vector_10 = pageRank(edges,0.20,10)
print probability_vector_10
print ''

print "Page rank probability vector (10 Iterations):"
probability_vector_10 = pageRank(edges,0.20,10)
print probability_vector_10

# Question 3:
# The pageRank function arrives at the Steady-state probabilites after approximately 5 iterations
# A vector probability was derived for randomWalk by dividing the number of times a page was visited by the total number of steps in a walk.
# The probability vector generated by the random walk is approximately equal to the previously derived steady-state probabilities 
# but it, unlike pageRank, doesn't find a completely stable state, even after 100,000 iterations.

counts_50 = randomWalk(edges,0.20,50000)
prob_50 = []

print "Random walk probability vector (50,000 Iterations):"
for count in counts_50:
    prob_50.append(count/50000.00)
print prob_50
print ''

counts_100 = randomWalk(edges,0.20,100000)
prob_100 = []

print "Random walk probability vector (100,000 Iterations):"
for count in counts_100:
    prob_100.append(count/100000.00)
print prob_100
print ''

# Question 4:
# When adding more out-links to a page the pagerank score of the page is reduced
# In the example below more outlinks are added from page 6 to other pages resulting in a reduction in it's page-rank value.

print "Question 4 probability vector:"
test_edges_out = [(0,2),(1,1),(1,2),(2,0),(2,2),(2,3),(3,3),(3,4),(4,6),(5,6),(5,5),(6,4),(6,6),(6,3),(6,1),(6,0),(6,2)]
test_vector_out = pageRank(test_edges_out,0.20,10)
print test_vector_out
    
    