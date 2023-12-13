import websocket
import json
import threading
import time
import test2

def send_json_request(ws, request):
    ws.send(json.dumps(request))

def receive_json_response(ws):
    response = ws.recv()
    if response :
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op" : 1,
            "d" : "null"
        }    
        send_json_request(ws,heartbeatJSON)
        print('Heartbeat sent')
ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = receive_json_response(ws)       
heartbeat_interval = event['d']['heartbeat_interval']/1000
threading._start_new_thread(heartbeat,(heartbeat_interval,ws))
# token = "NzE1MjUzODQwODYxMjAwMzk0.GUSQNg.0WdF8wg00FDwJP8i9jfJmUGs8s1pbxIc-PNZTM"
token = "NzE1MjUzODQwODYxMjAwMzk0.GrfM41.knJyi5czomuPxT7RyIFKovcoqmvpSLBsM1zKjs"
# token = "NTM5NzEyMDAyMDAwNTUxOTM2.GqmB97.QuVsf0l0BS3ndmUnYyCaXy1Q41FrY89rATpJlk"
payload  = {
    'op' : 2,
    "d" : {
        "token" : token,
        "properties":{
            "$os" : "windows",
            "$browser" : "chrome",
            "$device" : 'pc'
        }
    }
}
send_json_request(ws,payload)
allowed_usernames = ['shadowtrader', 'catyline', 'cedar_trades']
while True:
    event = receive_json_response(ws)
    
    
    try :
        if event['d']['channel_id'] == '1102240963109331085' and event['d']['author']['username'] in allowed_usernames:
        
            print(f"{event['d']['author']['username']}: {event['d']['content']}")  
            test2.process_message(event['d']['author']['username'],event['d']['content'])
            op_code = event('op')
            if op_code == 11 :
                print('heartbeat received')
    except :
        pass  