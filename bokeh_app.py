import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from bokeh.models import ColumnDataSource
from sklearn.preprocessing import MinMaxScaler
from uszipcode import Zipcode
from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)


result = pd.read_csv('Data Cleaning.csv')

# Fill NAs in From Zip Code with 00000 and change to int type

result['FromZipCode'] = result['FromZipCode'].fillna('00000')
result['FromZipCode'] = result['FromZipCode'].astype(int)

result['ShipToZipCode'] = result['ShipToZipCode'].fillna('00000')
result['ShipToZipCode'] = result['ShipToZipCode'].astype(int)

# Pad 0 to zipcode

zipcode_col = ['FromZipCode', 'ShipToZipCode', 'FinalLocationZipCode']
for col in zipcode_col:
    result[col] = result[col].astype(str).str.zfill(5)
    

# Change to datetime type and find min and max date in dataset

result['TheDate'] = pd.to_datetime(result['TheDate'], format='%m/%d/%Y')

min_date1 = result['TheDate'].min()
max_date1 = result['TheDate'].max()


# All physical store location

store_zip = result['FromZipCode'].unique().tolist()


# Function to find all of neigbor zipcode within x miles (input list)

from pyzipcode import ZipCodeDatabase # pip install pyzipcode3

def find_neighbors_list(store_zip, radius = 5):
    zcdb = ZipCodeDatabase()

    in_radius = []

    for sz in store_zip:
            for neighbors in zcdb.get_zipcodes_around_radius(sz, radius):
                in_radius.append(neighbors.zip)
    
    zipcode_reach = list(set(in_radius)) # remove dupplicate zipcode
    return(zipcode_reach)
    
    
# Function to find all of neigbor zipcode within x miles MINUS REACH OF PHYSICAL STORE (input str)

def find_neighbors_str(store_zip1, radius = 5):
    zcdb = ZipCodeDatabase()

    in_radius = []

    for neighbors in zcdb.get_zipcodes_around_radius(store_zip1, radius):
        in_radius.append(neighbors.zip)
    
    zipcode_reach2 = find_neighbors_list(store_zip, radius = radius)
    
    return(list(set(in_radius).difference(set(zipcode_reach2))))
    
    
# Create a table with all Latititude, Longitude, major_city and state from a list of zipcode

def table_from_zipcodelist(listzip):
    lat = []
    lng = []
    city = []
    state = []
    
    for x in listzip:
        zipcode = search.by_zipcode(x)
        zipcode =zipcode.to_dict()
    
        lat.append(zipcode['lat'])
        lng.append(zipcode['lng'])
        city.append(zipcode['major_city'])
        state.append(zipcode['state'])
        
    store_zip_df = pd.DataFrame({'store_zip': listzip, 'lat': lat, 'lng': lng, 'in_city': city, 'in_state': state})
    
    return store_zip_df



# Function to create existing stores info

def create_store_now(state_choose = 'MA'):
    lat = []
    lng = []
    city = []
    state = []
    
    for x in store_zip:
        zipcode = search.by_zipcode(x)
        zipcode =zipcode.to_dict()
    
        lat.append(zipcode['lat'])
        lng.append(zipcode['lng'])
        city.append(zipcode['major_city'])
        state.append(zipcode['state'])
        
    store_zip_df = pd.DataFrame({'store_zip': store_zip, 'lat': lat, 'lng': lng, 'in_city': city, 'in_state': state})
    store_zip_df = store_zip_df[store_zip_df['in_state'] == state_choose]

    return ColumnDataSource(store_zip_df)


# Function to create predict stores info

def create_store_future(state_choose = 'MA', radius = 5, Number = 0, tran_type = ['Sale', 'Return'], min_date=min_date1, max_date=max_date1):
    zip_dict = {}
    
    sea_zipcode = result['ShipToZipCode'][result['State'] == state_choose].unique().tolist()
    
    try:
        sea_zipcode.remove('00000')
    except:
        pass
    
    zipcode_reach2 = find_neighbors_list(store_zip, radius = radius)
    
    # add more parameter here
    ecom_filter = result[(result['TransactionType'].isin(tran_type)) & (result['TheDate'] >= min_date) & (result['TheDate'] <= max_date)][['ShipToZipCode', 'Transactions']].groupby('ShipToZipCode').sum()

        
    try:
        for i in sea_zipcode:
            zcdb = ZipCodeDatabase()
            in_radius = []
            for neighbors in zcdb.get_zipcodes_around_radius(i, radius):
                in_radius.append(neighbors.zip)
            zipcode_reach_search = list(set(in_radius).difference(set(zipcode_reach2)))   
            zip_dict[i] = ecom_filter[ecom_filter.index.isin(zipcode_reach_search)]['Transactions'].sum()
    except:
        pass
    
    predict1 = pd.DataFrame.from_dict(zip_dict, orient = 'index', columns = ['Transactions']).sort_values('Transactions', ascending = False)
    
    store_future_zip = [predict1.index[Number]]

    store_future = table_from_zipcodelist(list(store_future_zip))

    store_future['Transactions'] = predict1['Transactions'][Number]
    
    return ColumnDataSource(store_future)



