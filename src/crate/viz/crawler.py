# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"


import time
from crate import client
from pprint import pprint
from datetime import datetime


def main():
    # create table cluster_viz (ts timestamp, name string, num_shards integer, disk_bytes long, memory long, load float) with (number_of_replicas = '0-2')
    # local crate
    local = client.connect('127.0.0.1:4200', error_trace=True)
    lcursor = local.cursor()
    # remote crate
    conn = client.connect([
        'https://demo.crate.io',
        ])
    rcursor = conn.cursor()
    while True:
        ts = datetime.now().isoformat()
        print(ts)
        rcursor.execute('''select sys.nodes.name as name,
                                  count(*) as num_shards,
                                  sum(size) as disk_bytes
                           from sys.shards
                           group by sys.nodes.name order by 1''')
        res1 = rcursor.fetchall()

        rcursor.execute('''select heap['used'] as memory,
                                  load['1'] as load
                           from sys.nodes order by name''')
        res2 = rcursor.fetchall()

        d = [None for x in xrange(len(res1))]
        for x in xrange(len(d)):
            dx = [ts,] + res1[x] + res2[x]
            lcursor.execute('''insert into cluster_viz (ts, name, num_shards, disk_bytes, memory, load) values (?, ?, ?, ?, ?, ?)''', dx)
            d[x] = dx
        pprint(d)

        # res = lcursor.executemany('''insert into cluster_viz (ts, name, num_shards, disk_bytes, memory, load) values (?, ?, ?, ?, ?, ?)''', d)
        time.sleep(5)
