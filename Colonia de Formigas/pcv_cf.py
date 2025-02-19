import numpy as np
import pandas as pd
import time

def carregar_matriz(arquivo):
    with open(arquivo, 'r') as arq:
        matriz = [list(map(int, linha.split())) for linha in arq]
    return np.array(matriz)

class ColoniaFormigas:
    def __init__(self, matriz, melhorFormiga, iteracoes, evaporacao, alfa=1, beta=2):
        self.matriz = matriz
        self.feromonio = np.ones(self.matriz.shape) * 1e-6
        self.indice = range(len(matriz))
        self.formigas = len(matriz)
        self.melhorFormiga = melhorFormiga
        self.iteracoes = iteracoes
        self.evaporacao = evaporacao
        self.alfa = alfa
        self.beta = beta

    def melhorCaminho(self):
        menorCusto = float('inf')
        estagnacao = 0 

        for _ in range(self.iteracoes):
            caminhos = self.gerar_todos_caminhos()
            self.atualizarFeromonio(caminhos)  
            
            caminhoAtual = min(caminhos, key=lambda x: x[1]) 

            if caminhoAtual[1] < menorCusto: 
                menorCusto = caminhoAtual[1]
                estagnacao = 0  
            else:
                estagnacao += 1
                
            self.feromonio *= self.evaporacao 
            if estagnacao >= 20:  #critério de parada por estagnação
                break
        return menorCusto        

    def atualizarFeromonio(self, caminhos):
        caminhos.sort(key=lambda x: x[1])
        for caminho, custo in caminhos[:self.melhorFormiga]:
            for i in range(len(caminho) - 1):
                a, b = caminho[i], caminho[i + 1]
                self.feromonio[a][b] += 100 / custo
                self.feromonio[b][a] += 100 / custo

    def calcularCusto(self, caminho):
        return sum(self.matriz[caminho[i]][caminho[i + 1]] for i in range(len(caminho) - 1)) + self.matriz[caminho[-1]][caminho[0]]

    def gerar_todos_caminhos(self):
        caminhos = []
        for _ in range(self.formigas):
            caminho = [0]  # Começa no nó inicial (0)
            visitados = {0}
            atual = 0
            custo_total = 0

            for _ in range(len(self.matriz) - 1):
                prox = self.escolher_movimento(self.feromonio[atual], self.matriz[atual], visitados)
                custo_total += self.matriz[atual][prox]  # Soma o custo da aresta
                caminho.append(prox)
                visitados.add(prox)
                atual = prox

            caminhos.append((caminho, custo_total))
        
        return caminhos

    def escolher_movimento(self, feromonio, distancias, visitados):
        feromonio = np.copy(feromonio)
        feromonio[list(visitados)] = 0
        distancias = np.where(distancias == 0, np.inf, distancias)
        probabilidades = (feromonio ** self.alfa) * ((1.0 / distancias) ** self.beta)
        soma_prob = probabilidades.sum()
        if soma_prob == 0 or np.isnan(soma_prob):
            return np.random.choice(list(set(self.indice) - visitados))
        probabilidades /= soma_prob
        return np.random.choice(self.indice, 1, p=probabilidades)[0]

def experimentoFatorial():
    parametros = {
        "formigas": [10, 20, 30],
        "beta": [2, 5, 10],
        "evaporacao": [0.1, 0.5, 0.9]
    }
    matriz = carregar_matriz("matriz.txt")
    melhorFormiga = 2
    iteracoes = 100
    alfa = 1
    resultados = []
    for formigas in parametros["formigas"]:
        for beta in parametros["beta"]:
            for evaporacao in parametros["evaporacao"]:
                inicio = time.time()
                colonia = ColoniaFormigas(matriz, melhorFormiga, iteracoes, evaporacao, alfa, beta)
                custo = colonia.melhorCaminho()
                tempo_execucao = time.time() - inicio
                print(f"Formigas: {formigas}, Beta: {beta}, Evaporacao: {evaporacao}, Custo: {custo}")  
                resultados.append({"Formigas": formigas, "Beta": beta, "Evaporacao": evaporacao, "Custo": custo, "Tempo": tempo_execucao})

    df = pd.DataFrame(resultados)
    df.to_csv("resultados.csv", index=False) #csv para gerar grafico e tabela

def main():
    experimentoFatorial()

if __name__ == "__main__":
    main()
