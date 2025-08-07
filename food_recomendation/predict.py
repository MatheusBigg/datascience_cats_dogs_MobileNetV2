import os
os.environ["TF_USE_LEGACY_KERAS"] = "1" 
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

def load_and_preprocess_image(image_path, img_size=(224, 224)):
    try:
        image = Image.open(image_path).resize(img_size)
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        return image
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return None

image_path = './imgs_to_predict/cebola.jpg'

class_names = ['Bread', 'Dairy product', 'Dessert', 'Egg', 'Fried food', 'Meat', 'Noodles/Pasta', 'Rice', 'Seafood', 'Soup', 'Vegetable/Fruit']

print("Carregando o melhor modelo...")
try:
    model = tf.keras.models.load_model(
        'best_model.h5', 
        custom_objects={'KerasLayer': hub.KerasLayer}
    )
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print("Certifique-se de que o arquivo 'best_model.h5' existe.")
    exit()

processed_image = load_and_preprocess_image(image_path)
if processed_image is None:
    exit()

print("Fazendo a previsão...")
predictions = model.predict(processed_image)

predicted_class_index = np.argmax(predictions, axis=1)[0]
predicted_class_name = class_names[predicted_class_index]
confidence_score = predictions[0][predicted_class_index]

print("\nResultado da Previsao")
print(f"A imagem é um(a) '{predicted_class_name}'")
print(f"Confiança: {confidence_score*100:.2f}%")