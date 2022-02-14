import pandas as pd

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn as sns

spacex_df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv', 
                            encoding = "ISO-8859-1")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.Label(['Space X Launch Performance'] ,style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                     
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                   
            ],
            value='OPT1',
            placeholder="Select a Launch Site:",searchable=True,
            style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'color': '#503D36',  'font-size': '20px'}),
        
        
    ]),

    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),
     html.Br(),

     html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    #dcc.RangeSlider(id='payload-slider',...)
    dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,marks={0: '0',100: '100'},
    value=[0, 10000]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),

])

#---------------------------------------------------------------
@app.callback(
    [Output(component_id='success-pie-chart', component_property='figure'),
     Output(component_id='success-payload-scatter-chart', component_property='figure')],
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)

def update_graph(my_dropdown, slider_range):
    low, high = slider_range
    
   
    if (my_dropdown == "ALL" ):
        dff = spacex_df
        mask = dff[(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)]
        piechart=px.pie(
            data_frame=dff,
            labels = 'Launch Site',
            names='Launch Site',
            hole=.3,
            )
        catplot = px.scatter(mask, y="class", x="Payload Mass (kg)", color="Booster Version Category", hover_data=['Payload Mass (kg)'])

    else:
            dff = spacex_df[spacex_df['Launch Site'] == my_dropdown]
            mask = dff[(dff['Payload Mass (kg)'] > low) & (dff['Payload Mass (kg)'] < high)]
            piechart=px.pie(
            data_frame=dff[dff['Launch Site'] == my_dropdown],            
            names='class',
            hole=.3,
            )
            catplot = px.scatter(mask, y="class", x="Payload Mass (kg)", color="Booster Version Category",hover_data=['Payload Mass (kg)'])

    return [piechart, catplot]


if __name__ == '__main__':
    app.run_server(debug=True)
