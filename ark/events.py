from ark.cli import *

class Events(object):
    E_CONNECT = 1
    E_DISCONNECT = 2
    E_CHAT = 3
    E_NEW_ARK_VERSION = 4
    E_NEW_PLAYER = 5
    E_CHAT_FROM_SERVER = 6

    _event_callbacks = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: []
    }
    
    @staticmethod
    def _valid_event_type(event_type):
        """Validate event type argument
        
        Constants E_* use integer
        """
        
        assert type(event_type) is int, 'Recommend using constants Events.E_*'
        if event_type not in range(1,5):
            raise TypeError('Unknown event type: {}. Recommend using constants Events.E_*'.format(event_type))
        
        
    @staticmethod
    def registerEvent(event_type,callback):
        """Register callback for event
        
        Args:
            event_type: of constant E_*
        
        Returns:
            None
        """
        
        Events._valid_event_type(event_type)
        if callable(callback) is False:
            raise TypeError('argument callback not callable()')
        
        Events._event_callbacks[event_type].append(callback)
        return None
            
    def _triggerEvent(event_type,*args):
        """Run by Arkon core code.
        
        Triggers event and runs all callbacks registered with registerEvent()
        
        Args:
            event_type: of constant E_*
        
        Returns:
            None
        """
        
        Events._valid_event_type(event_type)
        
        debug_out('Triggering event type: {} with {} callbacks'.format(event_type,len(Events._event_callbacks[event_type])),level=2)
        
        for callback in Events._event_callbacks[event_type]:
            callback(*args)
            
        return None