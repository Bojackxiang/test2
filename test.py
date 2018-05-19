import math
import random

lambda_number = 10
mu = 5
time_end = 70

time = 0

arrival = []
service = []

while time <= time_end:
    random_number = math.log(1-random.random())
    arrival.append(time-random_number / lambda_number)
    service.append(-random_number/mu)
    time = arrival[-1]

print(arrival)
print("- - - - - - - - -")
print(service)


