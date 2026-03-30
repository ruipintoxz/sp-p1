import os
import timeit
import numpy as np
import csv
from cryptography.hazmat.primitives.hashes import Hash, SHA256
from cryptography.hazmat.backends import default_backend

# Tamanhos de ficheiro 
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

# Função de hash 
def sha256_hash(data):
    digest = Hash(SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()

# Benchmark 

REPS = 30

def benchmark_sha(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    times = [
        timeit.timeit(lambda: sha256_hash(data), number=1) * 1e6
        for _ in range(REPS)
    ]

    mean = np.mean(times)
    std  = np.std(times, ddof=1)
    ci   = 2.045 * std / np.sqrt(REPS)

    return mean, std, ci

# Correr para todos os tamanhos 
results = {}
print(f"{'Tamanho':>10} | {'SHA-256 (µs)':>12} | {'Std':>8} | {'IC95':>8}")
print("-" * 46)

for size in file_sizes:
    file_path = f"ficheiros/file_{size}.txt"
    mean, std, ci = benchmark_sha(file_path)
    results[size] = (mean, std, ci)
    print(f"{size:>10} | {mean:>12.2f} | {std:>8.2f} | {ci:>8.2f}")

# Guardar CSV
os.makedirs("resultados", exist_ok=True)
with open("resultados/sha_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file_size", "sha_mean_us", "sha_std_us", "sha_ci95_us"])
    for size, vals in results.items():
        writer.writerow([size, *vals])

print("\nResultados guardados em resultados/sha_results.csv")