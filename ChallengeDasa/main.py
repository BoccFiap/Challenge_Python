from bisect import bisect_left

# Estrutura de dados de exemplo
estoque_hospitais = {
    "Hospital A": {
        "alcool": {"quantidade": 30, "ideal": 50},
        "luvas": {"quantidade": 60, "ideal": 60},
        "mascara": {"quantidade": 10, "ideal": 40},
    },
    "Hospital B": {
        "alcool": {"quantidade": 55, "ideal": 50},
        "luvas": {"quantidade": 20, "ideal": 60},
        "mascara": {"quantidade": 50, "ideal": 40},
    }
}

# Memoização para função recursiva
memo = {}

# ✅ Função recursiva com memorização
# Complexidade: O(n), onde n é a diferença entre ideal e atual
def calcular_urgencia(qtd, ideal):
    chave = (qtd, ideal)
    if chave in memo:
        return memo[chave]
    if qtd >= ideal:
        return 0
    memo[chave] = 1 + calcular_urgencia(qtd + 1, ideal)
    return memo[chave]

# Função de ordenação dos produtos pela maior urgência de reposição
def ordenar_por_urgencia(estoque):
    produtos = []
    for hospital, itens in estoque.items():
        for nome, dados in itens.items():
            urg = calcular_urgencia(dados["quantidade"], dados["ideal"])
            produtos.append((nome, urg, hospital))
    produtos.sort(key=lambda x: x[1], reverse=True)  # Ordena por urgência decrescente
    return produtos

# Função de busca binária para verificar se um produto existe na lista
def busca_binaria(lista_ordenada, item):
    idx = bisect_left(lista_ordenada, item)
    return idx < len(lista_ordenada) and lista_ordenada[idx] == item

# Funções de apoio
def mostrar_produtos_em_falta(estoque):
    for hospital, itens in estoque.items():
        for nome, dados in itens.items():
            if dados["quantidade"] < dados["ideal"]:
                print(f"{nome.title()} em {hospital}: {dados['quantidade']} / {dados['ideal']}")

def menu():
    while True:
        print("\n===== Sistema de Controle de Estoque Médico =====")
        print("1. Ver produtos em falta")
        print("2. Ver urgência de reposição (ordenado)")
        print("3. Buscar se um produto existe na lista (busca binária)")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            print("\n--- Produtos em Falta ---")
            mostrar_produtos_em_falta(estoque_hospitais)


        elif escolha == "2":
            print("\n--- Urgência de Reposição (Maior para Menor) ---")
            urgencias = ordenar_por_urgencia(estoque_hospitais)

            for nome, urg, hosp in urgencias:
                if urg < 20:
                    alerta = "‼️" if urg < 10 else "⚠️"
                    print(f"{alerta} {nome.title()} em {hosp} - Urgência: {urg}")
                    print("Pedido ao depósito já foi solicitado para reposição.")
                else:
                    print(f"{nome.title()} em {hosp} - estoque atual: {urg}")


        elif escolha == "3":
            lista_produtos = sorted({nome for itens in estoque_hospitais.values() for nome in itens})
            produto = input("Digite o nome do produto a buscar: ").lower()
            if busca_binaria(lista_produtos, produto):
                print(f"{produto.title()} está cadastrado no sistema.")
            else:
                print(f"{produto.title()} NÃO está no sistema.")

        elif escolha == "4":
            print("Saindo do sistema. Obrigado!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Execução principal
menu()
