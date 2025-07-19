import sys
from pathlib import Path
# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Adiciona yolov5 ao sys.path se necessário
YOLOV5_DIR = BASE_DIR / "yolov5"
if str(YOLOV5_DIR) not in sys.path:
    sys.path.insert(0, str(YOLOV5_DIR))  # Isso ajuda no import dentro do detect_torch.py

# Caminho do modelo
MODEL_PATH = YOLOV5_DIR / "runs" / "train" / "custom_model14" / "weights" / "last.pt"
print(f"Verificando modelo em: {MODEL_PATH}")
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Arquivo do modelo não encontrado em {MODEL_PATH}")


from detect_torch import CustomDetector

detector = CustomDetector(
    model_path=str(MODEL_PATH),
    conf_thres=0.6
)

IMG_PATH = BASE_DIR  / "imgs_to_predict" / "mulher_kombi.jpg"
SAVE_PATH = BASE_DIR / "imgs_to_predict" / "mulher_kombi_result.jpg"

# Detecta e salva
results = detector.predict(
    image_path=str(IMG_PATH),
    save_path=str(SAVE_PATH)
)

print("Objetos detectados:")
for obj in results:
    print(f"- {obj['class']} ({obj['confidence']:.2f}): {obj['bbox']}")