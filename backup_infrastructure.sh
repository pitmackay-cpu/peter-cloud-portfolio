#!/usr/bin/env bash
#
# backup_infrastructure.sh
# ========================
# Sauvegarde hors-site des services du VPS peter-cloud.com.
#
# Contexte : le VPS (Ubuntu 24.04) héberge Nginx Proxy Manager et
# AdGuard Home en conteneurs Docker. Ce script, exécuté SUR LE VPS,
# archive leurs configurations puis réplique l'archive vers le serveur
# de sauvegarde du lab local, à travers le tunnel WireGuard site-à-site
# (aucun transfert ne transite en clair sur Internet).
#
# Démontre : robustesse shell, journalisation, vérifications préalables,
# gestion des codes de retour et nettoyage automatique.
#
# Usage :
#   sudo ./backup_infrastructure.sh
#
# Planification (crontab root, tous les jours à 03h15) :
#   15 3 * * * /opt/scripts/backup_infrastructure.sh >> /var/log/backup.log 2>&1
#
# Auteur : Peter Mackay — peter-cloud.com
# ---------------------------------------------------------------------------

# Mode strict :
#   -e : arrêt immédiat en cas d'erreur d'une commande
#   -u : erreur si une variable non définie est utilisée
#   -o pipefail : un pipe échoue si l'une de ses commandes échoue
set -euo pipefail

# --------------------------------------------------------------------------- #
# Configuration (à adapter à l'environnement)
# --------------------------------------------------------------------------- #

# Répertoires sources sur le VPS.
readonly NPM_DATA_DIR="/opt/npm/data"               # config + base NPM
readonly NPM_LETSENCRYPT_DIR="/opt/npm/letsencrypt" # certificats TLS
readonly ADGUARD_CONF_DIR="/opt/adguard/conf"       # configuration AdGuard
readonly COMPOSE_DIR="/opt/compose"                 # fichiers docker-compose

# Répertoire de travail local pour les archives temporaires.
readonly STAGING_DIR="/tmp/peter-cloud-backup"

# Destination : serveur de sauvegarde du lab, joint via le tunnel
# WireGuard (adresse interne du VPN — jamais l'IP publique).
readonly REMOTE_USER="backup"
readonly REMOTE_HOST="10.8.0.2"     # pair WireGuard côté lab
readonly REMOTE_PORT="22"
readonly REMOTE_DIR="/srv/backups/vps"

# Journalisation et rétention.
readonly LOG_FILE="/var/log/backup_infrastructure.log"
readonly RETENTION_DAYS=7   # purge des archives locales plus anciennes

# Horodatage utilisé pour nommer l'archive.
readonly TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
readonly ARCHIVE_NAME="vps_peter-cloud_${TIMESTAMP}.tar.gz"

# --------------------------------------------------------------------------- #
# Fonctions utilitaires
# --------------------------------------------------------------------------- #

# Écrit un message horodaté à la fois sur stdout et dans le fichier de log.
log() {
    local level="$1"; shift
    local message="$*"
    local line
    line="$(date '+%Y-%m-%d %H:%M:%S') [${level}] ${message}"
    echo "${line}"
    echo "${line}" >> "${LOG_FILE}" 2>/dev/null || true
}

# Affiche une erreur puis quitte avec un code de sortie donné.
die() {
    local code="$1"; shift
    log "ERREUR" "$*"
    exit "${code}"
}

# Supprime le répertoire de staging temporaire (appelé via trap).
cleanup() {
    if [[ -d "${STAGING_DIR}" ]]; then
        rm -rf "${STAGING_DIR}"
        log "INFO" "Répertoire temporaire nettoyé : ${STAGING_DIR}"
    fi
}

# Vérifie qu'une commande externe requise est disponible.
require_command() {
    local cmd="$1"
    if ! command -v "${cmd}" >/dev/null 2>&1; then
        die 3 "Commande requise introuvable : ${cmd}"
    fi
}

# Vérifie qu'un répertoire source existe ; avertit sinon (non bloquant).
check_source_dir() {
    local dir="$1"
    if [[ -d "${dir}" ]]; then
        log "INFO" "Source présente : ${dir}"
        return 0
    fi
    log "AVERT" "Source absente, ignorée : ${dir}"
    return 1
}