# Function to create data table source for all predict stores in a state

def create_data_table(state_choose = 'MA', radius = 5, Number = 0, tran_type = ['Sale', 'Return'], min_date=min_date1, max_date=max_date1):
    zip_dict = {}
    
    sea_zipcode = result['ShipToZipCode'][result['State'] == state_choose].unique().tolist()
    
    try:
        sea_zipcode.remove('00000')
    except:
        pass
    
    zipcode_reach2 = find_neighbors_list(store_zip, radius = radius)
    
    # add more parameter here
    ecom_filter = result[(result['TransactionType'].isin(tran_type)) & (result['TheDate'] >= min_date) & (result['TheDate'] <= max_date)][['ShipToZipCode', 'Transactions']].groupby('ShipToZipCode').sum()

        
    try:
        for i in sea_zipcode:
            zcdb = ZipCodeDatabase()
            in_radius = []
            for neighbors in zcdb.get_zipcodes_around_radius(i, radius):
                in_radius.append(neighbors.zip)
            zipcode_reach_search = list(set(in_radius).difference(set(zipcode_reach2)))   
            zip_dict[i] = ecom_filter[ecom_filter.index.isin(zipcode_reach_search)]['Transactions'].sum()
    except:
        pass
    
    predict1 = pd.DataFrame.from_dict(zip_dict, orient = 'index', columns = ['Transactions']).sort_values('Transactions', ascending = False)
    
    store_future_zip = predict1.index

    store_future = table_from_zipcodelist(list(store_future_zip))

    store_future['Transactions'] = predict1['Transactions'].tolist()
    
    return ColumnDataSource(store_future)


# Function to create ecommerce info in 1 state and categorize ecommerce transaction type: Unreached, Reached or Future Reach

def create_ecom_zipcode_all(state_choose = 'MA', radius = 5, tran_type = ['Sale', 'Return'], min_date=min_date1, max_date=max_date1, Number = 0):
    
    future_neighbor = find_neighbors_str(create_store_future(state_choose = state_choose, radius = radius, tran_type = tran_type, min_date = min_date, max_date = max_date, Number = Number).data['store_zip'][0], radius = radius)
    
    sea_zipcode_init = result['ShipToZipCode'][result['State'] == state_choose].unique().tolist()
    
    try:
        sea_zipcode_init.remove('00000')
    except:
        pass
    
    sea_zipcode = list(set(future_neighbor).union(set(sea_zipcode_init)))
    
    ecom_zipcode = table_from_zipcodelist(sea_zipcode)
    
    zipcode_reach3 = find_neighbors_list(store_zip, radius = radius)
    
    ecom_zipcode['inrange'] = 'Unreached'

    ecom_zipcode['inrange'][ecom_zipcode['store_zip'].isin(zipcode_reach3)] = 'Reached'
    
    # Add parameter here 2
    ecom_zipcode['inrange'][ecom_zipcode['store_zip'].isin(future_neighbor)] = 'Future Reach'
    
    # Add parameter here 1
    sum_by_shiptozipcode_all = result[(result['TransactionType'].isin(tran_type)) & (result['TheDate'] >= min_date) & (result['TheDate'] <= max_date)][['ShipToZipCode', 'Transactions']].groupby('ShipToZipCode').sum()
    
    sum_by_shiptozipcode = sum_by_shiptozipcode_all[sum_by_shiptozipcode_all.index.isin(sea_zipcode)].reset_index()
    
    # Join ecom_zipcode with sum_by_shiptozipcode
    ecom_zipcode_all = pd.merge(ecom_zipcode, sum_by_shiptozipcode, left_on = 'store_zip', right_on = 'ShipToZipCode')
    
    
    ecom_zipcode_all = ecom_zipcode_all[ecom_zipcode_all['store_zip'] != '00000']
    
    scaler = MinMaxScaler(feature_range = (5,15))

    ecom_zipcode_all['Size'] = scaler.fit_transform(ecom_zipcode_all['Transactions'].values.reshape(-1,1))
    
    return ColumnDataSource(ecom_zipcode_all)



# Function to make plot for tab1

