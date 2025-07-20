import os
import sys
from pathlib import Path

# Caminho ABSOLUTO para a pasta yolov5
YOLO_DIR = Path(__file__).parent.parent / "yolov5"
sys.path.insert(0, str(YOLO_DIR))  # Insere no início do path

# Imports internos do YOLOv5
try:
    from utils.augmentations import letterbox
    from models.common import DetectMultiBackend
    from utils.general import non_max_suppression, scale_boxes
    from utils.plots import Annotator, colors
except ImportError as e:
    print(f"Erro de importação! sys.path={sys.path}")
    print(f"Conteúdo de {YOLO_DIR}: {list(YOLO_DIR.glob('*'))}")
    raise

import cv2
import torch
from datetime import datetime


class CustomDetector:
    def __init__(self, model_path, conf_thres=0.5, iou_thres=0.45):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = DetectMultiBackend(model_path, device=self.device)
        self.model.eval()
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.stride = self.model.stride
        self.names = self.model.names

    def predict(self, image_path, save_path=None):
        # Carrega a imagem
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Imagem {image_path} não encontrada.")
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Pré-processamento
        img_processed = letterbox(img_rgb, 640, stride=self.stride, auto=True)[0]
        img_processed = img_processed.transpose((2, 0, 1)).copy()  # HWC to CHW + remove strides negativos
        img_processed = torch.from_numpy(img_processed).to(self.device).float() / 255.0
        img_processed = img_processed.unsqueeze(0)

        # Inferência
        with torch.no_grad():
            pred = self.model(img_processed)
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)

        # Verifica se houve detecção
        if pred[0] is None or len(pred[0]) == 0:
            print("Nenhum objeto detectado!")
            return []

        # Ajusta as caixas para o tamanho original da imagem
        pred[0][:, :4] = scale_boxes(img_processed.shape[2:], pred[0][:, :4], img_rgb.shape).round()

        # Processa e anota resultados
        results = []
        annotator = Annotator(img_rgb, line_width=3, example=str(self.names))

        for det in pred[0]:
            xyxy, conf, cls = det[:4], det[4], det[5]
            label = f'{self.names[int(cls)]} {conf:.2f}'
            annotator.box_label(xyxy, label, color=colors(int(cls), True))

            results.append({
                'class': self.names[int(cls)],
                'confidence': float(conf),
                'bbox': xyxy.cpu().numpy().tolist()
            })

        # Salva ou exibe o resultado
        output_img = annotator.result()
        if save_path:
            cv2.imwrite(save_path, cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
        else:
            cv2.imshow('Detection', cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return results

    def predict_webcam(self, cam_index=0, save_path=None):
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            raise RuntimeError(f"Não foi possível abrir a câmera com índice {cam_index}.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Falha ao capturar frame.")
                break

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Repete a lógica do preprocessamento e inferência para webcam
            img_processed = letterbox(img_rgb, 640, stride=self.stride, auto=True)[0]
            img_processed = img_processed.transpose((2, 0, 1)).copy()
            img_processed = torch.from_numpy(img_processed).to(self.device).float() / 255.0
            img_processed = img_processed.unsqueeze(0)

            with torch.no_grad():
                pred = self.model(img_processed)
                pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)

            if pred[0] is not None and len(pred[0]) > 0:
                pred[0][:, :4] = scale_boxes(img_processed.shape[2:], pred[0][:, :4], img_rgb.shape).round()
                annotator = Annotator(img_rgb, line_width=2, example=str(self.names))
                for det in pred[0]:
                    xyxy, conf, cls = det[:4], det[4], det[5]
                    label = f'{self.names[int(cls)]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(int(cls), True))
                output_img = annotator.result()
            else:
                output_img = img_rgb

            cv2.imshow("Webcam", cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and save_path is not None:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
                filename = f"frame_{timestamp}.jpg"
                full_path = os.path.join(save_path, filename)
                # Salvar com as detecções desenhadas (BGR)
                cv2.imwrite(full_path, cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
                print(f"Frame salvo em {full_path}")

        cap.release()
        cv2.destroyAllWindows()
