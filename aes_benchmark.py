import os
import timeit
import numpy as np
import csv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Tamanhos de ficheiro 
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

# Chave e nonce (AES-CTR usa nonce de 128 bits, sem padding) 
key   = os.urandom(32)   # 256 bits
nonce = os.urandom(16)   # 128 bits

#  Funções de cifra e decifra 
def encrypt_aes(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def decrypt_aes(encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

#  Benchmark 
REPS = 30

def benchmark_aes(file_path):
    enc_times = [
        timeit.timeit(lambda: encrypt_aes(file_path), number=1) * 1e6
        for _ in range(REPS)
    ]

    encrypted_data = encrypt_aes(file_path)
    dec_times = [
        timeit.timeit(lambda: decrypt_aes(encrypted_data), number=1) * 1e6
        for _ in range(REPS)
    ]

    enc_mean, enc_std = np.mean(enc_times), np.std(enc_times, ddof=1)
    dec_mean, dec_std = np.mean(dec_times), np.std(dec_times, ddof=1)
    enc_ci = 2.045 * enc_std / np.sqrt(REPS)
    dec_ci = 2.045 * dec_std / np.sqrt(REPS)

    return enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci

#  Correr para todos os tamanhos 
results = {}
print(f"{'Tamanho':>10} | {'Enc (µs)':>10} | {'Enc std':>8} | {'Enc IC95':>8} | {'Dec (µs)':>10} | {'Dec std':>8} | {'Dec IC95':>8}")
print("-" * 80)

for size in file_sizes:
    file_path = f"ficheiros/file_{size}.txt"
    enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci = benchmark_aes(file_path)
    results[size] = (enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci)
    print(f"{size:>10} | {enc_mean:>10.2f} | {enc_std:>8.2f} | {enc_ci:>8.2f} | {dec_mean:>10.2f} | {dec_std:>8.2f} | {dec_ci:>8.2f}")

#  Guardar CSV 
os.makedirs("resultados", exist_ok=True)
with open("resultados/aes_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file_size", "enc_mean_us", "enc_std_us", "enc_ci95_us",
                                  "dec_mean_us", "dec_std_us", "dec_ci95_us"])
    for size, vals in results.items():
        writer.writerow([size, *vals])

print("\nResultados guardados em resultados/aes_results.csv")
