import argparse
import os
import torch
from ultralytics import YOLO
from pathlib import Path


def main():
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))  # .../src/evasol
    PROJECT_ROOT = os.path.dirname(os.path.dirname(FILE_DIR))  # .../EvaSol

    # ── Argumentos ───────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="Entrenamiento YOLO para detección de defectos"
    )
    parser.add_argument(
        "epochs", type=int, help="Número de epochs, o iteraciones de entrenamiento"
    )
    parser.add_argument("output", type=str, help="Nombre del modelo de salida (.pt)")
    args = parser.parse_args()

    # ── Info de dispositivo ──────────────────────────────────────────────────
    print("PyTorch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("Device count:", torch.cuda.device_count())
    print(
        "GPU name:",
        torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No CUDA GPU",
    )
    device_available = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device_available)

    # ── Cargar modelo ─────────────────────────────────────────────────────────
    # yaml_path = os.path.join(
    #     PROJECT_ROOT, "Imagenes", "defectos_de_soldaduras", "defectos_de_soldaduras", "data.yaml"
    # )
    yaml_path = os.path.join(
        PROJECT_ROOT, "Imagenes", "dataset", "data.yaml"
    )
    model = YOLO(os.path.join(PROJECT_ROOT, "src", "modelos", "yolo11n.pt"))

    # ── Entrenamiento ─────────────────────────────────────────────────────────
    try:
        model.train(
            data=yaml_path,
            epochs=args.epochs,
            # imgsz=640,
            augment=True,
            device=device_available,
            workers=0,
            name=args.output.replace(".pt", ""),
        )
        print("Entrenamiento finalizado correctamente.")

    except Exception as e:
        print(f"Error durante el entrenamiento: {e}")
        raise

    # ── Guardar modelo ────────────────────────────────────────────────────────
    final_model_path = os.path.join(PROJECT_ROOT, "src", "modelos", args.output)
    model.save(final_model_path)
    print(f"Modelo {args.output} guardado en {final_model_path}")


if __name__ == "__main__":
    main()
