from argon2 import PasswordHasher


def gerar_hash_argon2(texto: str) -> str:
    ph = PasswordHasher()
    return ph.hash(texto)


if __name__ == "__main__":
    senha = "admin"
    hash_gerado = gerar_hash_argon2(senha)
    print("Hash gerado:")
    print(hash_gerado)