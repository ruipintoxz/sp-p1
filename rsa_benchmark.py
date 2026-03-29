import os
import timeit
import numpy as np
import csv
import struct
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Tamanho dos ficheiros
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

# Gerar par de chaves RSA 2048 bits 
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Função auxiliar: H(i, r) = SHA-256(i || r) 
def H(i, r):
    # converte o índice i para 4 bytes e concatena com r antes de fazer o hash
    from cryptography.hazmat.primitives.hashes import Hash, SHA256
    digest = Hash(SHA256(), backend=default_backend())
    digest.update(struct.pack(">I", i) + r)
    return digest.finalize()  # 32 bytes

# RSA puro: cifrar r com a chave pública 
def rsa_encrypt_r(r):
    # OAEP é o padding recomendado para RSA, mas aqui usamos RAW (sem padding)
    # porque o enunciado pede RSA(r) diretamente — r tem de caber em 2048 bits
    return public_key.encrypt(
        r,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

#  RSA inverso: decifrar RSA(r) com a chave privada 
def rsa_decrypt_r(rsa_r):
    return private_key.decrypt(
        rsa_r,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# ── Cifra: Enc(m; r) = (RSA(r), H(0,r)⊕m₀, ..., H(n,r)⊕mₙ) ────────────────
def encrypt_rsa(plaintext):
    r = os.urandom(32)          # r uniforme de 32 bytes (256 bits)
    rsa_r = rsa_encrypt_r(r)   # primeira componente do criptograma

    # dividir a mensagem em blocos de 32 bytes (tamanho do output SHA-256)
    block_size = 32
    n_blocks = (len(plaintext) + block_size - 1) // block_size  # ceil(|m|/32)

    encrypted_blocks = []
    for i in range(n_blocks):
        block = plaintext[i * block_size : (i + 1) * block_size]
        h     = H(i, r)
        # XOR bloco com H(i,r) — se o bloco for menor que 32 bytes (último),
        # usa apenas os primeiros len(block) bytes do hash
        enc_block = bytes(a ^ b for a, b in zip(block, h))
        encrypted_blocks.append(enc_block)

    return rsa_r, encrypted_blocks

# ── Decifra ───────────────────────────────────────────────────────────────────
def decrypt_rsa(rsa_r, encrypted_blocks):
    r = rsa_decrypt_r(rsa_r)   # recuperar r

    decrypted_blocks = []
    for i, enc_block in enumerate(encrypted_blocks):
        h     = H(i, r)
        block = bytes(a ^ b for a, b in zip(enc_block, h))
        decrypted_blocks.append(block)

    return b"".join(decrypted_blocks)

# ── Benchmark ─────────────────────────────────────────────────────────────────
REPS = 30

def benchmark_rsa(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    # 30 medições de cifra
    enc_times = [
        timeit.timeit(lambda: encrypt_rsa(data), number=1) * 1e6
        for _ in range(REPS)
    ]

    # pré-cifrar uma vez para ter o criptograma para a decifra
    rsa_r, enc_blocks = encrypt_rsa(data)

    # 30 medições de decifra
    dec_times = [
        timeit.timeit(lambda: decrypt_rsa(rsa_r, enc_blocks), number=1) * 1e6
        for _ in range(REPS)
    ]

    enc_mean, enc_std = np.mean(enc_times), np.std(enc_times, ddof=1)
    dec_mean, dec_std = np.mean(dec_times), np.std(dec_times, ddof=1)
    enc_ci = 2.045 * enc_std / np.sqrt(REPS)
    dec_ci = 2.045 * dec_std / np.sqrt(REPS)

    return enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci

# ── Correr para todos os tamanhos ─────────────────────────────────────────────
results = {}
print(f"{'Tamanho':>10} | {'Enc (µs)':>10} | {'Enc std':>8} | {'Enc IC95':>8} | {'Dec (µs)':>10} | {'Dec std':>8} | {'Dec IC95':>8}")
print("-" * 80)

for size in file_sizes:
    file_path = f"ficheiros/file_{size}.txt"
    print(f"{size:>10} a processar...", end="\r")
    enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci = benchmark_rsa(file_path)
    results[size] = (enc_mean, enc_std, enc_ci, dec_mean, dec_std, dec_ci)
    print(f"{size:>10} | {enc_mean:>10.2f} | {enc_std:>8.2f} | {enc_ci:>8.2f} | {dec_mean:>10.2f} | {dec_std:>8.2f} | {dec_ci:>8.2f}")

# ── Guardar CSV ───────────────────────────────────────────────────────────────
os.makedirs("resultados", exist_ok=True)
with open("resultados/rsa_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["file_size", "enc_mean_us", "enc_std_us", "enc_ci95_us",
                                  "dec_mean_us", "dec_std_us", "dec_ci95_us"])
    for size, vals in results.items():
        writer.writerow([size, *vals])

print("\nResultados guardados em resultados/rsa_results.csv")