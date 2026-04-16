# Teoría de Algoritmos - TP1 (Curso Echevarría)

Este repositorio contiene la resolución del Trabajo Práctico 1. 

## Informe

El informe se encuentra en la carpeta `informe/` y el archivo principal es `main.tex`.

### Requisitos

Para compilar el informe, es necesario tener una distribución de LaTeX instalada en el sistema.

*   **Windows**: Se recomienda instalar [MiKTeX](https://miktex.org/download) o [TeX Live](https://www.tug.org/texlive/).
*   **Linux**: Instalar `texlive-full` usando el gestor de paquetes (ej. `sudo apt install texlive-full`).
*   **macOS**: Se recomienda instalar [MacTeX](https://www.tug.org/mactex/).

#### Herramientas Recomendadas

*   **Editor**: Se recomienda utilizar [Visual Studio Code](https://code.visualstudio.com/) con la extensión [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop).
*   **Compilador**: `latexmk` (ya viene incluido en la mayoría de las distribuciones de LaTeX y automatiza las múltiples pasadas necesarias).

### Compilación

#### Desde la Terminal

Para compilar el informe de forma automática, navegar hasta la carpeta `informe` y ejecutar:

```bash
cd informe
latexmk -pdf -shell-escape main.tex
```

> **Nota:** Se requiere el flag `-shell-escape` ya que el archivo `estilo.cls` utiliza `texcount` para el conteo de palabras mediante `\write18`.

Si prefiere compilar manualmente con `pdflatex`:

```bash
pdflatex -shell-escape main.tex
# Si hay bibliografía o referencias cruzadas:
biber main # o bibtex main
pdflatex -shell-escape main.tex
pdflatex -shell-escape main.tex
```

#### Desde VS Code (LaTeX Workshop)

Si utiliza la extensión LaTeX Workshop, puede configurar la compilación automática en el archivo `settings.json` de VS Code para que incluya el flag `--shell-escape`:

```json
"latex-workshop.latex.tools": [
    {
        "name": "latexmk",
        "command": "latexmk",
        "args": [
            "-synctex=1",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-pdf",
            "-outdir=%OUTDIR%",
            "-shell-escape",
            "%DOC%"
        ],
        "env": {}
    }
]
```

### Estructura del Informe

*   `informe/main.tex`: Archivo principal.
*   `informe/estilo.cls`: Clase personalizada con el formato del curso.
*   `informe/tex/`: Contiene los archivos `.tex` de cada sección.
*   `informe/img/`: Imágenes utilizadas en el informe.
*   `informe/code/`: Fragmentos de código fuente.