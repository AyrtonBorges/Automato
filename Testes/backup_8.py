class Automato:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = dict()
        self.estado_inicial = None
        self.estados_finais = set()
        self.variaveis = set()
        self.simbolos = set()
        self.producao = dict()
        self.inicial = None

    def imprimir_automato(self):
        print("Estados: ", self.estados)
        print("Alfabeto: ", self.alfabeto)
        print("Transições: ", self.transicoes)
        print("Estado Inicial: ", self.estado_inicial)
        print("Estados Finais: ", self.estados_finais)

    def carregar_automato_arquivo(self, nome_arquivo):
        '''

            Essa função pega linha por linha e cria listas ou dicionários para armazenar o automato na memória

        '''
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                if "Q" in linha:
                    self.estados = set(linha.strip("Q = {").strip("}\n").split(";"))
                    self.estados = sorted(self.estados)
                elif "Sigma" in linha:
                    self.alfabeto = set((((linha.strip("Sigma = ")).strip("{")).strip("}\n")).split(";"))
                    self.alfabeto = sorted(self.alfabeto)
                elif "delta" in linha:
                    transicoes_raw = ((linha.strip("delta = ")).strip("{")).strip("}\n").split(";")
                    temp = self.alfabeto
                    self.transicoes = {estado: {simbolo: [] for simbolo in temp} for estado in self.estados}
                    for transicao in transicoes_raw:
                        primeira, segunda = transicao.split("->")
                        estado_atual, simbolo = ((primeira.strip("(")).strip(")")).split(",")
                        estado_proximo = list((((segunda.strip("(")).strip(")"))).split(","))
                        self.transicoes[estado_atual][simbolo] = estado_proximo
                elif "I" in linha:
                    self.estado_inicial = (((linha.strip("I = ")).strip("{")).strip("}")).strip("}\n")
                elif "F" in linha:
                    self.estados_finais = set((((linha.strip("F = ")).strip("{")).strip("}")).strip("}\n").split(";"))
                    self.estados_finais = sorted(self.estados_finais)

    def carregar_gramatica_arquivo(self, nome_arquivo):
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                if "V" in linha:
                    self.variaveis = set(linha.strip("V = {").strip("}").split(";"))
                elif "Sigma" in linha:
                    self.simbolos = set(linha.strip("Sigma = {").strip("}").split(";"))
                elif "P" in linha:
                    producao_raw = linha.strip("P = {").strip("}").split(";")
                    self.producao = {variavel: [] for variavel in self.variaveis}
                    for regra in producao_raw:
                        variavel, producao = regra.split("->")
                        if variavel in self.producao:
                            self.producao[variavel].append(producao)
                        else:
                            self.producao[variavel] = [producao]
                elif "I" in linha:
                    self.inicial = linha.strip("I = ")

    def automato_determinismo(self):
        for estado in self.transicoes:
            for simbolo in self.transicoes[estado]:
                if len(self.transicoes[estado][simbolo]) > 1:
                    print("O autômato é não-determinístico.")
                    return
        print("O autômato é determinístico.")

    def gramatica_determinismo(self):
        for variavel in self.variaveis:
            for simbolo in self.simbolos:
                producoes = [x for x in self.producao[variavel] if simbolo in x]
                if len(producoes) > 1:
                    print("A gramática não é determinística")
                    return
        print("A gramática é determinística")

    def submeter_cadeia(self, cadeia):
        temp_type = []
        estado_atual = self.estado_inicial
        estado_importante = ""
        tem = True
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:  # Verifica se o automato contém todos os simbolos, verificando até o vazio
                if simbolo != "ε":
                    print("A cadeia contém símbolos que não estão no alfabeto do autômato.")
                    return
            if type(estado_atual) == type(
                    temp_type):  # Verifica se o automato não-determinístico contém o simbolo na transição correta
                tem = False
                for i in range(len(estado_atual)):
                    if estado_atual[i] not in self.transicoes:
                        print("A cadeia foi rejeitada pelo autômato.")
                        return
                    if simbolo in self.transicoes[estado_atual[i]]:
                        estado_atual = "".join(estado_atual[i])
                        tem = True
                        break
                if tem == False:
                    print("A cadeia foi rejeitada pelo autômato.")
                    return
            else:  # Verifica se o automato determinístico contém o símbolo na transição correta
                if estado_atual not in self.transicoes or simbolo not in self.transicoes[estado_atual]:
                    print("A cadeia foi rejeitada pelo autômato.")
                    return
            if tem == False:
                print("A cadeia foi rejeitada pelo autômato.")
                return

            '''

                Verifica se é o final da cadeia, e faz a ultima verificação para identificar algum vazio e determinar se a cadeia foi ou não aceita pelo automato

            '''
            estado_importante = estado_atual
            if (simbolo == cadeia[len(cadeia) - 1]):
                for comparar in self.transicoes[estado_atual][simbolo]:
                    if comparar in self.estados_finais and "ε" in self.transicoes[comparar]:
                        estado_importante = comparar
                        break

            '''

                Coleta a próxima transição

            '''
            if type(self.transicoes[estado_atual][simbolo]) != type(temp_type):
                estado_atual = "".join(self.transicoes[estado_atual][simbolo])
            else:
                estado_atual = self.transicoes[estado_atual][simbolo]
        '''

            Printa o resultado final

        '''
        if estado_importante in self.estados_finais:
            print("A cadeia foi aceita pelo autômato.")
        else:
            print("A cadeia foi rejeitada pelo autômato.")

    def verificar_transicoes_vazio(self):
        transicoes_vazio = False
        for estado in self.transicoes:
            for simbolo in self.transicoes[estado]:
                if simbolo == "ε":
                    transicoes_vazio = True
                    break
            if transicoes_vazio:
                break
        if transicoes_vazio:
            print("O autômato possui transições em vazio.")
            opcao = input("Deseja remover as transições em vazio do autômato? (s/n) ")
            if opcao == "s":
                self.remover_transicoes_vazio()
        else:
            print("O autômato não possui transições em vazio.")

    def remover_transicoes_vazio(self):
        for transicao_temp in self.estados:
            if "ε" in self.transicoes[transicao_temp]:
                for i in self.estados:
                    for y in self.alfabeto:
                        if transicao_temp in self.transicoes[i][y]:
                            for k in range(len(self.transicoes[i][y])):
                                if transicao_temp == self.transicoes[i][y][k]:
                                    self.transicoes[i][y].pop(k)
                                    for inserir in self.transicoes[transicao_temp]["ε"]:
                                        self.transicoes[i][y].append(inserir)
                for i in self.estados:
                    if transicao_temp == i:
                        self.estados.remove(i)
                for i in self.estados_finais:
                    if transicao_temp == i:
                        self.estados_finais.remove(i)
                self.transicoes.pop(transicao_temp)

    def verificar_estados_inacessiveis(self):
        encontrou = set()
        for i in self.estados:
            if i != self.estado_inicial:
                achou = False
                for y in self.transicoes:
                    for k in self.alfabeto:
                        if i in self.transicoes[y][k]:
                            achou = True
                if (achou == False):
                    encontrou.add(i)
        for i in encontrou:
            self.estados.remove(i)
            for y in self.transicoes[i]:
                if len(self.transicoes[i][y]) > 0:
                    self.alfabeto.remove(y)
            self.transicoes.pop(i)


automato = Automato()
automato.carregar_automato_arquivo("automato.txt")
automato.automato_determinismo()
automato.imprimir_automato()
cadeia = input("Digite a cadeia para ser submetida ao autômato: ")
'''for i in range(3):
    cadeia.append(input("Digite a cadeia para ser submetida ao autômato: "))'''
automato.submeter_cadeia(cadeia)
automato.verificar_transicoes_vazio()
automato.imprimir_automato()
automato.verificar_estados_inacessiveis()
automato.imprimir_automato()