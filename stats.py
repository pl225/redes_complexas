from graph_tool.all import load_graph, vertex_average, vertex_hist, shortest_distance, distance_histogram
from graph_tool.all import local_clustering, global_clustering
import numpy as np
import matplotlib.pyplot as plt
import sys

def histogram(distribution, title, xlabel, ylabel, filename):
	plt.bar(distribution[1][:-1], distribution[0])
	plt.gca().set(title = title, xlabel = xlabel, ylabel = ylabel)
	plt.savefig(filename + ".png")

def stats(distribution):
	maximum = np.amax(distribution)
	minimum = np.amin(distribution)
	med = np.median(distribution)
	avg = np.average(distribution)
	std = np.std(distribution)
	print("\tMédia: ", avg)
	print("\tMaior: ", maximum)
	print("\tMínimo: ", minimum)
	print("\tMediana: ", med)
	print("\tDesvio padrão", std)

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
	print("Distâncias")
	stats(np_dist)

	distribution = distance_histogram(g)
	histogram(distribution, "Distribuição de distâncias", "$d$", "$f_{D}(d)$", sys.argv[1][:-8] + ".distancias")

def clusteringStats(g):
	clustring_vertices = local_clustering(g).a
	print("Clusterização")
	stats(clustring_vertices)
	print("\tGlobal", global_clustering(g)[0])

	histogram(np.histogram(clustring_vertices), "Distribuição de clusterização", "$C_i$", "$C$", sys.argv[1][:-8] + ".clusterizacao")

g = load_graph(sys.argv[1])

degreeStats(g)
distanceStats(g)
clusteringStats(g)