import random
import math

def check_all_busy(arr):
    # servers_busy = ["off" for i in range(m)]
    for item in arr:
        if item != "busy":
            return False
    return True

def min_find_idel(arr):
    index_list = [] 
    for item in arr:
        if item == "off":
            return arr.index(item)


def submission(mode=None, arrival=None, service=None, m=None, setup_time=None, delayoff_time=None, time_end=None):
    path = "departure_*.txt"
    mrt_all = "mrt_*.txt"

    output1 = open(path, 'w')
    output2 = open(mrt_all, 'w')
    


    response_time_cumulative = 0
    num_customer_served = 0
    
    lambda_number = 5
    mu = 5

    next_arrival_time = -math.log(1-random.random())/lambda_number;
    service_time_next_arrival = -math.log(1-random.random())/mu;

    inf = 99999
    next_departure_time = [inf for i in range(m)]
    
    master_clock = 0

    buffer_content = []

    server_busy = [0 for i in range(m)]
    server_status = ['off' for i in range(m)]

    arrival_time_next_departure = [0 for i in range(m)]

    queue_length = 0

    while master_clock < time_end:
        
        first_departure_time = min(next_departure_time)
        first_departure_server = next_departure_time.index(min(next_departure_time))
        

        # 在里面的客户比进来的客户先出去
        if next_arrival_time < first_departure_time:
            next_event_time = next_arrival_time
            next_event_type = 1
        else:
            next_event_time = first_departure_time
            next_event_type = 0
        
        master_clock = next_event_time
        

        if next_event_type == 1:       # 下一个事件是有job进来
            if check_all_busy(server_busy): # 
                buffer_content += [next_arrival_time, service_time_next_arrival, "UNMARKED"] #在这里添加新的进来的buffer信息
                queue_length += 1
                '''testing buffer content'''
                print(buffer_content)
                '''testing buffer content'''
            else:                           # 如果有闲置的server
                idel_server = server_busy.index(min(server_busy)) # 返回的是一个位置
                next_departure_time[idel_server] = next_arrival_time + service_time_next_arrival
                arrival_time_next_departure[idel_server] = next_arrival_time
                num_customer_served += 1
            
            
            next_arrival_time = master_clock - math.log(1-random.random())/lambda_number;
            service_time_next_arrival = -math.log(1-random.random())/mu; 
        elif next_event_type == 0:     # 下一个事件是有job离开
            num_customer_served = num_customer_served + 1;
            response_time_cumulative = response_time_cumulative + master_clock - arrival_time_next_departure[first_departure_server]
            output1.write(format(arrival_time_next_departure[first_departure_server], '0.3f') + "\t" + format(master_clock, '0.3f') + "\n")
            
            if queue_length > 0:
                # 下一个等着进来：
                next_departure_time[first_departure_server] = master_clock + buffer_content[0][1]
                arrival_time_next_departure[first_departure_server] = buffer_content[0][0]
                '''testing buffer content'''
                buffer_content = buffer_content[1:]
                '''testing buffer content'''
                queue_length -= 1
            else: # queue 里面已经没有东西
                next_departure_time[first_departure_server] = inf
                server_busy[first_departure_server] = 0
        elif next_event_type == 2:     # setup
            
        else:
            print("never happend")

    g_response_time = response_time_cumulative/num_customer_served

    output2.write(format(g_response_time, '0.3f'))




    output1.close()
    output2.close()
    
    
    

submission(arrival="./assets/arrival_1.txt", service="./assets/service_1.txt", m = 5, time_end=170)
