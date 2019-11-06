from graph_tool.all import load_graph, is_bipartite, adjacency, vertex_similarity
from scipy.sparse import csr_matrix
import numpy as np


# calcula a similaridade de um vértice para todos os outros do mesmo grupo que ele
def sim_i_vertices(g, i, termos):
	row = np.full(termos.size, 0)
	pares_termos = [(i, j) for j in termos]
	similaridades_termos = vertex_similarity(g, "salton", pares_termos)
	return csr_matrix((similaridades_termos, (row, termos)), shape = (1, g.num_vertices()))


# somatorio das similaridades entre i e todos os vizinhos de cada anuncio
def sum_sim(g, anuncios, sim_i_j):
	row = np.full(anuncios.size, 0)
	data = []
	for a in anuncios:
		vizinhos = g.get_all_neighbors(a)
		data.append(np.sum(sim_i_j[0, vizinhos]))
	return csr_matrix((data, (row, anuncios)), shape = (1, g.num_vertices()))

"""
	g = grafo
	adjMatrix = matriz de adjacências
	partition = vertor que indica a qual conjunto de partição cada vértice pertence
	i = termo para o qual se deseja recomendar anúncios
"""
def msd(g, adjMatrix, partition, i, l):
	termos = g.get_vertices()[partition.a == 1]
	anuncios = g.get_vertices()[partition.a == 0]
	v = []

	similaridades_i_j = sim_i_vertices(g, i, termos)
	somatorios_alpha = sum_sim(g, anuncios, similaridades_i_j)
	f_alpha = np.zeros(g.num_vertices())
	f_alpha[g.get_all_neighbors(i)] = 1

	for beta in anuncios:
		f_i_beta = 0
		for j in termos:
			f_i_j = 0
			for alpha in anuncios:
				f_i_j += f_alpha[alpha] * ((adjMatrix[i, alpha] * adjMatrix[j, alpha] * similaridades_i_j[0, j]) / somatorios_alpha[0, alpha])

			imp_grau_beta = g.get_total_degrees([beta])[0] ** l
			imp_grau_j = g.get_total_degrees([j])[0] ** (1 - l)
			
			f_i_beta += f_i_j * (adjMatrix[j, beta] / (imp_grau_beta * imp_grau_j))
		v.append((beta, f_i_beta))
	return v

"""
	g = grafo
	adjMatrix = matriz de adjacências
	partition = vertor que indica a qual conjunto de partição cada vértice pertence
	i = termo para o qual se deseja recomendar anúncios
"""
def md(g, adjMatrix, partition, i):
	termos = g.get_vertices()[partition.a == 1]
	anuncios = g.get_vertices()[partition.a == 0]
	v = []

	f_alpha = np.zeros(g.num_vertices())
	f_alpha[g.get_all_neighbors(i)] = 1

	for beta in anuncios:
		f_i_beta = 0
		for j in termos:
			f_i_j = 0
			for alpha in anuncios:
				f_i_j += f_alpha[alpha] * ((adjMatrix[i, alpha] * adjMatrix[j, alpha]) / g.get_total_degrees([alpha])[0])
			
			f_i_beta += f_i_j * (adjMatrix[j, beta] / (g.get_total_degrees([j])[0]))
		
		v.append((beta, f_i_beta))
	return v

def main():
	g = load_graph("permu-hw7.graphml")
	_, partition = is_bipartite(g, True)
	a = adjacency(g)
	#msd(g, a, partition, 0, 0.55)
	r = md(g, a, partition, 0)
	print (r)

if __name__ == '__main__':
	main()