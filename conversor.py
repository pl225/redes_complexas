from graph_tool.all import *
import sys

def txtToGraphFile(filename):
	
	file = open(filename, "r")
	g = Graph(directed = len(sys.argv) > 3)
	g.add_vertex(int(sys.argv[2]))

	for line in file:
		vertices = line.split()
		g.add_edge(g.vertex(vertices[0]), g.vertex(vertices[1]))

	g.save("{0}.graphml".format(filename[:-4]))


txtToGraphFile(sys.argv[1])