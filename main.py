import os
import socket
import threading

from log import *
import mistral as mst


# ---------- MAIN ---------------------------------------------------------------------------------------------------- #
def main_loop():
    host, port = '0.0.0.0', 1312

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    log(Logs.event, f"{GREEN}Server listening on {host}:{port}, waiting for connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        log(Logs.event, f"{GREEN}Connection to {BGREEN}{client_address[0]}:{client_address[1]}{RESET}{GREEN} accept !")
        client_thread = threading.Thread(target=bot_connection, args=(client_socket, client_address))
        client_thread.start()


def bot_connection(client_socket, client_address):
    messages = {}

    while True:
        messages_received = client_socket.recv(1024).decode()
        if not messages_received:
            log(Logs.close, f"Connection closed on {client_address[0]}:{client_address[1]}")
            break

        for message_received in messages_received.split("\r\n"):
            if not message_received:
                continue
            first_part, message = message_received.split(" :", 1)

            args = first_part.split(" ")
            if len(args) == 3:
                target = args[0]
                message_user = args[1]
                type_ = args[2]
            else:
                message_user = args[0]
                target = first_part
                type_ = "REQUEST"

            if target not in messages:
                log(Logs.event, f"{GREEN}Create new message history for {trg_log(target, GREEN)}")
                messages[target] = mst.create_new_prompt(len(args) == 3)

            if type_ == "JOIN":
                messages[target].append(mst.ChatMessage(role="user", content=message_user + " vient de rejoindre la discussion"))
                log(Logs.receive, "join channel", target, message_user)
            elif type_ == "PART":
                valid_message = message and message != "leave channel"
                messages[target].append(mst.ChatMessage(role="user", content=message_user + " vient de quitter la discussion" + ((" parce que: " + message) if valid_message else "")))
                log(Logs.receive, "quit channel" + (f": {message}" if valid_message else ""), target, message_user)
            else:
                messages[target].append(mst.ChatMessage(role="user", content=message_user + ": " + message))
                log(Logs.receive, message, target, message_user)

            if type_ == "REQUEST" or (type_ == "ADD" and mst.is_question(message)):
                mistral_response = mst.request(messages[target])
                messages[target].append(mistral_response)
                log(Logs.send, mistral_response.content, target)
                try:
                    client_socket.send((target + " :" + mistral_response.content).encode('utf-8'))
                except Exception as e:
                    log(Logs.error, str(e), type_error="Error sending mistral response")
                    break
    client_socket.close()


if __name__ == '__main__':
    log(Logs.title, f"Start {mist}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        main_loop()
    except KeyboardInterrupt as e:
        log(Logs.quit, f"Stop {mist} 🫡")
        server_socket.close()
        os._exit(0)
