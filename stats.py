from graph_tool.all import load_graph, vertex_average, vertex_hist, shortest_distance, distance_histogram
from graph_tool.all import local_clustering, global_clustering
import numpy as np
import matplotlib.pyplot as plt
import sys

def histogram(distribution, title, xlabel, ylabel, filename):
	plt.hist(distribution[0], distribution[1])
	plt.gca().set(title = title, xlabel = xlabel, ylabel = ylabel)
	plt.savefig(filename + ".png")

def degreeStats(g):
	avg, std = vertex_average(g, "total")
	total_degrees = g.get_out_degrees(g.get_vertices())
	maximum = np.amax(total_degrees)
	minimum = np.amin(total_degrees)
	med = np.median(total_degrees)

	print("Graus")
	print("\tMédia: ", avg)
	print("\tMáximo: ", maximum)
	print("\tMínimo: ", minimum)
	print("\tMediana: ", med)
	print("\tDesvio padrão: ", std)

	distribution = vertex_hist(g, "total")
	histogram(distribution, "Distribuição de graus", "$k_{total}$", "$NP(k_{in})$", sys.argv[1][:-8] + ".graus")

def distanceStats(g):
	dist = shortest_distance(g)
	np_dist = np.array(dist.get_2d_array(g.get_vertices()))
	maximum = np.amax(np_dist)
	minimum = np.amin(np_dist)
	med = np.median(np_dist)
	avg = np.average(np_dist)
	std = np.std(np_dist)

	print("Distâncias")
	print("\tMédia: ", avg)
	print("\tDiâmetro: ", maximum)
	print("\tMínimo: ", minimum)
	print("\tMediana: ", med)
	print("\tDesvio padrão", std)

	distribution = distance_histogram(g)
	print(distribution)
	histogram(distribution, "Distribuição de distâncias", "$d$", "$f_d(d)$", sys.argv[1][:-8] + ".distancias")

g = load_graph(sys.argv[1])

degreeStats(g)
distanceStats(g)