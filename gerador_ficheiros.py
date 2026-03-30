import os # Importa funções do Operative System (Criar pastas e gerar bytes aleatórios)

tamanho = [8, 64, 512, 4096, 32768, 262144, 2097152] # Lista dos tamanhos dos ficheiros em bytes

os.makedirs("ficheiros", exist_ok=True) # Cria uma pasta "ficheiros", para onde vão ser enviados os ficheiros

for x in tamanho: # corre os tamanhos
    nome = f"ficheiros/file_{x}.txt" # Cria o nome do ficheiro dependente do tamanho do mesmo
    
    data = os.urandom(x)  # Gera x bytes aleatórios
    
    with open(nome, "wb") as f: # abre o ficheiro em modo de escrita binária (wb)
        f.write(data) # Escreve os dados gerados no ficheiro

    print(f"Ficheiro criado: {nome} ({x} bytes)") # Dá um feedback no terminal que o ficheiro foi criado com sucesso
