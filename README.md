# La derivada que abarata tu lata

Infografía de una lámina (cálculo diferencial aplicado): cómo la derivada `C'(r)` encuentra el radio que minimiza el costo de material de una lata cilíndrica de volumen fijo `V`.

- `infografia-lata.html` — lámina autocontenida (HTML + SVG). Ábrela en el navegador.
- `lamina.html` — misma lámina sin el esqueleto `<html>`, usada para publicarla como Artifact.

## Exportar

- **PDF:** abre `infografia-lata.html` en Chrome → Imprimir → Guardar como PDF (la hoja está configurada en A3 horizontal; activa "Gráficos de fondo").
- **PowerPoint:** exporta el PDF a imagen o haz una captura de pantalla completa y pégala en una diapositiva.

## Modelo

| | |
|---|---|
| Costo | `C(r) = 2πr² + 2V/r` (área de lámina, k = 1) |
| Derivada | `C'(r) = 4πr − 2V/r²` |
| Punto crítico | `C'(r) = 0 ⇒ r* = ∛(V/2π)` |
| Forma óptima | `h = V/(πr*²) = 2r*` (altura = diámetro) |

Las latas de comparación (+8 % y +27 % de lámina) usan `r = 0.75 r*` y `r = 1.6 r*`; el porcentaje no depende de `V`.
