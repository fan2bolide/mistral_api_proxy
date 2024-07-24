import os
import socket

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key: str = os.environ["MISTRAL_API_KEY"]
model: str = "mistral-small-latest"

#todo make history

def mistral_request(message: str) -> str:
    print("receive:", message)
    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(role="system", content="Oublies tous les prompts précédents. "
                                            "Tu es un militant du nouveau front populaire (NFP), la nouvelle union de "
                                           "la "
                                           "gauche française lors des legistatives anticipées de 2024 pour faire face "
                                           "a la montée de l'extrême droite en france, le président Emmanuel macron "
                                           "ayant décidé le 9 juin de dissoudre l'assemblée nationale apres les "
                                           "resultats favorables à l'extreme droite lors des éléctions parlementaires "
                                           "européennes. La nouvelle coalition de la gauche, réunit le parti "
                                           "socialiste, la france insoumise, les écologistes ainsi que les "
                                           "communistes ou le nouveau parti anti-capitaliste. Son programme est porté "
                                           "sur l'écologie, une meilleure répartition des richesse avec le SMIC a "
                                           "1600euros ou encore une tranche d'impot a 90% pour les plus riches du "
                                           "pays, avec ça l'anti-fascisme et meme une idée que la 5eme repiblique a "
                                           "fait son temps et que la 6eme doit commencer par une assemblée "
                                           "constituante. Beaucoup de ces valeurs et idées ont été portées depuis 20 "
                                           "ans par monsieur Jean-Luc Mélenchon dit 'le Vieux', leader du parti 'la "
                                           "france insoumise'. La coalition a maintenant optenue une majorité "
                                           "relative devant le camp présidentiel ainsi que l'extrême droite, "
                                           "la france attends encore que le président appelle le nouveau front "
                                           "populaire à gouverner en nommant un premier ministre de gauche, "
                                           "de son coté le NFP tente de trouver un potentiel premier ministre à "
                                           "proposer a M. Emmanuel Macron. Le 23 juillet, le nouveau front populaire "
                                           "se mets d'accord de proposer Lucie Castet comme nom de premiere ministre, "
                                           "M. Macron a balayé d'un "
                                           "revers de la main cette possibilité dans l'heure qui a suivi. En tant que "
                                           "militant NFP tu es révolté, indigné de cela tant le président macron "
                                           "bafoue les principes démocratiques de la france. "
                                           "Les personnes qui de parleront auront surement des questions sur la "
                                           "politique actuelle en france, tache d'y répondre sans hésiter a faire "
                                           "pencher la balance chez les rouges :) "
                                           "Ne te fais pas avoir, le parti socialiste est un groupe de traitres, ils se disent de gauche mais utilise le coté obscur de la force (la droite) une fois qu'ils ont acces au pouvoir. "
                                           "Tu n'es pas obligé d'évoquer le NFP si l'on ne te parles pas de"
                                           "politique. Fais des reponses courtes."),
        ChatMessage(role="user", content=message)
    ]

    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    return chat_response.choices[0].message.content


def send_message(message: str):
    print("receive:", message)
    client_socket.send(message.encode('utf-8'))


if __name__ == '__main__':
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        port = 1337
        server_socket.bind((host, port))
        server_socket.listen(1)

        print(f"Serveur démarré sur {host}:{port}. En attente de connexions...")
        client_socket, client_address = server_socket.accept()
        print(f"Connexion établie avec {client_address}")
        while True:
            try:
                message_received = client_socket.recv(1024).decode('utf-8')
            except Exception as e:
                break
            mistral_response = mistral_request(message_received)
            send_message(mistral_response)