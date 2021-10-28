import requests

class MyAPI:
    def __init__(self, config) -> None:
        self.host_url = config['host']

    def _get_water_level(self):
        pass

    def request_data(url):
    """
    Send request data and convert format
    """
    data = requests.get(url).json()
    
    
    for location in data.keys():
        date_row = list(data[location].keys())
        value_col = list(data[location].value())

    df = pd.DataFrame(list(zip(date_row, value_col)),
               columns =['Date', 'Value'])

    # Vincent chart
    line_chart = vincent.Line(df, width=600, height=300)
    line_chart.axis_titles(x='Date', y='Value')
    line_chart.legend(title='Water Level by Date')

    # Convert it to JSON.
    scatter_json = line_chart.to_json()
    return scatter_json