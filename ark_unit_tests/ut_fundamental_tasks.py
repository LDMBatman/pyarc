from ark.config import Config
Config.display_output = False
from ark.cli import *

def get_chat():
    from ark.fundamental_tasks import TaskResponses
    from ark.rcon_packet import Packet
    
    packet = Packet()
    packet.decoded['type'] = 2
    
    #One line
    packet.decoded['body'] = "Alpha (Alpha1): This is a line\n"
    lines = TaskResponses.get_chat(packet)
    if len(lines) == 0:
        print('Failed to parse text: ',packet.decoded['body'])
        return False
    line = lines.pop(0)
    if _get_chat_check_respones(line,'Alpha','Alpha1','This is a line','Alpha (Alpha1): This is a line') == False:
        return False
    
    #One line no linebreak
    packet.decoded['body'] = "Alpha (Alpha1): This is a line"
    lines = TaskResponses.get_chat(packet)
    if len(lines) == 0:
        print('Failed to parse text: ',packet.decoded['body'])
        return False
    line = lines.pop(0)
    if _get_chat_check_respones(line,'Alpha','Alpha1','This is a line','Alpha (Alpha1): This is a line') == False:
        return False
        
    #Several lines
    packet.decoded['body'] = "Alpha (Alpha1): This is a line\nBeta (Beta1): Another line\n"
    lines = TaskResponses.get_chat(packet)
    if len(lines) == 0:
        print('Failed to parse text: ',packet.decoded['body'])
        return False
    line = lines.pop(0)
    if _get_chat_check_respones(line,'Alpha','Alpha1','This is a line','Alpha (Alpha1): This is a line') == False:
        return False
    line = lines.pop(0)
    if _get_chat_check_respones(line,'Beta','Beta1','Another line','Beta (Beta1): Another line') == False:
        return False
    
    #Server message
    packet.decoded['body'] = "SERVER: I am the server\n"
    lines = TaskResponses.get_chat(packet)
    if len(lines) == 0:
        print('Failed to parse text: ',packet.decoded['body'])
        return False
    line = lines.pop(0)
    if _get_chat_check_respones(line,'SERVER','SERVER','I am the server','SERVER: I am the server') == False:
        return False
    
    return True
    #packet.decoded['body'] = "Beta (Beta1): This is another line\n"
    
def _get_chat_check_respones(result,steam_name, player_name, text, line):
    if result['steam_name'] != steam_name:
        print('Steam name failed: ', result['steam_name'])
        print('Tested against: ', steam_name)
        return False
    if result['player_name'] != player_name:
        print('Player name failed: ', result['player_name'])
        print('Tested against: ', player_name)
        return False
    if result['text'] != text:
        print('Text failed: ', result['text'])
        print('Tested against: ', text)
        return False
    if result['line'] != line:
        print('line failed: ', result['line'])
        print('Tested against: ', line)
        return False
    return True
        
def list_players():
    from ark.rcon_packet import Packet
    
    test_packet = Packet()
    
    test_packet.decoded['body'] = "1. Test Alpha, 10\n"
    if _list_player_check_response(test_packet,1,0,1) == False:
        return False
    
    test_packet.decoded['body'] = "1. Test Alpha, 10\n2. Test Beta, 11\n"
    if _list_player_check_response(test_packet,1,0,2) == False:
        return False
    
    test_packet.decoded['body'] = "1. Test Beta, 11\n2. Test Charlie, 12"
    if _list_player_check_response(test_packet,1,1,2) == False:
        return False
    
    test_packet.decoded['body'] = ""
    if _list_player_check_response(test_packet,0,2,0) == False:
        return False
    
    test_packet.decoded['body'] = "1. Test Beta, 11\n2. Test Charlie, 12"
    if _list_player_check_response(test_packet,2,0,2) == False:
        return False
    
    return True
        
def _list_player_check_response(packet,connected,disconnected,online):
    from ark.fundamental_tasks import TaskResponses
    
    c,d,o = TaskResponses.list_players(packet)

    if len(c) != connected:
        print('Failed. Wrong number of connected: ',packet.decoded['body'])
        return False
    elif len(d) != disconnected:
        print('Failed. Wrong number of disconnected: ',packet.decoded['body'])
        return False
    elif len(o) != online:
        print('Failed. Wrong number online: ',packet.decoded['body'])
        return False
    return True