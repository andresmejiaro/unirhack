import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import openai
import json

icon_style = {
    'verticalAlign': 'middle',
    'marginRight': '10px',
    'fontSize': '48px',
    'color': 'olive'
}

# Create the icon element
icon = html.I(className="fa fa-leaf", style=icon_style)


openai.api_key = "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"

def chat(msg):
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=("You are an expert in Agricultural sciences with over 20 years experience helping olive farmers grow their crops. "
                "Answer any question given in language a farmer with high school education can understand. Give your answer in peninsular spanish "
                "Do not answer questions not related to olive farming, Ask for a related question instead in spanish.\n\n"
                "Q: " + msg + "\nA: "),
        temperature=0.7,
        max_tokens=2000,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].text.strip()

# def chat(msg):
#     return ("Hola")

# Create a Dash app with Bootstrap CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/index.css"])
app.title = "Olitech - Olive Chatbot"

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src="assets/Olitech Logo.png", className="img-fluid")
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

# Define the callbacks
@app.callback(
    Output("chat-output", "children"),
    [Input("send-button", "n_clicks"),
     Input("user-input", "n_submit")],
    [State("user-input", "value")]
)
def update_chat_output(n_clicks, n_submit, user_input):
    if not user_input:
        return ""
    elif n_clicks > 0 or n_submit > 0:
        chatbot_response = chat(user_input)
        return chatbot_response

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)