import socket
import json
import builtins
import math
import sys
showMsg = builtins.print
class client_2048:
    def __init__(self,serIp,serPort):
        self.connected = False
        self.new = False
        self.serIp = serIp
        self.serPort = serPort
        self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cmd = {"whosyourdaddy":"whosyourdaddy", "help":"Help", "disconnect":"Disconnect", "connect":"Connect", "new":"New", "end":"End", "w":"moveUp", "s":"moveDown", "a":"moveLeft", "d":"moveRight", "u":"unDo"}
        showMsg("Welcom to Game 2048!")
        showMsg("enter 'help' to get more information")
    def connect(self):
        if self.connected:
            showMsg("Have already connected to server")
            return
        try:
            self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.soc.connect((self.serIp,self.serPort))
            showMsg("connect to game server")
            self.connected = True
            self.new = False
        except socket.error as msg:
            showMsg(msg)
    def disconnect(self):
        if self.connected == False:
            showMsg("not connected to server")
            return
        try:
            self.soc.shutdown(1)
            self.soc.close()
            showMsg("disconnect from game server")
            self.connected = False
            self.new = False
        except socket.error as msg:
            showMsg(msg)
    def help(self):
        showMsg("Enter keyboard:")
        showMsg("'connect' - connect to game server")
        showMsg("'disconnect' - disconnect from game server")
        showMsg("'new' - new a game round")
        showMsg("'end' - close the game")
        showMsg("'w' - move bricks up")
        showMsg("'s' - move bricks down")
        showMsg("'a' - move bricks left")
        showMsg("'d' - move bricks right")
        showMsg("'u' - undo the last move")
    def send(self,cmd):
        self.soc.send(("{'action':'"+cmd+"'}").encode())
    def printSquare(self,string):
        data = string.split(',')
        showMsg("---------------------")
        win = False
        for i in [0,4,8,12]:
            if data[i]=="2048" or data[i+1]=="2048" or data[i+2]=="2048" or data[i+3]=="2048":
                win = True
            if data[i]=='0':
                showMsg("|    |",end="")
            else:
                showMsg("|{0:4d}|".format(int(data[i])),end="")
            if data[i+1]=='0':
                showMsg("    |",end="")
            else:
                showMsg("{0:4d}|".format(int(data[i+1])),end="")
            if data[i+2]=='0':
                showMsg("    |",end="")
            else:
                showMsg("{0:4d}|".format(int(data[i+2])),end="")
            if data[i+3]=='0':
                showMsg("    |")
            else:
                showMsg("{0:4d}|".format(int(data[i+3])))
        showMsg("---------------------")
        if win:
            showMsg("Congrats! You win the game")
            self.send("End")
            buffer = self.soc.recv(204118)
            buffer = buffer.decode()
            res = json.loads(buffer)
            if res['status'] == 0:
                showMsg(res['message'])
            else:
                if len(res['message'])>19:
                    self.printSquare(res['message'])
                else:
                    showMsg(res['message'])
            self.new = False
    def main(self):
        while True:
            if self.new:
                showMsg("move>",end="")
            else:
                showMsg(">",end="")
            cmd = input()
            if cmd == "help":
                self.help()
                continue
            elif cmd == "connect":
                self.connect()
                continue
            elif cmd == "disconnect":
                self.disconnect()
                continue
            else:
                if self.connected:
                    if cmd in self.cmd:

                        if cmd == "new" and self.new == False:
                            self.new = True
                        elif cmd == "new" and self.new == True:
                            showMsg("Have already in a game round")
                            continue
                        elif cmd == "end" and self.new == True:
                            self.new = False

                        self.send(self.cmd[cmd])
                    else:
                        showMsg("command error")
                        continue
                else:
                    showMsg("not connected to server")
                    continue
            buffer = self.soc.recv(204118)
            buffer = buffer.decode()
            res = json.loads(buffer)
            if res['status'] == 0:
                showMsg(res['message'])
            else:
                if len(res['message'])>19:
                    self.printSquare(res['message'])
                else:
                    showMsg(res['message'])
if __name__ == '__main__':
    if len(sys.argv) != 3:
        showMsg("Usage: python "+sys.argv[0]+" [server_ip] [server_port]")
        sys.exit(1)
    game = client_2048(sys.argv[1],int(sys.argv[2]))
    game.main()
        
    
