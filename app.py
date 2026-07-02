"""Interface web (Flask) para o gerador de senhas.

Reaproveita a lógica de `password_generator.py`. A rota `/` serve a página
e `/api/generate` devolve a senha em JSON, com estimativa de entropia.
"""
from flask import Flask, jsonify, render_template, request

from password_generator import (
    MIN_LENGTH,
    entropy_bits,
    generate_password,
    pool_size,
)

app = Flask(__name__)


def strength_label(bits):
    """Traduz a entropia em uma classificação simples de força."""
    if bits < 50:
        return "Fraca"
    if bits < 80:
        return "Boa"
    if bits < 120:
        return "Forte"
    return "Excelente"


@app.route("/")
def index():
    return render_template("index.html", min_length=MIN_LENGTH)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}

    try:
        length = int(data.get("length", MIN_LENGTH))
    except (TypeError, ValueError):
        return jsonify(error="Informe um tamanho numérico."), 400

    options = dict(
        use_lower=bool(data.get("use_lower", True)),
        use_upper=bool(data.get("use_upper", True)),
        use_digits=bool(data.get("use_digits", True)),
        use_symbols=bool(data.get("use_symbols", True)),
    )

    try:
        password = generate_password(length, **options)
    except ValueError as error:
        return jsonify(error=str(error)), 400

    size = pool_size(**options)
    bits = entropy_bits(length, size)
    return jsonify(
        password=password,
        length=length,
        pool_size=size,
        entropy_bits=bits,
        strength=strength_label(bits),
    )


if __name__ == "__main__":
    app.run(debug=True)
