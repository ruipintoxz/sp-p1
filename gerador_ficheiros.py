import os

tamanho = [8, 64, 512, 4096, 32768, 262144, 2097152]

os.makedirs("ficheiros", exist_ok=True)

for x in tamanho:
    nome = f"ficheiros/file_{x}.txt"
    
    data = os.urandom(x)
    
    with open(nome, "wb") as f:
        f.write(data)

    print(f"Ficheiro criado: {nome} ({x} bytes)")