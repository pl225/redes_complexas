from graph_tool.all import load_graph, vertex_average, vertex_hist, shortest_distance, distance_histogram
from graph_tool.all import local_clustering, global_clustering, assortativity
from graph_tool.all import pagerank, betweenness, closeness, katz, collection
from graph_tool.all import graph_draw, label_largest_component, GraphView, prop_to_size
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import gist_heat
import sys

def histogram(distribution, title, xlabel, ylabel, filename):
	plt.bar(distribution[1][:-1], distribution[0])
	plt.gca().set(title = title, xlabel = xlabel, ylabel = ylabel)
	plt.savefig(filename + ".png")
	plt.clf()

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
	avg, std = vertex_average(g, "total" if not g.is_directed() else "in")
	total_degrees = g.get_out_degrees(g.get_vertices())
	print("Graus")
	stats(total_degrees)
	print("\tDesvio padrão (graphtools): ", std)

	distribution = vertex_hist(g, "total" if not g.is_directed() else "in")
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

def assort(g):
	print("Assortatividade")
	print("\tTotal: ", assortativity(g, "total")[0])
	print("\tIncidência: ", assortativity(g, "in")[0])
	print("\tSaída: ", assortativity(g, "out")[0])

def centralidadeStats(g, callback, title):
	pr = None 
	if callback == betweenness:
		pr = callback(g)[0].a
	else:
		if callback == closeness:
			pr = callback(g, harmonic = True).a
		else:
			pr = callback(g).a
	print(title)
	stats(pr)
	histogram(np.histogram(pr), title, "Frequência", "Quantidade", sys.argv[1][:-8] + ".{}".format(title.lower()))

g = load_graph(sys.argv[1])
#g = collection.data["cond-mat-2003"]

degreeStats(g)
distanceStats(g)
clusteringStats(g)
assort(g)
centralidadeStats(g, pagerank, "PageRank")
centralidadeStats(g, betweenness, "Betweenness")
centralidadeStats(g, closeness, "Closeness")
centralidadeStats(g, katz, "Katz")