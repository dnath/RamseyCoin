import Client
import Server
import sys

def main():
    isServer = int(sys.argv[1])

    # Start as client
    if isServer == 0:
        serverIP = sys.argv[2]
        Client.main(serverIP)

        while True:
            Client.main(serverIP)
            serverIP = Server.main()

    # Start as server
    else:
        while True:
            serverIP = Server.main()
            Client.main(serverIP)
