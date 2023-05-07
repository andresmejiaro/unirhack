#%%

from transformers import AutoFeatureExtractor, AutoModelForImageClassification

extractor = AutoFeatureExtractor.from_pretrained("OttoYu/Tree-ConditionHK")

model = AutoModelForImageClassification.from_pretrained("OttoYu/Tree-ConditionHK")



# Preprocess the image using the feature extractor

# %%
# Make a prediction using the model

def mmodel(imagepath):
    new_image = Image.open(imagepath)
    inputs = extractor(new_image, return_tensors="pt")
    outputs = model(**inputs)
    return(outputs.logits.argmax().item())

def label(imagepath):
    return(imagepath)



#%%
import os
import random
from PIL import Image
import base64
import time
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from io import BytesIO


def get_random_image(folder):
    images = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                images.append(os.path.join(root, file))

    return random.choice(images) if images else None
#%%
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Interval(id='image-update', interval=5000, n_intervals=0),
    html.Img(id='random-image', src=''),
    html.Div(id='results'),
])

@app.callback(
    [Output('random-image', 'src'),
     Output('results', 'children')],
    [Input('image-update', 'n_intervals')]
)
def update_image(n_intervals):
    image_path = get_random_image('/Users/amejia/bt__hackaton/TreeDisease')
    if image_path is None:
        return '', 'No images found.'

    with Image.open(image_path) as img:
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_data = base64.b64encode(img_io.getvalue()).decode()

    prediction = mmodel(image_path)
    true_label = label(image_path)
    result_match = prediction == true_label
    result_icon = html.I(className='fas fa-check text-success') if result_match else html.I(className='fas fa-times text-danger')

    results = [
        html.P(f"Prediction: {prediction}"),
        html.P(f"True Label: {true_label}"),
        result_icon
    ]

    return f"data:image/png;base64,{img_data}", results

if __name__ == '__main__':
    app.run_server(debug=True)
