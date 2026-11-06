# Détecteur de brute force ssh

## Description
Extrait les ip d'un fichier de log linux et les trie en fonction du nombre de tentatives de connexion pour mettre en évidence les tentatives de brute force.
Il écrit trois rapports (txt, csv et json). Si un de ces rapports est déjà présent, le script refuse de s'exécuter.

## Utilisation
```
python3 brute_detector.py fichier.log [options]
```
- --force force l'exécution du script si un fichier de rapport est déjà présent.
- --threshold définit le seuil pour l'inscription des IPs dans le rapport

## Exemples
```
$ python3 brute_detector.py auth_sample.log
Analysis date: 2026-11-05T10:50:25
Rapport de comptage d'ip sur le fichier auth_sample.log :
203.0.113.45, 10x
192.168.1.20, 4x
198.51.100.7, 2x
192.0.2.99, 2x
192.168.1.30, 1x

$ python3 brute_detector.py auth_sample.log
Pas de rapports générés :
Le(s) fichier(s) report.txt, report.csv et report.json déjà présent(s), utiliser --force pour écraser.
```

## Fichiers
- auth_sample.log
- brute_detector.py
- README.md