def make_plot(store_now, store_future, ecom_zipcode_all):
    # Source: http://www.bigendiandata.com/2017-06-27-Mapping_in_Jupyter/

    from bokeh.io import output_file, output_notebook, show
    from bokeh.models import GMapOptions, ColumnDataSource, CategoricalColorMapper, HoverTool, LassoSelectTool
    from bokeh.palettes import RdBu3
    from bokeh.plotting import gmap


    map_options = GMapOptions(lat=42.37, lng=-71.23, map_type="roadmap", zoom=10)

    plot = gmap(map_options=map_options, google_api_key='AIzaSyCrnuAv4K0j80AZzUsYFS2NwyY49-yMXRI',plot_width=780, plot_height=780, output_backend="webgl")
    plot.title.text = "PUMA Retail Store and Ecommerce Transactions"

    mapper = CategoricalColorMapper(factors=['Unreached', 'Reached', 'Future Reach'], 
                                    palette=[RdBu3[1], RdBu3[0], RdBu3[2]])

    plot1 = plot.square(x="lng", y="lat", size = 20, color = 'blue', source = store_now)
    plot2 = plot.square(x="lng", y="lat", size = 20, color = 'red', source = store_future)
    plot3 = plot.circle(x="lng", y="lat", size = 'Size', fill_color={'field': 'inrange','transform': mapper}, source = ecom_zipcode_all, legend = 'inrange')

    
    tooltips1 = [
        ("Ship To ZipCode", "@store_zip"),
        ("Ship To City","@in_city"),
        ('Ecom Transactions', '@Transactions')
    ]
    plot.add_tools(HoverTool(tooltips=tooltips1, renderers = [plot3]))

    tooltips3 = [
        ("Store ZipCode", "@store_zip"),
        ("City located","@in_city"),
        ('Ecom Transactions in range', '@Transactions')
    ]
    plot.add_tools(HoverTool(tooltips=tooltips3, renderers = [plot2]))
    
    plot.add_tools(LassoSelectTool())
    
    return plot



# Function to make data table from data table source

def make_data_table(data_table_source, option):
    
    from bokeh.models.widgets import DataTable, TableColumn
    
    if option == 'data_table1':
        
        columns = [
            TableColumn(field="store_zip", title="Future Store ZipCode"),
            TableColumn(field="lat", title="Latitude"),
            TableColumn(field="lng", title="Longitude"),
            TableColumn(field="in_city", title="City"),
            TableColumn(field="in_state", title="State"),
            TableColumn(field="Transactions", title="Total Transactions within x miles")
        ]
    
    if option == 'data_table2':
        
        columns = [
            TableColumn(field="store_zip", title="Ecommerce ZipCode"),
            TableColumn(field="lat", title="Latitude"),
            TableColumn(field="lng", title="Longitude"),
            TableColumn(field="in_city", title="City"),
            TableColumn(field="in_state", title="State"),
            TableColumn(field="Transactions", title="Transactions"),
            TableColumn(field="inrange", title="In Range")
        ]
        
    data_table = DataTable(source=data_table_source, columns=columns, width=1000, height=750)
    
    return data_table


# Function to update attributes

def update(attr, old, new):
    state_plot = state_choose.value
    trantype_to_plot = [tran_type_select.labels[i] for i in tran_type_select.active]
    
    new_store_now = create_store_now(state_choose = state_plot)
    new_store_future = create_store_future(state_choose = state_plot, radius = int(radius_select.value), tran_type = trantype_to_plot, min_date = min_date_select.value, max_date = max_date_select.value, Number = int(solution_select.value))
    new_ecom_zipcode_all = create_ecom_zipcode_all(state_choose = state_plot, radius = int(radius_select.value), tran_type = trantype_to_plot, min_date = min_date_select.value, max_date = max_date_select.value, Number = int(solution_select.value))
    new_data_table_source = create_data_table(state_choose = state_plot, radius = int(radius_select.value), tran_type = trantype_to_plot, min_date=min_date_select.value, max_date=max_date_select.value, Number = int(solution_select.value))
    
    data_table_source.data = new_data_table_source.data
    store_now.data = new_store_now.data
    store_future.data = new_store_future.data
    ecom_zipcode_all.data = new_ecom_zipcode_all.data
    
    
    
# Bokeh Widgets

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput, Slider, CheckboxGroup, DatePicker, DataTable, Div

state_choose = TextInput(value="MA", title="Choose State")
state_choose.on_change('value', update)


radius_select = TextInput(value = '5', title = 'Select Radius (Miles)')
radius_select.on_change('value', update)


solution_select = TextInput(value = '0', title = 'Select Solution')
solution_select.on_change('value', update)


tran_type_select = CheckboxGroup(labels=['Sale', 'Return'], active = [0, 1], name = 'Transaction Type')
tran_type_select.on_change('active', update)


