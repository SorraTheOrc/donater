# First open an tunnel to your ACS cluster master:
# ssh -L 8080:master0:8080 -N azureuser@acsmesos100303man.eastus.cloudapp.azure.com -p 2211

import json
import os
import requests
import time

def write_settings():
    with open('/tmp/donateacs.json', 'w') as outfile:
        json.dump(settings, outfile)

def running_donate_tasks_count():
    response = requests.get("http://localhost:8080/v2/apps?id=donateacs")
    apps = response.json()['apps']
    if len(apps) == 0:
        return 0
    else:
        instances = apps[0]['instances']
        return instances
    
    
def start_donate_task():
    global running_donate_tasks

    next_time = int(settings['last_queued_task_time']) + int(settings['cool_down_time'])
    current_time = int(time.time())
    
    if next_time - current_time > 0:
        print "In cooldown period, not starting a new task. Cooldown ends in : " + str(next_time - current_time) + " seconds."
        return
    else:
        print "Starting a donateACS task"
    
    running_donate_tasks = running_donate_tasks_count();

    docker = {}
    docker['image'] = "rgardler/fah"
    
    container = {}
    container['type'] = "DOCKER"
    container['docker'] = docker
    
    app = {}
    app['id'] = '/donateacs'
    app["instances"] = running_donate_tasks + 1
    app['cpus'] = 1
    app["mem"] = 512
    app["container"] = container

    apps = []
    apps.append(app)

    response = requests.put("http://localhost:8080/v2/apps", json.dumps(apps))
    
def stop_donate_task():
    print "Attempting to stop a donateACS task"
    app = {}
    app["id"] = '/donateacs'
    app["instances"] = running_donate_tasks_count() - 1
    apps = []
    apps.append(app)
    
    response = requests.put("http://localhost:8080/v2/apps?force=true", json.dumps(apps))
    
def get_queue_size():
    global _last_queued_task_time
    
    uri = "http://localhost:8080/v2/queue"
    response = requests.get(uri)
    queue = response.json()['queue']

    size = len(queue)
    if size > 0:
        settings['last_queued_task_time'] = time.time()
        write_settings()
    print "Current queue size is " + str(size)
    return size

# Application starts here

settings = {}
if os.path.isfile('/tmp/donateacs.json'):
    with open('/tmp/donateacs.json') as data_file:
        settings = json.load(data_file)
else:
    settings['last_queued_task_time'] = time.time()
    settings['cool_down_time'] = 60 * 5
    write_settings()
    
if get_queue_size() > 0:
    stop_donate_task()
else:
    start_donate_task()
