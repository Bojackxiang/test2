import random
import queue
import math

def submission(mode, arrival, service, m, setup_time, delayedoff_time, time_end):
    
    
    if mode != "random" and mode != "trace":
        print("no such a mode")
        return 
    
    if mode == "random":
        origianl_mode = "random"       
        # In this mode, the arrival and service turns into lambda and mu
        time = 0
        lambda_number = arrival
        mu = service
        arrival = []
        service = []
        

        while time < time_end:
            random_number = random.random()
            arrival.append(time-(math.log(1 - random_number)) / lambda_number)
            service.append(random_number/mu)
            time = arrival[-1]
        # this let the mode go to the code in trace
        mode = "trace"
    
    if mode == "trace":
        origianl_mode = "trace"       

        path_arrival = arrival
        path_service = service
        
        with open(path_arrival) as file_1:
            arrival_content = file_1.readlines()
        
        with open(path_service) as file_2:
            service_content = file_2.readlines() 
        
        arrival = []
        service = []

        for each_number in arrival_content:
            arrival.append(int(each_number.strip()))
        
        for each_number_2 in service_content:
            service.append(int(each_number_2.strip()))
        
        # print(arrival)
        # print(service)

        # set up and delay time is given for the system
        buffer_content = queue.Queue()
        time_line = 0
        next_job_arrive_time = arrival[0]
        next_job_arrive_service_time = service[0]
        next_job_depart_arrive_time = 0
        next_leave = 0
        arrival_count = 0
        # since we pick the first one, so we need to add one at the beginning
        arrival_count+=1
        leave_count = 0
        # this is decided by the given txt file
        jobs_number = len(arrival)

        #################################################
        #
        #     This is the server initialization
        #
        #################################################
        server_state_list = ["off" for i in range(m)]

        set_up_finish = [99999 for i in range(m)]
        delay_finish = [99999 for i in range(m)]
        job_leave_finish = [99999 for i in range(m)]
        
        server_finish = [0 for i in range(m)]

        job_status = []

        cumulative_res_time = 0

        # print(next_job_arrive_time)
        # print(next_job_arrive_service_time)
        # print("= = = = = = = = = = = = = = = = = =")

        while True:

            off_number = server_state_list.count("off")
            setup_number = server_state_list.count("setup")
            busy_number = server_state_list.count("busy")
            delay_number = server_state_list.count("delay_off")
            time_list = [99999, next_job_arrive_time, min(job_leave_finish), min(set_up_finish), min(delay_finish)]
            
            next_event_time = min(time_list)
            
            if next_event_time == time_list[0]:
                next_event_type = "general"  

            elif next_event_time == time_list[1]:
                next_event_type = "arrival"

            elif next_event_time == time_list[2]:

                next_event_type = "leave" 

            elif next_event_time == time_list[3]: 
                next_event_type = "setup_finish"

            elif next_event_time == time_list[4]:
                next_event_type = "delay_off_finish"

            time_line = next_event_time

            # print(' - - - - - - - - - - - - - - - - -')
            # print("next time：",next_event_time)
            # print("next event：",next_event_type)



            if next_event_type == "arrival":
                if delay_number > 0:
                    time_max = 0
                    for time_point in delay_finish:
                        if time_point == 99999:
                            continue
                        else:
                            if time_max < time:
                                time_max = time_point
                    server_number = delay_finish.index(time_max)

                    job_leave_finish[server_number] = time_line + next_job_arrive_service_time
                    server_finish[server_number] = next_job_arrive_time
                    delay_finish[server_number] = 99999
                    server_state_list[server_number] = 'busy'
                else:
                    if off_number > 0:
                        for index in range(len(server_state_list)):
                            if server_state_list[index] == "off":
                                set_up_finish[index] = time_line + setup_time
                                server_state_list[index] = "setup"
                                buffer_content.put([next_job_arrive_time, next_job_arrive_service_time, "marked"])
                                break
                    else:
                        buffer_content.put([next_job_arrive_time, next_job_arrive_service_time, "unmarked"])

                if arrival_count < jobs_number:
                    next_job_arrive_time = arrival[arrival_count]
                    next_job_arrive_service_time = service[arrival_count]
                    arrival_count += 1
                else:
                    next_job_arrive_time = 99999
                    next_job_arrive_service_time = 0
            
            elif next_event_type == "leave":
                # here time line is the time for the current event 
                server_number = job_leave_finish.index(time_line)
                job_leave_finish[server_number] = 99999
                next_leave = server_finish[server_number]
                # right now next leave still is the current one for leaving, 
                # so response time for the current one is time line - next_leave
                cumulative_res_time += time_line - next_leave
                updated_status = (round(next_leave, 3), round(time_line, 3))
                job_status.append(updated_status)
                leave_count += 1
                if origianl_mode == "random":
                    if time_line >= time_end:
                        break
                
                buffer_size = buffer_content.qsize()

                if buffer_size == 0:
                    server_state_list[server_number] = "delay_off"
                    delay_finish[server_number] = time_line + delayedoff_time
                    job_leave_finish[server_number] = 99999
                    next_leave = 0
                    server_finish[server_number] = next_leave
                else:
                    # there are some content in the queue
                    # still need to handle them
                    job_assign = buffer_content.get()
                    buffer_size = buffer_content.qsize()
                    

                    server_state_list[server_number] = "busy"
                    
                    next_job_leave_service_time = job_assign[1]

                    next_leave = job_assign[0]
                    server_finish[server_number] = next_leave
                    
                    job_leave_finish[server_number] = time_line + next_job_leave_service_time

                    if job_assign[2] == "marked":
                        
                        sub_buffer_content = [buffer_content.get() for _ in range(buffer_size)]
                        
                        try:
                            sub_buffer_content[next(i for i, sublist in enumerate(sub_buffer_content) if sublist[2] == "unmarked")][2] = "marked"
                            
                        except StopIteration:
                            print("stop the ilteration")
                            max_setup_done_t = 0
                            for time in set_up_finish:
                                if time == 99999:
                                    continue
                                else:
                                    if max_setup_done_t < time:
                                        max_setup_done_t = time
                            server_number = set_up_finish.index(max_setup_done_t)
                            server_state_list[server_number] = "off"
                            set_up_finish[server_number] = 99999
                        for item in sub_buffer_content:
                            buffer_content.put(item)
                            
            elif next_event_type == "delay_off_finish":
                server_number = delay_finish.index(min(delay_finish))
                server_state_list[server_number] = 'off'
                delay_finish[server_number] = 99999
            
            elif next_event_type == "setup_finish":
                job_assign = buffer_content.get()
                server_number = set_up_finish.index(time_line)
                server_state_list[server_number] = 'busy'
                
                job_leave_finish[server_number] = time_line + job_assign[1]
                server_finish[server_number] = job_assign[0]
                set_up_finish[server_number] = 99999

            elif next_event_type == "general":
                # print("whole process is ended")
                break
            else:
                print("you may never get over here")
                break
            
            # else:
            #     print("warning!! You can never get to this step")

        # print("= = = = = = = = general info print = = = = = = = = = =")
        # print("crt:", cumulative_res_time)
        # print("num count",leave_count)
        return delayedoff_time, cumulative_res_time

        
        
delay, cumulative = submission("trace", './assets/arrival_1.txt','./assets/service_1.txt', 5, 10, 5, 70)

while i<50:
    delay, cumulative_res_time = submission("trace", './assets/arrival_1.txt','./assets/service_1.txt', 5, 5, i, 100)
    i += 1
