import sys
from datetime import datetime

from utils.color import *


class Logs:
    close = "CLOSE"
    error = "ERROR"
    event = "EVENT"
    quit = "QUIT"
    receive = "RECEIVE"
    send = "SEND"
    title = "TITLE"
    warning = "WARNING"


def log(log_type, arg, target="", nickname="mistral", type_error=""):
    log_msg = GREY + datetime.now().strftime("[%d/%m/%y %H:%M:%S]") + " " + BOLD + ITALIC + "mistral_api" + RESET + GREY + ": " + RESET

    if log_type == Logs.close:
        log_msg += RED
    elif log_type == Logs.error:
        log_msg += BRED + type_error + RED
    elif log_type == Logs.event:
        log_msg += BGREEN
    elif log_type == Logs.event:
        log_msg += BGREEN
    elif log_type == Logs.quit:
        log_msg += BRED
    elif log_type == Logs.title:
        log_msg += BOLD + BCYAN + UNDERLINE
    elif log_type == Logs.warning:
        log_msg += BYELLOW + "Warning" + RESET + YELLOW

    if log_type == Logs.close or log_type == Logs.event or log_type == Logs.title or log_type == Logs.quit:
        log_msg += arg
    elif log_type == Logs.receive or log_type == Logs.send:
        color, bcolor = ((BLUE, BBLUE), (PURPLE, BPURPLE))[log_type == Logs.send]
        log_msg += f"{color}[{trg_log(target, color)}] {cmd_log(nickname, bcolor, color)}"
        if arg != "join channel" and arg != "quit channel":
            log_msg += ":"
        log_msg += " " + arg
    else:
        log_msg += ": " + arg

    log_msg += RESET
    if log_type == Logs.error:
        print(log_msg)
    else:
        print(log_msg, file=sys.stderr)


def cmd_log(x, bcolor, color):
    return bcolor + ITALIC + x + RESET + color


def trg_log(x, color):
    return color + BOLD + x + RESET + color
