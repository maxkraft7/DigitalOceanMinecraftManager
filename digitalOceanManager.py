from time import strftime

import digitalocean
from doToken import token  # private module that holds the digitalOcean access token
import sys
from datetime import datetime


# my_droplets = manager.get_all_droplets()

# sshKeys = manager.get_all_sshkeys()


# latestSnapshot = manager.get_all_snapshots()[-1]

# manager.get_all_droplets()[0].take_snapshot()


# droplet = digitalocean.Droplet(name="Test", region="FRA",ssh_keys=sshKeys,size_slug='2048mb', backups=False, image=latestSnapshot)

# droplet.create()  # create new droplet

class digitalOceanManager:
    manager = False
    dropletRunning = False
    prefix = 'MC-'

    def __init__(self):

        if len(sys.argv) != 2:
            digitalOceanManager.printUsage()
        else:
            # init do-API
            self.manager = digitalocean.Manager(token=token.get("API_KEY"))

            # check if at least one droplet is running
            self.dropletRunning = self.__countDropletsWithPrefix(self.prefix) > 0

            if sys.argv[1] == "start":
                if self.dropletRunning:
                    print("Droplet is already running, no need to start it")
                else:
                    self.startServer()
            elif sys.argv[1] == "stop":
                if not self.dropletRunning:
                    print("Droplet isn't running, can't be stopped")
                else:
                    self.stopServer()
            else:
                digitalOceanManager.printUsage()

        pass

    @staticmethod
    def printUsage():
        print("USAGE: SRVMGR.exe start|stop")

    def __createDroplet(self):
        pass

    def __fetchSnapshot(self,prefix):
        snapshots = self.manager.get_all_snapshots()
        for snapshot in snapshots:
            if snapshot.name.startswith(prefix):
                return snapshot

        return False


    # def

    def startServer(self):
        print("starting..")

        # get latest snapshot, with given prefix
        snapshot = self.__fetchSnapshot(self.prefix)

        keys = self.manager.get_all_sshkeys()

        #print(self.manager.get_all_regions())

        # create droplet based on it



        droplet = digitalocean.Droplet(token=self.manager.token,
                                       name=self.prefix+"DROPLET-"+self.__getTimeString(),
                                       region='fra1',  # Frankfurt
                                       # https://www.digitalocean.com/community/questions/create-droplet-from-snapshot-by-rest-api
                                       image=snapshot.id,  # current latest snapshot
                                       size_slug='s-2vcpu-4gb',  # 1GB RAM, 1 vCPU
                                       ssh_keys=keys,  # Automatic conversion
                                       backups=False)
        droplet.create()


        # delete snapshot
        snapshot.destroy()
        pass

    def __countDropletsWithPrefix(self, prefix):
        amount = 0
        droplets = self.manager.get_all_droplets()

        for droplet in droplets:
            if droplet.name.startswith(prefix):
                amount += 1

        return amount

    """
        :returns the first droplet with a given prefix
    """

    def __getDropletWithPrefix(self, prefix):
        droplets = self.manager.get_all_droplets()

        for droplet in droplets:
            if droplet.name.startswith(prefix):
                return droplet

    def __getTimeString(self):
        now = datetime.now()
        nowstring = now.strftime("%m-%d-%Y--%H-%M-%S")
        return nowstring

    def __takeSnapshotAndDestroy(self, droplet, prefix):
        droplet.shutdown()
        droplet.take_snapshot(prefix + 'snapshot-' + self.__getTimeString())
        droplet.destroy()

        pass

    def stopServer(self):
        print("Stopping..")
        # check if a droplet is running, if not abort
        # print("running: "+ str(self.dropletRunning))
        if self.dropletRunning:
            # get current droplet with correft prefix
            targetDroplet = self.__getDropletWithPrefix(self.prefix)
            #print("target droplet: "+str(targetDroplet))
            self.__takeSnapshotAndDestroy(targetDroplet, self.prefix)


# process args
digitalOceanManager()
