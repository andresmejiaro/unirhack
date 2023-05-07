import os
import random
from PIL import Image
import base64
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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src="assets/Olitech Logo.png", className="img-fluid"),
            html.Img(id='random-image', src='', className='mx-auto'),
        ], className="text-center mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(id="user-input", placeholder="Type your message...", n_submit=0),
                dbc.Button("Enviar", id="send-button", color="yellow", n_clicks=0)
            ], className="mb-3")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Loading(id="loading", type="circle",
                        children=[html.Div(id="chat-output")]),
        ])
    ]),
], style={"backgroundColor": "#2f4e01"})

@app.callback(
    Output('random-image', 'src'),
    [Input('image-update', 'n_intervals')]
)
def update_image(n_intervals):
    image_path = get_random_image('/path/to/image/folder')
    if image_path is None:
        return ''

    with Image.open(image_path) as img:
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_data = base64.b64encode(img_io.getvalue()).decode()

    return f"data:image/png;base64,{img_data}"

if __name__ == '__main__':
    app.run_server(debug=True)