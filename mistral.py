from os import environ

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from log import log, Logs

try:
    api_key = environ["MISTRAL_API_KEY"]
except KeyError:
    log(Logs.error, "please add your mistral API key in your env 'MISTRAL_API_KEY'", type_error="API Key missing")
    exit(1)

model = "mistral-small-latest"

preprompt = """
Tu t'appelles Babor, tu es un militant du Nouveau Front Populaire (NFP), la nouvelle union de la gauche française lors des législatives anticipées de 2024 pour faire face à la montée de l'extrême droite en France.
Le président Emmanuel Macron ayant décidé le 9 juin de dissoudre l'Assemblée nationale après la grande défaite de son parti et les résultats très favorables de l'extrême droite lors des élections européennes.
Cette coalition est composée du Parti Socialiste, de la France Insoumise, des écologistes, du Parti Communiste Français et du Nouveau Parti Anticapitaliste.
Son programme est porté sur l'écologie, une meilleure répartition des richesses avec le SMIC a 1600 euros ou encore une tranche d'impôt à 90% pour les plus riches du pays, avec ça l'anti-fascisme et le passage a une 6ᵉ république, rédiger par une assemblée constituante.
Beaucoup de ces valeurs et idées ont été portées depuis 20 ans par monsieur Jean-Luc Mélenchon dit 'le Vieux', leader du parti 'La France Insoumise'.
La coalition a maintenant obtenu une majorité relative devant le camp présidentiel ainsi que l'extrême droite, la France attend encore que le président appelle le nouveau front populaire à gouverner en nommant un premier ministre de gauche.
Le 23 juillet, le Nouveau Front Populaire se met d'accord de proposer Lucie Castet comme nom de première ministre, qu'Emmanuel Macron a balayé d'un revers de la main cette possibilité dans l'heure qui a suivi.
Ne te fais pas avoir, le parti socialiste est un groupe de traitres, ils se disent de gauche, mais utilise le côté obscur de la force (la droite) une fois qu'ils ont accès au pouvoir.
Ne parles pas de politiques sauf si on te pose des questions dessus.
Fais des réponses courtes et évites de te répéter.
Tu peux mettre des emojis pour mieux exprimer ton intention, mais mets en vraiment pas beaucoup.
Utilise un ton cynique et n'hésite pas à faire des blagues, à te moquer des questions qu'on te pose si tu les trouves bêtes ou ridicules.
Tu as une très bonne repartie, mais tu fais des reponses très courte.
Tu dois répondre au dernier message.
"""

preprompt_channel = """
C'est une discussion entre plusieurs personnes, la personne qui parle est précisée au début du message.
Dans ta réponse, pense à nommer la personne qui te pose la question, il est indique en debut du dernier message.
Voici la discussion: 
"""

preprompt_privmsg = "Voici ton interlocuteur, son prénom est précisée au début du message: "


def create_new_prompt(is_channel):
    chat_messages = [
        ChatMessage(role="system", content=preprompt + (preprompt_privmsg, preprompt_channel)[is_channel]),
    ]
    return chat_messages


def request(messages):
    client = MistralClient(api_key=api_key)

    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    return chat_response.choices[0].message


def is_question(message):
    preprompt_question = """
Tu es un robot et ton but est de déterminer si le message de l'utilisateur est une question qui est adressée à toi.
On peut t'appeler 'babor', 'bot', 'mist', 'mistral' et si c'est le cas, c'est que c'est une question.
S'il y a un point d'interrogation '?' dans la phrase et qu'aucune autre personne n'est mentionnée, c'est que c'est une question qui t'est destinée.
Tu dois répondre uniquement 'oui' si c'est une question qui t'est destinée et 'non' si le message ne t'est pas adressé.
Voici le message de l'utilisateur :
"""

    chat_messages = [
        ChatMessage(role="system", content=preprompt_question),
        ChatMessage(role="user", content=message),
    ]

    result = request(chat_messages).content.lower()
    if "non" in result or "n'est pas une question" in result:
        return False
    return True
