def carregar_automato(nome_arquivo):
    automato = {}
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            config = (((linha.strip("\n")).strip("{")).strip("}")).split(" = ")
            config[1] = ((config[1].strip("{")).strip("}")).strip().split(";")
            automato[config[0]] = config[1]
    return automato

def verificar_determinismo(automato):
    delta = automato["delta"]
    alfabeto = automato["Sigma"]

    for transicao in delta:
        estado_atual, simbolo = transicao.split(",")
        contador = 0
        for t in delta:
            if estado_atual in t and simbolo in t:
                contador += 1
        if contador > 1:
            return "Não-determinístico"
    return "Determinístico"

def verificar_cadeia(automato):
    cadeia = input("Informe a cadeia a ser verificada: ")
    estado_atual = "".join(automato["I"])
    delta = automato["delta"]
    alfabeto = automato["Sigma"]
    estados_finais = "".join(automato["F"])
    for simbolo in cadeia:
        if simbolo not in alfabeto:
            return "Rejeitado"
        transicao = "".join(estado_atual) + "," + simbolo
        novo_estado = ""
        for t in delta:
            if transicao in t:
                novo_estado = t.split("->")[1]
                break
        if novo_estado == "":
            return "Rejeitado"
        estado_atual = novo_estado

    if estado_atual in estados_finais:
        return "Aceito"
    else:
        return "Rejeitado"

def verificar_transicoes_vazio(automato):
    delta = automato["delta"]
    transicoes_vazio = []
    for transicao in delta:
        estado_atual, simbolo = transicao.split(",")
        temp,saia = simbolo.split("->")
        print(transicao.split("->")[1])
        if temp == "ε)":
            transicoes_vazio.append((estado_atual.strip("("), transicao.split("->")[1]))
    if len(transicoes_vazio) > 0:
        print("O autômato possui transições em vazio.")
        opcao = input("Deseja criar um autômato finito equivalente sem transições em vazio? (S/N)")
        if opcao.upper() == "S":
            print(transicoes_vazio)
            novo_automato = remover_transicoes_vazio(automato, transicoes_vazio)
            return novo_automato
        else:
            return automato
    else:
        print("O autômato não possui transições em vazio.")
        return automato

def remover_transicoes_vazio(automato, transicoes_vazio):
    novo_automato = automato.copy()
    novo_delta = []
    estados = automato["Q"]
    alfabeto = automato["Sigma"]
    estado_inicial = "".join(automato["I"])
    for estado in estados:
        print(estado)
        alcancaveis = alcancaveis_transicoes_vazio(estado, transicoes_vazio)
        for simbolo in alfabeto:
            transicao = estado + "," + simbolo
            novo_estado = ""
            for t in automato["delta"]:
                if transicao in t:
                    novo_estado = t.split("->")[1]
                    break
            for alcancavel in alcancaveis:
                if novo_estado != "":
                    nova_transicao = "("+alcancavel + "," + simbolo+ ")" + "->" + novo_estado
                    novo_delta.append(nova_transicao)

    novo_automato["delta"] = novo_delta
    novo_automato["I"] = alcancaveis_transicoes_vazio(estado_inicial, transicoes_vazio)
    return novo_automato

def alcancaveis_transicoes_vazio(estado, transicoes_vazio):
    alcancaveis = [estado]
    verificar = [estado]
    while len(verificar) > 0:
        atual = verificar.pop(0)
        for transicao in transicoes_vazio:
            if transicao[0] == atual and transicao[1] not in alcancaveis:
                alcancaveis.append(transicao[1])
                verificar.append(transicao[1])
    return alcancaveis

automato = carregar_automato("automato.txt")
print(automato)
determinismo = verificar_determinismo(automato)
print(determinismo)
resultado = verificar_cadeia(automato)
print(resultado)
automato_sem_transicoes_vazio = verificar_transicoes_vazio(automato)
print(automato_sem_transicoes_vazio)

