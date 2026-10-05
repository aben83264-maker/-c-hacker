import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type

st.set_page_config(page_title="Security Checker (Réel)", page_icon="🛡️")

# --- AUTHENTIFICATION ---
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

st.success("✅ Accès autorisé !")
st.title("🛡️ Security Checker — Outils Réels")

menu = st.sidebar.selectbox(
    "Navigation", 
    ["Géolocalisation IP Réelle", "Scan de Ports Réel", "OSINT Téléphone (Réel)"]
)

# --- MODULE 1 : VRAIE GÉOLOCALISATION D'UNE IP ---
if menu == "Géolocalisation IP Réelle":
    st.subheader("🌍 Vraie Localisation d'une Adresse IP (Publique)")
    ip_saisie = st.text_input("Entrez une adresse IP publique (ex: 8.8.8.8)", "8.8.8.8")
    
    if st.button("Interroger la base mondiale"):
        try:
            # Requête réelle vers une API publique de géolocalisation IP
            url = f"http://ip-api.com/json/{ip_saisie}"
            reponse = requests.get(url, timeout=5).json()
            
            if reponse.get("status") == "success":
                st.success("Données récupérées avec succès depuis le réseau mondial !")
                st.write(- f"**Pays** : {reponse.get('country')} ({reponse.get('countryCode')})")
                st.write(f"- **Région / Ville** : {reponse.get('regionName')} - {reponse.get('city')}")
                st.write(f"- **Fournisseur d'accès (FAI / ISP)** : {reponse.get('isp')}")
                st.write(f"- **Organisation** : {reponse.get('org')}")
                st.write(f"- **Coordonnées GPS approximatives** : Lat: {reponse.get('lat')}, Lon: {reponse.get('lon')}")
            else:
                st.error("❌ Impossible de géolocaliser cette IP (IP invalide ou privée).")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# --- MODULE 2 : VRAI SCAN DE PORTS (TCP SOCKET) ---
elif menu == "Scan de Ports Réel":
    st.subheader("🔍 Vrai Scan de Ports (TCP)")
    st.write("Teste si des ports spécifiques sont réellement ouverts sur une cible autorisée.")
    
ip_cible = st.text_input("Adresse IP ou Domaine cible", "scanme.nmap.org")
ports_a_tester = [21, 22, 80, 443, 8080]

if st.button("Lancer le vrai scan TCP"):
    st.write(f"Analyse des ports sur **{ip_cible}** en cours...")
    
    for port in ports_a_tester:
        try:
            # Création d'un vrai socket réseau
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5) # Temps limite de réponse
            resultat = s.connect_ex((ip_cible, port))
            s.close()
            
            if resultat == 0:
                st.success(f"Port {port}/tcp : **OUVERT** 🟢")
            else:
                st.write(f"Port {port}/tcp : Fermé / Filtré 🔴")
        except Exception as e:
            st.error(f"Erreur sur le port {port} : {e}")

# --- MODULE 3 : OSINT TÉLÉPHONE RÉEL ---
elif menu == "OSINT Téléphone (Réel)":
    st.subheader("📱 Analyse OSINT Réelle d'un Numéro")
    numero_input = st.text_input("Numéro au format international", "+33612345678")
    
    if st.button("Analyser le numéro"):
        try:
            parsed = phonenumbers.parse(numero_input)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                st.success("Numéro valide analysé !")
                st.write(f"- **Pays** : {pays}")
                st.write(f"- **Opérateur** : {op if op else 'Non public / Porté'}")
            else:
                st.error("Numéro invalide.")
        except Exception as e:
            st.error(f"Erreur : {e}")
