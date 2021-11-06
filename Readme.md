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

#### Matching policy:
NN: choose the matching with the smallest total distance
NNwithOrder: According to some order (waiting time), assign the first customers the nearest vehicle, the second customers the nearest vehicle among the remaining vehicles
FD: first dispatch policy; 
#### Simulation(simuLoss, simuQueue): 

every second, we check the customers in the system (arrive at or before this second and are not be served), then assign a free vehicle and driver to them according to the given matching policy (FD, NN). 
For simuLoss, FD and NN are reduced to the same one; Every second, we query the customers waiting in the system, idle vehicles, and idle drivers, and choose NN as matching policy.


For simuQueue, Nearest Neighbor every time, we check the customers waiting in the system, idle vehicles, and idle drivers and then choose the NNwithOrder
FD: if the number of waiting customers c is less than the number of idle drivers n, then it reduced to NNwithOrder; 
Otherwise, we can only serve n customers. Then it is still NNwithOrder with first n customers   
#### Service level: 

we use the customers arriving to the system from 11:00 am - 13:00pm as the effective arrivals. We query the number of served arrivals among all of the effective arrivals from 10:00 am -13:pm and use the ratio as the service level. 

#### Expected waiting time: 

we use the customers arriving to the system from 11:00 am - 13:00pm as the effective arrivals. We compute the total waiting time of these effective arrivals and use that value divides by the total number of effective arrivals as the expected waiting time of the system. 