import socket
import json
import sys
#dest_ip = "127.0.0.1"
#dest_port = 5566
bottom = 3000
top = 60000
mid = 0
soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
if len(sys.argv) <4:
    print("Usage: "+sys.argv[0]+" [dest_ip] [dest_port] [your_id]")
    exit()
dest_ip = sys.argv[1]
dest_port = int(sys.argv[2])
Id = sys.argv[3]
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
        goal.sendto("{'student_id':'"+Id+"'}",(dest_ip,mid))
        r, ad = goal.recvfrom(1024)
        print r
        break
    else: 
        print res['result']
        break
