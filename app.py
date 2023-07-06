import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots


file = "./output.csv"

def inflation_reader(file):
    df = pd.read_csv(file)
    return df

df = inflation_reader(file)
#Visualization functions

def create_line_plot(df, x_col, y_col, title, x_label, y_label): #Basic line plots to assess normality 
    fig = go.Figure(data=[go.Scatter(x=df[x_col], y=df[y_col])])
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    return fig

def create_histogram(df, column, title, x_label, y_label): #Basic histograms to assess normality 
    fig = go.Figure(data=[go.Histogram(x=df[column])])
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    return fig

def create_plot_against_cpi(df, x_col, y_col): #Plotting specific crime metrics against inflation to assess trends 
    sorted_df = df.sort_values(by=x_col)
    
    fig = go.Figure()

    fig.add_shape(type="line", 
                  x0=sorted_df[x_col].min(), y0=sorted_df[y_col].min(), 
                  x1=sorted_df[x_col].max(), y1=sorted_df[y_col].min(),
                  line=dict(color="Gray", width=2))

    fig.add_trace(go.Scatter(x=sorted_df[x_col], y=sorted_df[y_col], mode='lines'))

    fig.update_layout(title=f'{y_col} Over {x_col}',
                      xaxis_title=x_col,
                      yaxis_title=y_col)

    return fig   

def calculate_cpi_correlations(df):
    # Calculate correlations
    correlations = df[['CPI', 'Violent', 'Property', 'Murder', 'Rape', 'Robbery', 'assault', 'Burglary', 'Larceny theft', 'Vehicle theft']].corr()

    # Filter only correlations with CPI
    cpi_correlations = correlations['CPI'].round(4)

    return cpi_correlations

def create_cpi_correlation_plot(cpi_correlations):
    # Create a bar plot of the correlations
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'limegreen', 'cadetblue', 'darkred', 'cyan', 'orangered']

    fig = go.Figure(data=[go.Bar(
        x=cpi_correlations.index[1:],  # Exclude the 'CPI' from the x-axis (it's the first entry)
        y=cpi_correlations.values[1:],  # Exclude the correlation of 'CPI' with itself from the y-axis (it's the first entry)
        text=cpi_correlations.values[1:],  # Same here for the text
        textposition='auto',
        marker_color = colors
    )])
    fig.update_layout(title_text='Correlations between CPI and Crime Types')
    
    return fig


# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown options
dropdown_options = [
    {'label': 'Consumer Price Index Change', 'value': 'CPI'},
    {'label': 'Property Crime Over Time', 'value': 'Property'},
    {'label': 'Murder Over Time', 'value': 'Murder'},
    {'label': 'Violent Crime Over Time', 'value': 'Violent'},
    {'label': 'Burglary Over Time', 'value': 'Burglary'},
    {'label': 'Total Crime Over Time', 'value': 'Total'},
    {'label': 'Distribution of Consumer Price Index', 'value': 'CPI_hist'},
    {'label': 'Distribution of Property Crime Incidents', 'value': 'Property_hist'},
    {'label': 'Distribution of Violent Crime Incidents', 'value': 'Violent_Crime_hist'},
    {'label': 'Distribution of Burglary Incidents', 'value': 'Burglary_hist'},
    {'label': 'Distribution of Total Crime Incidents', 'value': 'Total_hist'},
    # {'label': 'Crime Percentage against Inflation Rate', 'value': 'crime_inf'},
    # {'label': 'Property Crime against Inflation Rate', 'value': 'property_inf'},
    # {'label': 'Crime Percentage against Inflation Rate', 'value': 'crime_percentage_inf'},
    # {'label': 'Robbery against Inflation Rate', 'value': 'robbery_inf'}

    {'label': 'Violent Crime against CPI', 'value': 'Violent_CPI'},
    {'label': 'Property Crime against CPI', 'value': 'Property_CPI'},
    {'label': 'Murder Crime against CPI', 'value': 'Murder_CPI'},
    {'label': 'Rape Crime against CPI', 'value': 'Rape_CPI'},
    {'label': 'Robbery Crime against CPI', 'value': 'Robbery_CPI'},
    {'label': 'Assault Crime against CPI', 'value': 'Assault_CPI'},
    {'label': 'Burglary Crime against CPI', 'value': 'Burglary_CPI'},
    {'label': 'Larceny Theft Crime against CPI', 'value': 'Larceny_Theft_CPI'},
    {'label': 'Vehicle Theft Crime against CPI', 'value': 'Vehicle_Theft_CPI'},
    {'label': 'Correlations between CPI and Crime Types', 'value': 'CPI_correlations'}
]




