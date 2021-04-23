from random import random
from math import sqrt, pow, fsum, fabs
import matplotlib.pyplot as plt
import argparse

from voting import *

#############
# FUNCTIONS #
#############

def distance(pointA, pointB):
    return sqrt(fsum([pow(fabs(pointA[i]-pointB[i]), 2) for i in range (0, len(pointA))]))

def iniate_dict(number, dimension):
    dict = {}
    for i in range(0, number):
        element = []
        for j in range(0, dimension):
            element.append(random())
        dict[i] = element
    return (dict)

def plot_grid(electors, candidates):
    fig, ax = plt.subplots()
    ax.scatter([electors[v][0] for v in electors], [electors[v][1] for v in electors],
    s=10, c="black")
    for c in candidates:
        ax.scatter(candidates[c][0], candidates[c][1])
        ax.annotate(str(c), (candidates[c][0], candidates[c][1]))
    ax.grid(True)
    fig.suptitle("elector and candidate positions")
    plt.savefig("img/positions.png")


##############
# PARAMETERS #
##############

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version='1.0')
parser.add_argument("-d", "--dimension", type=int, default=2, help="number of dimensions to use")
parser.add_argument("-e", "--electors", type=int, default=50, help="number of electors for the simulation")
parser.add_argument("-c", "--candidates", type=int, default=10, help="number of candidates for the simulation")
parser.add_argument("-t", "--threshold", type=float, default=0.5, help="rejection threshold for scoring methods")
parser.add_argument("--noplot", action='store_true', help="creates the positions image")
parser.add_argument("-r", "--repeat", type=int, default=1, help="number of repetitions of the simulation")
parser.add_argument("-o", "--output", type=str, help="output file to write the results")
parser.add_argument("--test", type=int, help="number of times to test the method given in the test() function")
args = parser.parse_args()

########
# MAIN #
########

def main():
    if args.output != None:
        output_string = ""

    for i in range (0, args.repeat):
        electors = iniate_dict(args.electors, args.dimension)
        candidates = iniate_dict(args.candidates, args.dimension)

        if not args.noplot:
            plot_grid(electors, candidates)

        distances = {elector: { candidate: distance(electors[elector], candidates[candidate]) for candidate in candidates} for elector in electors }
        ranked_preferences = {elector: [candidate for candidate, distance in sorted(distances[elector].items(), key=lambda item: item[1])] for elector in electors}

        if args.output == None:
            print("plurality:\t\t", N_rounds(ranked_preferences, 1))
            print("two round:\t\t", N_rounds(ranked_preferences, 2))
            print("instant runoff:\t\t", N_rounds(ranked_preferences, args.candidates-1))
            print("condorcet:\t\t", condorcet(ranked_preferences))
            print("borda:\t\t\t", borda(ranked_preferences))
            print("approval:\t\t", approval(distances, args.threshold))
            print("majority judgement:\t", majority_judgement(distances, args.threshold))

        else:
            output_string += (str) (N_rounds(ranked_preferences, 1)) + ','
            output_string += (str) (N_rounds(ranked_preferences, 1)) + ','
            output_string += (str) (N_rounds(ranked_preferences, 2)) + ','
            output_string += (str) (N_rounds(ranked_preferences, args.candidates-1)) + ','
            output_string += (str) (condorcet(ranked_preferences)) + ','
            output_string += (str) (borda(ranked_preferences)) + ','
            output_string += (str) (approval(distances, args.threshold)) + ','
            output_string += (str) (majority_judgement(distances, args.threshold)) + '\n'


    if args.output != None:
        f = open(args.output, "w", newline='\n')
        f.write(output_string)
        f.close()

###############
# VOTING TEST #
###############

def test(n):
    count = 0
    for i in range (0, n):
        electors = iniate_dict(args.electors, args.dimension)
        candidates = iniate_dict(args.candidates, args.dimension)
        distances = {elector: { candidate: distance(electors[elector], candidates[candidate]) for candidate in candidates} for elector in electors }
        ranked_preferences = {elector: [candidate for candidate, distance in sorted(distances[elector].items(), key=lambda item: item[1])] for elector in electors}
        if (condorcet(ranked_preferences) == None):
            count+=1
            print (count*100/i)
    print (count*100/n)

if __name__ == '__main__':
    if args.test != None:
        test(args.test)
    else:
        main()
