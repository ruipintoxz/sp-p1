import os
import timeit
import numpy as np
import csv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Tamanho dos ficheiros
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

key = os.urandom(32)  # AES-256

# Funções de Encriptação e Desencriptação
def encrypt_data(data):
    nonce = os.urandom(16)  # novo nonce por execução
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    return nonce + encryptor.update(data) + encryptor.finalize()

def decrypt_data(encrypted_data):
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


# Benchmark com o mesmo ficheiro

REPS = 30

def benchmark_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    enc_times = [
        timeit.timeit(lambda: encrypt_data(data), number=1) * 1e6
        for _ in range(REPS)
    ]

    encrypted = encrypt_data(data)

    dec_times = [
        timeit.timeit(lambda: decrypt_data(encrypted), number=1) * 1e6
        for _ in range(REPS)
    ]

    enc_mean, enc_std = np.mean(enc_times), np.std(enc_times, ddof=1)
    dec_mean, dec_std = np.mean(dec_times), np.std(dec_times, ddof=1)

    enc_ci = 2.045 * enc_std / np.sqrt(REPS)
    dec_ci = 2.045 * dec_std / np.sqrt(REPS)

    return enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci


# Benchmark com ficheiros diferentes

def benchmark_random(size):
    enc_times = []
    dec_times = []

    for _ in range(REPS):
        data = os.urandom(size)

        enc_time = timeit.timeit(lambda: encrypt_data(data), number=1) * 1e6
        enc_times.append(enc_time)

        encrypted = encrypt_data(data)

        dec_time = timeit.timeit(lambda: decrypt_data(encrypted), number=1) * 1e6
        dec_times.append(dec_time)

    enc_mean, enc_std = np.mean(enc_times), np.std(enc_times, ddof=1)
    dec_mean, dec_std = np.mean(dec_times), np.std(dec_times, ddof=1)

    enc_ci = 2.045 * enc_std / np.sqrt(REPS)
    dec_ci = 2.045 * dec_std / np.sqrt(REPS)

    return enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci



# Correr para todos os ficheiros

print("\n=== TESTE COM FICHEIROS ===")
print(f"{'Tamanho':>10} | {'Enc (µs)':>10} | {'Enc std':>8} | {'Enc IC95':>8} | {'Dec (µs)':>10} | {'Dec std':>8} | {'Dec IC95':>8}")
print("-" * 80)

results = {}

for size in file_sizes:
    file_path = f"ficheiros/file_{size}.txt"

    enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci = benchmark_file(file_path)
    results[size] = (enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci)

    print(f"{size:>10} | {enc_mean:>10.2f} | {enc_std:>8.2f} | {enc_ci:>8.2f} | {dec_mean:>10.2f} | {dec_std:>8.2f} | {dec_ci:>8.2f}")


# Correr para um mesmo ficheiro

print("\n=== TESTE: MESMO FICHEIRO (4096 bytes) ===")
test_file = "ficheiros/file_4096.txt"

enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci = benchmark_file(test_file)

print(f"Encrypt: média={enc_mean:.2f} µs | std={enc_std:.2f} | IC95={enc_ci:.2f}")
print(f"Decrypt: média={dec_mean:.2f} µs | std={dec_std:.2f} | IC95={dec_ci:.2f}")

# Correr para um ficheiro aleatório

print("\n=== TESTE: FICHEIROS ALEATÓRIOS (4096 bytes) ===")

enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci = benchmark_random(4096)

print(f"Encrypt: média={enc_mean:.2f} µs | std={enc_std:.2f} | IC95={enc_ci:.2f}")
print(f"Decrypt: média={dec_mean:.2f} µs | std={dec_std:.2f} | IC95={dec_ci:.2f}")



# Guardar CSV

os.makedirs("resultados", exist_ok=True)

with open("resultados/aes_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file_size", "enc_mean_us", "enc_std_us", "enc_ci95_us",
                     "dec_mean_us", "dec_std_us", "dec_ci95_us"])
    for size, vals in results.items():
        writer.writerow([size, *vals])

print("\nResultados guardados em resultados/aes_results.csv")
