from ark.scheduler import Scheduler
from ark.cli import *
from ark.server_control import ServerControl
from ark.events import Events

class Task_CheckForUpdates(Scheduler):
    def run(self):
        if ServerControl.new_version() is True:
            Events._triggerEvent(Events.E_NEW_ARK_VERSION)
        else:
            debug_out('No server update available',level=3)