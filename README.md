# davi.net.nodns

- [English](#operation)
- [Français](#fonctionnement)


### Operation

This daemon is for those who want to communicate with a computer that has only a dynamic public IP address. Start by running the daemon on the server. Here's what he'll do:

- Make a DNS request to OpenDNS requesting the address of "myip.opendns.com".
- OpenDNS will return the public IP address of the server.
- This public IP address will be sent to Pastebin using their API.
- The daemon will regularly request the public IP address and send it to Pastebin if it has changed since the last time.

All you have to do is retrieve the public IP address of the server either by using the Pastebin API or by going directly to Pastebin with your web browser.

### Configuration file

**/sources/settings.py** :

    |    Name    |   Type    |                                    Value                                           |
    | ---------- | ----------| ---------------------------------------------------------------------------------- |
    | devKey     |  String   |  Your unique developer API key, get it from https://pastebin.com/api#1             |
    | userKey    |  String   |  User key, get it from https://pastebin.com/api/api_user_key.html                  |
    | pasteName  |  String   |  The name that your post will have on pastebin.                                    |
    | TTS        |  Integer  |  Time to sleep, delay before reasking for public IP adress ; time is in minute     |

***

### Fonctionnement

Ce démon est destiné à ceux qui veulent communiquer avec un ordinateur ne disposant que d'une adresse IP publique dynamique. Commencez par lancer le démon sur le serveur. Voici ce qu'il va faire :

- Effectuer une requète DNS à OpenDNS demandant l'adresse de "myip.opendns.com".
- OpenDNS va renvoyer l'adresse IP publique du serveur.
- Cette adresse IP publique sera envoyé à Pastebin en utilisant leur API.
- Le démon demandera régulièrement l'adresse IP publique et l'enverra à Pastebin si elle à changée depuis la dernière fois.

Il ne vous reste plus qu'a récupérer l'adresse IP publique du serveur soit en utilisant l'API de Pastebin soit en vous rendant directement sur Pastebin avec votre navigateur Web.

### Fichier de configuration

**/sources/settings.py** :

    |    Nom     |         Type          |                                        Valeur                                         |
    | ---------- | ----------------------| ------------------------------------------------------------------------------------- |
    | devKey     |  Chaîne de caractère  |  Votre clef unique pour l'API developpeur, trouvez la sur  https://pastebin.com/api#1 |
    | userKey    |  Chaîne de caractère  |  Clé utilisateur, trouvez la sur https://pastebin.com/api/api_user_key.html           |
    | pasteName  |  Chaîne de caractère  |  Le nom qu'aura votre post sur Pastebin                                               |
    | TTS        |  Entier               |  Délai avant de retester l'adresse IP publique; Le temps est en minute                |