# Vérifie que le tunnel WireGuard est actif avant de tenter le transfert.
check_wireguard_peer() {
    log "INFO" "Test de joignabilité du pair WireGuard (${REMOTE_HOST}) ..."
    if ping -c 1 -W 3 "${REMOTE_HOST}" >/dev/null 2>&1; then
        log "INFO" "Tunnel WireGuard opérationnel."
    else
        die 6 "Pair WireGuard injoignable — tunnel down ? (wg show)"
    fi
}

# Nettoyage garanti même en cas d'interruption (Ctrl-C, kill).
trap cleanup EXIT INT TERM

# --------------------------------------------------------------------------- #
# Étapes de sauvegarde
# --------------------------------------------------------------------------- #

# 1) Vérification des prérequis (binaires nécessaires).
check_prerequisites() {
    log "INFO" "Vérification des prérequis ..."
    require_command tar
    require_command rsync
    require_command ssh
    require_command ping
    log "INFO" "Prérequis OK."
}

# 2) Création de l'archive tar.gz à partir des sources existantes.
create_archive() {
    mkdir -p "${STAGING_DIR}"

    # Liste dynamique des sources réellement présentes sur la machine.
    local sources=()
    check_source_dir "${NPM_DATA_DIR}"        && sources+=("${NPM_DATA_DIR}")
    check_source_dir "${NPM_LETSENCRYPT_DIR}" && sources+=("${NPM_LETSENCRYPT_DIR}")
    check_source_dir "${ADGUARD_CONF_DIR}"    && sources+=("${ADGUARD_CONF_DIR}")
    check_source_dir "${COMPOSE_DIR}"         && sources+=("${COMPOSE_DIR}")

    if [[ ${#sources[@]} -eq 0 ]]; then
        die 4 "Aucune source à sauvegarder n'a été trouvée."
    fi

    local archive_path="${STAGING_DIR}/${ARCHIVE_NAME}"
    log "INFO" "Création de l'archive : ${archive_path}"

    if tar -czf "${archive_path}" "${sources[@]}" 2>>"${LOG_FILE}"; then
        log "INFO" "Archive créée ($(du -h "${archive_path}" | cut -f1))."
    else
        die 5 "Échec de la création de l'archive tar."
    fi

    echo "${archive_path}"
}

# 3) Transfert via rsync over SSH, à travers le tunnel WireGuard.
transfer_archive() {
    local archive_path="$1"

    log "INFO" "Transfert vers ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"

    # Préparation du répertoire distant.
    if ! ssh -p "${REMOTE_PORT}" "${REMOTE_USER}@${REMOTE_HOST}" \
            "mkdir -p '${REMOTE_DIR}'" 2>>"${LOG_FILE}"; then
        die 7 "Impossible de préparer le répertoire distant (SSH)."
    fi

    # -a archive, -z compression, --partial reprise sur coupure.
    if rsync -az --partial \
            -e "ssh -p ${REMOTE_PORT}" \
            "${archive_path}" \
            "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/" \
            2>>"${LOG_FILE}"; then
        log "INFO" "Transfert réussi."
    else
        die 8 "Échec du transfert rsync."
    fi
}

# 4) Rotation côté distant : suppression des archives trop anciennes.
rotate_remote_backups() {
    log "INFO" "Rotation distante (> ${RETENTION_DAYS} jours) ..."
    if ssh -p "${REMOTE_PORT}" "${REMOTE_USER}@${REMOTE_HOST}" \
            "find '${REMOTE_DIR}' -type f -name '*.tar.gz' \
             -mtime +${RETENTION_DAYS} -delete" 2>>"${LOG_FILE}"; then
        log "INFO" "Rotation effectuée."
    else
        # Non bloquant : la sauvegarde du jour a réussi.
        log "AVERT" "Rotation distante échouée (à vérifier manuellement)."
    fi
}

# --------------------------------------------------------------------------- #
# Programme principal
# --------------------------------------------------------------------------- #

main() {
    log "INFO" "===== Démarrage de la sauvegarde VPS peter-cloud.com ====="

    check_prerequisites
    check_wireguard_peer

    local archive_path
    archive_path="$(create_archive)"

    transfer_archive "${archive_path}"
    rotate_remote_backups

    log "INFO" "===== Sauvegarde terminée avec succès ====="
    # cleanup() est appelé automatiquement via le trap EXIT.
    exit 0
}

main "$@"
