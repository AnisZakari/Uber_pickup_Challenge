import dash
import numpy as np
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly
from plotly.graph_objs import Scattermapbox
import  plotly.graph_objs as go
from app import server

app = dash.Dash(__name__)
server = app.server


# let's create a function to filter data by day and hour given a month
# We also add a remove_outliers function that will be usefull later. 

#def select_date_time(df, month, day, hour, remove_outliers = False):
'''   
    if remove_outliers:
        mask = (df['month'] == month) & (df['day_name'] == day) & (df['hour'] == hour) \
                                      & (df['labels'] != -1)
    else:
        mask = (df['month'] == month) & (df['day_name'] == day) & (df['hour'] == hour)
       
    
    return df[mask]
'''
#let's create a function to select data and that plot it on a map

def select_data_and_plot(month, day, hour):
    
#Preprocessing 

    #We filter on the desired month, day, and hour and we remove outliers
    #data = select_date_time(df, month, day, hour, remove_outliers = True)
    #We get centers coordinates of each cluster
    cluster_centers = centers_info_dataset.loc[(centers_info_dataset['month'] == month) &
                                                (centers_info_dataset['day_name'] == day) &
                                                (centers_info_dataset['hour'] == hour)
                                               ,:]


    #Plotly Token to have access to maps
    mapbox_access_token = 'pk.eyJ1IjoiYW5pc3pha2FyaSIsImEiOiJja2k4MG4xZW0wMTZwMnFwanVvdG5sMWpqIn0.MGKzhSzS6zaZRQM14fAPcQ'
    fig = go.Figure()

    '''
    #Display dots for a given month
    fig.add_trace(go.Scattermapbox(
            lat = data['Lat'],
            lon = data['Lon'],
            mode = 'markers',
            showlegend = False,
            marker = dict(
                size = 6,
                color = data['labels'],
                colorscale = 'Blugrn',
                opacity = 0.6
            )
        )) 
    #This is just a trick to display outlines for the dots (we create the same dots but bigger in the background, see size) 
    fig.add_trace(go.Scattermapbox(
            lat = data['Lat'],
            lon = data['Lon'],
            name = 'Position of potential clients (whole month)',
            mode = 'markers',
            marker = dict(
                size = 7,
                color = 'blue',
                opacity = 0.7
            )
        )) 
    '''

    #Red bubles with average number of people in a give month  
    fig.add_trace(go.Scattermapbox(
            lat = cluster_centers['Lat'],
            lon = cluster_centers['Lon'],
            mode = 'markers+text',
            name = 'Average number of potential clients for the selected hour (for a selected day of the week, on a given month)',
            textposition = 'middle center',
            text = [str(n) for n in cluster_centers['number_of_people/day_average']], #It displays average number of people for a given hour, a given day, in a given month
            textfont = dict( color = 'white', family = 'Calibri', size = 14),
            marker = dict(
                size = np.log(cluster_centers['number_of_people/day_average'])*20, #We use log so that the difference in size is not extreme between 2 Bubbles
    #            color ='rgb(51, 53, 255)',
                color = 'rgb(255, 0, 0)',
    #           color = 'rgb(102, 204, 0)',
                opacity=0.6,
            ),
            hoverinfo='none'
            
        ))


    fig.update_layout(
            title = dict(text = 'Hot Zones based on uber data', x = 0.5),
            font = dict(family='Tw Cen MT, monospace', size=24, color='rgb(0,0,0)'),
            autosize = True,
            hovermode = 'closest',
            showlegend=True,
            width=1000,
            height=700,
            legend=dict(yanchor="top", y=0.00005,xanchor="center",x=0.5,
                        borderwidth = 1,
                        font = dict (family="Courier", size=12, color="black")
                       ),

            mapbox=dict(
                accesstoken = mapbox_access_token,
                center = dict(lat = centers_info_dataset['Lat'].mean() , lon = centers_info_dataset['Lon'].mean()),
                bearing = 0,
                pitch = 0,
                zoom = 9.8,
    #            style = 'outdoors'
    #            style = 'dark'
    #            style = 'light'
                style = 'streets'
            ),
        )                    


    return fig


# Load CSV with Pandas.
centers_info_dataset = pd.read_csv('centers_info_dataset.csv')
#labeled_data = pd.read_csv('labeled_data_le.csv')
#month_list = labeled_data['month'].unique()
#day_list = labeled_data['day_name'].unique()
month_list = centers_info_dataset['month'].unique()
day_list = centers_info_dataset['day_name'].unique()
decoder = pd.DataFrame(['April', 'May', 'June', 'July', 'August', 'September'], index = [4, 5, 6, 7, 8, 9])

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Find Clusters of Uber Clients"),


    html.Div(id="select-date-div"),

    html.Div(children = html.P(children="""
        Select an hour.
    """)),

   dcc.RadioItems(
        id="select-hour",
        options=[{"label": hour, "value": hour} for hour in range(24)],
        value = 18,
        labelStyle={'display': 'inline-block'}
    ),

    html.Div(children = html.P(children="""
        Select a month.
    """)),

   dcc.RadioItems(
        id="select-month",
        options=[{"label": month, "value": month} for month in month_list],
        value=month_list[0],
        labelStyle={'display': 'inline-block'}
    ),

    html.Div(children = html.P(children="""
        Select a day.
    """)),

   dcc.RadioItems(
        id="select-day",
        options=[{"label": month, "value": month} for month in day_list],
        value=day_list[-1],
        labelStyle={'display': 'inline-block'}
    ),

    # Call our function which return a graph.
    dcc.Graph(
        id="uber_graph",
        figure = select_data_and_plot(0 , 'Monday', 18)
    ),
    


])


@app.callback(

    dash.dependencies.Output("select-date-div", "children"),

    dash.dependencies.Input("select-hour", "value"),
    dash.dependencies.Input("select-month", "value"),
    dash.dependencies.Input("select-day", "value")   
    )
def display_date(hour, month, day):
    # We return an H3 HTML with date settings
    #to_write = 'Where are uber clients on a typical '  + day + 'of ' + month + 'at ' + hour + '?'
    to_write = 'Where are uber clients on a typical ', day, ' of ',  str(decoder.loc[month][0]), ' at ', hour, ' h, in New York ?'
    return html.H3(children = to_write)

@app.callback(
    dash.dependencies.Output("uber_graph", "figure"),
    dash.dependencies.Input("select-hour", "value"),
    dash.dependencies.Input("select-month", "value"),
    dash.dependencies.Input("select-day", "value")
    )
def generate_stats(selected_hour, selected_month, selected_day):
    fig = select_data_and_plot(selected_month, selected_day, selected_hour)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)