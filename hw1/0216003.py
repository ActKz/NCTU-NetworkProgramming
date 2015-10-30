import socket
import json
dest_ip = "127.0.0.1"
dest_port = 5566
bottom = 3000
top = 60000
mid = 0
soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    mid = (bottom + top) /2
    soc.sendto("{'guess':"+str(mid)+"}",(dest_ip,dest_port))
    print "send{'guess':"+str(mid)+"}"
    data, addr = soc.recvfrom(1024)
    print "receive"+data
    res = json.loads(data)
    if res['result'] == "larger":
        bottom = mid
    elif res['result']=="smaller":
        top = mid
    elif res['result']=="bingo!":
        goal = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        goal.sendto("{'student_id':'0216003'}",(dest_ip,mid))
        r, ad = goal.recvfrom(1024)
        print r
        break
    else: 
        print res['result']
        break
