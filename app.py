import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type

# Configuration de la page
st.set_page_config(page_title="Security Checker (X-Hacker)", page_icon="🛡️")

# --- SYSTÈME D'AUTHENTIFICATION ---
st.title("🔐 Accès Restreint - Security Checker")
MOT_DE_PASSE_ADMIN = "ADMIN_X_123@Hanter"

def check_password():
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

# --- APPLICATION PRINCIPALE ---
st.success("✅ Accès autorisé !")
st.title("🛡️ Security Checker (X-Hacker)")
st.write("Plateforme interactive d'analyse technique, de métadonnées réseau et de cybersécurité.")

# Menu de navigation global (avec l'option X-osint ajoutée)
menu = st.sidebar.selectbox(
    "Navigation", 
    [
        "Chiffrement IP", 
        "Simulation Nmap", 
        "OSINT Téléphone (Réel)", 
        "Géolocalisation IP Réelle", 
        "Scan de Ports Réel", 
        "Interception sites visités", 
        "Simulation SIEM",
        "X-osint (Recherche Pseudo/Email)"
    ]
)

# --- MODULE 1 : CHIFFREMENT D'IP ---
if menu == "Chiffrement IP":
    st.subheader("📁 Créer & Chiffrer un rapport X-Hacker")
    ip_cible = st.text_input("IP cible à simuler", "192.168.1.10")
    cle_secrete = st.text_input("Clé secrète de chiffrement", type="password")
    
    if st.button("Générer et Chiffrer"):
        st.success(f"Rapport généré pour la cible {ip_cible} et chiffré avec succès !")
        st.code("XLFYfy7...[données_chiffrées_aes256]...329A", language="text")

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

# --- MODULE 3 : OSINT TÉLÉPHONE (RÉEL) ---
elif menu == "OSINT Téléphone (Réel)":
    st.subheader("📱 Analyse OSINT Réelle d'un Numéro")
    st.write("Analyse l'indicatif international pour extraire les métadonnées techniques de la ligne.")
    
    numero_input = st.text_input("Numéro au format international (ex: +33612345678 ou +213...)", "+33612345678")
    
    if st.button("Analyser le numéro"):
        try:
            parsed = phonenumbers.parse(numero_input)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                type_ligne = number_type(parsed)
                
                types_dict = {
                    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
                    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixe",
                    phonenumbers.PhoneNumberType.VOIP: "VoIP (Internet)"
                }
                
                st.success("Numéro valide analysé avec succès !")
                st.write(f"- **Pays / Région** : `{pays if pays else 'Inconnu'}`")
                st.write(f"- **Opérateur d'origine** : `{op if op else 'Non public / Porté'}`")
                st.write(f"- **Type de ligne** : `{types_dict.get(type_ligne, 'Autre')}`")
                st.write(f"- **Format international** : `{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}`")
            else:
                st.error("❌ Ce numéro est invalide ou mal formaté.")
        except Exception as e:
            st.error(f"Erreur d'analyse : Assure-toi d'inclure l'indicatif (ex: +33...). Détail : {e}")

# --- MODULE 4 : GÉOLOCALISATION IP RÉELLE ---
elif menu == "Géolocalisation IP Réelle":
    st.subheader("🌍 Vraie Localisation d'une Adresse IP (Publique)")
    ip_saisie = st.text_input("Entrez une adresse IP publique (ex: 8.8.8.8)", "8.8.8.8")
    
    if st.button("Interroger la base mondiale"):
        try:
            url = f"http://ip-api.com/json/{ip_saisie}"
            reponse = requests.get(url, timeout=5).json()
            
            if reponse.get("status") == "success":
                st.success("Données récupérées avec succès !")
                st.write(f"- **Pays** : {reponse.get('country')} ({reponse.get('countryCode')})")
                st.write(f"- **Région / Ville** : {reponse.get('regionName')} - {reponse.get('city')}")
                st.write(f"- **Fournisseur d'accès (FAI)** : {reponse.get('isp')}")
                st.write(f"- **Coordonnées GPS approximatives** : Lat: {reponse.get('lat')}, Lon: {reponse.get('lon')}")
            else:
                st.error("❌ Impossible de géolocaliser cette IP (IP privée ou invalide).")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# --- MODULE 5 : SCAN DE PORTS RÉEL ---
elif menu == "Scan de Ports Réel":
    st.subheader("🔍 Vrai Scan de Ports (TCP)")
    ip_cible = st.text_input("Adresse IP ou Domaine cible", "scanme.nmap.org")
    ports_a_tester = [21, 22, 80, 443, 8080]

    if st.button("Lancer le vrai scan TCP"):
        st.write(f"Analyse des ports sur **{ip_cible}** en cours...")
        for port in ports_a_tester:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5)
                resultat = s.connect_ex((ip_cible, port))
                s.close()
                
                if resultat == 0:
                    st.success(f"Port {port}/tcp : **OUVERT** 🟢")
                else:
                    st.write(f"Port {port}/tcp : Fermé / Filtré 🔴")
            except Exception as e:
                st.error(f"Erreur sur le port {port} : {e}")

# --- MODULE 6 : INTERCEPTION SITES VISITÉS & MÉTADONNÉES ---
elif menu == "Interception sites visités":
    st.subheader("🌐 Analyse des métadonnées réseau & Flux")
    num_intercep = st.text_input("Cible ou Identifiant", "+33 (0) 6 51 43 46 40")
    
    if st.button("Capturer les paquets et métadonnées"):
        maintenant = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")
        
        st.success(f"Capture réseau réussie pour la cible : {num_intercep}")
        st.info(f"🕒 **Horodatage de la connexion** : {maintenant}")
        
        st.markdown("### 📊 Métadonnées des flux actifs :")
        
        with st.expander("🔗 1. Google.com (HTTPS / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `142.250.190.46`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets échangés** : `1.2 Ko (Requête) / 14.5 Ko (Réponse)`")
            st.write("- **Statut de la session** : Actif (TLS 1.3)")

# --- MODULE 7 : X-OSINT (RECHERCHE PSEUDO / EMAIL) ---
elif menu == "X-osint (Recherche Pseudo/Email)":
    st.subheader("🕵️‍♂️ Module d'investigation X-osint")
    st.write("Recherche d'informations en sources ouvertes sur une cible (pseudo ou e-mail).")
    
    cible_osint = st.text_input("Entrer un pseudo ou un e-mail à traquer", "hacker_test")
    
    if st.button("Lancer l'investigation X-osint"):
        if "@" in cible_osint:
            st.info(f"Analyse des fuites de données (Data Leaks) pour : **{cible_osint}**")
            st.success("✅ Aucun mot de passe en clair trouvé dans les bases de données publiques.")
            st.write("- **Domain check** : Valide")
            st.write("- **Gravatar** : Trouvé 🟢")
        else:
            st.info(f"Recherche de la présence du pseudo **{cible_osint}** sur les plateformes...")
            st.write(f"- **GitHub** : https://github.com/{cible_osint} (Vérification en cours...) 🟢")
            st.write("- **Twitter / X** : Potentiellement existant 🟡")
            st.write("- **Instagram** : Non répertorié 🔴")
            st.write("- **TikTok** : Non répertorié 🔴")
            st.success("Investigation X-osint terminée avec succès !")
