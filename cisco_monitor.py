#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cisco_monitor.py
================

Supervision des interfaces d'un switch Cisco Catalyst 1000 via SSH.

Ce script se connecte au switch avec la bibliothèque Netmiko, exécute la
commande ``show interfaces status``, analyse le résultat et affiche un
rapport synthétique mettant en évidence les interfaces hors service.

Dépendances :
    pip install netmiko

Usage :
    python3 cisco_monitor.py            # utilise les variables ci-dessous
    SWITCH_PASSWORD=xxx python3 cisco_monitor.py   # mot de passe via env

Bonne pratique de sécurité : ne jamais committer un mot de passe en clair.
Le script lit donc d'abord la variable d'environnement SWITCH_PASSWORD ;
à défaut, il le demande de façon interactive (getpass).

Auteur : Peter — peter-cloud.com
"""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from getpass import getpass
from typing import List

# Imports Netmiko. On capture l'ImportError pour donner un message clair
# si la bibliothèque n'est pas installée.
try:
    from netmiko import ConnectHandler
    from netmiko.exceptions import (
        NetmikoAuthenticationException,
        NetmikoTimeoutException,
    )
except ImportError:
    sys.exit(
        "[ERREUR] La bibliothèque 'netmiko' est requise.\n"
        "         Installez-la avec : pip install netmiko"
    )


# --------------------------------------------------------------------------- #
# Configuration et journalisation
# --------------------------------------------------------------------------- #

# Configuration du logger : horodatage + niveau + message.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("cisco_monitor")


@dataclass
class SwitchConfig:
    """Paramètres de connexion au switch.

    L'utilisation d'une dataclass rend la configuration explicite et facile
    à étendre (ajout d'un port, d'un secret enable, etc.).
    """

    host: str
    username: str
    password: str
    device_type: str = "cisco_ios"  # Catalyst 1000 = IOS classique
    port: int = 22


@dataclass
class Interface:
    """Représente l'état d'une interface réseau du switch."""

    name: str
    status: str  # connected / notconnect / disabled ...
    vlan: str
    speed: str

    @property
    def is_down(self) -> bool:
        """Une interface est considérée 'down' si elle n'est pas connectée."""
        return self.status.lower() not in ("connected",)


# --------------------------------------------------------------------------- #
# Fonctions métier
# --------------------------------------------------------------------------- #

def build_config() -> SwitchConfig:
    """Construit la configuration de connexion.

    Le mot de passe est lu depuis la variable d'environnement
    SWITCH_PASSWORD, sinon demandé de manière interactive afin de ne jamais
    l'écrire en dur dans le code.
    """
    host = os.environ.get("SWITCH_HOST", "192.168.10.2")
    username = os.environ.get("SWITCH_USER", "admin")
    password = os.environ.get("SWITCH_PASSWORD") or getpass(
        f"Mot de passe SSH pour {username}@{host} : "
    )
    return SwitchConfig(host=host, username=username, password=password)


def fetch_interface_status(config: SwitchConfig) -> str:
    """Se connecte au switch et renvoie la sortie brute de la commande.

    La connexion est ouverte dans un bloc try/except afin de distinguer
    clairement les erreurs réseau (timeout) des erreurs d'authentification.
    La connexion est systématiquement fermée dans le bloc finally.
    """
    device = {
        "device_type": config.device_type,
        "host": config.host,
        "username": config.username,
        "password": config.password,
        "port": config.port,
        "fast_cli": False,  # plus robuste sur de vieux IOS
    }

    connection = None
    try:
        logger.info("Connexion SSH à %s ...", config.host)
        connection = ConnectHandler(**device)
        # 'show interfaces status' donne un tableau compact et parsable.
        output = connection.send_command("show interfaces status")
        logger.info("Commande exécutée avec succès.")
        return output

    except NetmikoTimeoutException:
        logger.error("Timeout : %s injoignable (réseau ou SSH fermé).",
                     config.host)
        raise
    except NetmikoAuthenticationException:
        logger.error("Authentification refusée pour %s.", config.username)
        raise
    except Exception as exc:  # filet de sécurité pour toute autre erreur
        logger.error("Erreur inattendue : %s", exc)
        raise
    finally:
        if connection is not None:
            connection.disconnect()
            logger.info("Connexion fermée.")


def parse_interfaces(raw_output: str) -> List[Interface]:
    """Transforme la sortie texte en une liste d'objets Interface.

    Format attendu (colonnes à largeur fixe) :
        Port      Name   Status       Vlan       Duplex  Speed Type
        Gi1/0/1          connected    10         a-full  a-1000 ...

    On ignore l'en-tête et les lignes vides, et on découpe sur les
    espaces multiples.
    """
    interfaces: List[Interface] = []

    for line in raw_output.splitlines():
        # On saute l'en-tête et les lignes vides.
        if not line.strip() or line.lower().startswith("port"):
            continue

        parts = line.split()
        if len(parts) < 4:
            continue  # ligne incomplète, on l'ignore prudemment

        # La colonne "Name" est optionnelle : on lit donc depuis la fin,
        # où Status / Vlan / Duplex / Speed sont positionnés de façon fiable.
        name = parts[0]
        # Heuristique simple : status est le champ qui suit le nom éventuel.
        # On reconstruit en se basant sur des valeurs de statut connues.
        known_status = {"connected", "notconnect", "disabled",
                        "err-disabled", "monitoring"}
        status = next((p for p in parts if p in known_status), parts[1])
        idx = parts.index(status)
        vlan = parts[idx + 1] if idx + 1 < len(parts) else "?"
        speed = parts[idx + 3] if idx + 3 < len(parts) else "?"

        interfaces.append(
            Interface(name=name, status=status, vlan=vlan, speed=speed)
        )

    return interfaces


def print_report(interfaces: List[Interface]) -> None:
    """Affiche un rapport lisible et un résumé des interfaces down."""
    if not interfaces:
        logger.warning("Aucune interface analysée.")
        return

    print("\n=== État des interfaces — Catalyst 1000 ===")
    print(f"{'Interface':<14}{'Statut':<14}{'VLAN':<8}{'Débit':<10}")
    print("-" * 46)
    for itf in interfaces:
        flag = "  <-- DOWN" if itf.is_down else ""
        print(f"{itf.name:<14}{itf.status:<14}{itf.vlan:<8}"
              f"{itf.speed:<10}{flag}")

    down = [i for i in interfaces if i.is_down]
    print("-" * 46)
    print(f"Total : {len(interfaces)} interfaces, "
          f"{len(down)} hors service.")
    if down:
        print("Interfaces à vérifier : "
              + ", ".join(i.name for i in down))


# --------------------------------------------------------------------------- #
# Point d'entrée
# --------------------------------------------------------------------------- #

def main() -> int:
    """Orchestration : config -> récupération -> parsing -> rapport.

    Renvoie un code de sortie Unix (0 = succès, 1 = erreur) pour pouvoir
    être intégré dans une chaîne de supervision ou un cron.
    """
    try:
        config = build_config()
        raw = fetch_interface_status(config)
        interfaces = parse_interfaces(raw)
        print_report(interfaces)
        return 0
    except KeyboardInterrupt:
        logger.warning("Interruption par l'utilisateur.")
        return 130
    except Exception:
        # L'erreur détaillée a déjà été journalisée plus bas dans la pile.
        logger.error("Échec de la supervision.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
