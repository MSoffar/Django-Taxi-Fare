from django import forms


class InputForm(forms.Form):
    User_ID = forms.CharField(label='User ID', max_length=100)
    User_Name = forms.CharField(label='User Name', max_length=100)
    Driver_Name = forms.CharField(label='Driver Name', max_length=100)

    CAR_CONDITION_CHOICES = [
        ('Bad', 'Bad'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
        ('Excellent', 'Excellent')
    ]
    Car_Condition = forms.ChoiceField(label='Car Condition', choices=CAR_CONDITION_CHOICES)

    WEATHER_CHOICES = [
        ('rainy', 'Rainy'),
        ('sunny', 'Sunny'),
        ('stormy', 'Stormy'),
        ('windy', 'Windy'),
        ('cloudy', 'Cloudy')
    ]
    Weather = forms.ChoiceField(label='Weather', choices=WEATHER_CHOICES)

    TRAFFIC_CONDITION_CHOICES = [
        ('Congested Traffic', 'Congested Traffic'),
        ('Flow Traffic', 'Flow Traffic'),
        ('Dense Traffic', 'Dense Traffic')
    ]
    Traffic_Condition = forms.ChoiceField(label='Traffic Condition', choices=TRAFFIC_CONDITION_CHOICES)

    key = forms.CharField(label='Key', max_length=100)
    pickup_datetime = forms.DateTimeField(label='Pickup Datetime',
                                          widget=forms.TextInput(attrs={'type': 'datetime-local', 'step': 1}))
    pickup_longitude = forms.FloatField(label='Pickup Longitude')
    pickup_latitude = forms.FloatField(label='Pickup Latitude')
    dropoff_longitude = forms.FloatField(label='Dropoff Longitude')
    dropoff_latitude = forms.FloatField(label='Dropoff Latitude')
    passenger_count = forms.IntegerField(label='Passenger Count', min_value=1)
    hour = forms.IntegerField(label='Hour', min_value=1, max_value=24)
    day = forms.IntegerField(label='Day', min_value=1, max_value=31)
    month = forms.IntegerField(label='Month', min_value=1, max_value=12)
    weekday = forms.IntegerField(label='Weekday', min_value=1, max_value=7)
    year = forms.IntegerField(label='Year')
    jfk_dist = forms.FloatField(label='JFK Distance')
    ewr_dist = forms.FloatField(label='EWR Distance')
    lga_dist = forms.FloatField(label='LGA Distance')
    sol_dist = forms.FloatField(label='SOL Distance')
    nyc_dist = forms.FloatField(label='NYC Distance')
    distance = forms.FloatField(label='Distance')
    bearing = forms.FloatField(label='Bearing')
