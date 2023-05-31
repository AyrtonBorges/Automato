def load_automaton(filepath):
    automaton = {}
    with open(filepath, "r") as config_file:
        for line in config_file:
            key, value = line.strip().split(" = ")
            automaton[key] = set(value.split(";"))
    return automaton

def is_deterministic(automaton):
    delta_transitions = automaton["delta"]
    for transition in delta_transitions:
        current_state, input_symbol = transition.split(",")
        matching_transitions = [t for t in delta_transitions if t.startswith(f"({current_state},{input_symbol})")]
        if len(matching_transitions) > 1:
            return False
    return True

def check_string(automaton, string):
    current_state = automaton["I"]
    for symbol in string:
        transition = f"({current_state},{symbol})"
        if transition in automaton["delta"]:
            next_state = automaton["delta"][transition]
            current_state = next_state
        else:
            return "Cadeia rejeitada"
    if current_state in automaton["F"]:
        return "Cadeia aceita"
    else:
        return "Cadeia rejeitada"

def has_epsilon_transitions(automaton):
    for transition in automaton["delta"]:
        _, input_symbol = transition.split(",")
        if input_symbol == "ε":
            return True
    return False

def remove_unreachable_states(automaton):
    reachable_states = set()
    queue = [automaton["I"]]
    while queue:
        current_state = queue.pop(0)
        reachable_states.add(current_state)
        for transition in automaton["delta"]:
            state, symbol = transition.split(",")
            if state == current_state and symbol != "ε" and transition not in reachable_states:
                next_state = automaton["delta"][transition]
                queue.append(next_state)
    automaton["Q"] = reachable_states
    return automaton

def remove_useless_states(automaton):
    useful_states = set(automaton["F"])
    queue = list(automaton["F"])
    while queue:
        current_state = queue.pop(0)
        for transition in automaton["delta"]:
            symbol, next_state = transition.split(",")
            if next_state == current_state and transition not in useful_states:
                state = transition.split(",")[0][1:]
                queue.append(state)
                useful_states.add(state)
    automaton["Q"] = useful_states
    return automaton

def automaton_to_grammar(automaton):
    if not is_deterministic(automaton):
        raise ValueError("O autômato não é determinístico.")

    grammar = {}
    grammar["V"] = automaton["Q"]
    grammar["Sigma"] = automaton["Sigma"]
    grammar["P"] = set()
    grammar["S"] = automaton["I"]

    for transition in automaton["delta"]:
        state, symbol = transition.split(",")
        next_state = automaton["delta"][transition]
        rule = f"{state}->{symbol}{next_state}"
        grammar["P"].add(rule)
    return grammar

def grammar_to_automaton(grammar):
    automaton = {}
    automaton["Q"] = grammar["V"]
    automaton["Sigma"] = grammar["Sigma"]
    automaton["delta"] = {}
    automaton["I"] = grammar["S"]
    automaton["F"] = set()

    for production in grammar["P"]:
        state, symbol_next_state = production.split("->")
        next_state = symbol_next_state[-1]
        if next_state in automaton["Q"]:
            automaton["F"].add(next_state)
        for symbol in symbol_next_state[:-1]:
            if symbol in automaton["Sigma"]:
                transition = f"({state},{symbol})"
                automaton["delta"][transition] = next_state
    return automaton


automaton = load_automaton("automaton_config.txt")
print(automaton)
deterministic = is_deterministic(automaton)
print("O autômato é determinístico" if deterministic else "O autômato é não-determinístico")
string = []
for t in range(3):
    string.append(input("Insira a cadeia para verificação: "))
result = check_string(automaton, string)
print(result)
epsilon_transitions = has_epsilon_transitions(automaton)
if epsilon_transitions:
    print("O autômato é finito não-determinístico com transições em vazio.")
else:
    print("O autômato não possui transições em vazio.")
automaton = remove_unreachable_states(automaton)
print("Estados acessíveis: ", automaton["Q"])
automaton = remove_useless_states(automaton)
print("Estados úteis: ", automaton["Q"])
grammar = automaton_to_grammar(automaton)
print(grammar)
automaton = grammar_to_automaton(grammar)
print(automaton)


