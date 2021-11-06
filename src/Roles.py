import config as conf
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'

class CUSTOMERS:
    def __init__(self, df, SysType=None):
        if SysType == "LS":
            self.customers = df.loc[(df.arrival_time >=0 )&(df.arrival_time <=conf.totalTime ), :]
        else:
            self.customers = df

        self.customers.loc[:, ["response_time","pickup_time", "waiting_time", "state"]] = 0  # 0: coming. 1: served, 2: waiting/lost

    def arrivingCustomer(self, currentTime: int):
        self.update(currentTime)
        subDf = self.customers.loc[self.customers.arrival_time == currentTime, :]
        if len(subDf) > 0:
            IDs = subDf["id"]
            if isinstance(IDs, pd.Series):
                return IDs.values, subDf[["pickup_lon", "pickup_lat"]].values
            else:
                return np.array([IDs]), subDf[["pickup_lon", "pickup_lat"]].values
        else:
            return None, None

    def serveCustomer(self, id: int, currentTime: int, pickupTime: float):
        self.customers.loc[id, "response_time"] = currentTime - self.customers.loc[id, "arrival_time"]
        self.customers.loc[id, "pickup_time"] = pickupTime
        self.customers.loc[id, "waiting_time"] = pickupTime + currentTime - self.customers.loc[id, "arrival_time"]
        self.customers.loc[id, "state"] = 1

    def waitingCustomers(self, currentTime: int):
        self.update(currentTime)
        subDf = self.customers.loc[(self.customers.state == 2), :]# & (self.customers.arrival_time <= currentTime)
        if len(subDf) > 0:
            IDs = subDf["id"]
            if isinstance(IDs, pd.Series):
                return IDs.values, subDf[["pickup_lon", "pickup_lat"]].values
            else:
                return np.array([IDs]), subDf[["pickup_lon", "pickup_lat"]].values
        else:
            return None, None

    def update(self, currentTime: int):
        need_to_update_index = (self.customers.state != 1) & (self.customers.arrival_time <= currentTime)
        self.customers.loc[need_to_update_index, "state"] = 2
        self.customers.loc[need_to_update_index, "waiting_time"] = currentTime - self.customers.loc[need_to_update_index, "arrival_time"]

    def computeMeasure(self, Dtype):
        effCus = self.customers.loc[range(conf.countStartTime, conf.countEndTime), :]
        if Dtype == "LS":
            numServed = sum(effCus.state == 1)
            return numServed / len(effCus)
        elif Dtype == "QS":
            return effCus.waiting_time.mean()
        else:
            raise Exception("\n error @ CUSTOMERS: computeMeasure---> wrong Dtype = {}!\n".format(Dtype))



class FLEET:
    def __init__(self, initData):
        self.fleets = [VEHICLE(x, i) for i, x in enumerate(initData)]

    def update(self, currentTime):
        for veh in self.fleets:
            veh.update(currentTime)

    def idleVehicles(self, currentTime):
        self.update(currentTime)
        return np.array([veh.ID for veh in self.fleets if veh.FFT <= currentTime]), np.array([veh.location for veh in self.fleets if veh.FFT <= currentTime])

    def checkVehi(self, id):
        return self.fleets[id]


class DRIVERS:
    def __init__(self, initData):
        self.drivers = [HUMAN(x, i) for i, x in enumerate(initData)]

    def update(self, currentTime):
        for human in self.drivers:
            human.update(currentTime)

    def idleDrivers(self, currentTime):
        self.update(currentTime)
        return np.array([human.ID for human in self.drivers if human.FFT <= currentTime])

    def contactHuman(self, id):
        return self.drivers[id]



class HUMAN:
    def __init__(self, initData, ID):
        self.ID = ID
        self.FFT = initData
        if self.FFT <= 0:
            self.state = 0 # idle
        else:
            self.state = 1 # busy

    def update(self, currentTime):
        if self.FFT <= currentTime:
            self.stats = 0

    def serveCus(self, fft):
        self.state = 1
        self.FFT = fft




class VEHICLE:
    def __init__(self, initData, ID):
        self.ID = ID
        self.location = initData[:2]
        self.FFT = initData[2]  # first free time
        if self.FFT <= 0:
            self.state = 0
        else:
            self.state = 1

    def update(self, currentTime):
        if self.FFT <= currentTime:
            self.state = 0

    def serveCus(self, dropoffLocation, fft):
        self.state = 1
        self.location = dropoffLocation
        self.FFT = fft
