"""ARK Survival RCON Interface. Connect, authenticate and transmit data to your favorite ARK Server.

by Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

Class initialization requires host,port and password and will connect to the server unless specified.
Upon connecting commences authentication.

Through class inheritance you will not need to change core code (steam_socket, steam_socket_core class).
You can just add same name function to this class and use super().function()
This way you can alter without fearing breaking the core functionality.

For easy reading of code all transmittable RCON commands are in class RconCommands
The RCON class is simply just a collection of helper functions and a wrapper for core code.
"""

from ark.rcon_commands import RconCommands
from ark.steam.source_server_query import ArkSourceQuery
from .cli import *
from .thread_handler import ThreadHandler
from ark.storage import Storage
from ark.events import Events
from ark.database import Db


class Rcon(RconCommands):

    @staticmethod
    def is_admin(steam_id=None, steam_name=None):
        player = Db.find_player(steam_id=steam_id, steam_name=steam_name)
        if not player:
            return False

        if player.admin:
            return True
        return False

    @classmethod
    def reconnect(cls):
        Events.triggerEvent(Events.E_DISCONNECT, Storage.players_online)
        Storage.players_online = {}
        super().reconnect()

    @staticmethod
    def find_online_steam_id(steam_name=None):
        for steam_id, name in Storage.players_online.items():
            if steam_name == name:
                return steam_id
        return None

    @classmethod
    def debug_compare_packet_count(cls):
        out("{} incoming packets and {} outgoing packets".format(len(Rcon.incoming_packets),len(Rcon.outgoing_packets)))
        
    @classmethod
    def init(cls,host,port,password,timeout=None):
        if host is None or port is None:
            raise TypeError("Please initialize the rcon module with host and port")
        if password is None:
            raise TypeError("Please provide rcon password")

        result, err = cls.socket_connect(host,port,password,timeout)
        if not result:
            cls.reconnect()
        ThreadHandler.create_thread(cls.loop_communication)

    @classmethod
    def response_callback_default(cls, packet):
        out('> {}\n[Response]: {}'.format(packet.outgoing_command,packet.decoded["body"].strip()))

    @classmethod
    def response_callback_response_only(cls,packet):
        out('[Response]: {}'.format(packet.decoded["body"].strip()))

    @classmethod
    def none_response_callback(cls,packet):
        pass

    @staticmethod
    def query_server():
        Storage.query_data = ArkSourceQuery.query_info(Config.rcon_host,Config.query_port)
