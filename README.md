# PUMA Retail Store Location Opening

`Bokeh` web app shows the best location in a predefined state to open a new PUMA physical store.

[![](https://img.shields.io/badge/Heroku-Open_Web_App-blue?logo=Heroku)](https://pumacps.herokuapp.com/bokeh_app)

## Description
In today's digital age with same-day ecommerce deliveries, brick & mortal stores are in being contracted. However, for a market player which already has a broad range of ecommerce supply chain like PUMA, extending the physical footmark concurrently with online shopping is negligible. [Puma SE](https://about.puma.com/), branded as Puma, is a German multinational corporation that designs and manufactures athletic and casual footwear, apparel and accessories, which is headquartered in Herzogenaurach, Bavaria, Germany. Puma is the third largest sportswear manufacturer in the world.

This dashboard shows the best in-state location covering the most unreached PUMA ecommerce transactions, which are not in vicinity of a physical store.

The dashboard has 3 tabs:
+ **Map** tab is the map plotting all online transactions and retail location in the local area, along with chosen locations.
+ **All Possible Locations** tab is the prediction of all locations in one state if PUMA tends to place a physical store there. This second tab acts as a guide to select solution number in the first dashboard.
+ **All Online Transactions by ZipCode** tab is information about online transactions in each Zip code used to aggregate data in tab *All Possible Locations*.

## Prerequisites
- Python <= 3.7.9
- Anaconda (optional, is used to install environment, you can use python `venv` instead)

## Screenshots (click on image for video demo)
[![](https://user-images.githubusercontent.com/40580775/113587122-8d7d0000-9658-11eb-9c03-644b3cb168fc.PNG)](https://drive.google.com/file/d/13Uib7wqFNDIh7SfF8-qrYX4w24EScYKf/view)

## Parameters
- `Choose State`: Input state as abbreviation. Default state is MA.
- `Select Radius` (Miles): Coverage of a retail store with Ecommerce transactions. Intuitively, Countryside have higher radius than urban area because of population density and transportation access.
- `Transaction Type`: Checkbox to choose Sale or Return or both.
- `Start & End Date`: Data will be aggregated between Start and End date.
- `Select Solutions`: Solution based on "#" column in **All Possible Locations** tab. Default solution is 0 for maximum ecommerce transactions.

## Notes
- The dashboard runs really slow so please changing each parameters once at a time and be patient.
- Choosing different state will not change current view and you have to scroll to chosen state
- If new store chosen is adjacent to the border of 2 state, Ecommerce transactions in nearby state within radius are included and shown in **All Online Transactions by ZipCode** tab. For example, a store in NYC can still attract online customers in Newark, NJ.
- The dashboard can also identify best in-city location by sorting **All Possible Locations** by *city*
- Some locations are not shown on map because coordinates for those ZipCode are missing. However, transactions are included and shown in 2 table tabs.
- Choosing timeframe based on desirable season. For example, examining store location measurement for different year, different quarter


## Installation
1. Clone repository:
```bash
$ git clone https://github.com/yoogun143/PUMA-Retail-Location-Opening.git
```

2. Install dependencies using Anaconda and pip
```bash
$ conda create -n puma-location-app python=3.7.9  #Create new environment
$ conda activate puma-location-app #Activate environment
$ conda install pip #install pip inside the environment
$ pip install -r requirements.txt #Install required dependencies
```

3. Run the app
```bash
$ bokeh serve --show bokeh_app.py
 * Bokeh app running at: http://localhost:5006/bokeh_app
```

The app will run at http://localhost:5006/bokeh_app.

## Roadmap
- [ ] Automatically change view to current state when choose state.
- [ ] Fix bug of transactions in other states are included in chose state.
- [ ] Use other Zipcode API for better geo-tagging.
- [ ] Reduce web app latency, loading function.
- [ ] Improve UI to be more user friendly.
- [ ] Mobile application.


## Credits
Northeastern University - College of Professional Studies.

PUMA North America, Inc.

## License
MIT License

Copyright (c) [2019] [Thanh Hoang]
