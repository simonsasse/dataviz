# %% [markdown]
# 

# %% [markdown]
# # App for Dataviz

# %%

import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.colors as pc
import pandas as pd
import numpy as np
import math

# %% [markdown]
# ## import data

# %%
# read dataframe (preprocessed in main.ipynb)
df = pd.read_csv("data/merged_data_clean.csv").drop(columns = "Unnamed: 0")
# df = df.replace("Eswatini","Swaziland")
df

# %% [markdown]
# ## Modify Data

# %%
# create lookup table for bar chart
iso3_countrynames = pd.DataFrame()
iso3_countrynames["Code"] = df["Code"].unique()
iso3_countrynames["Country"] = df["Country"].unique()
iso3_countrynames

# %% [markdown]
# ## Load Geojson data

# %%
# source: https://public.opendatasoft.com/explore/dataset/country_shapes/export/ 
import geojson
with open("data/country_shapes.geojson") as f:
    gj = geojson.load(f)
gj.get
gj

# %% [markdown]
# ## Color maps

# %%
country_zipper = zip(df["Country"].unique(), pc.sample_colorscale("turbo", df["Country"].unique().size))
color_map_country = dict(country_zipper)
cause_zipper = zip(df.iloc[0, 5:].index.values,  pc.sample_colorscale("rainbow", df.iloc[0, 5:].index.values.size))
color_map_cause = dict(cause_zipper)

# %% [markdown]
# ## Create App

# %%
# define color scheme
colors = {
    'background': 'black',
    'text': 'white',
    'highlight':'yellow'
}
darkScheme ={
    'backgroundColor':colors['background'],
    'color': colors['text']
}
# define hover style
hoverStyle = dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )

# %%
# the variable that holds our final webAPP
app = JupyterDash(__name__)

# create our map with animations already built in
chloropleth = px.choropleth(
        df,
        geojson=gj,
        color="Deaths from HIV/AIDS in 100 thousand people",
        locations="Code",
        featureidkey="properties.cou_iso3_code",
        projection="mercator",
        animation_frame="Year", 
        animation_group="Country",
        range_color=[df['Deaths from HIV/AIDS in 100 thousand people'].min(), df["Deaths from HIV/AIDS in 100 thousand people"].max()],
        hover_name=df["Year"].astype(str) + " " +  df["Country"],
        hover_data={"Deaths from HIV/AIDS in 100 thousand people" : ":.1f",
                        "Life expectancy": ":.1f",
                        "Code":False,
                        "Year":False,
                        "Country":False},
        custom_data=["Code"],
        color_continuous_scale='reds'
        )
# chloropleth.update_traces(colorbar_orientation='h', selector=dict(type='chloropleth'))
chloropleth.update_coloraxes(
        colorbar_thicknessmode="pixels",
        colorbar_orientation='h',
        colorbar_thickness=10,
        colorbar_lenmode="fraction",
        colorbar_len=0.5
)
chloropleth.update_geos(fitbounds="locations", visible=False)
chloropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                             autosize = True)





# here we define the layout and components of our app
app.layout = html.Div([
    #  africa map container
    html.Div([
        html.H1("HIV deaths per 100 Thousand people:", style={'width':'100vw',
                                                                'height':'auto',
                                                                'textAlign': 'center'
                                                                }), # heading
        dcc.Graph(id="chloropleth", config={"displayModeBar": False, "showTips": False},
                                    figure=chloropleth, style={'width': '60vw',
                                                                    'height': '85vh',
                                                                    'display':'inline-block',
                                                                    'verticalAlign':'top'}), # africa map figure with id "chloropleth"
        html.P(
            "Text bezeichnet im nichtwissenschaftlichen Sprachgebrauch eine abgegrenzte, zusammenhängende, meist schriftliche sprachliche Äußerung, im weiteren Sinne auch nicht geschriebene, aber schreibbare Sprachinformation. Aus sprachwissenschaftlicher Sicht sind Texte die sprachliche Form einer kommunikativen Handlung.",
            style={
                    'margin':10,
                    'width': '25vw',
                    'height': '85vh',
                    'display':'inline-block',
                    'fontSize':'150%',
                    'padding':10,
                    'verticalAlign':'middle'
            }
        )
    ], style={
        'width': '100vw',
        'height':'100vh',
        'margin':'20px',
        'verticalAlign':'top'}),
    # dropdown for country selection
    html.Div([
        html.Div(dcc.Dropdown(
                            id='country_select',
                            options=[{'label': code, 'value': country} for index, country, code in iso3_countrynames.itertuples()],
                            multi=True
                        ), style={
                            'margin':'20px',
                            'height': 'auto',
                            'width': '45vw'
                        }),
            # graph (later for the wormgraph)
            html.Div([dcc.Graph(id="worm_figure", style={
                                                    'margin': '20px 20px 20px 20px',
                                                    'display': 'inline-block',
                                                    'height':'70vh',
                                                    'width':'45vw'},
                                                    config={"displayModeBar": False, "showTips": False}),
                    dcc.Graph(id="bar_chart", style={
                                                    'margin': '20px 20px 20px 20px',
                                                    'display': 'inline-block',
                                                    'height':'70vh',
                                                    'width':'45vw'},
                                                    config={"displayModeBar": False, "showTips": False})])
                    ], style={'width':'100vw',
                            'height':'100vh',
                            'padding':'0px',
                            'margin':'10px'})
    ], style={
        'height':'200vh',
        'width':'100vw',
        'font':'Verdana'
    })
  

