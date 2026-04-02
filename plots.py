import os
import pandas as pd
import matplotlib.pyplot as plt

aes = pd.read_csv("resultados/aes_results.csv")
rsa = pd.read_csv("resultados/rsa_results.csv")
sha = pd.read_csv("resultados/sha_results.csv")

os.makedirs("graficos", exist_ok=True)

# =============================================================================
# (i) AES — cifra e decifra
# =============================================================================
plt.figure()
plt.errorbar(aes["file_size"], aes["enc_mean_us"], yerr=aes["enc_ci95_us"],
             marker='o', capsize=4, label="AES Encrypt")
plt.errorbar(aes["file_size"], aes["dec_mean_us"], yerr=aes["dec_ci95_us"],
             marker='o', capsize=4, label="AES Decrypt")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("AES-256 CTR — Encryption and Decryption Times")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_aes.png", dpi=150)
plt.close()

# =============================================================================
# (ii) RSA — só cifra
# =============================================================================
plt.figure()
plt.errorbar(rsa["file_size"], rsa["enc_mean_us"], yerr=rsa["enc_ci95_us"],
             marker='o', capsize=4, color="tab:blue", label="RSA Encrypt")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("RSA-2048 — Encryption Times")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_rsa_enc.png", dpi=150)
plt.close()

# =============================================================================
# (iii) RSA — só decifra
# =============================================================================
plt.figure()
plt.errorbar(rsa["file_size"], rsa["dec_mean_us"], yerr=rsa["dec_ci95_us"],
             marker='o', capsize=4, color="tab:orange", label="RSA Decrypt")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("RSA-2048 — Decryption Times")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_rsa_dec.png", dpi=150)
plt.close()

# =============================================================================
# (iv) SHA-256
# =============================================================================
plt.figure()
plt.errorbar(sha["file_size"], sha["sha_mean_us"], yerr=sha["sha_ci95_us"],
             marker='o', capsize=4, color="tab:green", label="SHA-256")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("SHA-256 — Digest Generation Times")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_sha.png", dpi=150)
plt.close()

# =============================================================================
# Comparação 1 — AES cifra vs RSA cifra
# =============================================================================
plt.figure()
plt.errorbar(aes["file_size"], aes["enc_mean_us"], yerr=aes["enc_ci95_us"],
             marker='o', capsize=4, label="AES Encrypt")
plt.errorbar(rsa["file_size"], rsa["enc_mean_us"], yerr=rsa["enc_ci95_us"],
             marker='s', capsize=4, label="RSA Encrypt")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("AES-256 CTR vs RSA-2048 — Encryption Times")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_aes_vs_rsa.png", dpi=150)
plt.close()

# =============================================================================
# Comparação 2 — AES cifra vs SHA
# =============================================================================
plt.figure()
plt.errorbar(aes["file_size"], aes["enc_mean_us"], yerr=aes["enc_ci95_us"],
             marker='o', capsize=4, label="AES Encrypt")
plt.errorbar(sha["file_size"], sha["sha_mean_us"], yerr=sha["sha_ci95_us"],
             marker='s', capsize=4, color="tab:green", label="SHA-256")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("AES-256 CTR vs SHA-256")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_aes_vs_sha.png", dpi=150)
plt.close()

# =============================================================================
# Comparação 3 — RSA cifra vs RSA decifra (gráfico completo)
# =============================================================================
plt.figure()
plt.errorbar(rsa["file_size"], rsa["enc_mean_us"], yerr=rsa["enc_ci95_us"],
             marker='o', capsize=4, label="RSA Encrypt")
plt.errorbar(rsa["file_size"], rsa["dec_mean_us"], yerr=rsa["dec_ci95_us"],
             marker='s', capsize=4, label="RSA Decrypt")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("RSA-2048 — Encryption vs Decryption Times")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_rsa_enc_vs_dec.png", dpi=150)
plt.close()

# =============================================================================
# Comparação 3 zoom — RSA cifra vs RSA decifra (só ficheiros pequenos)
# Para ficheiros grandes o loop de SHA-256 domina e as linhas ficam sobrepostas.
# Este zoom mostra a diferença real da operação RSA nos ficheiros pequenos.
# =============================================================================
rsa_small = rsa[rsa["file_size"] <= 4096]

plt.figure()
plt.errorbar(rsa_small["file_size"], rsa_small["enc_mean_us"], yerr=rsa_small["enc_ci95_us"],
             marker='o', capsize=4, label="RSA Encrypt")
plt.errorbar(rsa_small["file_size"], rsa_small["dec_mean_us"], yerr=rsa_small["dec_ci95_us"],
             marker='s', capsize=4, label="RSA Decrypt")
plt.xscale("log")
plt.ylim(bottom=0)
plt.xlabel("File size (bytes)")
plt.ylabel("Time (µs)")
plt.title("RSA-2048 — Encryption vs Decryption Times (small files zoom)")
plt.legend()
plt.tight_layout()
plt.savefig("graficos/plot_rsa_enc_vs_dec_zoom.png", dpi=150)
plt.close()
