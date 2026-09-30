#!/usr/bin/env python3
"""Genera la entrega v2 a partir de fuente.html.

1. Descarga las fuentes de Google Fonts y las incrusta como data URI
   -> infografia-lata-v2.html (autocontenido, funciona sin internet).
2. Imprime ese mismo HTML con Chromium (Playwright) en una sola página
   del tamaño exacto de la lámina -> infografia-lata-v2.pdf.

Requisitos: curl, node y el paquete `playwright` de Node con Chromium.
Uso: python3 v2/exportar.py
"""
import base64
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "fuente.html"
HTML = AQUI / "infografia-lata-v2.html"
PDF = AQUI / "infografia-lata-v2.pdf"
ANCHO = 1520  # px, ancho de diseño de la lámina
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
SUBCONJUNTOS = {"latin", "latin-ext", "greek", "math", "symbols"}


def curl(url: str) -> bytes:
    return subprocess.run(["curl", "-sSfL", "-A", UA, url], capture_output=True, check=True).stdout


def incrustar_fuentes(html: str) -> str:
    bloque = re.search(r"<!--FUENTES-->(.*?)<!--/FUENTES-->", html, re.S)
    url = re.search(r'href="(https://fonts\.googleapis\.com/[^"]+)"', bloque.group(1)).group(1)
    css = curl(url.replace("&amp;", "&")).decode()
    caras = []
    cache = {}
    for nombre, regla in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
        if nombre not in SUBCONJUNTOS:
            continue
        src = re.search(r"url\((https://[^)]+)\)", regla).group(1)
        if src not in cache:
            cache[src] = "data:font/woff2;base64," + base64.b64encode(curl(src)).decode()
        caras.append(regla.replace(src, cache[src]))
    estilo = "<style>\n" + "\n".join(caras) + "\n</style>"
    return html[: bloque.start()] + estilo + html[bloque.end():]


PDF_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [html, pdf, ancho] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +ancho, height: 900 } });
  await p.goto('file://' + html, { waitUntil: 'load' });
  await p.emulateMedia({ media: 'screen' });
  await p.evaluate(() => document.fonts.ready);
  const alto = await p.evaluate(() => Math.ceil(document.documentElement.scrollHeight));
  await p.pdf({ path: pdf, width: ancho + 'px', height: (alto + 1) + 'px',
                printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await b.close();
  console.log(`PDF de una página: ${ancho} x ${alto + 1} px`);
})();
"""


def main() -> None:
    HTML.write_text(incrustar_fuentes(FUENTE.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"HTML autocontenido: {HTML.name} ({HTML.stat().st_size // 1024} KB)")
    raiz_npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["node", "-e", PDF_JS, str(HTML), str(PDF), str(ANCHO)],
                   check=True, env={**__import__("os").environ, "NODE_PATH": raiz_npm})


if __name__ == "__main__":
    main()
