from afd import AFD

afd = AFD('./automato_config4.txt', './')

with open('./input3.txt', 'r') as file:

    index = 1
    for linha in file.readlines():
        linha = linha.strip()
        afd.exec(linha, index)
        index += 1
        print()
