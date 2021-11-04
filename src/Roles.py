import config as conf
import pandas as pd
import numpy as np

class CUSTOMERS:
    def __init__(self, df):
        self.customers = df.loc[range(conf.totalTime), :]
        self.customers["id"] = range(len(self.customers))
        self.customers["response_time"] = 0
        self.customers["pickup_time"] = 0
        self.customers["waiting_time"] = 0
        self.customers["state"] = 0  # 0: coming. 1: served, 2: waiting/lost

    def arrivingCustomer(self, currentTime: int):
        return self.customers.loc[currentTime]

    def serveCustomer(self, id: int, currentTime: int, pickupTime: int):
        self.customers.loc[id, "response_time"] = currentTime - self.customers.loc[id, "pickup_seconds"]
        self.customers.loc[id, "pickup_time"] = pickupTime
        self.customers.loc[id, "waiting_time"] = pickupTime + currentTime - self.customers.loc[id, "pickup_seconds"]
        self.customers.loc[id, "state"] = 1

    def waitingCustomers(self, currentTime: int):
        return self.customers.loc[(self.customers.status == 2) & (self.customers.arrival_time <= currentTime), :]

    def update(self, currentTime: int):
        need_to_update_index = (self.customers.status != 1) & (self.customers.arrival_time <= currentTime)
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
        return [veh.ID for veh in self.fleets if veh.FFT <= currentTime], np.array([veh.location for veh in self.fleets if veh.FFT <= currentTime])


class DRIVERS:
    def __init__(self, initData):
        self.drivers = [HUMAN(x, i) for i, x in enumerate(initData)]

    def update(self, currentTime):
        for human in self.drivers:
            human.update(currentTime)

    def idleDrivers(self, currentTime):
        return [human.ID for human in self.drivers if human.FFT <= currentTime]



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

    def serveCus(self, cus, fft):
        self.state = 1
        self.location = cus.dropoff_location
        self.FFT = fft
