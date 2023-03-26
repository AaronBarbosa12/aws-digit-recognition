import gradio as gr
import numpy as np
import subprocess
import base64

def predict(image):
    '''
    Predict the value of the digit contained in `image`.
    This is done by querying an AWS lambda function on the input `image`.
    '''
    
    filename = 'image.npy'
    url = 'LAMDA_API_GATEWAY_URL'

    # Construct the JSON payload
    file_content = base64.b64encode(image.tobytes()).decode('utf-8').replace('\n', '')
    json_payload = f'{{"file_content": "{file_content}", "file_name": "{filename}"}}'

    # Call the lambda function
    return subprocess.run(['curl', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', json_payload, url]) 

# Create a Gradio sketchpad input interface for drawing a digit
sp = gr.Sketchpad().style(height=280, width=280, description="Draw a digit")

# Create a Gradio interface for the `predict` function
demo = gr.Interface(fn = predict,
    inputs = sp, 
    outputs = "text"
)

# Launch the interface
demo.launch()