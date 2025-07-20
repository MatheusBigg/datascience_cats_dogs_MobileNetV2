import sys
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
YOLOV5_DIR = BASE_DIR / "yolov5"
sys.path.insert(0, str(YOLOV5_DIR))

MODEL_PATH = YOLOV5_DIR / "runs" / "train" / "custom_model14" / "weights" / "last.pt"
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")

from detect_torch import CustomDetector

SAVE_PATH = BASE_DIR / "imgs_to_predict"

# Instancia o detector
detector = CustomDetector(
    model_path=str(MODEL_PATH),
    conf_thres=0.6
)

# Usa a webcam padrão (índice 0)
cam_index = [0, 1, 2, 3, 4]
for idx in cam_index:
    try:
        print(f"Tentando acessar webcam no índice {idx}...")
        detector.predict_webcam(cam_index=idx, save_path=str(SAVE_PATH))
        break  # Se conseguir acessar, sai do loop
    except RuntimeError as e:
        print(f"Erro ao acessar webcam no índice {idx}: {e}")

