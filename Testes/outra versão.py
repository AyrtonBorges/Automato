import re

def load_automaton(file_path):
    automaton = {"Q": [], "Sigma": [], "delta": [], "I": [], "F": []}
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r'([A-Z]+) = {(.*)}', line)
            if match:
                automaton_property = match.group(1)
                automaton_values = match.group(2)
                if automaton_property == "delta":
                    automaton_values = re.findall(r'\((.*)\)', automaton_values)
                else:
                    automaton_values = automaton_values.split(";")
                automaton[automaton_property] = automaton_values
    return automaton

def is_deterministic(automaton):
    delta = automaton['delta']
    for transition in delta:
        if ';' in transition:
            return False
    return True

def automaton_type(automaton):
    if is_deterministic(automaton):
        print("Deterministic")
    else:
        print("Non-Deterministic")

def automaton_acceptance(automaton, input_string):
    current_state = automaton['I'][0]
    for char in input_string:
        next_state = None
        for transition in automaton['delta']:
            match = re.search(r'\((.*),(.*)\)->(.*)', transition)
            if match and match.group(1) == current_state and match.group(2) == char:
                next_state = match.group(3)
                break
        if next_state is None:
            return False
        current_state = next_state
    return current_state in automaton['F']

def has_epsilon_transitions(automaton):
    for transition in automaton['delta']:
        match = re.search(r'\((.*),(.*)\)->(.*)', transition)
        if match and match.group(2) == "epsilon":
            return True
    return False

def remove_epsilon_transitions(automaton):
    new_automaton = automaton.copy()
    new_automaton["delta"] = [transition for transition in automaton["delta"] if "epsilon" not in transition]
    return new_automaton

def get_reachable_states(automaton):
    reachable_states = set()
    queue = [automaton["I"][0]]
    while queue:
        state = queue.pop(0)
        reachable_states.add(state)
        for transition in automaton["delta"]:
            match = re.search(r'\((.*),(.*)\)->(.*)', transition)
            if match and match.group(1) == state:
                next_state = match.group(3)
                if next_state not in reachable_states:
                    queue.append(next_state)
    return reachable_states

def remove_unreachable_states(automaton):
    reachable_states = get_reachable_states(automaton)
    new_automaton = {}
    new_automaton["Q"] = list(reachable_states & set(automaton["Q"]))
    new_automaton["Sigma"] = automaton["Sigma"]
    new_automaton["delta"] = [transition for transition in automaton["delta"] if any(state in reachable_states for state in re.findall(r'(q[0-9]+)', transition))]
    new_automaton["I"] = [state for state in automaton["I"] if state in reachable_states]
    new_automaton["F"] = list(reachable_states & set(automaton["F"]))
    return new_automaton

def get_useful_states(automaton):
    useful_states = set(automaton["F"])
    queue = list(automaton["F"])
    while queue:
        state = queue.pop(0)
        for transition in automaton["delta"]:
            match = re.search(r'\((.*),(.*)\)->(.*)', transition)
            if match and match.group(3) == state:
                prev_state = match.group(1)
                if prev_state not in useful_states:
                    useful_states.add(prev_state)
                    queue.append(prev_state)
    return useful_states

def remove_useless_states(automaton):
    useful_states = get_useful_states(automaton)
    new_automaton = {}
    new_automaton["Q"] = list(useful_states & set(automaton["Q"]))
    new_automaton["Sigma"] = automaton["Sigma"]
    new_automaton["delta"] = [transition for transition in automaton["delta"] if any(state in useful_states for state in re.findall(r'(q[0-9]+)', transition))]
    new_automaton["I"] = [state for state in automaton["I"] if state in useful_states]
    new_automaton["F"] = list(useful_states & set(automaton["F"]))
    return new_automaton

def automaton_to_grammar(automaton):
    grammar = {}
    grammar["N"] = automaton["Q"]
    grammar["S"] = automaton["I"][0]
    grammar["T"] = automaton["Sigma"]
    grammar["P"] = {}
    for state in automaton["Q"]:
        grammar["P"][state] = []
    for transition in automaton["delta"]:
        match = re.search(r'\((.*),(.*)\)->(.*)', transition)
        if match:
            current_state = match.group(1)
            char = match.group(2)
            next_state = match.group(3)
            grammar["P"][current_state].append(char + next_state)
    return grammar

def grammar_to_automaton(grammar_file):
    automaton = {}
    with open(grammar_file, 'r') as file:
        for line in file:
            match = re.search(r'([A-Z]+) = {(.*)}', line)
            if match:
                automaton[match.group(1)] = match.group(2).split(';')
    automaton["delta"] = []
    for production in automaton["P"]:
        for production_rule in production.split("|"):
            automaton["delta"].append("(" + production.split("->")[0] + "," + production_rule[0] + ")->" + production_rule[1])
    return automaton

if __name__ == "__main__":

    # Carregando o autômato finito
    automaton = load_automaton("automato.txt")
    print("Automaton Loaded: ", automaton)

    # Verificando se o autômato é determinístico ou não-determinístico
    automaton_type(automaton)

    # Lendo uma cadeia de entrada e verificando se é aceita pelo autômato
    input_string = input("Enter input string: ")
    if automaton_acceptance(automaton, input_string):
        print("Accepted")
    else:
        print("Rejected")

    # Verificando se o autômato possui transições em vazio
    if has_epsilon_transitions(automaton):
        print("Automaton has epsilon transitions")
        choice = input("Do you want to remove epsilon transitions? (y/n)")
        if choice == "y":
            automaton = remove_epsilon_transitions(automaton)
            print("Automaton after removing epsilon transitions: ", automaton)

    # Verificando se o autômato possui estados inacessíveis
    unreachable_states = set(automaton["Q"]) - get_reachable_states(automaton)
    if unreachable_states:
        print("Automaton has unreachable states: ", unreachable_states)
        choice = input("Do you want to remove unreachable states? (y/n)")
        if choice == "y":
            automaton = remove_unreachable_states(automaton)
            print("Automaton after removing unreachable states: ", automaton)

    # Verificando se o autômato possui estados inúteis
    useful_states = get_useful_states(automaton)
    if set(automaton["Q"]) - useful_states:
        print("Automaton has useless states: ", set(automaton["Q"]) - useful_states)
        choice = input("Do you want to remove useless states? (y/n)")
        if choice == "y":
            automaton = remove_useless_states(automaton)
            print("Automaton after removing useless states: ", automaton)

    # Gerando uma gramática linear à direita a partir do autômato finito
    if is_deterministic(automaton):
        grammar = automaton_to_grammar(automaton)
        print("Grammar generated from automaton: ", grammar)

    # Gerando um autômato finito a partir de uma gramática linear à direita
    grammar_file = input("Enter the path of grammar file: ")
    automaton = grammar_to_automaton(grammar_file)
    print("Automaton generated from grammar: ", automaton)