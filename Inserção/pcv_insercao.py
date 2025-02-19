import numpy as np
import os
print(os.getcwd())

def carregarMatriz(arquivo):
    with open(arquivo, 'r') as arq:
        matriz = [list(map(int, linha.split())) for linha in arq]
    return np.array(matriz)

def insercao(matriz):
    
    numVertices = len(matriz)
    

    ini = 0
    maisDistante = np.argmax(matriz[ini])
    caminho = [ini, maisDistante, ini]
    naoVisitados = set(range(numVertices)) - set(caminho[:-1])
    
    while naoVisitados:
        #seleciona o vertice mais distante do ciclo
        prox = max(naoVisitados, key=lambda v: min(matriz[v][i] for i in caminho))
        
        posicao = None
        menorCusto = float('inf')  
        #testa a melhor posicao para inserir o vertice no caminho
        for i in range(len(caminho) - 1):
            custo = (matriz[caminho[i]][prox] +
                       matriz[prox][caminho[i+1]] -
                       matriz[caminho[i]][caminho[i+1]])
            if custo < menorCusto:
                menorCusto = custo
                posicao = i + 1
        
        caminho.insert(posicao, prox)
        naoVisitados.remove(prox)
        caminho = [int(v) for v in caminho]
    return caminho

def CustoTotal(caminho, matriz):
    #calcula a soma total do custo do caminho encontrado
    return sum(matriz[caminho[i]][caminho[i+1]] for i in range(len(caminho) - 1))

if __name__ == "__main__": 
    matriz = carregarMatriz("matriz.txt")
    caminho = insercao(matriz)
    custo = CustoTotal(caminho, matriz)
    
    print("Caminho:", caminho)
    print("Custo:", custo)
