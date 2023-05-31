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
        print("Variaveis: ", self.variaveis)
        print("Simbolos: ", self.simbolos)
        print("Producoes: ", self.producao)
        print("Estado Inicial: ", self.inicial)

    def carregar_automato_arquivo(self, nome_arquivo):
        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                if "Q" in linha:
                    self.estados = set(linha.strip("Q = {").strip("}\n").split(";"))
                elif "Sigma" in linha:
                    self.alfabeto = set((((linha.strip("Sigma = ")).strip("{")).strip("}\n")).split(";"))
                elif "delta" in linha:
                    transicoes_raw = ((linha.strip("delta = ")).strip("{")).strip("}\n").split(";")
                    print(transicoes_raw)
                    self.transicoes = {estado: {simbolo: [] for simbolo in self.alfabeto} for estado in self.estados}
                    for transicao in transicoes_raw:
                        estado_atual, simbolo_estado_proximo = ((transicao.strip("(")).strip("\n")).split(",")
                        simbolo, estado_proximo = simbolo_estado_proximo.split(")->")
                        print(estado_atual)
                        print(simbolo)
                        print(estado_proximo)
                        self.transicoes[estado_atual][simbolo].append(estado_proximo.strip("\n"))
                elif "I" in linha:
                    self.estado_inicial = (linha.strip("I = ")).strip("\n")
                elif "F" in linha:
                    self.estados_finais = set((((linha.strip("F = ")).strip("{")).strip("}")).strip("\n").split(";"))

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
        estado_atual = self.estado_inicial
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                print("A cadeia contém símbolos que não estão no alfabeto do autômato.")
                return
            if estado_atual not in self.transicoes or simbolo not in self.transicoes[estado_atual]:
                print("A cadeia foi rejeitada pelo autômato.")
                return
            estado_atual = "".join(self.transicoes[estado_atual][simbolo])
        if estado_atual in self.estados_finais:
            print("A cadeia foi aceita pelo autômato.")
        else:
            print("A cadeia foi rejeitada pelo autômato.")

automato = Automato()
automato.carregar_automato_arquivo("automato.txt")
automato.automato_determinismo()
automato.imprimir_automato()
cadeia = input("Digite a cadeia para ser submetida ao autômato: ")
'''for i in range(3):
    cadeia.append(input("Digite a cadeia para ser submetida ao autômato: "))'''
automato.submeter_cadeia(cadeia)
automato.carregar_gramatica_arquivo("gramatica.txt.txt")
automato.gramatica_determinismo()