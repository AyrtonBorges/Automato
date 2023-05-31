#import copy
import copy

class Automato:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = dict()
        self.estado_inicial = ""
        self.estados_finais = set()
        self.variaveis = set()
        self.simbolos = set()
        self.producao = dict()
        self.inicial = ""
        self.estados_aceitacao = set()

    def imprimir_gramatica(self):
        print("Variavel: ", self.variaveis)
        print("Simbolos: ", self.simbolos)
        print("Producao: ", self.producao)
        print("Inicial: ", self.inicial)

    def imprimir_automato(self):
        '''

            Exibe na tela todas as informações

        '''
        print("Estados: ", self.estados)
        print("Alfabeto: ", self.alfabeto)
        print("Transições: ", self.transicoes)
        print("Estado Inicial: ", self.estado_inicial)
        print("Estados Finais: ", self.estados_finais)

    def salvar_automato(self, auto, nome_arquivo):
        '''

            Salva o automato em um arquivo

        '''
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write("Q = {" + ";".join(auto.estados) + "}\n")
            arquivo.write("Sigma = {" + ";".join(auto.alfabeto) + "}\n")
            arquivo.write("delta = {")
            transicoes = []
            for estado_atual in auto.transicoes:
                for simbolo in auto.transicoes[estado_atual]:
                    estado_proximo = auto.transicoes[estado_atual][simbolo]
                    if(len(estado_proximo) > 1):
                        temp = "(" + ",".join(estado_proximo) + ")"
                        transicoes.append(("(" + estado_atual + "," + simbolo + ")->" + temp))
                    elif(len(estado_proximo) == 1):
                        transicoes.append(("(" + estado_atual + "," + simbolo + ")->" + estado_proximo[0]))
            arquivo.write(";".join(transicoes) + "}\n")
            arquivo.write("I = " + auto.estado_inicial + "\n")
            arquivo.write("F = {" + ";".join(auto.estados_finais) + "}\n")
        print("Arquivo "+nome_arquivo+".txt salvo!")
    def carregar_automato_arquivo(self, nome_arquivo):
        '''

            Essa função pega linha por linha e cria listas ou dicionários para armazenar o automato na memória

        '''
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                if "Q" in linha:
                    self.estados = set(linha.strip("Q = {").strip("}\n").split(";"))
                    self.estados = copy.deepcopy(sorted(self.estados))
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
        temp_variavel = set()
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                if "V" in linha:
                    self.variaveis = set(((linha.strip("V = {")).strip("}\n")).split(";"))
                    self.variaveis = sorted(self.variaveis)
                    for i in self.variaveis:
                        if i.isupper():
                            temp_variavel.add(i)
                    self.variaveis = temp_variavel
                elif "Sigma" in linha:
                    self.simbolos = set(((linha.strip("Sigma = ").strip("{")).strip("}\n")).split(";"))
                    self.simbolos = sorted(self.simbolos)
                elif "P" in linha:
                    producao_raw = (((linha.strip("P = ")).strip("{")).strip("}\n")).split(";")
                    self.producao = {variavel: [] for variavel in temp_variavel}
                    for regra in producao_raw:
                        variavel, producao = regra.split("->")
                        if variavel in self.producao:
                            self.producao[variavel].append(producao)
                        else:
                            self.producao[variavel] = [producao]
                elif "I" in linha:
                    self.inicial = linha.strip("I = ")

    def automato_deterministico(self):
        for estado in self.transicoes:
            for simbolo in self.transicoes[estado]:
                if len(self.transicoes[estado][simbolo]) > 1:
                    print("O autômato é não-determinístico.")
                    return False
        print("O autômato é determinístico.")
        return True

    '''def gramatica_deterministico(self):
        for variavel in self.variaveis:
            for simbolo in self.simbolos:
                producoes = [x for x in self.producao[variavel] if simbolo in x]
                if len(producoes) > 1:
                    print("A gramática não é determinística")
                    return
        print("A gramática é determinística")'''
    def submeter_cadeia(self, cadeia):
        '''

            Função que submete uma cadeia no automato

        '''
        temp_type = []
        estado_atual = self.estado_inicial
        estado_importante = ""
        tem = True
        for simbolo in cadeia:
                if simbolo not in self.alfabeto: #Verifica se o automato contém todos os simbolos, verificando até o vazio
                    if simbolo != "ε":
                        print("A cadeia contém símbolos que não estão no alfabeto do autômato.")
                        return
                if type(estado_atual) == type(temp_type): #Verifica se o automato não-determinístico contém o simbolo na transição correta
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
                else: #Verifica se o automato determinístico contém o símbolo na transição correta
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
                if(simbolo == cadeia[len(cadeia)-1]):
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
        '''

            Verifica transições vazias

        '''
        print("Função verificar transições vazias escolhida!")
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
        auto = self
        for transicao_temp in auto.estados:
            if "ε" in auto.transicoes[transicao_temp]:
                for i in auto.estados:
                    for y in auto.alfabeto:
                        if transicao_temp in auto.transicoes[i][y]:
                            for k in range(len(auto.transicoes[i][y])):
                                if transicao_temp == auto.transicoes[i][y][k]:
                                    auto.transicoes[i][y].pop(k)
                                    for inserir in auto.transicoes[transicao_temp]["ε"]:
                                            auto.transicoes[i][y].append(inserir)
                vezes = 0
                for i in auto.estados:
                    if transicao_temp == i:
                        for x in auto.transicoes[i]:
                            if(len(auto.transicoes[i][x]) > 0):
                                vezes += 1
                auto.transicoes[transicao_temp]["ε"] = []
                if (vezes == 1):
                    auto.estados.remove(i)
                    if (i in auto.estados_finais):
                        auto.estados_finais.remove(i)

                """for i in auto.estados_finais:
                    if transicao_temp == i:
                        auto.estados_finais.remove(i)
                auto.transicoes.pop(transicao_temp)"""
        nome_arquivo = input("Insira o nome do arquivo: ")
        self.salvar_automato(auto, nome_arquivo)

    def verificar_estados_inacessiveis(self):
        print("Função verificar estados inacessiveis escolhida!")
        auto = self
        encontrou = set()
        for i in auto.estados:
            if i != auto.estado_inicial:
                achou = False
                for y in auto.transicoes:
                    for k in auto.alfabeto:
                        if i in auto.transicoes[y][k]:
                            achou = True
                if (achou == False):
                    encontrou.add(i)
        for i in encontrou:
            auto.estados.remove(i)
            for y in auto.transicoes[i]:
                if len(auto.transicoes[i][y]) > 0:
                    auto.alfabeto.remove(y)
            auto.transicoes.pop(i)
        nome_arquivo = input("Insira o nome do arquivo: ")
        self.salvar_automato(auto, nome_arquivo)

    def verificar_estados_inuteis(self):
        confirmar = self.automato_deterministico()
        if (confirmar):
            print("Então pode usar a função!")
            estados_inuteis = set()
            estados_uteis = []
            estados_finais = set(self.estados_finais)

            auto = self
            encontrou = set()
            for i in auto.estados:
                if i != auto.estado_inicial:
                    achou = False
                    for y in auto.transicoes:
                        for k in auto.alfabeto:
                            if i in auto.transicoes[y][k]:
                                achou = True
                    if (achou == False):
                        encontrou.add(i)
            temp_estados = copy.deepcopy(self.estados)
            for i in encontrou:
                temp_estados.remove(i)

            agora = copy.deepcopy(self.estados_finais[0])
            while True:
                continua = True
                novos_estados_uteis = set()
                temp_estados = sorted(temp_estados, reverse=True)
                for estado_atual in temp_estados:
                    for simbolo in self.transicoes[estado_atual]:
                        if (estado_atual is not estados_uteis or estado_atual in self.estados_finais) and agora in \
                                self.transicoes[estado_atual][simbolo]:
                            continua = False
                            agora = estado_atual
                            estados_uteis.append(estado_atual)
                estados_uteis = sorted(estados_uteis)
                if (continua):
                    break
            # Adiciona todos os estados não úteis à lista de estados inúteis
            for i in estados_uteis:
                temp_estados.remove(i)
            estados_inuteis = temp_estados
            # Verifica se existe algum estado inútil
            if estados_inuteis:
                print("O autômato possui estados inúteis.")
                opcao = input("Deseja removê-los? (s/n) ")

                if opcao.lower() == "s":
                    for estado_inutil in estados_inuteis:
                        # Remove as transições que levam ao estado inútil
                        temp_letra = ""
                        for i in self.estados:
                            for y in self.alfabeto:
                                if estado_inutil in self.transicoes[i][y]:
                                    temp_letra = copy.deepcopy(y)
                                    self.transicoes[i][y].remove(estado_inutil)
                        temp_bool = True
                        print(temp_letra)
                        for i in self.estados:
                            if (len(self.transicoes[i][temp_letra]) > 0):
                                temp_bool = False
                        if (temp_bool):
                            self.alfabeto.remove(temp_letra)
                            for i in self.estados:
                                del self.transicoes[i][temp_letra]
                        del self.transicoes[estado_inutil]

                        # Remove o estado inútil da lista de estados
                        self.estados.remove(estado_inutil)
                    nome = input("Insira o nome do arquivo: ")
                    self.salvar_automato(self, (nome + ".txt"))
                    print("Estados inúteis removidos.")
            else:
                print("Não há estados inúteis no autômato.")
        else:
            print("Então não pode usar a função!")

    def gerar_gramatica_linear_direita(self, automato):
        producoes = {}
        for estado in automato.estados:
            for simbolo in automato.alfabeto:
                estado_proximo = copy.deepcopy(automato.transicoes[estado][simbolo])
                if estado_proximo:
                    if estado not in producoes:
                        producoes[estado] = []
                    producoes[estado].append(simbolo + estado_proximo[0].upper())
        for estado_final in automato.estados_finais:
            if estado_final not in producoes:
                producoes[estado_final] = []
            producoes[estado_final].append("ε")
        for i in range(len(automato.estados)):
            automato.estados[i] = automato.estados[i].upper()
        automato2 = Automato()
        automato2.variaveis = copy.deepcopy(automato.alfabeto)+copy.deepcopy(automato.estados)
        automato2.simbolos = copy.deepcopy(automato.alfabeto)
        automato2.producao = copy.deepcopy(producoes)
        automato2.inicial = copy.deepcopy(automato.estado_inicial)

        return automato2

    def salvar_gramatica(self, gramatica, nome_arquivo):
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write("V = {" + ";".join(gramatica.variaveis) + "}\n")
            arquivo.write("Sigma = {" + ";".join(gramatica.simbolos) + "}\n")
            arquivo.write("P = {")
            producoes = []
            for variavel, producao in gramatica.producao.items():
                for prod in producao:
                    producoes.append(variavel.upper() + "->" + prod)
            arquivo.write(";".join(producoes) + "}\n")
            arquivo.write("I = " + str(gramatica.inicial).upper() + "\n")

    def gerar_automato_deterministico(self, gramatica_arquivo):
        with open(gramatica_arquivo) as arquivo:
            variaveis = set()
            terminais = set()
            producoes = {}
            inicial = None
            for linha in arquivo:
                partes = linha.strip().split("=")
                if partes[0].strip() == "V":
                    variaveis = set(partes[0].strip().strip("{").strip("}").split(";"))
                elif partes[0].strip() == "Sigma":
                    terminais = set(partes[1].strip().strip("{").strip("}").split(";"))
                elif partes[0].strip() == "P":
                    producao = partes[1].strip().strip("{").strip("}").split(";")
                    for p in producao:
                        var, producao = p.strip().split("->")
                        if var not in producoes:
                            producoes[var] = []
                        producoes[var].append(producao)
                elif partes[0].strip() == "I":
                    inicial = partes[1].strip()

        estados = variaveis.copy()
        estados.add("inicial")
        simbolos = terminais.copy()
        inicial = "inicial"
        finais = variaveis.copy()
        transicoes = {}
        for variavel, producoes in producoes.items():
            for producao in producoes:
                novo_estado = variavel + "_" + producao
                estados.add(novo_estado)
                transicoes[(variavel, producao[0])] = novo_estado
                for simbolo in producao[1:]:
                    proximo_estado = novo_estado + "_" + simbolo
                    estados.add(proximo_estado)
                    transicoes[(novo_estado, simbolo)] = proximo_estado
                    novo_estado = proximo_estado
                finais.add(novo_estado)

        self.estados = estados
        self.alfabeto = simbolos
        self.inicial = inicial
        self.finais = finais
        self.transicoes = transicoes
        print(self.estados)
        print(self.simbolos)
        print(self.inicial)
        print(self.finais)
        print(self.transicoes)



def copiar(self, entrada):
    self.estados = copy.deepcopy(entrada.estados)
    self.alfabeto = copy.deepcopy(entrada.alfabeto)
    self.transicoes = copy.deepcopy(entrada.transicoes)
    self.estado_inicial = copy.deepcopy(entrada.estado_inicial)
    self.estados_finais = entrada.estados_finais

automato = Automato()
automato.carregar_automato_arquivo("automato.txt")
automato.automato_deterministico()
automato.imprimir_automato()
cadeia = input("Digite a cadeia para ser submetida ao autômato: ")
'''for i in range(3):
    cadeia.append(input("Digite a cadeia para ser submetida ao autômato: "))'''
automato.submeter_cadeia(cadeia)
automato2 = Automato()
copiar(automato2,automato)
automato2.verificar_transicoes_vazio()
copiar(automato2,automato)
automato2.verificar_estados_inacessiveis()
automato.imprimir_automato()
automato_temp = copy.deepcopy(automato)
automato_temp.verificar_estados_inuteis()
automato.imprimir_automato()
nome = input("Insira o nome do arquivo: ")
automato.salvar_gramatica(automato.gerar_gramatica_linear_direita(automato), (nome+".txt"))

