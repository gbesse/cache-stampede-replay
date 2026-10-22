import heapq
from .common import integer,identifier,unique_ids

def run(data):
    requests=data['requests'];ttl=integer(data['ttl_ms'],1,10**9);load=integer(data['load_ms'],1,10**9);early=integer(data.get('early_refresh_ms',0),0,ttl)
    if len(requests)>10000:raise ValueError('size')
    unique_ids(requests)
    for r in requests:integer(r['time_ms'],0,10**12);identifier(r['key'])
    def simulate(mode):
        cache={};inflight={};pending=[];responses={};counter=0;coalesced=0;max_active=0
        def start(key,time,waiter=None):
            nonlocal counter,max_active
            counter+=1;job={'id':counter,'key':key,'start':time,'end':time+load,'waiters':[] if waiter is None else [waiter]};heapq.heappush(pending,(job['end'],counter,job));
            if mode!='plain':inflight[key]=job
            max_active=max(max_active,len(pending));return job
        def complete(until):
            while pending and pending[0][0]<=until:
                end,_,job=heapq.heappop(pending);cache[job['key']]={'expires':end+ttl,'version':job['id']}
                if inflight.get(job['key']) is job:del inflight[job['key']]
                for r,kind in job['waiters']:responses[r['id']]={'id':r['id'],'route':kind,'latency_ms':end-r['time_ms'],'version':job['id']}
        for r in sorted(requests,key=lambda r:(r['time_ms'],r['id'])):
            time=r['time_ms'];key=r['key'];complete(time);entry=cache.get(key)
            if entry and time<entry['expires']:
                refresh=mode=='early_refresh' and time>=entry['expires']-early
                if refresh and key not in inflight:start(key,time)
                responses[r['id']]={'id':r['id'],'route':'fresh_during_refresh' if key in inflight else 'hit','latency_ms':0,'version':entry['version']}
            elif mode!='plain' and key in inflight:
                inflight[key]['waiters'].append((r,'coalesced'));coalesced+=1
            else:start(key,time,(r,'miss'))
        complete(float('inf'));latencies=[r['latency_ms'] for r in responses.values()]
        return {'mode':mode,'provider_loads':counter,'coalesced_requests':coalesced,'maximum_inflight_loads':max_active,'mean_latency_ms':sum(latencies)/len(latencies) if latencies else 0,'maximum_latency_ms':max(latencies,default=0),'responses':[responses[r['id']] for r in requests]}
    return {'policies':[simulate(mode) for mode in ('plain','singleflight','early_refresh')],'scope':'discrete-event simulation, constant declared load time, no errors; fresh responses only before TTL; early refresh is request-triggered'}
