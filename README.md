# ML-Driven Taxi Positioning for Enhanced Efficiency

## Problem Statement

1. Taxi drivers continue to grapple with falling incomes - ever-rising overhead costs, competition and lower passenger pick-ups
2. Commuters continue to deal with longer waiting times and higher price surges

Objective: Improve and optimize taxi driver positioning through ML-driven prediction and recommendation system


## Data Preparation
### Data Collection
1. Public Crowds Volume
- Potential taxi demand using public transport passenger volume
- Data from LTA DataMall on Bus Stops and Train Stations passenger volume

2. Taxi Availability
- Supply of taxi based on all available taxis for hire - exclude “Hired” or “Busy”
- Data extracted from Data.gov.sg API

### Preprocessing

1. Public Crowds Volume
- Take the total passengers tap in volume as the crowd volume
- Create new feature for day_type and time_per_hour combined
- Represent station code with longitude and latitude
- Dummify and multiply

2. Taxi Availability
- Retrieve taxi availability within a month in an hourly format
- Data extracted contains latitude and longitude of availability taxis at specific date and time
- Convert the date and time into an hourly time format
- Use datetime feature to determine if date is weekday or weekend

## Exploratory Data Analysis
### Uber H3 Spatial Indexing
Partitioning the Earth's surface into hexagonal cells

Key Features and Advantages:
- Grid system to bucket into hexagonal areas
- Multiple levels of resolution, allowing representation at varying levels of details
- Simplify analysis - only one distance between a hexagon centerpoint to its neighbors’
- Scalable analysis, enabling efficient zooming in and out

Procedures:
- Initiate a hexagon from center of Singapore with resolution = 7
- Expand the hexagon by 1 time, then continuously until it occupies the entire Singapore
- Iterate through each taxis, bus, and train points
- Locate at which hexagon each point is
- Count the number of points at each hexagon

Final Parameter:
- Number of trains and buses passengers and available taxis at each hexagon at different time
- Use taxi Demand (Train and Bus Passenger) / Supply (Taxi Availability) ratio

### Some Facts
Top 5 areas with highest available taxis at the start and end of office hours
- Weekday 08:00 -> Woodlands, Yishun, Hougang, Tanjong Pagar, Changi
- Weekday 18:00 -> Yishun, Hougang, Tanjong Pagar, Marina Bay, Changi
- Weekend 11:00 -> Marina Bay, Newton, Bugis, Kallang, Changi
- Weekend 18:00 -> Yishun, Marina Bay, Bugis, Tanjong Pagar, Changi

Top 5 areas with highest passenger volumes at the start and end of office hours
- Weekday 08:00 -> Bukit Panjang, Yishun, Sengkang, Hougang, Bedok
- Weekday 18:00 -> Jurong East, Sengkang, Tanjong Pagar, Bugis, Marina Bay
- Weekend 11:00 -> Yishun, Sengkang, Toa Payoh, Bugis, Tanjong Pagar
- Weekend 18:00 -> Sengkang, Tanjong Pagar, Bugis, Marina Bay, Kallang

## Modeling
### Process
What are we modeling?
- Demand / supply ratio for next hour, from 08:00 to 23:59 weekday and weekend
- For all the hexagons
- Rolling window approach with size = 3

Process:
- Remove all irrelevant columns
- Transpose to move the time frame into rows
- Remove the 01 to 04 data as trains and buses are not in operation during 02 to 05 AM

### Model
- Auto ARIMA - Baseline
- RNN - SimpleRNN
- RNN - LSTM

### Metrics 
Root Mean Squared Error (RMSE)
- Evaluate the accuracy of model
- Average magnitude of the errors between predicted vs actual values
- Lower values = better model

### Modeling Conclusion
Result:
A) Auto ARIMA - Baseline = 143.74 RMSE
B) SimpleRNN - 32 units = 131.43 RMSE
C) SimpleRNN - 50 units = 53.34 RMSE
D) SimpleRNN - 128 units = 139.50 RMSE
E) LSTM - 50 units = 130.76 RMSE

Evaluation:
Best performing model is SimpleRNN with 50 units of layer

Why SimpleRNN with 50 units of layer performs better than those with 32 and 128 units?
- 50 units might provide the right balance between underfitting and overfitting
- Moderate complexity of the data might align better with 50 units

Why SimpleRNN performs better than LSTM at the same 50 units of layer?
- Data contains short-term patterns which gives SimpleRNN the advantage
- Data is relatively simple
- LSTM might result in overfitting when dealing with simple dataset

Now that we have developed the model to predict taxis demand/supply ratio at different area, how can we bring this to the taxi drivers? Build Recommender System through Streamlit

## Recommender Systems
Three Features:
- Recommend the area to go for the next hour based on highest ratio. If now is 21:45, recommend for 22:00
- Calculate the duration in traffic to the recommended area and use Google Map Distance API
- Provide the direction from origin to the recommended area and Google Map Direction API

Methodology:
- Calculate the time until the next hour
- Generate prediction for the next hour
- Iterate through the predicted values for all area
- Recommend the area with highest ratio
- Calculate the time required from origin to the recommended area
- Check if the time required is less than the time until next hour
- If not, provide the next highest ratio
- Provide the direction to the destination

## Limitation
- Public transport volume dataset
Data comes in the hourly format for weekday or weekend. More granular data in hour or minutes time frame
- Inaccuracy of taxi demand
Taxi demand is based on public transport volume. Get the actual taxi demand based on the taxi pick up time
- Limited application
Applicable to only taxi as it is the only open source data. Extend the concept to ride hailing services provided the demand and supply data are available
