import tensorflow.lite as tflite
import numpy as np
import tempfile
import base64
import json

# Load the tflite model
interpreter = tflite.Interpreter(model_path="model/model.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def call_model(image):
    '''
    Predict the value of the handwritten digit contained in `image`.

    Parameters
    --------
    image: np.ndarray
        Image of a handwritten digit, size (28,28,1).

    Returns
    --------
    result: str
        String containing the model's prediction for contents of the `image`.
    '''
    # Set the input data
    image_tensor = np.expand_dims(np.asarray(image, dtype=np.float32), axis=(0, -1))
    interpreter.set_tensor(input_details[0]["index"], image_tensor)

    # Run the model
    interpreter.invoke()

    # Get the output data
    output_data = interpreter.get_tensor(output_details[0]["index"])
    return f"I see the number {np.argmax(output_data, axis = 1)[0]}!"

def handler(event, context):
    '''
    Lambda handler for querying the pretrained ML model. 

    Returns
    --------
    result: str
        String containing the model's prediction
    '''
    body = json.loads(event["body"])
    file_content = base64.b64decode(body["file_content"])

    file_name = event["file_name"]
    with tempfile.NamedTemporaryFile(suffix=file_name, delete=False) as f:
        f.write(file_content)
        f.flush()
        image = np.load(f.name)

    result = call_model(image)
    return result
