import config as conf
import pandas as pd

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

    df = df.astype({"arrival_time":"int64", "dropoff_seconds":"int64", "duration": "int64"})

    startIndex = df.loc[df.pickup_datetime == conf.startTime, :].index[0]
    vehicleInitData = df.loc[startIndex - m:startIndex-1, ['dropoff_lon', 'dropoff_lat','dropoff_seconds']].values
    driverInitData = df.loc[startIndex - n:startIndex - 1, ['dropoff_seconds']].values
    df.index = df.pickup_seconds
    dfSub = df.loc[startIndex:, ["arrival_time", 'duration', 'pickup_lon', 'pickup_lat','dropoff_lon', 'dropoff_lat']]
    return dfSub, vehicleInitData, driverInitData



if __name__ == "__main__":
    fitSystem(10, 5)
