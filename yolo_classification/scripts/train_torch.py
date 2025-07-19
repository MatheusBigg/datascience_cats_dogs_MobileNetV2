import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # yolo_classification/

import torch
from yolov5.train import run
from yolov5.utils.torch_utils import EarlyStopping
from yolov5.utils.torch_utils import select_device

class CustomTrainer:
    def __init__(self):
        self.config = {
            'weights': 'yolov5s.pt',  # Modelo pré-treinado (YOLOv5 small)
            'data': 'datasets/VOC2007/VOC.yaml',  # Caminho do dataset
            'epochs': 100,  # Número máximo de épocas
            'batch-size': 16,  # Tamanho do lote
            'img-size': 640,  # Tamanho da imagem de entrada
            'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',  # Seleciona GPU/CPU automaticamente
            'name': 'custom_model',  # Nome do experimento
            'freeze': [0, 1, 2, 3, 4],  # Congela as primeiras 5 camadas
            'optimizer': 'AdamW',  # Otimizador (Adam com weight decay)
            'lr0': 0.001,  # Taxa de aprendizado inicial
            'lrf': 0.01,  # Fator final de LR (lr0 * lrf)
            'momentum': 0.937,  # Momentum para SGD
            'weight_decay': 0.0005,  # Regularização L2
            'warmup_epochs': 3.0,  # Épocas de aquecimento do LR
            'augment': True,  # Ativa aumento de dados
            'hsv_h': 0.015,  # Variação de matiz (HSV augmentation)
            'hsv_s': 0.7,  # Variação de saturação
            'hsv_v': 0.4,  # Variação de valor (brightness)
            'degrees': 10.0,  # Rotação máxima (em graus)
            'translate': 0.1,  # Translação máxima (fração da imagem)
            'scale': 0.5,  # Escala máxima (zoom in/out)
            'shear': 0.0,  # Cisalhamento máximo
            'patience': 10,  # Épocas sem melhoria para early stopping
            'save_period': -1,  # Salva checkpoints a cada X épocas (-1 = desligado)
            'local_rank': -1,  # Para treino distribuído (-1 = single GPU)
            'workers': 8  # Número de threads para carregar dados
        }
        
        self.early_stopping = EarlyStopping(
            patience=self.config['patience']
        )


    def setup_augmentation(self):
        return {
            'hsv_h': self.config['hsv_h'],
            'hsv_s': self.config['hsv_s'],
            'hsv_v': self.config['hsv_v'],
            'degrees': self.config['degrees'],
            'translate': self.config['translate'],
            'scale': self.config['scale'],
            'shear': self.config['shear']
        }

    def train(self):
        augmentation = self.setup_augmentation()
        
        results = run(
            weights=self.config['weights'],
            data=self.config['data'],
            epochs=self.config['epochs'],
            batch_size=self.config['batch-size'],
            imgsz=self.config['img-size'],
            device=self.config['device'],
            name=self.config['name'],
            freeze=self.config['freeze'],
            optimizer=self.config['optimizer'],
            lr0=self.config['lr0'],
            lrf=self.config['lrf'],
            momentum=self.config['momentum'],
            weight_decay=self.config['weight_decay'],
            warmup_epochs=self.config['warmup_epochs'],
            augment=self.config['augment'],
            hsv_h=augmentation['hsv_h'],
            hsv_s=augmentation['hsv_s'],
            hsv_v=augmentation['hsv_v'],
            degrees=augmentation['degrees'],
            translate=augmentation['translate'],
            scale=augmentation['scale'],
            shear=augmentation['shear'],
            patience=self.config['patience'],
            save_period=self.config['save_period'],
            local_rank=self.config['local_rank'],
            workers=self.config['workers'],
            nosave=True,
            exist_ok=True,  # Permite sobrescrever a pasta
        )
        
        return results

if __name__ == '__main__':
    trainer = CustomTrainer()
    trainer.train()