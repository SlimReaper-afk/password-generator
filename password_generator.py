"""Gerador de senhas seguras.

Usa o módulo `secrets` para aleatoriedade criptograficamente segura.
Pode ser usado pela linha de comando ou importado (por exemplo, pela API Flask).
"""
import math
import secrets
import string
from random import SystemRandom

MIN_LENGTH = 12
_secure_random = SystemRandom()  # embaralhamento seguro (usa os.urandom)


def _build_pools(use_lower, use_upper, use_digits, use_symbols):
    """Monta a lista de conjuntos de caracteres conforme as opções."""
    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)
    return pools


def generate_password(length, *, use_lower=True, use_upper=True,
                      use_digits=True, use_symbols=True):
    """Gera uma senha aleatória e segura.

    Garante ao menos um caractere de cada tipo selecionado.

    Levanta ValueError se o tamanho for menor que MIN_LENGTH ou se
    nenhum tipo de caractere for selecionado.
    """
    if length < MIN_LENGTH:
        raise ValueError(f"A senha deve ter pelo menos {MIN_LENGTH} caracteres.")

    pools = _build_pools(use_lower, use_upper, use_digits, use_symbols)
    if not pools:
        raise ValueError("Selecione ao menos um tipo de caractere.")

    # Um caractere garantido de cada tipo selecionado...
    chars = [secrets.choice(pool) for pool in pools]
    # ...e o restante retirado do conjunto combinado.
    combined = "".join(pools)
    chars += [secrets.choice(combined) for _ in range(length - len(chars))]

    # Embaralha para não expor a posição dos caracteres garantidos.
    _secure_random.shuffle(chars)
    return "".join(chars)


def pool_size(use_lower=True, use_upper=True, use_digits=True, use_symbols=True):
    """Quantidade de caracteres possíveis com as opções escolhidas."""
    pools = _build_pools(use_lower, use_upper, use_digits, use_symbols)
    return sum(len(pool) for pool in pools)


def entropy_bits(length, alphabet_size):
    """Estimativa de entropia em bits = comprimento × log2(tamanho do alfabeto)."""
    if alphabet_size <= 1 or length <= 0:
        return 0.0
    return round(length * math.log2(alphabet_size), 1)


if __name__ == "__main__":
    try:
        size = int(input("Digite o tamanho da senha: "))
    except ValueError:
        print("Erro: digite um número inteiro.")
    else:
        try:
            senha = generate_password(size)
            print(f"Senha gerada: {senha}")
        except ValueError as error:
            print(f"Erro: {error}")
