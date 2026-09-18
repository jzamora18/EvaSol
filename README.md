# EvaSol — Evaluador de Soldaduras

[English](#english-version) | [Español](#evasol--evaluador-de-soldaduras)

## ¿Qué es?

**EvaSol** es una aplicación de inspección visual para evaluar la calidad de soldaduras utilizando YOLO (ultralytics). Permite:

- Cargar imágenes o usar la cámara para capturar fotos de soldaduras
- Detectar defectos con un modelo YOLO entrenado
- Generar reportes en Word (.docx) con los resultados de la inspección
- Administrar proyectos y números de reporte

## Características

| Característica                          | Descripción                                               |
| ---------------------------------------- | ---------------------------------------------------------- |
| **Detección de defectos**         | Inspección con YOLO, umbral de confianza fijo en 0.4 |
| **Múltiples métodos de entrada** | Subir una o varias imágenes, o usar la cámara web                            |
| **Reportes automatizados**         | Genera reportes Word con plantilla personalizable          |
| **Gestión de proyectos**          | Agrupa inspecciones por nombre de obra                     |
| **Historial**                      | Imágenes guardadas por proyecto y número de reporte      |

## Requisitos

- Python >= 3.10
- Dependencias en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/jzamora18/EvaSol.git
cd EvaSol

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Iniciar la aplicación

`Validador.py` importa con `from Reporte import generar_reporte`, por lo que `src/evasol` debe estar en el `PYTHONPATH`:

```bash
# Opción 1: ejecutar desde la carpeta del módulo
cd src/evasol
streamlit run Validador.py

# Opción 2: desde la raíz del proyecto
PYTHONPATH=src/evasol streamlit run src/evasol/Validador.py
```

### Flujo de trabajo

1. **Llenar datos del reporte** — Obra, inspector, número de reporte
2. **Proporcionar imagen** — Sube una o varias fotos (`jpg`, `jpeg`, `png`, `webp`) o usa la cámara
3. **Seleccionar modelo** — Elige un modelo `.pt` de la carpeta `src/modelos/`
4. **Evaluar** — Pulsa "Evaluar imágenes"; se muestran original y evaluación lado a lado con las detecciones (confianza fija 0.4)
5. **Generar reporte** — Pulsa "Generar reporte" y descarga el `.docx` (`Inspección_Soldadura_<obra>_<reporte>.docx`)

Las imágenes evaluadas se guardan en `evaluación/<obra>/` como `Inspección_<obra>_<reporte>_<clase>_<n>.png` (`sin_defecto` si no hay detecciones).

### Flujo de entrenamiento (Entrenador.py)

```bash
python src/evasol/Entrenador.py <epochs> <nombre_salida.pt>
```

Ejemplo: `python src/evasol/Entrenador.py 50 soldadura_v1.pt`

El entrenamiento parte del modelo base `src/modelos/yolo11n.pt`, usa el dataset de `Imagenes/dataset/data.yaml` (con `device=cuda` si hay GPU, si no `cpu`) y guarda el modelo resultante en `src/modelos/<nombre_salida.pt>`. Los artefactos de entrenamiento de Ultralytics quedan en `runs/detect/`.

> Nota: `Imagenes/dataset/data.yaml` trae un `path:` absoluto apuntando a otra máquina (`.../EvaSol_Labels/dataset`). Actualízalo a la ruta local antes de entrenar.

## Estructura del proyecto

```
EvaSol/
├── .gitignore
├── requirements.txt       # Dependencias
├── README.md              # Esta documentación
├── formatos/              # Plantilla Word
│   └── plantilla.docx     # Plantilla base del reporte
├── evaluación/            # Resultados de inspección por proyecto (ignorado por git)
│   └── <obra>/
│       └── Inspección_<obra>_<reporte>_<clase>_<n>.png
├── runs/                  # Ejecuciones de entrenamiento YOLO (ignorado por git)
│   └── detect/
├── weights/               # Pesos de referencia
│   └── yolo26n.pt
├── src/
│   ├── modelos/           # Modelos YOLO (.pt)
│   │   ├── yolo11n.pt     # Modelo base para entrenar
│   │   ├── yolo26m.pt
│   │   ├── yolo26n.pt
│   │   └── Pesos_Entrenamiento_25_Epochs.pt
│   └── evasol/
│       ├── __init__.py
│       ├── Validador.py   # Aplicación Streamlit principal
│       ├── Reporte.py     # Generación de reportes Word
│       └── Entrenador.py  # Script de entrenamiento YOLO
└── Imagenes/              # Dataset YOLO (ignorado por git)
    └── dataset/
        ├── data.yaml      # Configuración del dataset (clases: NO OK, OK)
        ├── train/images/  # + train/labels/
        ├── valid/images/  # + valid/labels/
        └── test/images/   # + test/labels/
```

## Configuración

### Modelos

Coloca tus archivos `.pt` en `src/modelos/`. La aplicación los listará automáticamente.

### Plantilla de reporte

La aplicación usa `formatos/plantilla.docx` como base. Los placeholders soportados son:

- `{{OBRA}}` — Nombre de la obra
- `{{INSPECTOR}}` — Nombre del inspector
- `{{N_REPORTE}}` — Número de reporte
- `{{FECHA}}` — Fecha y hora actual (`dd/mm/yyyy hh:mm`)
- `{{IMAGEN}` — Punto de inserción de las imágenes evaluadas (así, con una sola `}` de cierre en la plantilla)

Para agregar un nuevo placeholder de texto, añade la entrada al dict `reemplazos` en `Validador.py` (la sustitución la hace `_reemplazar_parrafo()` en `src/evasol/Reporte.py`).

### Dataset para entrenamiento

El dataset en `Imagenes/dataset/` sigue el formato Ultralytics YOLO (`train/`, `valid/`, `test/`, cada uno con `images/` y `labels/`). El `data.yaml` declara 2 clases: `NO OK`, `OK`.

---

## English Version

# EvaSol — Welding Inspector

EvaSol is a visual inspection application for weld quality evaluation using YOLO (ultralytics). It allows:

- Loading images or using the camera to capture weld photos
- Detecting defects with a trained YOLO model
- Generating Word (.docx) inspection reports
- Managing projects and report numbers

## Features

| Feature                          | Description                                                  |
| -------------------------------- | ------------------------------------------------------------ |
| **Defect detection**       | YOLO inspection with fixed 0.4 confidence threshold |
| **Multiple input methods** | Upload one or several images, or use the webcam                                   |
| **Automated reports**      | Generates Word reports from a customizable template                          |
| **Project management**     | Groups inspections by project name                           |
| **History**                | Images saved per project and report number                   |

## Requirements

- Python >= 3.10
- Dependencies in `requirements.txt`

## Installation

```bash
# Clone the repository
git clone https://github.com/jzamora18/EvaSol.git
cd EvaSol

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the application

`Validador.py` imports via `from Reporte import generar_reporte`, so `src/evasol` must be on the `PYTHONPATH`:

```bash
# Option 1: run from the module folder
cd src/evasol
streamlit run Validador.py

# Option 2: from the project root
PYTHONPATH=src/evasol streamlit run src/evasol/Validador.py
```

### Workflow

1. **Fill report data** — Project (`obra`), inspector, report number
2. **Provide images** — Upload one or more photos (`jpg`, `jpeg`, `png`, `webp`) or use the camera
3. **Select model** — Choose a `.pt` model from `src/modelos/`
4. **Evaluate** — Click "Evaluar imágenes"; original and evaluated images are shown side by side with detections (fixed 0.4 confidence)
5. **Generate report** — Click "Generar reporte" and download the `.docx` (`Inspección_Soldadura_<obra>_<reporte>.docx`)

Evaluated images are saved under `evaluación/<obra>/` as `Inspección_<obra>_<reporte>_<class>_<n>.png` (`sin_defecto` when nothing is detected).

### Training workflow (Entrenador.py)

```bash
python src/evasol/Entrenador.py <epochs> <output_name.pt>
```

Example: `python src/evasol/Entrenador.py 50 soldadura_v1.pt`

Training starts from the base model `src/modelos/yolo11n.pt`, uses the dataset in `Imagenes/dataset/data.yaml` (`device=cuda` when a GPU is available, otherwise `cpu`) and saves the resulting model to `src/modelos/<output_name.pt>`. Ultralytics training artifacts go to `runs/detect/`.

> Note: `Imagenes/dataset/data.yaml` ships with an absolute `path:` pointing to another machine (`.../EvaSol_Labels/dataset`). Update it to your local path before training.

## Project Structure

```
EvaSol/
├── .gitignore
├── requirements.txt       # Dependencies
├── README.md              # This documentation
├── formatos/              # Word template
│   └── plantilla.docx     # Base report template
├── evaluación/            # Inspection results per project (git-ignored)
│   └── <obra>/
│       └── Inspección_<obra>_<reporte>_<clase>_<n>.png
├── runs/                  # YOLO training runs (git-ignored)
│   └── detect/
├── weights/               # Reference weights
│   └── yolo26n.pt
├── src/
│   ├── modelos/           # YOLO models (.pt)
│   │   ├── yolo11n.pt     # Base model for training
│   │   ├── yolo26m.pt
│   │   ├── yolo26n.pt
│   │   └── Pesos_Entrenamiento_25_Epochs.pt
│   └── evasol/
│       ├── __init__.py
│       ├── Validador.py   # Main Streamlit application
│       ├── Reporte.py     # Word report generation
│       └── Entrenador.py  # YOLO training script
└── Imagenes/              # YOLO dataset (git-ignored)
    └── dataset/
        ├── data.yaml      # Dataset config (classes: NO OK, OK)
        ├── train/images/  # + train/labels/
        ├── valid/images/  # + valid/labels/
        └── test/images/   # + test/labels/
```

## Configuration

### Models

Place `.pt` files in `src/modelos/`. The app will list them automatically.

### Report template

The app uses `formatos/plantilla.docx` as the base template. Supported placeholders:

- `{{OBRA}}` — Project name
- `{{INSPECTOR}}` — Inspector name
- `{{N_REPORTE}}` — Report number
- `{{FECHA}}` — Current date and time (`dd/mm/yyyy hh:mm`)
- `{{IMAGEN}` — Insertion point for the evaluated images (single closing `}` in the template, as-is)

To add a new text placeholder, add the entry to the `reemplazos` dict in `Validador.py` (substitution is done by `_reemplazar_parrafo()` in `src/evasol/Reporte.py`).

### Dataset for training

The dataset in `Imagenes/dataset/` follows the Ultralytics YOLO format (`train/`, `valid/`, `test/`, each with `images/` and `labels/`). The `data.yaml` declares 2 classes: `NO OK`, `OK`.
