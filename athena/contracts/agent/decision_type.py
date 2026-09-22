from enum import Enum

class DecisionType(Enum):
    """ Represents the various types of decisions 
        an agent can make. """

    ANSWER = "answer"
    TOOL = "tool"
    SKILL = "skill"
    ASK_USER = "ask_user"
    DELEGATE = "delegate"
    STOP = "stop"