import tensorflow as tf
import os

#Pre-Processamento
BATCH_SIZE = 8
IMG_SIZE = (224, 224)
DATA_DIR = './food-11'

def get_datasets():
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{DATA_DIR}/training",
        shuffle=True,
        batch_size=BATCH_SIZE,
        image_size=IMG_SIZE
    )

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{DATA_DIR}/validation",
        shuffle=False,
        batch_size=BATCH_SIZE,
        image_size=IMG_SIZE
    )

    # O dataset de teste/avaliação também será carregado
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{DATA_DIR}/evaluation",
        shuffle=False,
        batch_size=BATCH_SIZE,
        image_size=IMG_SIZE
    )

    class_names = train_dataset.class_names

    # Normaliza os valores dos pixels de [0, 255] para [0, 1]
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    # Cache e prefetch para otimizar a performance
    AUTOTUNE = tf.data.AUTOTUNE

    #Normalização
    train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=AUTOTUNE)
    validation_dataset = validation_dataset.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=AUTOTUNE)
    
    return train_dataset, validation_dataset, test_dataset, class_names

if __name__ == '__main__':
    train_ds, val_ds, test_ds, class_names = get_datasets()
    print("Nomes das classes:", class_names)