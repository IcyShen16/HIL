import config as conf
from MatchPolicy import FD, NN
from utils import haversine_point_to_vector_distance
from tqdm import tqdm

def simuLoss(customers, drivers, fleet):
    # simulate the loss system: different matching policies (FD, NN) are reduced to the same one
    for t in tqdm(range(conf.totalTime)):
        cur_customers_IDs, cur_customers_locations = customers.arrivingCustomer(t)
        # query customers arrived at this second: may be empty
        if cur_customers_IDs is not None:
            cur_idle_drivers_IDs = drivers.idleDrivers(t) # query idle drivers
            cur_idle_vehicles_ID, cur_idle_vehicles_locations = fleet.idleVehicles(t) # query idle vehicles and their locations

            if len(cur_idle_drivers_IDs) > 0: # if we have idle drivers -> we have idle vehicles
                Cus_Ids, Veh_IDs, distance_vector = NN(cur_customers_locations.reshape(-1, 2), cur_idle_vehicles_locations.reshape(-1, 2), cur_idle_drivers_IDs, cur_idle_vehicles_ID, cur_customers_IDs)
                for index, cus_id in enumerate(Cus_Ids):
                    cus_id = int(cus_id)
                    cur_cus = customers.customers.loc[cus_id]

                    pickup_time = distance_vector[index]/conf.LinearSpeed
                    fft = t + pickup_time + cur_cus["duration"]

                    customers.serveCustomer(cus_id, t, pickup_time)
                    fleet.fleets[cur_idle_vehicles_ID[index]].serveCus(cur_cus[["dropoff_lon", "dropoff_lat"]], fft)
                    drivers.drivers[cur_idle_drivers_IDs[index]].serveCus(fft)

                    customers.update(t)
                    drivers.update(t)
                    fleet.update(t)
    SL = customers.computeMeasure("LS")
    return SL


def simuQueue(customers, drivers, fleet, matchPolicy):
    # simulate the queueing system with some matching policy (FD, NN)
    if matchPolicy == "FD":
        MP = globals()["FD"]
    elif matchPolicy == "NN":
        MP = globals()["NNwithOrder"]
    else:
        raise Exception("\nerror @ simuQueue: wrong matchPolicy = {}!!!!!!!\n".format(matchPolicy))

    for t in tqdm(range(conf.totalTime)):
        cur_customers_IDs, cur_customers_locations = customers.waitingCustomers(t)
        if cur_customers_IDs is not None:
            cur_idle_drivers_IDs = drivers.idleDrivers(t)  # query idle drivers
            cur_idle_vehicles_ID, cur_idle_vehicles_locations = fleet.idleVehicles(t)  # query idle vehicles and their locations

            if len(cur_idle_drivers_IDs) > 0:  # if we have idle drivers -> we have idle vehicles
                Cus_Ids, Veh_IDs, distance_vector = MP(cur_customers_locations.reshape(-1, 2),
                                                       cur_idle_vehicles_locations.reshape(-1, 2),
                                                       cur_idle_drivers_IDs, cur_idle_vehicles_ID,
                                                       cur_customers_IDs)

                for index, cus_id in enumerate(Cus_Ids):
                    cus_id = int(cus_id)
                    cur_cus = customers.customers.loc[cus_id]

                    pickup_time = distance_vector[index] / conf.LinearSpeed
                    fft = t + pickup_time + cur_cus["duration"]

                    customers.serveCustomer(cus_id, t, pickup_time)
                    fleet.fleets[cur_idle_vehicles_ID[index]].serveCus(cur_cus[["dropoff_lon", "dropoff_lat"]], fft)
                    drivers.drivers[cur_idle_drivers_IDs[index]].serveCus(fft)

                    customers.update(t)
                    drivers.update(t)
                    fleet.update(t)

    EW = customers.computeMeasure("QS")
    return EW


if __name__ == "__main__":
    from DataPreprocessing import fitSystem
    from Roles import CUSTOMERS, FLEET, DRIVERS


    m = 1000
    n = 1000
    df_cus, vehicleInitData, driverInitData = fitSystem(m, n)
    customers = CUSTOMERS(df_cus, "LS")
    fleet = FLEET(vehicleInitData)
    drivers = DRIVERS(driverInitData)
    matchPolicy = "FD"
    EW = simuQueue(customers, drivers, fleet, "FD")
    print("with {} vehicles and {} drivers, the expected waiting time is {}".format(m, n, EW))
