# brutect

**Détecte la force brute SSH dans un `auth.log`.**

`brutect` lit un journal d'authentification Linux et répond en une commande à trois questions :

- Quelles IP ont tenté de deviner un mot de passe SSH (force brute) ?
- Quels comptes ont-elles visés, dont `root` et les comptes qui n'existent pas ?
- L'une d'elles a-t-elle fini par se connecter (**compromission probable**) ?

C'est une analyse a posteriori d'un fichier, pratique pour un exercice de forensique, un CTF ou un contrôle de son propre serveur. Elle ne surveille rien en temps réel.

## Installation

Binaire pour **Linux x86_64**, statique : il ne dépend d'aucune bibliothèque et tourne sur n'importe quelle distribution.

```bash
curl -LO https://github.com/leudjoh/projets-publics/raw/main/Rust/brutect/brutect
curl -LO https://github.com/leudjoh/projets-publics/raw/main/Rust/brutect/brutect.sha256
sha256sum -c brutect.sha256      # doit afficher : brutect: OK
chmod +x brutect
sudo mv brutect /usr/local/bin/  # facultatif, pour le lancer de n'importe où
```

## Utilisation

```
brutect [--seuil N] [--fenetre SECONDES] [--json] <FICHIER | ->
```

| Option | Rôle | Par défaut |
|---|---|---|
| `--seuil N` | Nombre d'échecs à partir duquel une IP est signalée | 5 |
| `--fenetre SECONDES` | Durée maximale entre le premier et le dernier de ces échecs | 60 |
| `--json` | Rapport en JSON au lieu du texte | |
| `-` | Lit l'entrée standard au lieu d'un fichier | |

Le fichier peut être en texte ou compressé en gzip (`.gz`) : `brutect` le reconnaît tout seul.

Code de sortie : `0` si l'analyse aboutit, avec ou sans détection ; `1` en cas d'erreur (fichier absent, gzip corrompu, option invalide).

## Exemple

```
$ brutect /var/log/auth.log
Force brute détectée : 2 IP (seuil 5 échecs en 60 s)

203.0.113.7        8 échecs  Oct 23 09:15:03 → Oct 23 09:15:24  [ROOT]
  utilisateurs : admin (inexistant), oracle (inexistant), root, test (inexistant)

2001:db8::42       6 échecs  Oct 23 11:00:00 → Oct 23 11:00:25
  utilisateurs : pi (inexistant)

Compromissions probables : 1
  Oct 23 09:16:02  203.0.113.7  connexion acceptée pour root (password)

Lignes ignorées : 1
```

- `[ROOT]` : l'IP a visé le compte `root`.
- `(inexistant)` : le compte n'existe pas sur le serveur, signe d'une liste de noms essayés au hasard.
- **Compromission probable** : une connexion acceptée depuis une IP signalée, après le moment où elle a atteint le seuil.
- **Lignes ignorées** : les lignes `sshd` que l'outil n'a pas comprises, pour savoir ce qui a échappé à l'analyse.

## Analyser plusieurs fichiers

Sur Ubuntu et Debian, le journal est découpé chaque semaine : `auth.log` (en cours), `auth.log.1` (semaine précédente), `auth.log.2.gz`, etc. Une attaque peut être coupée en deux par ce découpage. Pour tout analyser d'un coup, du plus ancien au plus récent :

```bash
zcat -f /var/log/auth.log.2.gz /var/log/auth.log.1 /var/log/auth.log | brutect -
```

Lire `/var/log/auth.log` demande d'être dans le groupe `adm` ou d'utiliser `sudo`.

## Ce que l'outil reconnaît

- Les lignes `sshd` : `Failed password`, `Invalid user` et `Accepted` (mot de passe, clé publique…).
- Les dates au format syslog classique (`Oct 23 09:15:03`) ou ISO 8601 avec fuseau (`2026-10-23T09:15:03+02:00`).
- Les adresses IPv4 et IPv6.
- Les fichiers non triés et les octets invalides, sans planter.

Le rapport texte neutralise les caractères de contrôle venus du log : un nom d'utilisateur piégé ne peut pas injecter de séquence dans votre terminal.

## Comment il a été fait

Je ne connaissais pas Rust en commençant ce projet. `brutect` a été développé avec **Claude (IA)**, l'assistant d'Anthropic : j'ai tenu le rôle de Product Owner (définir le besoin, valider les plans, accepter ou refuser chaque étape) et Claude a écrit le code et les tests. Chaque étape a été relue par une autre instance de Claude que celle qui avait écrit le code.

Rust se prête bien à ce travail avec une IA : son compilateur, très strict, refuse un programme dès qu'une erreur de type, de mémoire ou un cas oublié est détecté, et explique précisément pourquoi. L'IA corrige ainsi ses erreurs avant même de lancer le programme, et ce qui compile a déjà passé de nombreuses vérifications.

Merci à **SFEIR** d'avoir partagé [sa méthode de travail avec l'IA](https://github.com/clubgenai/workshop-software-development-life-cycle) (cadrer, construire, relire, livrer, capitaliser). C'est elle qui m'a permis de livrer un binaire fonctionnel et testé dans un langage que je ne connaissais pas.

## Licence

[MIT](LICENSE)
