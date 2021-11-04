# import src files 
#### Roles.py
Define classes for all roles in the system (drivers, vehicles, customers)

#### MatchPolicy.py
different matching policies: First dispatch or Nearest Neighbor 

#### Model.py 

simulation

#### DataPreprocessing.py 

process the raw data 

#### Comparison.py 

compare different systems

#### config.py 

General parameters 

#### main.py 




# Stationary System
#### Stationary arrival process: 

10:00 am - 14:00 pm (not include 14:00 pm), i.e. startTime = 10:00 am, endTime = 14:00 pm.   

#### Initial system (initSys):  
assume the number of vehicles is $m$ and the number of drivers is $n$. Use the $m$ arrival before startTime as the initial states (dropoff locations as the location of vehicles, the dropoff time as the times the vehicles/drivers become available.), then the number of idle vehicles/drivers is less than or equal to $m$($n$). 

#### Simulation(simuLoss, simuQueue): 

every second, we check the customers in the system (arrive at or before this second and are not be served), then assign a free vehicle and driver to them according to the given matching policy (FD, NN). If it is FD, then we take the order of customers in the given data as the arrival order. So we stop the simulation at the second exactly before 14:00 pm. If it is NN, we stop the simulation when all of the customers (arrives to the system from startTime to endTime) are served 
#### Service level: 

we use the customers arriving to the system from 11:00 am - 13:00pm as the effective arrivals. We query the number of served arrivals among all of the effective arrivals from 10:00 am -13:pm and use the ratio as the service level. 

#### Expected waiting time: 

we use the customers arriving to the system from 11:00 am - 13:00pm as the effective arrivals. We compute the total waiting time of these effective arrivals and use that value divides by the total number of effective arrivals as the expected waiting time of the system. 