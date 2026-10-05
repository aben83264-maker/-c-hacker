import datetime
import json
import random
import string
import base64
import urllib.parse
import streamlit as st

# Configuration de la page web
st.set_page_config(page_title="Security Checker X-Hacker", page_icon="🛡️", layout="centered")

# Initialisation de l'historique dans la session web
if "historique_scans" not in st.session_state:
    st.session_state.historique_scans = []

base_vulnerabilites = {
    21: {"service": "FTP", "score": 7.5, "cve": "CVE-1999-0017", "faille": "Infiltration via canaux non chiffrés", "reco": "Migrer vers SFTP/FTPS."},
    22: {"service": "SSH", "score": 4.0, "cve": "CVE-2018-15473", "faille": "Énumération d'utilisateurs distante", "reco": "Désactiver l'accès root + Clés RSA."},
    23: {"service": "TELNET", "score": 10.0, "cve": "CVE-1999-0619", "faille": "Interception totale de mots de passe", "reco": "Remplacer immédiatement par SSH."},
    53: {"service": "DNS", "score": 2.5, "cve": "CVE-2008-1447", "faille": "Empoisonnement de cache DNS", "reco": "Restreindre le relais récursif."},
    80: {"service": "HTTP", "score": 5.0, "cve": "CWE-319", "faille": "Transmissions en texte clair", "reco": "Rediriger tout le trafic vers HTTPS (443)."},
    443: {"service": "HTTPS", "score": 1.0, "cve": "N/A", "faille": "Exposition minimale si TLS récent", "reco": "Maintenir les certificats TLS à jour."},
    8080: {"service": "HTTP-Alt", "score": 5.5, "cve": "CWE-16", "faille": "Interface d'administration mal configurée", "reco": "Restreindre l'accès par filtrage d'IP."}
}

def chiffrer_xor(texte, cle):
    texte_bytes = texte.encode('utf-8')
    cle_bytes = cle.encode('utf-8')
    resultat = bytearray()
    for i in range(len(texte_bytes)):
        resultat.append(texte_bytes[i] ^ cle_bytes[i % len(cle_bytes)])
    return base64.b64encode(resultat).decode('utf-8')

def dechiffrer_xor(texte_chiffre_b64, cle):
    try:
        texte_bytes = base64.b64decode(texte_chiffre_b64.encode('utf-8'))
        cle_bytes = cle.encode('utf-8')
        resultat = bytearray()
        for i in range(len(texte_bytes)):
            resultat.append(texte_bytes[i] ^ cle_bytes[i % len(cle_bytes)])
        return resultat.decode('utf-8')
    except Exception:
        return "[!] Erreur : Clé incorrecte ou données corrompues."

# --- INTERFACE WEB STREAMLIT ---

st.title("🛡️ Security Checker (X-Hacker)")
st.markdown("Plateforme interactive de simulation de cybersécurité offensive et défensive.")

# Menu latéral (Sidebar) pour choisir le module
menu = st.sidebar.selectbox("Sélectionner un module", [
    "1. Chiffrer un rapport",
    "2. Déchiffrer un rapport",
    "3. Base de données CVE",
    "4. Journal d'activité",
    "5. Générateur de mot de passe",
    "6. Analyseur de mot de passe",
    "7. Module OSINT Téléphone",
    "8. Interception web (Simulation)",
    "9. Scanner de ports",
    "10. Découverte Réseau / ARP",
    "11. Analyse d'URL (Phishing)",
    "12. Simulation SIEM (Logs)"
])

st.sidebar.markdown("---")
st.sidebar.markdown("✍️ *Signé : X-hacker*")

# --- LOGIQUE DES MODULES ---

if menu.startswith("1."):
    st.subheader("📁 Créer & Chiffrer un rapport X-Hacker")
    ip = st.text_input("IP cible à simuler", "192.168.1.10")
    cle = st.text_input("Clé secrète de chiffrement", "cle_par_defaut_securisee", type="password")
    if st.button("Générer et Chiffrer"):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rapport_texte = f"=== RAPPORT D'AUDIT SÉCURITÉ X-HACKER ===\nCible analysée : {ip}\nDate : {date_str}\nSignature : X-hacker (Web App)\n======================================="
        donnees_chiffrees = chiffrer_xor(rapport_texte, cle)
        st.success("Rapport chiffré avec succès !")
        st.code(donnees_chiffrees)
        st.session_state.historique_scans.append({"action": "Audit simulé", "cible": ip, "date": str(datetime.datetime.now())})

elif menu.startswith("2."):
    st.subheader("🔓 Déchiffrer un rapport")
    texte_chiffre = st.text_area("Colle le code chiffré (Base64)")
    cle_dec = st.text_input("Entre la clé secrète", type="password")
    if st.button("Déchiffrer"):
        res = dechiffrer_xor(texte_chiffre, cle_dec)
        st.text_area("Résultat en clair", res)

elif menu.startswith("3."):
    st.subheader("🔍 Base de données CVE locale")
    port = st.number_input("Numéro de port à interroger", value=80, step=1)
    if port in base_vulnerabilites:
        info = base_vulnerabilites[port]
        st.write(f"**Service:** {info['service']}")
        st.write(f"**Score de risque:** {info['score']}/10")
        st.write(f"**Référence CVE:** {info['cve']}")
        st.write(f"**Description:** {info['faille']}")
        st.write(f"**Recommandation:** {info['reco']}")
    else:
        st.info("Aucun détail enregistré pour ce port.")

