"""
acrescentar-convite.py - poe o convite "Gostou? Acompanhe o Abriu o Cofre" (canal do
Telegram + Pagina do Facebook) em todas as paginas-ponte JA existentes em p/.

Decisao dele em 30/10/2026 (questionario de visibilidade, C2: "Convite nos tres
lugares"). Paginas novas ja' nascem com o bloco, pelos geradores
(gerar-ponte.py / gerar-ponte-propria.py); este script e' so' para as antigas, e
insere o MESMO bloco e o MESMO css, entao uma pagina remendada e uma pagina
regerada ficam iguais.

Seguro de repetir: pagina que ja' tem `class="convite"` nao e' tocada. Pagina cujo
botao principal ja' e' o canal do Telegram recebe so' o convite do Facebook.

Uso:
    python -X utf8 _seo/acrescentar-convite.py            # ENSAIO: conta e nao grava
    python -X utf8 _seo/acrescentar-convite.py --gravar
"""
import argparse
import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

_spec = importlib.util.spec_from_file_location("gerar_ponte", AQUI / "gerar-ponte.py")
_gp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gp)


def remendar(texto: str) -> str | None:
    """Devolve a pagina com o convite, ou None se nao se aplica / ja' tem."""
    if 'class="convite"' in texto:
        return None
    if "<main>" not in texto or "</main>" not in texto or "</style>" not in texto:
        return None
    nl = "\r\n" if "\r\n" in texto else "\n"
    css = _gp.CONVITE_CSS.replace("\n", nl)
    com_telegram = 'class="ir ir-topo" href="https://t.me/' not in texto
    bloco = "  " + _gp.convite_html(com_telegram=com_telegram) + nl
    texto = texto.replace(nl + "</style>", css + nl + "</style>", 1)
    texto = texto.replace("</main>", bloco + "</main>", 1)
    return texto


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gravar", action="store_true", help="sem isso e' so' ensaio")
    a = ap.parse_args()
    feitas = puladas = outras = 0
    so_fb = 0
    for f in sorted((RAIZ / "p").glob("*.html")):
        bruto = f.read_bytes().decode("utf-8")
        novo = remendar(bruto)
        if novo is None:
            if 'class="convite"' in bruto:
                puladas += 1
            else:
                outras += 1
            continue
        if "Entrar no canal do Telegram</a><a" not in novo:
            so_fb += 1
        feitas += 1
        if a.gravar:
            f.write_bytes(novo.encode("utf-8"))
    print(f"{'GRAVADAS' if a.gravar else 'ENSAIO'}: {feitas} paginas ganham o convite ({so_fb} so' com o Facebook); "
          f"{puladas} ja' tinham; {outras} nao sao pagina-ponte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