# Create the Dash app layout
app.layout = html.Div([
    html.H1('Crime and Inflation Dashboard'),
    html.Div([
        html.H3('Select Visualization:'),
        dcc.Dropdown(
            id='visualization-dropdown',
            options=dropdown_options,
            value=dropdown_options[0]['value'],
            clearable=False
        )
    ]),
    html.Div(id='visualization-output')
])

# Define the callback for updating the visualization output
@app.callback(Output('visualization-output', 'children'),
              [Input('visualization-dropdown', 'value')])
def update_visualization(value):
    if value == 'CPI':
        fig = create_line_plot(df, 'Date', 'CPI', 'Consumer Price Index Change', 'Year', 'CPI')
    elif value == 'Property':
        fig = create_line_plot(df, 'Date', 'Property', 'Property Crime Over Time', 'Year', 'Number of Property Incidents')
    elif value == 'Murder':
        fig = create_line_plot(df, 'Date', 'Murder', 'Murder Over Time', 'Year', 'Number of Murder Incidents')
    elif value == 'Violent':
        fig = create_line_plot(df, 'Date', 'Violent', 'Violent Crime Over Time', 'Year', 'Number of Violent Incidents')
    elif value == 'Burglary':
        fig = create_line_plot(df, 'Date', 'Burglary', 'Burglary Over Time', 'Year', 'Total Number of Burglary Incidents')
    elif value == 'Total':
        fig = create_line_plot(df, 'Date', 'Total', 'Total Crime Over Time', 'Year', 'Total Number of Incidents')
    elif value == 'CPI_hist':
        fig = create_histogram(df, 'CPI', 'Distribution of Consumer Price Index', 'CPI', 'Count')
    elif value == 'Property_hist':
        fig = create_histogram(df, 'Property', 'Distribution of Property Crime Incidents', 'Number of Property Incidents', 'Count')

    elif value == "Murder_hist":
        fig = create_histogram(df, 'Property', 'Distribution of Property Crime Incidents', 'Number of Property Incidents', 'Count')
    
    elif value == "Violent_Crime_hist":
        fig = create_histogram(df, 'Date', 'Violent', 'Violent Crime Over Time', 'Year', 'Number of Violent Incidents')

    elif value == "Burglary_hist":
        fig = create_histogram(df, 'Date', 'Burglary', 'Burglary Over Time', 'Year', 'Total Number of Burglary Incidents')

    elif value == "Total_hist":
        fig = create_histogram(df, 'Date', 'Total', 'Total Crime Over Time', 'Year', 'Total Number of Incidents')

    elif value == 'Violent_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Violent')
    elif value == 'Property_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Property')
    elif value == 'Murder_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Murder')
    elif value == 'Rape_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Rape')
    elif value == 'Robbery_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Robbery')
    elif value == 'Assault_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'assault')
    elif value == 'Burglary_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Burglary')
    elif value == 'Larceny_Theft_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Larceny theft')
    elif value == 'Vehicle_Theft_CPI':
        fig = create_plot_against_cpi(df, 'CPI', 'Vehicle theft')

    elif value == 'CPI_correlations':
        cpi_correlations = calculate_cpi_correlations(df)
        fig = create_cpi_correlation_plot(cpi_correlations)

    return dcc.Graph(figure=fig)

def create_crime_percentage_plot(df, inf_rate, crime_percentage):
    sorted_df = df.sort_values(by=inf_rate)  # Sort DataFrame by the inf_rate column
    
    fig = go.Figure()

    # Add horizontal line trace at min crime_percentage
    fig.add_shape(type="line", 
                  x0=sorted_df[inf_rate].min(), y0=sorted_df[crime_percentage].min(), 
                  x1=sorted_df[inf_rate].max(), y1=sorted_df[crime_percentage].min(),
                  line=dict(color="Gray", width=2))

    # Add line trace
    fig.add_trace(go.Scatter(x=sorted_df[inf_rate], y=sorted_df[crime_percentage], mode='lines'))

    fig.update_layout(title='Crime Percentage Over Inflation Rate',
                      xaxis_title='Inflation Rate',
                      yaxis_title='Crime Percentage')

    return fig

fig = create_crime_percentage_plot(df, 'CPI', 'CrimePercentage')  # Here replace 'inf_rate' and 'crime_percentage' with your column names
fig.show()
# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
