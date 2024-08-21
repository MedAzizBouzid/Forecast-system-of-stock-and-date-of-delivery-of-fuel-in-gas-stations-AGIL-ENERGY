from django.shortcuts import render
from joblib import load 
from .models   import NextCallDelivery

import pandas as pd
import numpy as np 
from sklearn.preprocessing import MinMaxScaler

model=load('./notebooks/model_bo2.joblib')
scaler = load('./notebooks/scaler_bo2.pkl')
def add_date_features(df, date_column='DATLIV'):
    df[date_column] = pd.to_datetime(df[date_column])

    # Extract different date-related features
    df['Year'] = df[date_column].dt.year
    df['Month'] = df[date_column].dt.month
    df['Day'] = df[date_column].dt.day
    df['Weekday'] = df[date_column].dt.weekday
    df['Quarter'] = df[date_column].dt.quarter
    
    # Add cyclic features for month and day
    df['month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    df['day_sin'] = np.sin(2 * np.pi * df['Day'] / 31)
    df['day_cos'] = np.cos(2 * np.pi * df['Day'] / 31)

    return df
def predictor(request):
    return render(request,'main_bo2.html')
def formInfo(request):
    
    # Get the data from the form 

    ancscp=request.GET['ANCSCP']
    DATLIV=request.GET['DATLIV']
    LIBPRD=request.GET['LIBPRD']
    LIBGVR=request.GET['libgvr']
    LIBLOC=request.GET['libloc']
    prixHt=request.GET['prixHT']
    last_quantity_delivered=request.GET['last_quantity_delivered']



    data = {
    'ANCSCP': [ancscp],
    'DATLIV': [DATLIV],
    'LIBPRD': [LIBPRD],
    'LIBGVR': [LIBGVR],
    'LIBLOC': [LIBLOC],
    'prixHT': [prixHt],
    'last_quantity_delivered': [last_quantity_delivered]



}

    x = pd.DataFrame(data)
    x['DATLIV'] = pd.to_datetime(x['DATLIV'])
    #df['DATLIV'] = pd.to_datetime(df['DATLIV'])
    
        #enocde Categorical features
    categorical_columns = ['LIBPRD','LIBGVR','LIBLOC']
    x_transformed = pd.get_dummies(x, columns=categorical_columns)
    #encode Date feature
    x_transformed=add_date_features(x_transformed)
    x_transformed[x_transformed.select_dtypes(include='bool').columns] = x_transformed.select_dtypes(include='bool').astype(int)
        # Add other features remaining
    expected_columns = scaler.feature_names_in_
    for col in expected_columns:
        if col not in x_transformed.columns:
            x_transformed[col] = 0
    x_transformed = x_transformed[expected_columns]
    

    print(x_transformed)
    print('--------------------------------------------')


    # Data normalization
    x_scaled = scaler.transform(x_transformed)
    x_scaled = pd.DataFrame(x_scaled, columns=x_transformed.columns)
    print(x_scaled)
    # Delete target feature
    x_scaled.drop(columns=['next_call'], inplace=True)
    #Model prediction
    y_pred=model.predict(x_scaled)
    # temporairement
    y_pred=(y_pred*4)/0.666667
    y_pred=y_pred.round()
    DATLIV = pd.to_datetime(DATLIV)
    y_date = DATLIV + pd.to_timedelta(y_pred, unit='days')

    NextCallDelivery.objects.create(
    ANCSCP=ancscp,
    DATLIV=x['DATLIV'][0],  # Assurez-vous que la date est bien au format DateTime
    LIBPRD=LIBPRD,
    LIBGVR=LIBGVR,
    LIBLOC=LIBLOC,
    prixHT=prixHt,
    last_quantity_delivered=last_quantity_delivered,
    next_call=y_pred[0]  # y_pred est un tableau, donc on prend la première valeur
)


    return render(request,'result_bo2.html',{'prediction':y_date[0],
                                         'Client':ancscp,
                                         'Product':LIBPRD,
                                         'gvr':LIBGVR,
                                         'datliv':DATLIV,
                                         'loc':LIBLOC,
                                         'carb':LIBPRD,
                                         'x_scaled':x_transformed })
# Create your views here.