from graph_tool.all import load_graph, is_bipartite, vertex_similarity, pagerank, vertex_average
from itertools import combinations
import numpy as np
import re
import os
import operator
import collections
import matplotlib.pyplot as plt
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

def executar_recomendacoes(g, partition):
	with open("resultados.txt", 'a') as f:

		prop_e = g.new_edge_property("bool")
		prop_e.a = True

		termosSelecionados = np.random.choice(g.get_vertices()[partition.a == 1], 10000, False) #41800

		for ind, i in enumerate(termosSelecionados):
			viz = g.get_all_neighbors(i)
			e = np.random.choice(viz)
			aresta = g.edge(i, e)
			prop_e[aresta] = False
			g.set_edge_filter(prop_e)

			r = md(g, partition, i)
			indices = (-r).argsort()
			f.write("Termo: {}, anúncio: {}, posição: {}, valor: {}\n".format(i, e, np.argwhere(indices == e), r[e]))
			prop_e[aresta] = True
			print("Termo: {} de índice de loop {} terminado.".format(i, ind))

def graus_acumulados(g, funcao):
	file = open("resultados.txt", "r")
	graus = np.array([])
	for linha in file:
		tokens = linha.split()
		termo = int(tokens[1][:-1])
		pos = int(re.findall(r'\d+', tokens[5])[0])
		valor = float(tokens[7])
		if funcao(pos, valor): # pos < 5; pos > 100 and valor == 0.0; pos >= 5 and pos <= 100 and valor != 0.0; pos > 100 and valor != 0.0
			graus = np.append(graus, g.get_total_degrees([termo])[0])
	file.close()
	return graus

def ccdf(graus):
	counter = collections.Counter(graus)
	graus_sorted = sorted(counter.items(), key=operator.itemgetter(0))
	print(graus_sorted)
	x = []
	y = []
	acumulado = 0
	fracao = 0.0
	total = graus.size
	for tupla in graus_sorted:
		x.append(tupla[0])
		y.append(1 - fracao) #y.append((total - acumulado) / graus.size)
		fracao += tupla[1] / total
		#acumulado += tupla[1]
	return x, y

def similaridade_acumulada(g, funcao, np_funcao):
	file = open("resultados.txt", "r")
	xx = np.array([])
	for linha in file:
		tokens = linha.split()
		termo = int(tokens[1][:-1])
		pos = int(re.findall(r'\d+', tokens[5])[0])
		valor = float(tokens[7])
		if funcao(pos, valor): # pos < 5; pos > 100 and valor == 0.0; pos >= 5 and pos <= 100 and valor != 0.0; pos > 100 and valor != 0.0
			s = [np.intersect1d(g.get_all_neighbors(par[0]), g.get_all_neighbors(par[1])).size / np.union1d(g.get_all_neighbors(par[0]), g.get_all_neighbors(par[1])).size for par in list(combinations(g.get_all_neighbors(termo), 2))]
			xx = np.append(xx, np_funcao(s))
	file.close()
	return xx

def hist_ccdf(valores):
	m, n = np.histogram(valores)
	#acumulado = 0
	fracao = 0.0
	#total = graus.size
	x = []
	y = []
	soma = np.sum(m)
	for i in range(1, len(n)):
		x.append(n[i])
		y.append(1 - fracao) #y.append((total - acumulado) / graus.size)
		fracao += m[i - 1] / soma
	return x, y

def main():
	g = load_graph("permu-hw7.graphml")
	_, partition = is_bipartite(g, True)

	#executar_recomendacoes(g, partition)	
	
	similaridades = similaridade_acumulada(g, lambda pos, valor: pos < 5, np.max)
	x1, y1 = hist_ccdf(similaridades)
	plt.plot(x1, y1, 'ro')
	plt.show()
	
	"""
	distribuição de graus
	graus = graus_acumulados(g, lambda pos, valor: pos < 5)
	x1, y1 = ccdf(graus)

	graus = graus_acumulados(g, lambda pos, valor: pos >= 5 and pos <= 100 and valor != 0.0)
	x2, y2 = ccdf(graus)

	graus = graus_acumulados(g, lambda pos, valor: pos > 100 and valor != 0.0)
	x3, y3 = ccdf(graus)

	graus = graus_acumulados(g, lambda pos, valor: pos > 100 and valor == 0.0)
	x4, y4 = ccdf(graus)
	
	plt.plot(x1, y1, 'rx', x2, y2, 'y--', x3, y3, 'bs', x4, y4, 'g^')
	plt.xlabel('$d$')
	plt.ylabel('Fração de amostras $\\geq d$')
	plt.legend(('Bom', 'Médio', 'Ruim', 'Péssimo'), loc='right')
	plt.yscale('log')
	plt.suptitle('Distribuição de graus dos vértices termos classificados')
	plt.show()	
	"""

if __name__ == '__main__':
	main()