min_date_select = DatePicker(title='Start Date',value=min_date1,min_date=min_date1,max_date=max_date1)
min_date_select.on_change('value', update)
max_date_select = DatePicker(title='End Date',value=max_date1,min_date=min_date1,max_date=max_date1)
max_date_select.on_change('value', update)

guideline = Div(text="""<center>
<h2>Dashboard Guideline</h2>
</center><center>
<h3>Purpose</h3>
</center>
<p style="margin-left: 25px;">This dashboard shows the best in-state location covering the most unreached PUMA ecommerce transactions, which are not in vicinity of a physical store.</p>
<center>
<h3>Parameters</h3>
</center>
<ol>
<li><strong>Choose State:</strong> Input state as abbreviation. Default state is MA.</li>
<li><strong>Select Radius (Miles): </strong>Coverage of a retail store with Ecommerce transactions. Intuitively, Countryside have higher radius than urban area because of population density and transportation access.</li>
<li><strong>Transaction Type: </strong>Checkbox to choose Sale or Return or both.</li>
<li><strong>Start &amp; End Date: </strong>Data will be aggregated between Start and End date.</li>
<li><strong>Select Solutions: </strong>Solution based on "#" column in "All Possible Locations" tab. Default solution is 0 for maximum Ecommere transactions.</li>
</ol>
<center>
<h3>Notes</h3>
</center>
<ol>
  <li>The dashboard runs really slow so please changing each parameters once at a time and be patient.</li>
  <li>Choosing different state will not change current view and you have to scroll to chosen state</li>
<li>If new store chosen is adjacent to the border of 2 state, Ecommerce transactions in nearby state within radius are included and shown in "All Online Transactions by ZipCode" tab. For example, a store in NYC can still attract online customers in Newark, NJ.</li>
<li>The dashboard can also identify best in-city location by sorting 'All possible locations' by 'city'</li>
<li>Some locations are not shown on map because coordinates for those ZipCode are missing. However, transactions are included and shown in 2 table tabs.</li>
<li>Choosing timeframe based on desirable season. For example, examining store location measurement for different year, different quarter</li>
</ol>
<footer>
<p>&nbsp;</p>
<address>Contact me at <a href="mailto:thanhhl95@gmail.com">thanhhl95@gmail.com</a></address></footer>""",
width=400, height=100)


# Initiate data

store_now = create_store_now(state_choose = 'MA')

store_future = create_store_future(state_choose = 'MA', radius = 5, tran_type = ['Sale', 'Return'],min_date=min_date1,max_date=max_date1, Number = 0)

ecom_zipcode_all = create_ecom_zipcode_all(state_choose = 'MA', radius = 5, tran_type = ['Sale', 'Return'],min_date=min_date1,max_date=max_date1, Number = 0)

data_table_source = create_data_table(state_choose = 'MA', radius = 5, Number = 0, tran_type = ['Sale', 'Return'], min_date=min_date1, max_date=max_date1)

data_table1 = make_data_table(data_table_source, option = 'data_table1')

data_table2 = make_data_table(ecom_zipcode_all, option = 'data_table2')

p = make_plot(store_now, store_future, ecom_zipcode_all)



# Download data column

from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button

button1 = Button(label="Download", button_type="success")
button2 = Button(label="Download", button_type="success")

javaScript="""
function table_to_csv(source) {
    const columns = Object.keys(source.data)
    const nrows = source.get_length()
    const lines = [columns.join(',')]

    for (let i = 0; i < nrows; i++) {
        let row = [];
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j]
            row.push(source.data[column][i].toString())
        }
        lines.push(row.join(','))
    }
    return lines.join('\\n').concat('\\n')
}


const filename = 'data_result.csv'
filetext = table_to_csv(source)
const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename)
} else {
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.target = '_blank'
    link.style.visibility = 'hidden'
    link.dispatchEvent(new MouseEvent('click'))
}
"""

button1.callback = CustomJS(args=dict(source=data_table_source),code=javaScript)
button2.callback = CustomJS(args=dict(source=ecom_zipcode_all),code=javaScript)


# Dashboard layout

from bokeh.layouts import column, row, WidgetBox
from bokeh.io import show, curdoc
from bokeh.models.widgets import Tabs, Panel

controls = WidgetBox(state_choose, radius_select, tran_type_select, min_date_select, max_date_select, solution_select)

# Create a row layout
layout1 = row(controls, p, guideline)
layout2 = row(data_table1, button1)
layout3 = row(data_table2, button2)

tab1 = Panel(child=layout1, title = 'Map')
tab2 = Panel(child=layout2, title = 'All Possible Locations')
tab3 = Panel(child=layout3, title = 'All Online Transactions by ZipCode')

tabs = Tabs(tabs = [tab1, tab2, tab3])

# Add it to the current document (displays plot)
curdoc().add_root(tabs)
