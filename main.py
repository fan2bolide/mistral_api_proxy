import socket

from log import log, logs
import mistral as mst


def send_message(msg):
    log(logs.send, msg, fd=client_address)
    client_socket.send(msg.encode('utf-8'))


if __name__ == '__main__':
    log(logs.title, "Start Mistral API interface")
    messages = {}

    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = '0.0.0.0', 1312
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(1)
        log(logs.event, f"Server listening on {host}:{port}, waiting for connection...")
        client_socket, client_address = server_socket.accept()

        log(logs.event, f"Connected to {client_address}")
        while True:
            messages_received = client_socket.recv(1024).decode()
            if not messages_received:
                log(logs.eventclose, f"Connection closed {client_address}")
                server_socket.close()
                break

            for message_received in messages_received.split("\r\n"):
                if not message_received:
                    continue
                log(logs.receive, message_received, fd=client_address)
                first_part, message = message_received.split(" :", 1)

                args = first_part.split(" ")
                if len(args) == 3:
                    target = args[0]
                    message = args[1] + ": " + message
                    is_request = args[2] == "REQUEST"
                else:
                    message = args[0] + ": " + message
                    target = first_part
                    is_request = True

                if target not in messages:
                    log(logs.event, f"Create new message history for {target}")
                    messages[target] = mst.create_new_prompt(len(args) == 3)
                messages[target].append(mst.ChatMessage(role="user", content=message))
                if is_request:
                    mistral_response = mst.request(messages[target])
                    messages[target].append(mistral_response)
                    try:
                        send_message(target + " :" + mistral_response.content)
                    except Exception as e:
                        log(logs.error, str(e), type_error="Error sending mistral response")
                        server_socket.close()
                        break
