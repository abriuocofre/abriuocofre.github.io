"""
Acrescenta o trecho SCRIPT_REDE (?c=ig|fb|th) nas paginas-ponte da Amazon que
ja' existem (12/11/2026). Paginas novas ja' nascem com ele pelo gerar-ponte.py.

Idempotente: pagina que ja' tem o trecho e' pulada. Sem --gravar so' mostra o
que faria (ensaio). Insere o trecho IGUAL ao do gerador, entre </footer> e
</body>, so' em pagina que tem link da Amazon com a etiqueta fb.

Como rodar (da raiz do site):
    python -X utf8 _seo/acrescentar-etiqueta-por-rede.py            # ensaio
    python -X utf8 _seo/acrescentar-etiqueta-por-rede.py --gravar
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("gerar_ponte", RAIZ / "_seo" / "gerar-ponte.py")
gp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gp)
TRECHO = gp.SCRIPT_REDE

gravar = "--gravar" in sys.argv
mudar, ja, sem_amazon, estranhas = [], 0, 0, []
for arq in sorted((RAIZ / "p").glob("*.html")):
    bruto = arq.read_bytes()
    texto = bruto.decode("utf-8")
    crlf = "\r\n" in texto
    t = texto.replace("\r\n", "\n")
    if TRECHO in t:
        ja += 1
        continue
    if "amazon.com.br" not in t or "tag=abriuocofrefb-20" not in t:
        sem_amazon += 1
        continue
    alvo = "</footer>\n</body>"
    if t.count(alvo) != 1:
        estranhas.append(arq.name)
        continue
    novo = t.replace(alvo, "</footer>\n" + TRECHO + "</body>")
    if crlf:
        novo = novo.replace("\n", "\r\n")
    mudar.append((arq, novo))

print(f"ja' tem o trecho: {ja} | sem link Amazon fb (nao mexe): {sem_amazon} | a acrescentar: {len(mudar)} | formato estranho: {len(estranhas)}")
for n in estranhas:
    print("  ESTRANHA (nao mexi):", n)
if gravar:
    for arq, novo in mudar:
        arq.write_bytes(novo.encode("utf-8"))
    print(f"gravadas: {len(mudar)}")
else:
    print("ENSAIO: nada gravado (use --gravar).")
