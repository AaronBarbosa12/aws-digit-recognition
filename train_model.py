import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load the MNIST dataset into memory
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Create an ImageDataGenerator for random rotations
datagen = ImageDataGenerator(
    rotation_range=20, height_shift_range=0.2, width_shift_range=0.2
)
datagen.fit(x_train.reshape(-1, 28, 28, 1))

# Create a new dataset by applying the datagen to the original data
y_train = tf.keras.utils.to_categorical(y_train, 10)
training_data_augmented = datagen.flow(
    x_train.reshape(-1, 28, 28, 1), y_train, batch_size=64
)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# Define the neural network model
model = tf.keras.models.Sequential(
    [
        tf.keras.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ]
)

# Compile the model with an optimizer, loss function, and metrics
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.CategoricalAccuracy()],
)

# Train the model on the augmented data
model.fit(
    training_data_augmented,
    epochs=5,
    validation_data=(x_test.reshape(-1, 28, 28, 1), y_test),
)

# Convert the Keras model to a TensorFlow Lite model and save it to disk
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with tf.io.gfile.GFile("app/model/model.tflite", "wb") as f:
    f.write(tflite_model)
