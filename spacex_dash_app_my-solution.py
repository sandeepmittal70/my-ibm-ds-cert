# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Launch Sites
# CCAFS LC-40
# VAFB SLC-4E
# KSC LC-39A
# CCAFS SLC-40

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'site1'},
                                        {'label': 'CCAFS SLC-40', 'value': 'site2'},
                                        {'label': 'KSC LC-39A', 'value': 'site3'},
                                        {'label': 'VAFB SLC-4E', 'value': 'site4'},
                                    ],
                                    value='ALL', # Providing a vallue to dropdown
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

#Place to add @app.callback Decorator
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                    values='class', 
                    names='Launch Site',
                    title='Total Success Launches By Site')
        return fig
    elif entered_site == 'site1':
        # 'label': 'CCAFS LC-40', 'value': 'site1'
        filtered_df =  spacex_df[spacex_df['Launch Site']=='CCAFS LC-40'].groupby(['class'])['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                    values='Launch Site', 
                    names='class',
                    title='Total Success Launches For Site CCAFS LC-40')
        return fig
    elif entered_site == 'site2':
        # {'label': 'CCAFS SLC-40', 'value': 'site2'},
        filtered_df =  spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40'].groupby(['class'])['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                    values='Launch Site', 
                    names='class',
                    title='Total Success Launches For Site CCAFS SLC-40')
        return fig
    elif entered_site == 'site3':
        # {'label': 'KSC LC-39A', 'value': 'site3'},
        filtered_df =  spacex_df[spacex_df['Launch Site']=='KSC LC-39A'].groupby(['class'])['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                    values='Launch Site', 
                    names='class',
                    title='Total Success Launches For Site KSC LC-39A')
        return fig
    elif entered_site == 'site4':
        # {'label': 'VAFB SLC-4E', 'value': 'site4'},
        filtered_df =  spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E'].groupby(['class'])['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                    values='Launch Site', 
                    names='class',
                    title='Total Success Launches For Site VAFB SLC-4E')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, slider_range):
    low, high = slider_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
                        x="Payload Mass (kg)",
                        y="class", 
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for all Sites'
              )
    elif entered_site == 'site1':
        # 'label': 'CCAFS LC-40', 'value': 'site1'
        filtered_df =  filtered_df[filtered_df['Launch Site']=='CCAFS LC-40']
        fig = px.scatter(filtered_df, 
                        x="Payload Mass (kg)",
                        y="class", 
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for site CCAFS LC-40'
              )
    elif entered_site == 'site2':
        # {'label': 'CCAFS SLC-40', 'value': 'site2'},
        filtered_df =  filtered_df[filtered_df['Launch Site']=='CCAFS SLC-40']
        fig = px.scatter(filtered_df, 
                        x="Payload Mass (kg)",
                        y="class", 
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for site CCAFS SLC-40'
              )
    elif entered_site == 'site3':
        # {'label': 'KSC LC-39A', 'value': 'site3'},
        filtered_df =  filtered_df[filtered_df['Launch Site']=='KSC LC-39A']
        fig = px.scatter(filtered_df, 
                        x="Payload Mass (kg)",
                        y="class", 
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for site KSC LC-39A'
              )
    elif entered_site == 'site4':
        # {'label': 'VAFB SLC-4E', 'value': 'site4'},
        filtered_df =  filtered_df[filtered_df['Launch Site']=='VAFB SLC-4E']
        fig = px.scatter(filtered_df, 
                        x="Payload Mass (kg)",
                        y="class", 
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for site VAFB SLC-4E'
              )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
