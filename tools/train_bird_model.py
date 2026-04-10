import numpy as np
import tensorflow as tf

def generate_dummy_data(num_samples=1000, num_features=40, num_classes=5):
    """
    Generate dummy spectrogram-like data.
    Shape: (samples, time_steps, features, channels)
    """
    time_steps = 50
    X = np.random.rand(num_samples, time_steps, num_features, 1).astype(np.float32)
    y = np.random.randint(0, num_classes, size=(num_samples,))
    return X, y

def build_model(input_shape, num_classes):
    """
    Build a tiny CNN suitable for Android devices.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=input_shape),
        # Block 1
        tf.keras.layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        # Block 2
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        # Dense
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def convert_to_tflite(model, output_path):
    """
    Convert a Keras model to a TFLite model optimized for mobile.
    """
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # Apply optimizations to reduce model size and improve inference latency
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    print(f"TFLite model successfully saved to {output_path}")

def main():
    print("Generating dummy audio spectrogram dataset...")
    num_classes = 5
    X_train, y_train = generate_dummy_data(num_samples=800, num_classes=num_classes)
    X_test, y_test = generate_dummy_data(num_samples=200, num_classes=num_classes)

    input_shape = X_train.shape[1:]

    print(f"Building tiny model with input shape {input_shape}...")
    model = build_model(input_shape, num_classes)
    model.summary()

    print("Training model...")
    # Training for a few epochs just to verify the pipeline
    model.fit(X_train, y_train, epochs=3, validation_data=(X_test, y_test), batch_size=32)

    print("Converting model to TFLite format for Android...")
    tflite_path = "tools/bird_model.tflite"
    convert_to_tflite(model, tflite_path)

if __name__ == '__main__':
    main()
