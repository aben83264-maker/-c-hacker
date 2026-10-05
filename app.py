import streamlit as st
import datetime
import random

# Configuration de la page
st.set_page_config(page_title="Security Checker (X-Hacker)", page_icon="🛡️")

# --- SYSTÈME D'AUTHENTIFICATION UNIQUE ---
st.title("🔐 Accès Restreint - Security Checker")

# Mot de passe administrateur sécurisé
MOT_DE_PASSE_ADMIN = "ADMIN_X_123@Hanter"

def check_password():
    """Vérifie si le mot de passe entré est correct."""
    password_input = st.text_input("Entrez le mot de passe administrateur", type="password")
    if password_input == MOT_DE_PASSE_ADMIN:
        st.session_state["password_correct"] = True
        st.rerun()
    elif password_input != "":
        st.error("❌ Mot de passe incorrect.")

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    check_password()
    st.stop()

# --- LE RESTE DE L'APPLICATION ---
st.success("✅ Accès autorisé !")

st.title("🛡️ Security Checker (X-Hacker)")
st.write("Plateforme interactive de simulation de cybersécurité offensive et défensive.")

# Menu de navigation
menu = st.sidebar.selectbox(
    "Navigation", 
    ["Chiffrement IP", "Simulation Nmap", "OSINT Téléphone", "Interception sites visités", "Simulation SIEM"]
)

# --- MODULE 1 : CHIFFREMENT D'IP ---
if menu == "Chiffrement IP":
    st.subheader("📁 Créer & Chiffrer un rapport X-Hacker")
    ip_cible = st.text_input("IP cible à simuler", "192.168.1.10")
    cle_secrete = st.text_input("Clé secrète de chiffrement", type="password")
    
    if st.button("Générer et Chiffrer"):
        st.success(f"Rapport généré pour la cible {ip_cible} et chiffré avec succès !")
        st.code("XLFYfy7...[données_chiffrées]...329A", language="text")

# --- MODULE 2 : SIMULATION NMAP ---
elif menu == "Simulation Nmap":
    st.subheader("🔍 Simulation Nmap")
    ip_nmap = st.text_input("IP ou domaine cible", "192.168.1.1")
    
    if st.button("Lancer le balayage"):
        st.write("Port 21/tcp : **FERMÉ**")
        st.info("Port 22/tcp : **OUVERT** — Service: SSH (Risque: 4.0/10)")
        st.write("Port 23/tcp : **FERMÉ**")
        st.write("Port 53/tcp : **FERMÉ**")
        st.info("Port 80/tcp : **OUVERT** — Service: HTTP (Risque: 5.0/10)")
        st.info("Port 443/tcp : **OUVERT** — Service: HTTPS (Risque: 1.0/10)")
        st.write("Port 8080/tcp : **FERMÉ**")

# --- MODULE 3 : OSINT TÉLÉPHONE ---
elif menu == "OSINT Téléphone":
    st.subheader("📱 OSINT / Traque de numéro")
    numero = st.text_input("Numéro de téléphone cible", "+33651434640")
    
    if st.button("Analyser le numéro"):
        st.success(f"Analyse réussie pour le numéro : {numero}")
        st.write("- **Opérateur estimé** : Orange / France")
        st.write("- **Ligne** : Mobile active")

# --- MODULE 4 : INTERCEPTION SITES VISITÉS & MÉTADONNÉES ---
elif menu == "Interception sites visités":
    st.subheader("🌐 Analyse des métadonnées réseau & Flux")
    num_intercep = st.text_input("Numéro ou IP cible", "+33 (0) 6 51 43 46 40")
    
    if st.button("Capturer les paquets et métadonnées"):
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.success(f"Capture réseau réussie pour la cible : {num_intercep}")
        st.info(f"🕒 **Horodatage de la connexion** : {maintenant}")
        
        st.markdown("### 📊 Métadonnées des flux actifs :")
        
        with st.expander("🔗 1. Google.com (HTTPS / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `142.250.190.46`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets échangés** : `1.2 Ko (Requête) / 14.5 Ko (Réponse)`")
            st.write("- **Statut de la session** : Actif (TLS 1.3)")
            
        with st.expander("🔗 2. Instagram.com (HTTPS / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `157.240.199.174`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets échangés** : `850 octets (Requête) / 48.2 Ko (Médias/Images)`")
            st.write("- **Statut de la session** : Actif (Keep-Alive)")
            
        with st.expander("🔗 3. WhatsApp.com / API (Port 5222 / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `157.240.197.60`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets de données échangés** : `420 octets (Payload chiffré)`")
            st.write("- **Statut de la session** : Actif (Connexion persistante / WebSocket)")

# --- MODULE 5 : SIMULATION SIEM ---
elif menu == "Simulation SIEM":
    st.subheader("📊 Simulation SIEM & Analyse de Logs")
    
    if st.button("Analyser les logs"):
        st.text("192.168.1.55 -- GET /index.php (200)")
        st.text("203.0.113.42 -- POST /login.php (401)")
        st.error("🔴 ALERTE CRITIQUE : Tentative de Brute-Force détectée depuis 203.0.113.42")