# %% [markdown]
# ## Create Callbacks

# %%
# here we define the functionality and interactivity of our App
# define input and output of callback function
@app.callback(
    # Output("choropleth", "figure"),
    Output("worm_figure", "figure"),
    # Output("worm_container", "style"),
    Input("country_select", "value"))
    # the callback function: called when a value of the defined inputs above changes.
def display_choropleth(country_select):
    # if no countries are selected
    if(not country_select):
       raise PreventUpdate

    # select df
    df_temp = df[df["Code"].isin(country_select)]
    # create worm graph
    fig2 = px.scatter(df_temp,
                            x="Year",
                            y="Life expectancy",
                            color="Country",
                            color_discrete_map= color_map_country,
                            hover_name=df_temp["Year"].astype(str)+ " " + df_temp["Country"],
                            hover_data={"Deaths from HIV/AIDS in 100 thousand people" : ":.1f",
                                        "Life expectancy": ":.1f",
                                        "Code":False,
                                        "Year":False,
                                        "Country":False},
                            custom_data=["Code","Year","Country"],
                            size = 'Deaths from HIV/AIDS in 100 thousand people',
                            size_max = df["Deaths from HIV/AIDS in 100 thousand people"].max()/30
                            )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="left",
                                x=0
                            ))
    fig2.update_yaxes(range=[df["Life expectancy"].min(), df["Life expectancy"].max()])
    fig2.update_traces(marker = dict(
        sizemode='area',
        sizemin=1,
        )
    )
    fig2.show(config={"displayModeBar": False, "showTips": False})
        # marker_size = 0.1 * df_temp['Deaths from HIV/AIDS in 100 thousand people'])

    return fig2

# %%
# here we define the functionality and interactivity of our App
# define input and output of callback function
@app.callback(
    # Output("choropleth", "figure"),
    Output("country_select", "value"),
    # Output("worm_container", "style"),
    Input("chloropleth", "clickData"),
    State("country_select", "value"))
# the callback function: called when a value of the defined inputs above changes.
def click_callback(clickData, country_select):
    # worm_style = {'display', 'block'}
    # if any countries are selected
    if(not clickData):
        raise PreventUpdate
    if(not country_select):
        selection = clickData["points"][0]["customdata"]
    else:
        # concatenate lists
        selection = country_select + clickData["points"][0]["customdata"]
        # remove duplicates
        selection = pd.Series(selection).unique()
    return selection


# %%
# Create a color vector for causes of death
# colorDf = pd.DataFrame()
# colorDf["column"] = df.iloc[0, 5:].index.values
# colorDf["color"] = pc.sample_colorscale("reds", colorDf["column"].size)

# here we define the functionality and interactivity of our App
# define input and output of callback function
@app.callback(
    Output("bar_chart", "figure"),
    Input("worm_figure", "hoverData"))# the callback function: called when a value of the defined inputs above changes.
def hover_bar_chart(hoverData):
    # worm_style = {'display', 'block'}
    # if any countries are selected
    if(not hoverData):
        raise PreventUpdate
    else:
        # return bar chart
        data_selection = df[(df["Year"] == hoverData["points"][0]["customdata"][1]) &
                            (df["Code"] == hoverData["points"][0]["customdata"][0])]
        subSelection = data_selection.iloc[0, 5:].sort_values(ascending=False).head(10)
        barFig = px.bar(
            x = subSelection.index.values,
            y = subSelection,
            color = subSelection.index.values,
            color_discrete_map= color_map_cause,
            title=("Top 10 causes of death in " +
                    str(hoverData["points"][0]["customdata"][1]) +
                    " in " +
                    hoverData["points"][0]["customdata"][2] +
                    " in Percent.")
        )
        barFig.update_layout(showlegend=False,
                            yaxis_title = "Percentage of total deaths",
                            xaxis_title = "Cause of death"
                            )
        barFig.update_yaxes(range=[0, 70])
        barFig.show(config={"displayModeBar": False, "showTips": False})

    return barFig


# %% [markdown]
# ## RUN APP Server

# %%
# run the local server
# visit http://127.0.0.1:8050/ in webbrowser to see results and error codes
app.run_server(debug=True)

# %% [markdown]
# Possible deployment:
# https://austinlasseter.medium.com/how-to-deploy-a-simple-plotly-dash-app-to-heroku-622a2216eb73 


