import os
import sys
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
from datetime import datetime
try:
    from Reporte import generar_reporte
except ImportError:
    from evasol.Reporte import generar_reporte
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource
def load_model(model_path: str):
    return YOLO(model_path)


def main():
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../src/evasol
    PROJECT_ROOT = os.path.dirname(os.path.dirname(FILE_DIR))  # .../EvaSol
    EVAL_DIR = os.path.join(PROJECT_ROOT, "evaluación")
    os.makedirs(EVAL_DIR, exist_ok=True)
    TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "formatos", "plantilla.docx") # "reporte_plantilla.docx")

    st.title("Evaluador de Soldaduras")
    st.write(
        "Selecciona cómo proporcionar la imagen de la soldadura y evalúa su calidad."
    )

    # ── Datos del reporte ─────────────────────────────────────────────────────
    obra = st.text_input("Obra:")
    inspector = st.text_input("Inspector:")
    n_reporte = st.text_input("Número de reporte:")
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # ── Carpetas por obra ─────────────────────────────────────────────────────
    OBRA_DIR = os.path.join(EVAL_DIR, obra)
    os.makedirs(OBRA_DIR, exist_ok=True)

    # ── Método de entrada ─────────────────────────────────────────────────────
    input_method = st.radio(
        "Método de entrada:", ("Subir imagen", "Tomar foto con cámara")
    )

    img_file_buffer = None
    img_files_buffer = []

    if input_method == "Tomar foto con cámara":
        img_file_buffer = st.camera_input("Toma una foto")
        if img_file_buffer:
            img_files_buffer = [img_file_buffer]

    elif input_method == "Subir imagen":
        img_files_buffer = st.file_uploader(
            "Sube imágenes",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
        )

    # ── Cargar modelo ─────────────────────────────────────────────────────────
    MODELOS_DIR = os.path.join(PROJECT_ROOT, "src", "modelos")
    if not os.path.isdir(MODELOS_DIR):
        st.error(f"No se encontró la carpeta de modelos: {MODELOS_DIR}")
        return
    modelos = [f for f in os.listdir(MODELOS_DIR) if f.endswith(".pt")]

    if not modelos:
        st.error("No se encontraron modelos en la carpeta 'src/modelos/'.")
        return

    selected_model = st.selectbox("Modelo:", modelos)
    model = load_model(os.path.join(MODELOS_DIR, selected_model))

    # ── Colores por clase (BGR) ───────────────────────────────────────────────
    CLASS_COLORS = {
        0: (0, 0, 255),  # Clase 0 → Rojo
        1: (0, 255, 0),  # Clase 1 → Verde
    }
    DEFAULT_COLOR = (255, 255, 0)  # Cian (fallback)

    # ── Evaluación ────────────────────────────────────────────────────────────
    if img_files_buffer:
        if st.button("Evaluar imágenes"):

            all_results = []  # List of dicts: {img, result_img, detecciones, filename}

            for img_file_buffer in img_files_buffer:
                img = Image.open(img_file_buffer)

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".jpg"
                ) as tmp_file:
                    img.save(tmp_file.name)
                    temp_path = tmp_file.name

                try:
                    results = model(temp_path, conf=0.4)

                    for result in results:
                        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                        if result.boxes:
                            for box in result.boxes:
                                cls = int(box.cls)
                                conf = box.conf.item()
                                class_name = model.names[cls]
                                color = CLASS_COLORS.get(cls, DEFAULT_COLOR)

                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                cv2.rectangle(
                                    img_cv, (x1, y1), (x2, y2), color, thickness=2
                                )

                                label = f"{class_name} {conf:.0%}"
                                (tw, th), _ = cv2.getTextSize(
                                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                                )
                                cv2.rectangle(
                                    img_cv,
                                    (x1, y1 - th - 8),
                                    (x1 + tw + 4, y1),
                                    color,
                                    -1,
                                )
                                cv2.putText(
                                    img_cv,
                                    label,
                                    (x1 + 2, y1 - 4),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (255, 255, 255),
                                    2,
                                )

                        result_img = Image.fromarray(
                            cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                        )

                        # ── Mostrar en Streamlit ──────────────────────────────────
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(img, caption=f"Original — {img_file_buffer.name}")
                        with col2:
                            st.image(result_img, caption="Evaluación")

                        # ── Detecciones ───────────────────────────────────────────
                        detecciones = []
                        if result.boxes:
                            st.write("**Detecciones:**")
                            for box in result.boxes:
                                cls = int(box.cls)
                                conf = box.conf.item()
                                class_name = model.names[cls]
                                st.write(f"- {class_name}: {conf:.2%} confianza")
                                detecciones.append((class_name, conf))
                        else:
                            st.write("No se detectaron defectos.")

                        st.divider()

                        # ── Guardar imagen de resultado ───────────────────────────
                        top_class = detecciones[0][0] if detecciones else "sin_defecto"
                        img_filename = f"Inspección_{obra}_{n_reporte}_{top_class}_{len(all_results)+1}.png"
                        result_img.save(os.path.join(OBRA_DIR, img_filename))

                        all_results.append(
                            {
                                "img": img,
                                "result_img": result_img,
                                "detecciones": detecciones,
                                "filename": img_filename,
                            }
                        )

                except Exception as e:
                    st.error(f"Error evaluando {img_file_buffer.name}: {e}")
                finally:
                    os.unlink(temp_path)

            # Persist all results for the report button
            st.session_state["all_results"] = all_results

    # ── Generar reporte ───────────────────────────────────────────────────────
    if st.button("Generar reporte"):
        if "all_results" not in st.session_state or not st.session_state["all_results"]:
            st.warning(
                "Por favor, proporciona al menos una imagen antes de generar el reporte."
            )
        elif not obra or not inspector or not n_reporte:
            st.warning("Completa los datos del reporte antes de generarlo.")
        else:
            all_results = st.session_state["all_results"]

            imagenes_y_detecciones = [
                (r["result_img"], r["detecciones"]) for r in all_results
            ]

            reemplazos = {
                "{{OBRA}}": obra,
                "{{INSPECTOR}}": inspector,
                "{{N_REPORTE}}": n_reporte,
                "{{FECHA}}": fecha,
            }

            if not os.path.isfile(TEMPLATE_PATH):
                st.error(f"No se encontró la plantilla: {TEMPLATE_PATH}")
                return

            reporte_bytes = generar_reporte(
                TEMPLATE_PATH,
                imagenes_y_detecciones,  # now a list
                reemplazos,
            )

            st.download_button(
                label="📄 Descargar reporte",
                data=reporte_bytes,
                file_name=f"Inspección_Soldadura_{obra}_{n_reporte}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


if __name__ == "__main__":
    main()
