from graph_tool.all import *
import sys

def txtToGraphFile(filename):
	
	file = open(filename, "r")

	info = file.readline().split()

	g = Graph(directed = False)
	g.add_vertex(int(info[0]))

	v = 0
	for line in file:
		vertices = line.split()
		for i in range(len(vertices)):
			g.add_edge(g.vertex(v), g.vertex(int(vertices[i]) - 1))
		v += 1

	remove_parallel_edges(g)
	print(g)

	file.close()

	g.save("{0}.graphml".format(filename[:-6]))


txtToGraphFile(sys.argv[1])