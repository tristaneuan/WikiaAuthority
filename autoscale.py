from __future__ import division
import json
import requests
from argparse import ArgumentParser
from datetime import datetime
from math import ceil
from time import sleep
from wikia_dstk.loadbalancing import EC2Connection

import config


def get_args():
    ap = argparse.ArgumentParser(description='Automatically launch EC2 instances running celeryd according to task load.')
    ap.add_argument('--region', dest='region', default=config.REGION,
                    help='EC2 region')
    ap.add_argument('--price', dest='price',
                    default=config.PRICE,
                    help='Maximum spot instance price')
    ap.add_argument('--ami', dest='ami',
                    default=config.AMI,
                    help='The ID of the AMI running celeryd')
    ap.add_argument('--key', dest='key',
                    default=config.KEY,
                    help='The .pem key to use')
    ap.add_argument('--sec', dest='sec',
                    default=config.SEC,
                    help='The security group to use')
    ap.add_argument('--type', dest='type',
                    default=config.TYPE,
                    help='The EC2 instance type')
    ap.add_argument('--tag', dest='tag',
                    default=config.TAG,
                    help='The tag to assign to the instance')
    ap.add_argument('--max-tasks', dest='max_tasks', type=int,
                    default=config.MAX_TASKS,
                    help='Maximum # of tasks per instance before launching more')
    ap.add_argument('--max-instances', dest='max_instances', type=int,
                    default=config.MAX_INSTANCES,
                    help='Maximum # of instances to launch')
    ap.add_argument('--stall', dest='stall', type=int,
                    default=config.STALL,
                    help='# of minutes to wait for tasks before shutting down')
    return ap.parse_args()

args = get_args()

def num_instances(connection):
    return len(connection.get_tagged_instances(args.tag))

def num_workers():
    return len(json.loads(requests.get(config.FLOWER+'/api/workers').content).keys())

def num_tasks():
    return len(json.loads(requests.get(config.FLOWER+'/api/tasks').content).keys())


# I recall something about needing to be able to restart celeryd but I can't remmember why
user_data = """
"""

conn = EC2Connection(vars(args))
stall = 0

while True:
    if stall >= args.stall:
        print 'Terminating instances!'
        conn.terminate(conn.get_tagged_instances(args.tag))

    instances = num_instances(conn)
    tasks = num_tasks()

    print '%s: %d instances working on %d tasks.' % (
        datetime.today().isoformat(' '), instances, tasks)

    if not tasks:
        stall += 1
        print 'No tasks yet, stalling... (%d/%d)' % (stall, args.stall)
        sleep(60)
        continue

    stall = 0

    if not instances or tasks > args.max_tasks:
        optimal = int(ceil(tasks / args.max_tasks))
        num_to_add = optimal if optimal <= args.max_size else args.max_size
        conn.add_instances(num_to_add, user_data, args.tag)
        print 'Added %d instances.' % num_to_add

    sleep(60)
