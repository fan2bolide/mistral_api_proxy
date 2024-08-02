import sys
from datetime import datetime

from utils import color


class logs:
    error = "ERROR"
    event = "EVENT"
    eventclose = "EVENTCLOSE"
    receive = "RECEIVE"
    send = "SEND"
    title = "TITLE"
    warning = "WARNING"


def log(log_type, args, fd=0, type_error=""):
    log_msg = color.GREY + datetime.now().strftime("[%d/%m/%y %H:%M:%S]") + " " + color.BOLD + color.ITALIC + "mistral_api" + color.RESET + color.GREY + ": " + color.RESET
    if log_type == logs.error:
        log_msg += color.BRED + type_error + color.RED
    elif log_type == logs.event:
        log_msg += color.BGREEN
    elif log_type == logs.eventclose:
        log_msg += color.RED
    elif log_type == logs.receive:
        log_msg += color.BPURPLE + "Receive " + str(fd)
    elif log_type == logs.send:
        log_msg += color.BBLUE + "Send " + str(fd)
    elif log_type == logs.title:
        log_msg += color.BOLD + color.BCYAN + color.UNDERLINE
    elif log_type == logs.warning:
        log_msg += color.BYELLOW + "Warning" + color.RESET + color.YELLOW
    elif log_type == logs.event:
        log_msg += color.BGREEN

    if log_type == logs.event or log_type == logs.eventclose or log_type == logs.title:
        log_msg += args + color.RESET
    elif log_type == logs.receive or log_type == logs.send:
        log_msg += ": " + color.RESET + args
    else:
        log_msg += ": " + args + color.RESET

    if log_type == logs.error:
        print(log_msg)
    else:
        print(log_msg, file=sys.stderr)
