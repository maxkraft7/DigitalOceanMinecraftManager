import digitalocean
from doToken import token  # private module that holds the digitalOcean access token
import sys


# my_droplets = manager.get_all_droplets()

# sshKeys = manager.get_all_sshkeys()


# latestSnapshot = manager.get_all_snapshots()[-1]

# manager.get_all_droplets()[0].take_snapshot()


# droplet = digitalocean.Droplet(name="Test", region="FRA",ssh_keys=sshKeys,size_slug='2048mb', backups=False, image=latestSnapshot)

# droplet.create()  # create new droplet

class digitalOceanManager:
    manager = False

    def __init__(self):


        if len(sys.argv) != 2:
            digitalOceanManager.printUsage()
        else:
            # init do-API
            self.manager = digitalocean.Manager(token=token.get("API_KEY"))

            if sys.argv[1] == "start":
                self.startServer()
            elif sys.argv[1] == "stop":
                self.stopServer()
            else:
                digitalOceanManager.printUsage()

        pass

    @staticmethod
    def printUsage():
        print("USAGE: SRVMGR.exe start|stop")

    def __createDroplet(self):
        pass

    def __fetchSnapshot(self):
        pass

    def

    def startServer(self):
        print("starting..")
        # check if droplet is already running, then abort
        if len(self.manager.get_all_droplets()) > 0:
            print("")

        # get latest snapshot

        # create droplet based on it

        # delete snapshot

        pass

    def stopServer(self):
        print("Stopping..")
        # check if a droplet is running, if not abort

        # get current droplet

        # create snapshot from droplet

        # destroy droplet

        pass


# process args
digitalOceanManager()
