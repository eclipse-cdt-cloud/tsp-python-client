from enum import Enum

class VirtualTableTag(Enum):
    '''
    Tag is a bit mask to apply for tagging elements (e.g. table lines, states).
    This can be used by the server to indicate if a filter matches and what action to apply.
    '''

    '''
    Simply no tags
    '''
    NO_TAGS = 'NO_TAGS'

    '''
    Some tags are reserved for the server
    '''
    RESERVED = 'RESERVED'

    '''
    Border tag
    '''
    BORDER = 'BORDER'

    '''
    Highlight tag
    '''
    HIGHLIGHT = 'HIGHLIGHT'
