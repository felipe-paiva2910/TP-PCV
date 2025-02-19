import pandas as pd
import matplotlib.pyplot as plt

def visualizar_resultados():
    df = pd.read_csv("resultados.csv").sort_values(by="Custo", ascending=False)
    
    # exibir tabela
    print("\nTabela de Resultados:\n")
    print(df.to_string(index=False))
    
    # gerar grafico 3D
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(df["Formigas"], df["Beta"], df["Custo"], c=df["Evaporacao"], cmap='viridis', depthshade=True)
    ax.set_xlabel("Número de Formigas")
    ax.set_ylabel("Beta")
    ax.set_zlabel("Custo do Caminho")
    plt.title("Comparação de Parâmetros da Colônia de Formigas")
    cbar = plt.colorbar(sc, ax=ax, shrink=0.5)
    cbar.set_label("Taxa de Evaporação")
    plt.show()

if __name__ == "__main__":
    visualizar_resultados()
