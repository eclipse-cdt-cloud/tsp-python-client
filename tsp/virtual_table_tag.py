from enum import Flag, auto

class VirtualTableTag(Flag):
    '''
    Tag is a bit mask to apply for tagging elements (e.g. table lines, states).
    This can be used by the server to indicate if a filter matches and what action to apply.
    '''

    '''
    Simply no tags
    '''
    NO_TAGS = 0

    '''
    Some tags are reserved for the server
    '''
    RESERVED_1 = auto()
    RESERVED_2 = auto()

    '''
    Border tag
    '''
    BORDER = auto()

    '''
    Highlight tag
    '''
    HIGHLIGHT = auto()
