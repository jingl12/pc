import pandas as pd
from sklearn.linear_model import LinearRegression as lr

def Temperature():
    temp = pd.read_csv('GlobalSurfaceTemperature.csv')
    temp = temp[temp.columns[1:]].set_index(pd.to_datetime(temp.Year.astype('str')))
    gas = pd.read_csv('GreenhouseGas.csv')
    gas = gas[gas.columns[1:]].set_index(pd.to_datetime(gas.Year.astype('str')))
    co2 = pd.read_csv('CO2ppm.csv')
    co2 = co2[co2.columns[1:]].set_index(pd.to_datetime(co2.Year.astype('str')))
    co2.columns = ['CO2PPM']
    df = pd.concat([gas, co2, temp], axis=1)
    gas_part = df.iloc[:, :4].fillna(method='ffill').fillna(method='bfill')
    data = gas_part['1970': '2010'].iloc[:, :4]
    test = gas_part['2011': '2017'].iloc[:, :4]

    model = lr().fit(data, df['1970': '2010'].Median)
    median = model.predict(test)
    model = lr().fit(data, df['1970': '2010'].Upper)
    upper = model.predict(test)
    model = lr().fit(data, df['1970': '2010'].Lower)
    lower = model.predict(test)
    return list(upper), list(median), list(lower)

print(Temperature())
