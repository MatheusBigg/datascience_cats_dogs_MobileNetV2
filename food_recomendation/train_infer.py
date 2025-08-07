# train_and_predict.py
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1" # Compatibilidade com versões mais antigas do TensorFlow
import tensorflow as tf
import tensorflow_hub as hub
from pre_process import get_datasets

def create_model(num_classes):
    #model_url = "https://www.kaggle.com/models/google/bit/TensorFlow2/m-r152x4/1"
    print("Criando modelo com EfficientNetB0")
    model_url = "https://tfhub.dev/tensorflow/efficientnet/b0/feature-vector/1"
    effi_model = hub.KerasLayer(model_url, trainable=False) #Seta false para travar layers de peso ao baixar o modelo
    
    #Ultima camada densa para classificação
    print("Adicionando camada densa para classificação")
    model = tf.keras.Sequential([
        effi_model,
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    
    return model

def train_model(model, train_ds, val_ds, epochs=10):
    #Treinamento e checkpoint
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath='best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[checkpoint_callback],
        verbose=1
    )
    return history

def evaluate_model(model, test_ds):
    #Avaliação
    print("\nAvaliando o modelo no conjunto de teste")
    loss, accuracy = model.evaluate(test_ds)
    print(f"Acurácia no conjunto de teste: {accuracy*100:.2f}%")
    print(f"Perda no conjunto de teste: {loss:.4f}")

def main():
    train_ds, val_ds, test_ds, class_names = get_datasets()
    num_classes = len(class_names)
    print(f"Número de classes detectadas: {num_classes}")
    
    model = create_model(num_classes)
    print(f"Iniciando treinamento")
    train_model(model, train_ds, val_ds, epochs=10)
    
    best_model = tf.keras.models.load_model(
        'best_model.h5', custom_objects={'KerasLayer': hub.KerasLayer}
    )
    print(f"Avaliando o modelo")
    evaluate_model(best_model, test_ds)
    
if __name__ == '__main__':
    # --- Configuração da GPU ---
    print("Verificando dispositivos GPU...")
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            # Permite o crescimento dinâmico de memória da GPU para evitar erros
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(f"\nDispositivos GPU encontrados: {len(gpus)}")
            print(f"GPUs lógicas configuradas: {len(logical_gpus)}")
            print("Treinamento será executado na GPU.")
        except RuntimeError as e:
            # Erro de configuração de GPU
            print(e)
    else:
        print("\nNenhuma GPU encontrada. O treinamento será executado na CPU, o que pode ser lento.")
    # --- Fim da Configuração da GPU ---
    main()