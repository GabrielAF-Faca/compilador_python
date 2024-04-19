from afd import AFD

import json

afd = AFD('./automato_config3.txt', './')

with open('./input3.txt', 'r') as file:

    for linha in file.readlines():
        linha = linha.strip()
        afd.exec(linha)
        print()

    print(json.dumps(afd.tabela_simbolos, indent=4))