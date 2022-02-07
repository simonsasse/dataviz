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
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math

# %% [markdown]
# ## import data

# %%
# read dataframe (preprocessed in main.ipynb)
df = pd.read_csv("data/merged_data_clean.csv").drop(columns = "Unnamed: 0")
df = df[df["Country"].isin(["Botswana", "Zimbabwe", "South Africa", "Ghana"])]
#df

# %% [markdown]
# ## Modify Data

# %%
# create lookup table for bar chart
iso3_countrynames = pd.DataFrame()
iso3_countrynames["Code"] = df["Code"].unique()
iso3_countrynames["Country"] = df["Country"].unique()
#iso3_countrynames

# %% [markdown]
# ## Load Geojson data

# %%
# source: https://public.opendatasoft.com/explore/dataset/country_shapes/export/ 
import geojson
with open("data/country_shapes.geojson") as f:
    gj = geojson.load(f)
gj.get

# %% [markdown]
# ## Color maps

# %%
country_zipper = zip(df["Country"].unique(), pc.sample_colorscale("turbo", df["Country"].unique().size))
color_map_country = dict(country_zipper)
cause_zipper = zip(df.iloc[0, 5:].index.values,  pc.sample_colorscale("greys", df.iloc[0, 5:].index.values.size))
color_map_cause = dict(cause_zipper)
# make HIV red
color_map_cause.update({" HIV/AIDS":'rgb(255, 0, 0)'})

# %%
#color_map_cause

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
config_dict = {"displayModeBar": False, "showTips": False, "scrollZoom": False, "showAxisDragHandles":False, "showAxisRangeEntryBoxes": False}

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
        colorbar_len=0.5,
        colorbar_title_side="right"
)
chloropleth.update_geos(fitbounds="locations", visible=False)
chloropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                             autosize = True,
                             legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="left",
                                x=0
                                )
                            )




