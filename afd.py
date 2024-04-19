import json


class NotAStateError(Exception):
    def __init__(self, state):
        super().__init__(f"State '{state}' not defined in config file")


class NotATokenError(Exception):
    def __init__(self, token):
        super().__init__(f"Token '{token}' not defined in config file")


class NotFinalStateError(Exception):
    def __init__(self, state, state_input):
        super().__init__(f"State '{state}' not defined as final in config file. (Input: {state_input})")


class AFD:

    def __init__(self, config_path, save_path):

        self.save_path = save_path
        self.ref_stack = []

        self.tabela_simbolos = {}

        with open(config_path, 'r') as file:
            self.states = file.readline().strip().split(',')
            self.tokens = list(file.readline().strip())
            self.final_states = {}
            self.transitions = []
            self.actual_state = self.states[0]
            self.state_indexes = dict([(state, []) for state in self.states])

            finals = file.readline().strip().split(',')

            for state in finals:

                f, v = state.split(':')

                try:
                    self.states.index(f)
                except ValueError:
                    raise NotAStateError(f)

                self.final_states[f] = v

            index = 0
            for line in file.readlines():
                line = line.strip()

                transition = line.split(":")

                if len(transition) > 3:
                    transition[1] += ':'
                    transition[1] += transition[2]
                    transition.remove(transition[2])

                istate, ttokens, fstate = transition

                try:
                    self.states.index(istate)
                except ValueError:
                    raise NotAStateError(istate)

                self.state_indexes[istate].append(index)
                index += 1

                try:
                    self.states.index(fstate)
                except ValueError:
                    raise NotAStateError(fstate)

                for token in ttokens:

                    try:
                        self.tokens.index(token)
                    except ValueError:
                        raise NotATokenError(token)

                self.transitions.append({
                    'istate': istate,
                    'tokens': ttokens,
                    'fstate': fstate
                })

    def find_transition(self, token):

        for i in self.state_indexes[self.actual_state]:

            if token in self.transitions[i]['tokens']:
                return token, self.transitions[i]

        return token, None

    def exec(self, afd_input, line):
        if not len(afd_input):
            return

        self.actual_state = self.states[0]

        tabela = []
        char_stack = ""

        char = 0

        while char < len(afd_input):

            c, t = self.find_transition(afd_input[char])
            print(c, t)

            if t:
                self.actual_state = t['fstate']

            else:
                try:
                    print(self.actual_state)
                    tabela.append((char_stack, self.final_states[self.actual_state]))
                except KeyError:
                    print(f"{afd_input} -> Não reconhecido")
                    return None

                self.actual_state = self.states[0]
                char_stack = ""

                if c != ' ':
                    continue

            if c != ' ':
                char_stack += c

            char += 1

        tabela.append((char_stack, self.final_states[self.actual_state]))
        print(tabela)

        try:
            print(afd_input, '->', self.final_states[self.actual_state])
        except KeyError:
            raise NotFinalStateError(self.actual_state, afd_input)

        for e in tabela:
            ref = None
            tabela_id = len(self.tabela_simbolos) + 1

            if e[1] in ['apar', 'ach', 'acol']:
                self.ref_stack.append(tabela_id)

            elif e[1] in ['fpar', 'fch', 'fcol']:
                ref = self.ref_stack.pop()

            self.tabela_simbolos[tabela_id] = {
                'token': e[0],
                'tipo': e[1],
                'linha': line,
                'ref': ref
            }

        with open(f'{self.save_path}/tabela_simbolos.json', 'w', encoding='utf8') as file:
            file.write(json.dumps(self.tabela_simbolos, indent=4))