elif menu.startswith("4."):
    st.subheader("📋 Journal d'activité sécurisé")
    if not st.session_state.historique_scans:
        st.info("Aucun événement enregistré pour l'instant.")
    else:
        st.json(st.session_state.historique_scans)

elif menu.startswith("5."):
    st.subheader("🔑 Générateur de mot de passe fort")
    longueur = st.slider("Longueur souhaitée", 8, 32, 16)
    if st.button("Générer"):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        mdp = ''.join(random.choice(chars) for _ in range(longueur))
        st.code(mdp)

elif menu.startswith("6."):
    st.subheader("📊 Analyseur de robustesse de mot de passe")
    mdp_test = st.text_input("Mot de passe à tester", type="password")
    if mdp_test:
        score = sum([len(mdp_test) >= 8, any(c.isupper() for c in mdp_test), any(c.islower() for c in mdp_test), any(c.isdigit() for c in mdp_test), any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in mdp_test)])
        st.write(f"Score de robustesse : **{score} / 5**")
        if score == 5: st.success("🟢 Mot de passe très fort !")
        elif score >= 3: st.warning("🟡 Mot de passe moyen.")
        else: st.error("🔴 Mot de passe faible !")

elif menu.startswith("7."):
    st.subheader("📱 Module OSINT : Profilage Téléphonique")
    tel = st.text_input("Numéro de téléphone (ex: +33612345678)")
    if st.button("Lancer le profilage"):
        if tel.startswith("+"):
            pays = "France" if tel.startswith("+33") else "International"
            ip_associee = f"197.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            st.write(f"🌍 Pays : {pays}")
            st.write(f"🌐 Passerelle IP : {ip_associee}")
            st.success("🟢 Statut : Actif")
            st.session_state.historique_scans.append({"action": "OSINT Téléphone", "cible": tel, "date": str(datetime.datetime.now())})
        else:
            st.error("Veuillez inclure l'indicatif pays (ex: +33).")

elif menu.startswith("8."):
    st.subheader("🌐 Interception sites visités (Simulation)")
    tel = st.text_input("Numéro de téléphone cible")
    if st.button("Analyser les flux"):
        if tel.startswith("+"):
            sites = ["https://www.google.com", "https://www.whatsapp.com", "https://www.instagram.com", "https://www.tiktok.com"]
            trouves = random.sample(sites, 3)
            for s in trouves:
                st.write(f"🔗 {s}")
            st.session_state.historique_scans.append({"action": "Historique Web Simulé", "cible": tel, "date": str(datetime.datetime.now())})
        else:
            st.error("Format invalide. Utilisez un indicatif international.")

elif menu.startswith("9."):
    st.subheader("⚡ Scanner de ports (Simulation Nmap)")
    ip_cible = st.text_input("IP ou domaine cible", "192.168.1.1")
    if st.button("Lancer le balayage"):
        ports = [21, 22, 23, 53, 80, 443, 8080]
        for p in ports:
            etat = random.choice(["OUVERT", "FERMÉ"])
            if etat == "OUVERT":
                info = base_vulnerabilites.get(p, {"service": "Inconnu", "score": 3.0})
                st.warning(f"Port {p}/tcp : **{etat}** — Service: {info['service']} (Risque: {info['score']}/10)")
            else:
                st.text(f"Port {p}/tcp : {etat}")
        st.session_state.historique_scans.append({"action": "Scan de ports", "cible": ip_cible, "date": str(datetime.datetime.now())})

elif menu.startswith("10."):
    st.subheader("🌐 Découverte Réseau / Table ARP")
    prefixe = st.text_input("Préfixe réseau", "192.168.1")
    if st.button("Scanner le réseau"):
        hotes = [f"{prefixe}.1", f"{prefixe}.10", f"{prefixe}.15"]
        for h in hotes:
            mac = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)]).upper()
            st.text(f"IP: {h} ➔ MAC: {mac}")
        st.session_state.historique_scans.append({"action": "Découverte ARP", "cible": prefixe, "date": str(datetime.datetime.now())})

elif menu.startswith("11."):
    st.subheader("🔗 Analyseur de sécurité URL & Phishing")
    url_test = st.text_input("URL à analyser", "http://exemple.com")
    if st.button("Analyser l'URL"):
        score = 0
        alertes = []
        if not url_test.startswith("https://"):
            score += 3
            alertes.append("⚠️ Le site n'utilise pas HTTPS.")
        if any(m in url_test.lower() for m in ["login", "verify", "secure"]):
            score += 2
            alertes.append("⚠️ Présence de mots-clés suspects.")
        st.write(f"Niveau de risque : **{score} / 7**")
        for a in alertes:
            st.warning(a)
        st.session_state.historique_scans.append({"action": "Analyse URL", "cible": url_test, "date": str(datetime.datetime.now())})

elif menu.startswith("12."):
    st.subheader("📊 Simulation SIEM & Analyse de Logs")
    if st.button("Analyser les logs"):
        st.text("192.168.1.55 - - GET /index.php (200)")
        st.text("203.0.113.42 - - POST /login.php (401)")
        st.error("🔴 ALERTE CRITIQUE : Tentative de Brute-Force détectée depuis 203.0.113.42")
        st.session_state.historique_scans.append({"action": "Simulation SIEM", "cible": "Serveur Web", "date": str(datetime.datetime.now())})
