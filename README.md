# EvaSol — Evaluador de Soldaduras

[English](#english-version) | [Español](#versión-español)

## ¿Qué es?

**EvaSol** es una aplicación de inspección visual para evaluar la calidad de soldaduras utilizando YOLO (ultralytics). Permite:

- Cargar imágenes o usar la cámara para capturar fotos de soldaduras
- Detectar defectos con un modelo YOLO entrenado
- Generar reportes en Word (.docx) con los resultados de la inspección
- Administrar proyectos y números de reporte

## Características

| Característica | Descripción |
|---|---|
| **Detección de defectos** | YOLO-based inspection con umbral de confianza configurable |
| **Múltiples métodos de entrada** | Subir imagen o usar cámara web |
| **Reportes automatizados** | Genera reportes Word con plantilla personalizable |
| **Gestión de proyectos** | Agrupa inspecciones por nombre de obra |
| **Historial** | Imágenes guardadas por proyecto y número de reporte |

## Requisitos

- Python >= 3.10
- Dependencias (ver `requirements.txt` o `pyproject.toml`)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/evasol.git
cd evasol

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
# o con uv:
uv pip install -r requirements.txt
```

## Uso

### Iniciar la aplicación

```bash
streamlit run src/evasol/Validador.py
```

### Flujo de trabajo

1. **Seleccionar modelo** — Elige un modelo `.pt` de la carpeta `src/modelos/`
2. **Proporcionar imagen** — Sube una foto o usa la cámara
3. **Llenar datos del reporte** — Obra, inspector, número de reporte
4. **Evaluar** — La imagen se procesa y se muestran las detecciones
5. **Generar reporte** — Haz clic en "Generar reporte" para crear un .docx

### Flujo de entrenamiento (Entrenador.py)

```bash
python src/evasol/Entrenador.py <epochs> <nombre_salida.pt>
```

Ejemplo: `python src/evasol/Entrenador.py 50 soldadura_v1.pt`

## Estructura del proyecto

```
EvaSol/
├── .gitignore
├── .python-version
├── .venv/                 # Entorno virtual
├── pyproject.toml         # Configuración del proyecto
├── requirements.txt       # Dependencias
├── README.md              # Esta documentación
├── formatos/              # Plantillas y reportes Word
│   ├── reporte_plantilla.docx
│   └── reporte_soldadura.docx
├── evaluación/            # Resultados de inspección por proyecto
│   └── <obra>/
│       └── Inspección_<obra>_<reporte>_<clase>.png
├── runs/                  # Ejecuciones de entrenamiento YOLO
│   └── detect/
├── src/
│   └── evasol/
│       ├── __init__.py
│       ├── Validador.py   # Aplicación Streamlit principal
│       ├── Reporte.py     # Generación de reportes Word
│       └── Entrenador.py  # Script de entrenamiento YOLO
├── modelos/               # Modelos YOLO (.pt) entrenados o preentrenados
└── Imagenes/              # Imágenes de referencia y defectos
    └── defectos_de_soldaduras/
        └── data.yaml      # Configuración de dataset (para entrenar)
```

## Configuración

### Modelos

Coloca tus archivos `.pt` en la carpeta `src/modelos/`. La aplicación los listará automáticamente.

### Plantilla de reporte

La aplicación usa `formatos/reporte_plantilla.docx` como base. Los reemplazadores esperan estos placeholders:

- `{{OBRA}}` — Nombre de la obra
- `{{INSPECTOR}}` — Nombre del inspector
- `{{N_REPORTE}}` — Número de reporte
- `{{FECHA}}` — Fecha y hora actual
- `{{CONFIANZA}}` — Mejor confianza de detección
- `{{CLASIFICACIÓN}}` — Clase de defecto detectado (o "Sin defectos")

Para agregar un nuevo placeholder, modifica `_reemplazar_parrafo()` en `src/evasol/Reporte.py`.

### Dataset para entrenamiento

Si deseas entrenar un nuevo modelo, coloca tus datos en `Imagenes/defectos_de_soldaduras/` con la estructura:

```
Imagenes/defectos_de_soldaduras/
├── data.yaml
├── train/images/
├── train/labels/
└── val/images/
└── val/labels/
```

El `data.yaml` debe seguir el formato de Ultralytics YOLO.

## Licencia

No license specified. Check `pyproject.toml` for details.

---

## English Version

# EvaSol — Welding Inspector

EvaSol is a visual inspection application for weld quality evaluation using YOLO (ultralytics). It allows:

- Loading images or using the camera to capture weld photos
- Detecting defects with a trained YOLO model
- Generating Word (.docx) inspection reports
- Managing projects and report numbers

## Features

| Feature | Description |
|---|---|
| **Defect detection** | YOLO-based inspection with configurable confidence threshold |
| **Multiple input methods** | Upload image or use webcam |
| **Automated reports** | Generates customizable Word reports |
| **Project management** | Groups inspections by project name |
| **History** | Images saved per project and report number |

## Requirements

- Python >= 3.10
- Dependencies (see `requirements.txt` or `pyproject.toml`)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/evasol.git
cd evasol

# Create virtual environment (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or with uv:
uv pip install -r requirements.txt
```

## Usage

### Run the application

```bash
streamlit run src/evasol/Validador.py
```

### Workflow

1. **Select model** — Choose a `.pt` model from `src/modelos/`
2. **Provide image** — Upload a photo or use the camera
3. **Fill report data** — Project, inspector, report number
4. **Evaluate** — Image is processed and detections displayed
5. **Generate report** — Click "Generate report" to create .docx

### Training workflow (Entrenador.py)

```bash
python src/evasol/Entrenador.py <epochs> <output_name.pt>
```

Example: `python src/evasol/Entrenador.py 50 soldadura_v1.pt`

## Project Structure

```
EvaSol/
├── .gitignore
├ .python-version
├── .venv/                 # Virtual environment
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
├── README.md              # This documentation
├── formatos/              # Word templates and reports
│   ├── reporte_plantilla.docx
│   └── reporte_soldadura.docx
├── evaluacion/            # Inspection results per project
│   └── <project>/
│       └── Inspeccion_<project>_<report>_<class>.png
├── runs/                  # YOLO training runs
│   └── detect/
├── src/
│   └── evasol/
│       ├── __init__.py
│       ├── Validador.py   # Main Streamlit application
│       ├── Reporte.py     # Word report generation
│       └── Entrenador.py  # YOLO training script
├── modelos/               # Trained/pre-trained YOLO .pt models
└── Imagenes/              # Reference images and defects
    └── defectos_de_soldaduras/
        └── data.yaml      # YOLO dataset configuration
```

## Configuration

### Models

Place `.pt` files in `src/modelos/`. The app will list them automatically.

### Report template

The app uses `formatos/reporte_plantilla.docx` as the base template. Replacements use these placeholders:

- `{{OBRA}}` — Project name
- `{{INSPECTOR}}` — Inspector name
- `{{N_REPORTE}}` — Report number
- `{{FECHA}}` — Current date and time
- `{{CONFIANZA}}` — Best detection confidence
- `{{CLASIFICACIÓN}}` — Detected defect class (or "Sin defectos")

To add a new placeholder, modify `_reemplazar_parrafo()` in `src/evasol/Reporte.py`.

### Dataset for training

To train a new model, organize data under `Imagenes/defectos_de_soldaduras/` following Ultralytics YOLO format:

```
Imagenes/defectos_de_soldaduras/
├── data.yaml
├── train/images/
├── train/labels/
├── val/images/
└── val/labels/
```

The `data.yaml` must follow Ultralytics YOLO format.

## License

No license specified. Check `pyproject.toml` for details.