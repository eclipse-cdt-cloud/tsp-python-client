from enum import Enum

class IndexingStatus(Enum):
    '''
    Model is partial, data provider is still computing. If this status is
    returned, it's viewer responsability to request again the data provider after
    waiting some time. Request data provider until COMPLETED status is received
    '''
    RUNNING = "RUNNING"

    '''
    Model is complete, no need to request data provider again
    '''
    COMPLETED = "COMPLETED"

    '''
    
    '''
    CLOSED = "CLOSED"

