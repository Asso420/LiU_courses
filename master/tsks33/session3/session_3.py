import numpy as np

titles = open('titles/1.txt', 'r').read().strip().splitlines()
links = np.genfromtxt('links/1.txt', delimiter= ' ', dtype= int)

N = len(titles)

