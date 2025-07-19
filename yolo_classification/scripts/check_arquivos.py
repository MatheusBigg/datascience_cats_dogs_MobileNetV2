import os
from pathlib import Path

# Configurações
base_dir = Path("/home/gengar/Projetos/data/dio_datascience_bootcamp/yolo_classification/datasets/VOC2007")
image_dir = base_dir / "images/train"
label_dir = base_dir / "labels/train"

# Verifique correspondência entre imagens e labels
missing_pairs = []
for img_file in image_dir.glob("*.jpg"):
    label_file = label_dir / f"{img_file.stem}.txt"
    if not label_file.exists():
        missing_pairs.append((img_file.name, "label faltando"))

for txt_file in label_dir.glob("*.txt"):
    img_file = image_dir / f"{txt_file.stem}.jpg"
    if not img_file.exists():
        missing_pairs.append(("imagem faltando", txt_file.name))

if missing_pairs:
    print("⚠️ Problemas encontrados:")
    for img, lbl in missing_pairs:
        print(f"- {img} | {lbl}")
else:
    print("✅ Todos os arquivos estão pareados corretamente")

# Verifique conteúdo dos labels
print("\nAmostra de labels (3 primeiros):")
for txt_file in list(label_dir.glob("*.txt"))[:3]:
    print(f"\n{txt_file.name}:")
    with open(txt_file) as f:
        print(f.read())