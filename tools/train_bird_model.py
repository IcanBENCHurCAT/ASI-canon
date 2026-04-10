import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

def generate_dummy_data(num_samples=1000, num_classes=5):
    """
    Generate dummy audio waveform data.
    Shape for YAMNet: (samples, waveform_length)
    YAMNet expects 16kHz audio. We use 1 second = 16000 samples.
    """
    waveform_length = 16000
    X = np.random.uniform(-1.0, 1.0, size=(num_samples, waveform_length)).astype(np.float32)
    y = np.random.randint(0, num_classes, size=(num_samples,))
    return X, y

import tf_keras as keras

def build_yamnet_model(num_classes):
    """
    Build a model using YAMNet for embeddings + a dense classification head.
    """
    yamnet_model_handle = 'https://tfhub.dev/google/yamnet/1'
    yamnet_layer = hub.KerasLayer(yamnet_model_handle, trainable=False, output_key='embeddings')

    # YAMNet natively expects a 1D tensor of shape `(samples,)`.
    # However, for training with batches, we often need a shape `(batch, samples)`.
    # To handle batches, we can use `tf.map_fn` or `tf.vectorized_map`, or if we just want a simple model,
    # we can define it with Functional API. Wait, YAMNet can actually take batched input?
    # The documentation for YAMNet says: `waveform: A 1-D float32 tensor of shape [samples]`.
    # So we need to map over the batch.

    class YAMNetBatchLayer(keras.layers.Layer):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # YAMNet returns a tuple: (scores, embeddings, spectrogram)
            self.yamnet = hub.KerasLayer(yamnet_model_handle, trainable=False)

        def call(self, inputs):
            # Input is (batch, samples)
            # Map over batch
            def map_fn(x):
                # Returns (scores, embeddings, spectrogram)
                # We want embeddings, which is index 1
                _, embeddings, _ = self.yamnet(x)
                return embeddings

            # Use map_fn to process each waveform in the batch
            embeddings = tf.map_fn(map_fn, inputs, fn_output_signature=tf.float32)
            # embeddings is now (batch, frames, 1024)
            # Pool across frames
            return tf.reduce_mean(embeddings, axis=1)

    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(16000,)),
        YAMNetBatchLayer(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(num_classes, activation='softmax')
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
    # Required for tf.map_fn and complex ops in TFLite
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS
    ]
    tflite_model = converter.convert()

    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    print(f"TFLite model successfully saved to {output_path}")

def main():
    print("Generating dummy audio waveform dataset...")
    num_classes = 5
    X_train, y_train = generate_dummy_data(num_samples=200, num_classes=num_classes)
    X_test, y_test = generate_dummy_data(num_samples=50, num_classes=num_classes)

    print("Building model with YAMNet backbone...")
    model = build_yamnet_model(num_classes)
    model.summary()

    print("Training model...")
    # Training for a few epochs just to verify the pipeline
    model.fit(X_train, y_train, epochs=3, validation_data=(X_test, y_test), batch_size=32)

    print("Converting model to TFLite format for Android...")
    tflite_path = "tools/bird_model.tflite"
    convert_to_tflite(model, tflite_path)

if __name__ == '__main__':
    main()
