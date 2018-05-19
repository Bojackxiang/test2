def submission(mode=None, arrival=None, service=None, m=None, setup_time=None, delayoff_time=None, time_end=None):
    with open(arrival) as file:
        arrival_time = file.readlines()
        for i in range(len(arrival_time)):
            arrival_time[i] = int(arrival_time[i])/1.0
    with open(service) as file:
        service_time = file.readlines()
        for i in range(len(service_time)):
            service_time[i] = int(service_time[i])/1.0
    
    