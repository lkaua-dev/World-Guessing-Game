import unicodedata

def normalizar_texto(texto):
    """Remove acentos e deixa o texto em minúsculo."""
    if not texto:
        return ""
    return (
        "".join(
            c
            for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
        .lower()
        .strip()
    )