# here we define the layout and components of our app
app.layout = html.Div([
    #  africa map container
    html.Div([
        html.H1("The impact of HIV on the life expectancy in Africa", style={'width':'100vw',
                                                                'height':'auto',
                                                                'textAlign': 'center',
                                                                'fontSize':'300%',
                                                                 'font-family':'sans-serif'
                                                                }), # heading
        html.Div([
            html.H3(
                "HIV and AIDS"
        , style={'font-family':'sans-serif'}),
        html.P(
            "AIDS is the final stage of an HIV infection and was first diagnosed in 1981. It is an immunodeficiency disease which is so far not curable. HIV is most commonly contracted through unprotected sexual intercourse and drug consumption. Many lack the necessary education and thus do not know exactly how to protect themselves from the infection. Due to the missing education and since the medical treatment only developed over time, the deaths caused by HIV and Aids in the past had an impact on the life expectancy in many countries. "
        , style={'font-family':'sans-serif'}),
        html.H3(
            "HIV spreading in Africa"
        , style={'font-family':'sans-serif'}),
        html.P(
            "On the right there is a map showing the African continent. The different colors represent the rate of HIV/Aids deaths in the selected year. By clicking the play button next to the timeline, an animation will start playing and the change of the death rate over time can be seen. Hovering over the countries will show some additional information. By clicking on a specific country, two graphs will show underneath the map.",
           style={'font-family':'sans-serif'})
        ],
                style={
                    'margin':10,
                    'width': '25vw',
                    'height': '85vh',
                    'display':'inline-block',
                    'fontSize':'100%',
                    'padding':10,
                    'verticalAlign':'middle',
                    'font-family':'sans-serif'
            }
        ),
        dcc.Graph(id="chloropleth", config=config_dict,
                                    figure=chloropleth, style={'width': '70vw',
                                                                    'height': '85vh',
                                                                    'display':'inline-block',
                                                                    'verticalAlign':'top',
                                                                    'right':0 }) # africa map figure with id "chloropleth"
    ], style={
        'width': '100vw',
        'height':'auto',
        'margin':'20px',
        'verticalAlign':'top'}),
    html.Div([
        html.H3(
            "HIV and the impact on life expectancy in Africa"
        , style={'font-family':'sans-serif'}),
        html.P(
            "The left chart shows a bubble chart. In the graph, the y-axis describes the life expectancy and the x-axis represents the year. The bubble size represents the deaths caused by HIV/Aids in the chosen country over time. By hovering over the dots, the exact death rate can be seen. Another country can be added by clicking on it on the map above or via the drop-down menu. This way, multiple countries can be compared. By hovering over the bubbles, the bar chart on the right changes according to year and country. It shows the top ten shares of death in the selected country of the year of the bubble. The red bar represents the share of deaths caused by HIV/Aids."
        , style={'font-family':'sans-serif'})
    ], style={
        'height':'auto',
        'width':'70vw',
        'font-family':'sans-serif',
        'fontSize':'100%',
        'margin':10,
        'padding':30
    }),
    # dropdown for country selection
    html.Div([
            # graph (later for the wormgraph)
            html.Div([
                    html.Div(dcc.Dropdown(
                            id='country_select',
                            options=[{'label': code, 'value': country} for index, country, code in iso3_countrynames.itertuples()],
                            multi=True,
                            placeholder="Select one or more Countries",
                        ), style={
                            'margin':'20px',
                            'height': 'auto',
                            'width': '45vw'
                        }),
                    dcc.Graph(id="worm_figure", style={
                                                    'margin': '20px 20px 20px 20px',
                                                    'display': 'inline-block',
                                                    'height':'70vh',
                                                    'width':'45vw'},
                                                    config=config_dict),
                    dcc.Graph(id="bar_chart", style={
                                                    'margin': '20px 20px 20px 20px',
                                                    'display': 'inline-block',
                                                    'height':'70vh',
                                                    'width':'45vw'},
                                                    config=config_dict)]),
                    dcc.Link("The code, Project Documentation and Data.[↗]",
                    href="https://github.com/simonsasse/dataviz",
                    target="_blank",
                    style={
                        'padding':5
                    })
                    ], style={'width':'100vw',
                            'height':'auto',
                            'padding':'0px',
                            'margin':'10px'})
    ], id="main-window",
    style={
        'height':'auto',
        'width':'100vw',
        'font-family':'sans-serif'
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
    fig2 = px.scatter(
                            df_temp,
                            x="Year",
                            y="Life expectancy",
                            color="Country",
                            color_discrete_map= color_map_country,
                            # hover_name=df_temp["Year"].astype(str)+ " " + df_temp["Country"],
                            # hover_data={"Deaths from HIV/AIDS in 100 thousand people" : ":.1f",
                            #             "Life expectancy": ":.1f",
                            #             "Code":False,
                            #             "Year":False,
                            #             "Country":False},
                            custom_data=["Code","Year","Country","Deaths from HIV/AIDS in 100 thousand people"],
                            size = [math.ceil(i/df["Deaths from HIV/AIDS in 100 thousand people"].max()*30) for i in df_temp['Deaths from HIV/AIDS in 100 thousand people']],
                            size_max = df["Deaths from HIV/AIDS in 100 thousand people"].max()/30
                            )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="left",
                                x=0
                            ), 
                        yaxis_title="Life expectancy in years")
    fig2.update_traces(
        marker=dict(sizemin=1),
        hovertemplate='<b>%{x} %{customdata[2]}</b><br>Life expectancy: <b>%{y:.1f} years</b><br>Deaths from HIV per 100,000 population: <b>%{customdata[3]:.1f}<br>'
        )
    fig2.add_annotation(text="The HIV/AIDS death rate per 100,000 population is displayed as the Bubble size.",
                xref="paper", yref="paper",
                x=0, y=0.95, showarrow=False,
                font=dict(
                        family="sans-serif",
                        size=14,
                        color="#000000"
                    ),
                    borderpad=5,
                    bgcolor="#ffffff"
                )
    fig2.update_yaxes(range=[df["Life expectancy"].min()-3, df["Life expectancy"].max()+3])
    
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
            y = subSelection.index.values,
            x = subSelection,
            orientation="h",
            color = subSelection.index.values,
            color_discrete_map= color_map_cause,
            title=("Top 10 causes of death in <b>" +
                    str(hoverData["points"][0]["customdata"][1]) +
                    "</b> in <b>" +
                    hoverData["points"][0]["customdata"][2] +
                    "</b> in Percent.")
            )
        barFig.update_layout(showlegend=False,
                            xaxis_title = "Percentage of total deaths",
                            yaxis_title = "Cause of death"
                            )
        barFig.update_traces(
            hovertemplate='<b>%{x:.1f} Percent',
            name = ""
        )
        barFig.update_xaxes(range=[0, 60])

    return barFig


# %% [markdown]
# ## RUN APP Server

# %%


# %%
# run the local server
# visit http://127.0.0.1:8050/ in webbrowser to see results and error codes
app.run_server(debug=True)

# %% [markdown]
# Possible deployment:
# https://austinlasseter.medium.com/how-to-deploy-a-simple-plotly-dash-app-to-heroku-622a2216eb73 


