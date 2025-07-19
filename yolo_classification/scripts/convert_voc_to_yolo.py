import os, shutil
import xml.etree.ElementTree as ET
from tqdm import tqdm

# Configurações
VOC_ROOT = "datasets/VOC2007/VOCdevkit/VOC2007"
YOLO_ROOT = "datasets/VOC2007"  # Pasta final para YOLO

# Classes do Pascal VOC 2007
CLASSES = [
    "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

def convert_annotation(xml_file, output_txt):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    with open(output_txt, 'w') as f:
        for obj in root.findall('object'):
            cls = obj.find('name').text
            if cls not in CLASSES:
                continue
                
            cls_id = CLASSES.index(cls)
            bbox = obj.find('bndbox')
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)
            
            # Convert to YOLO format (normalized center-x, center-y, width, height)
            width = xmax - xmin
            height = ymax - ymin
            x_center = (xmin + width / 2) / int(root.find('size/width').text)
            y_center = (ymin + height / 2) / int(root.find('size/height').text)
            width /= int(root.find('size/width').text)
            height /= int(root.find('size/height').text)
            
            f.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")

# Criar estrutura de pastas
os.makedirs(f"{YOLO_ROOT}/images/train", exist_ok=True)
os.makedirs(f"{YOLO_ROOT}/images/val", exist_ok=True)
os.makedirs(f"{YOLO_ROOT}/labels/train", exist_ok=True)
os.makedirs(f"{YOLO_ROOT}/labels/val", exist_ok=True)

# Processar trainval (treino + validação)
with open(f"{VOC_ROOT}/ImageSets/Main/trainval.txt") as f:
    trainval_ids = [line.strip() for line in f.readlines()]

for img_id in tqdm(trainval_ids, desc="Processando trainval"):
    # Criar links simbólicos para as imagens (evita duplicar arquivos)
    shutil.move(
        f"{VOC_ROOT}/JPEGImages/{img_id}.jpg",
        f"{YOLO_ROOT}/images/train/{img_id}.jpg"
    )
    # Converter anotações XML para TXT (YOLO)
    convert_annotation(
        f"{VOC_ROOT}/Annotations/{img_id}.xml",
        f"{YOLO_ROOT}/labels/train/{img_id}.txt"
    )

# Processar test (validação)
with open(f"{VOC_ROOT}/ImageSets/Main/test.txt") as f:
    test_ids = [line.strip() for line in f.readlines()]

for img_id in tqdm(test_ids, desc="Processando test"):
    shutil.move(
        f"{VOC_ROOT}/JPEGImages/{img_id}.jpg",
        f"{YOLO_ROOT}/images/val/{img_id}.jpg"
    )
    convert_annotation(
        f"{VOC_ROOT}/Annotations/{img_id}.xml",
        f"{YOLO_ROOT}/labels/val/{img_id}.txt"
    )

#Criar arquivo VOC.yaml
with open(f"{YOLO_ROOT}/VOC.yaml", 'w') as f:
    f.write(f"""train: ../{YOLO_ROOT}/images/train
val: ../{YOLO_ROOT}/images/val
test: ../{YOLO_ROOT}/images/test

nc: {len(CLASSES)}
names: {CLASSES}""")

print("Conversão concluida!")
print(f"Estrutura criada em: {YOLO_ROOT}")