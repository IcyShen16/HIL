import config as conf
import pandas as pd
import numpy as np


def fitSystem(m, n):
    # read date
    df = pd.read_csv(conf.fileName)
    # transform datetime columns from object type to datetime
    df.loc[:, "pickup_datetime"] = pd.to_datetime(df.pickup_datetime)
    df.loc[:, "dropoff_datetime"] = pd.to_datetime(df.dropoff_datetime)
    # we will use the relative second as time in the system
    df["arrival_time"] = (df.pickup_datetime - conf.startTime).dt.total_seconds()
    df["dropoff_seconds"] = (df.dropoff_datetime - conf.startTime).dt.total_seconds()
    df["duration"] =( df.dropoff_datetime - df.pickup_datetime).dt.total_seconds()



    startIndex = df.loc[df.arrival_time == 0, :].index[0]

    vehicleInitData = df.loc[startIndex - m:startIndex-1, ['dropoff_lon', 'dropoff_lat','dropoff_seconds']].values
    driverInitData = df.loc[startIndex - n:startIndex - 1, ['dropoff_seconds']].values
    if m > n:
        # if the number of vehicles is strictly greater than the number of drivers
        # then at the beginning, we have at least m-n vehicles availables
        # so here we set the first m-n vehicles with least first free time as the idle vehicles at the beginning of the simulation
        FFTindex = np.argpartition(vehicleInitData[:, 2], m-n)
        vehicleInitData[FFTindex[:m-n], 2] = 0

    dfSub = df.loc[startIndex:, :]
    dfSub.reset_index(drop=True, inplace=True)
    dfSub.loc[:, "id"] = range(len(dfSub))
    dfSub = dfSub.astype({"arrival_time": "int64", "dropoff_seconds": "int64", "duration": "int64", "id":"int64"})
    dfSub = dfSub[["arrival_time", 'duration', 'pickup_lon', 'pickup_lat','dropoff_lon', 'dropoff_lat', "id"]]

    return dfSub, vehicleInitData, driverInitData



if __name__ == "__main__":
    fitSystem(10, 5)
