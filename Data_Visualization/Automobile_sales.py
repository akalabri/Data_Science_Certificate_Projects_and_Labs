import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"
app.config.suppress_callback_exceptions = True

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # Title
    html.H1('Automobile Sales Statistics Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

    # Dropdown for selecting statistics
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),

    # Dropdown for selecting a year
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select a year'
    )),

    # Output container for displaying graphs
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    ])
])


# Callback to enable or disable the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using a line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        average_sales = recession_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Year',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Average Vehicles Sold by Vehicle Type over Recession Period"
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type during Recessions"
            )
        )

        # Plot 4: Develop a Bar chart for the effect of the unemployment rate on vehicle type and sales
        unemployment_effect = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])[
            'Automobile_Sales'].sum().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemployment_effect,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title="Effect of Unemployment Rate on Vehicle Type and Sales during Recessions"
            )
        )

        # Return the plots for Recession Report Statistics
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]

    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using a line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales over the Whole Period"
            )
        )

        # Plot 2: Total Monthly Automobile sales using a line chart
        total_monthly_sales = data.groupby(['Year', 'Month'])['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                total_monthly_sales,
                x='Month',
                y='Automobile_Sales',
                color='Year',
                title="Total Monthly Automobile Sales by Year"
            )
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby(['Year', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Year',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title=f"Average Vehicles Sold by Vehicle Type in the year {input_year}"
            )
        )

        # Plot 4: Total Advertisement Expenditure for each vehicle using a pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f"Total Advertising Expenditure by Vehicle Type in the year {input_year}"
            )
        )

        # Return the plots for Yearly Report Statistics
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
        ]

    else:
        return None


# Run the Dash app
app.run_server(debug=True)
