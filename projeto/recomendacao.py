from graph_tool.all import load_graph, is_bipartite, vertex_similarity
from scipy.sparse import csr_matrix
import numpy as np

"""
	g = grafo
	partition = vertor que indica a qual conjunto de partição cada vértice pertence
	i = termo para o qual se deseja recomendar anúncios
	l = numero [0, 1] para indicar a importância dos graus dos termos e dos anúncios
"""
def msd(g, partition, i, l):
	termos = g.get_vertices()[partition.a == 1]
	anuncios = g.get_vertices()[partition.a == 0]

	f_beta = np.zeros(g.num_vertices()) # o número de anuncios e de termos não é igual ao número de vértices,
	f_i = np.zeros(g.num_vertices()) # mas isso é feito para facilitar a indexação

	anunciosNosTermos = set()
	vizinhosI = g.get_all_neighbors(i)

	for alpha in vizinhosI:
		jotas = g.get_all_neighbors(alpha)
		
		for j in jotas:
			if f_i[j] == 0:
				anunciosEmJ = g.get_all_neighbors(j)
				jotasComItensComum = np.intersect1d(vizinhosI, anunciosEmJ, True) #interseção dos vizinhos de j comuns a i
				sim_i_j = vertex_similarity(g, "salton", [(i, j)])[0]
				
				pares_i_k = [[(i, k) for k in g.get_all_neighbors(a)] for a in jotasComItensComum]
				sim_i_k = np.array([np.sum(vertex_similarity(g, "salton", arrayPar)) for arrayPar in pares_i_k])

				f_i[j] = np.sum(sim_i_j / sim_i_k)
				anunciosNosTermos |= set(anunciosEmJ)

	for beta in anunciosNosTermos:
		vizinhos = g.get_all_neighbors(beta)
		f_beta[beta] = np.sum((1 / ((g.get_total_degrees([beta])[0] ** l) * (g.get_total_degrees(vizinhos) ** (1 - l)))) * f_i[vizinhos])	

	return f_beta

"""
	g = grafo
	partition = vertor que indica a qual conjunto de partição cada vértice pertence
	i = termo para o qual se deseja recomendar anúncios
	booleano para indicar a normalização de f_i[j] pelo grau do vértice i
"""
def md(g, partition, i, normalizar = False):
	termos = g.get_vertices()[partition.a == 1]
	anuncios = g.get_vertices()[partition.a == 0]

	f_beta = np.zeros(g.num_vertices()) # o número de anuncios e de termos não é igual ao número de vértices,
	f_i = np.zeros(g.num_vertices()) # mas isso é feito para facilitar a indexação

	anunciosNosTermos = set()
	vizinhosI = g.get_all_neighbors(i)
	grauI = 1 if not normalizar else vizinhosI.size

	for alpha in vizinhosI:
		jotas = g.get_all_neighbors(alpha) #j

		for j in jotas:
			if f_i[j] == 0:
				anunciosEmJ = g.get_all_neighbors(j)
				jotasComItensComum = np.intersect1d(vizinhosI, anunciosEmJ, True) #interseção dos vizinhos de j comuns a i

				f_i[j] = np.sum(1 / g.get_total_degrees(jotasComItensComum)) / grauI
				anunciosNosTermos |= set(anunciosEmJ)

	for beta in anunciosNosTermos:
		vizinhos = g.get_all_neighbors(beta)
		f_beta[beta] = np.sum((1 / g.get_total_degrees(vizinhos)) * f_i[vizinhos])

	return f_beta

def main():
	g = load_graph("permu-hw7.graphml")
	_, partition = is_bipartite(g, True)

	#r = msd(g, partition, 3, 0.55)

	r = md(g, partition, 3)
	

if __name__ == '__main__':
	main()