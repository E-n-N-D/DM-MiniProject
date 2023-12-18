import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('spotify_songs.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("Spotify Songs Dashboard"),
    
    # Bar graph for total number of songs in each playlist
    dcc.Graph(id='playlist-bar-graph'),
    
    
    # Dropdown for filtering data
    dcc.Dropdown(
        id='filter-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='playlist_name',
        style={'width': '50%'}
    ),
    
    # Line graph for danceability vs energy
    dcc.Graph(id='danceability-energy-line-graph'),
    
    # Scatter plot for selected attributes
    dcc.Graph(id='scatter-plot'),
    
    # Dropdown for selecting genre or subgenre
    dcc.Dropdown(
        id='genre-subgenre-dropdown',
        options=[
            {'label': 'Playlist Genre', 'value': 'playlist_genre'},
            {'label': 'Playlist Subgenre', 'value': 'playlist_subgenre'}
        ],
        value='playlist_genre',
        style={'width': '50%'}
    ),
    
    # Pie chart for total number of songs by each genre or subgenre
    dcc.Graph(id='genre-subgenre-pie-chart'),
    
    html.Div([
        html.P(f"Most Popular Song: {df.loc[df['track_popularity'].idxmax(), 'track_name']}"),
        html.P(f"Least Popular Song: {df.loc[df['track_popularity'].idxmin(), 'track_name']}")
    ]),

     html.Div([
        html.P(f"Songs with Highest Duration: {df.loc[df['duration_ms'].idxmax(), 'track_name']}"),
        html.P(f"Songs with Least Duration: {df.loc[df['duration_ms'].idxmin(), 'track_name']}")
    ]),


])


# Callback for updating bar graph based on selected column
@app.callback(
    Output('playlist-bar-graph', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_bar_graph(selected_column):
    playlist_counts = df[selected_column].value_counts()
    bar_fig = px.bar(playlist_counts, x=playlist_counts.index, y=playlist_counts.values, labels={selected_column: 'Playlist Name', 'index': 'Count'}, title='Total Number of Songs in Each Playlist')
    return bar_fig

# Callback for updating line graph based on danceability and energy
@app.callback(
    Output('danceability-energy-line-graph', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_line_graph(selected_column):
    line_fig = px.scatter(df, x='danceability', y='energy', title='Danceability vs Energy')
    return line_fig

# Callback for updating scatter plot based on selected attributes
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('filter-dropdown', 'value')]
)
def update_scatter_plot(selected_column):
    scatter_fig = px.scatter(df, x='danceability', y='energy', title='Scatter Plot', color=selected_column)
    return scatter_fig

# Callback for updating pie chart based on genre or subgenre
@app.callback(
    Output('genre-subgenre-pie-chart', 'figure'),
    [Input('genre-subgenre-dropdown', 'value')]
)




def update_genre_subgenre_pie_chart(selected_column):
    counts = df[selected_column].value_counts()
    pie_fig = px.pie(counts, values=counts.values, names=counts.index, title=f'Total Number of Songs by Each {selected_column.capitalize()}')
    return pie_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
