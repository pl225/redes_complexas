Repositório criado para conter o Trabalho prático 1 efetuado na disciplina Redes Complexas do programa de mestrado do PESC/COPPE.

Os scripts foram feitos na linguagem [Python 3](www.python.org) com o uso da biblioteca [graph-tool](https://graph-tool.skewed.de/).

O script conversor converte grafos codificados da forma ```VERTICE_ID VERTICE_ID``` para o formato <i>graphml</i>.

O script stats calcula as métricas de graus, distâncias, assortatividade de grau, pagerank, betweenness, closeness e Katz.

Comandos:

  - ```python3 conversor.py CAMINHO/INSTANCIA/TEXTO N_VERTICES [GRAFO_ DIGIRIDO, opcional]```
  
  - ```python3 stats.py CAMINHO/INSTANCIA/GRAPHML```
