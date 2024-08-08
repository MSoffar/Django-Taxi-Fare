import os
import joblib
from django.conf import settings
from django.shortcuts import render
from .forms import InputForm
import numpy as np
import pandas as pd
from datetime import datetime
import math
from sklearn import preprocessing

# Load the model and scaler using relative paths
model_path = os.path.join(settings.BASE_DIR, 'myapp', 'model', 'lgb_model.pkl')
scaler_path = os.path.join(settings.BASE_DIR, 'myapp', 'model', 'X_scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


def haversine_distance(lat1, lon1, lat2, lon2):
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    radius = 6371
    distance = radius * c
    return distance


def manhattan(lon1, lat1, lon2, lat2):
    return np.abs(lon1 - lon2) + np.abs(lat1 - lat2)


def predict(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            # Extract input data
            data = {
                'pickup_longitude': form.cleaned_data['pickup_longitude'],
                'pickup_latitude': form.cleaned_data['pickup_latitude'],
                'dropoff_longitude': form.cleaned_data['dropoff_longitude'],
                'dropoff_latitude': form.cleaned_data['dropoff_latitude'],
                'passenger_count': form.cleaned_data['passenger_count'],
                'hour': form.cleaned_data['hour'],
                'day': form.cleaned_data['day'],
                'month': form.cleaned_data['month'],
                'weekday': form.cleaned_data['weekday'],
                'year': form.cleaned_data['year'],
                'jfk_dist': form.cleaned_data['jfk_dist'],
                'ewr_dist': form.cleaned_data['ewr_dist'],
                'lga_dist': form.cleaned_data['lga_dist'],
                'sol_dist': form.cleaned_data['sol_dist'],
                'nyc_dist': form.cleaned_data['nyc_dist'],
                'distance': form.cleaned_data['distance'],
                'bearing': form.cleaned_data['bearing'],
                'Car Condition': form.cleaned_data['Car_Condition'],
                'Weather': form.cleaned_data['Weather'],
                'Traffic Condition': form.cleaned_data['Traffic_Condition'],
            }

            df = pd.DataFrame([data])

            # Apply preprocessing
            df['pickup_latitude'] = np.radians(df['pickup_latitude'])
            df['pickup_longitude'] = np.radians(df['pickup_longitude'])
            df['dropoff_latitude'] = np.radians(df['dropoff_latitude'])
            df['dropoff_longitude'] = np.radians(df['dropoff_longitude'])

            df['haversine_distance'] = df.apply(
                lambda row: haversine_distance(row['pickup_latitude'], row['pickup_longitude'], row['dropoff_latitude'],
                                               row['dropoff_longitude']), axis=1)
            df['euclidean_distance'] = np.sqrt(np.power(df['pickup_latitude'] - df['dropoff_latitude'], 2) +
                                               np.power(df['pickup_longitude'] - df['dropoff_longitude'], 2))
            df['manhattan_distance'] = df.apply(
                lambda row: manhattan(row['pickup_longitude'], row['pickup_latitude'], row['dropoff_longitude'],
                                      row['dropoff_latitude']), axis=1)

            # Encode categorical variables using label mappings from training
            car_condition_mapping = {'Bad': 0, 'Good': 1, 'Very Good': 2, 'Excellent': 3}
            traffic_condition_mapping = {'Congested Traffic': 0, 'Flow Traffic': 1, 'Dense Traffic': 2}
            weather_mapping = {'rainy': 0, 'sunny': 1, 'stormy': 2, 'windy': 3, 'cloudy': 4}

            df['Car Condition'] = df['Car Condition'].map(car_condition_mapping)
            df['Weather'] = df['Weather'].map(weather_mapping)
            df['Traffic Condition'] = df['Traffic Condition'].map(traffic_condition_mapping)

            # Drop unnecessary columns
            df.drop(['day'], axis=1, inplace=True)

            # Ensure the dataframe columns match the training columns
            required_columns = [
                'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude',
                'passenger_count', 'hour', 'month', 'weekday', 'year',
                'jfk_dist', 'ewr_dist', 'lga_dist', 'sol_dist', 'nyc_dist', 'distance', 'bearing',
                'haversine_distance', 'euclidean_distance', 'manhattan_distance'
            ]

            for col in required_columns:
                if col not in df.columns:
                    df[col] = 0

            df = df[required_columns]

            # Transform data using the scaler
            processed_data = scaler.transform(df)
            prediction = model.predict(processed_data)

            return render(request, 'result.html', {'prediction': prediction[0]})

    else:
        form = InputForm()

    return render(request, 'predict.html', {'form': form})
