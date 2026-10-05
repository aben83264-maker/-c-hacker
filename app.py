import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type

# Configuration de la page
st.set_page_config(page_title="Security Checker (Réel)", page_icon="🛡️")

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

st.success("✅ Accès autorisé !")
st.title("🛡️ Security Checker — Outils Réels")
st.write("Plateforme d'analyse technique et de cyber-sécurité (Données réelles et autorisées).")

# Menu de navigation
menu = st.sidebar.selectbox(
    "Navigation", 
    ["Géolocalisation IP Réelle", "Scan de Ports Réel", "OSINT Téléphone (Réel)"]
)

# --- MODULE 1 : VRAIE GÉOLOCALISATION D'UNE IP ---
if menu == "Géolocalisation IP Réelle":
    st.subheader("🌍 Vraie Localisation d'une Adresse IP (Publique)")
    st.write("Interroge les bases de données mondiales pour obtenir les informations d'une adresse IP publique.")
    
    ip_saisie = st.text_input("Entrez une adresse IP publique (ex: 8.8.8.8 ou 1.1.1.1)", "8.8.8.8")
    
    if st.button("Interroger la base mondiale"):
        try:
            url = f"http://ip-api.com/json/{ip_saisie}"
            reponse = requests.get(url, timeout=5).json()
            
            if reponse.get("status") == "success":
                st.success("Données récupérées avec succès !")
                st.write(f"- **Pays** : {reponse.get('country')} ({reponse.get('countryCode')})")
                st.write(f"- **Région / Ville** : {reponse.get('regionName')} - {reponse.get('city')}")
                st.write(f"- **Fournisseur d'accès (FAI / ISP)** : {reponse.get('isp')}")
                st.write(f"- **Organisation** : {reponse.get('org')}")
                st.write(f"- **Coordonnées GPS approximatives** : Lat: {reponse.get('lat')}, Lon: {reponse.get('lon')}")
            else:
                st.error("❌ Impossible de géolocaliser cette IP (IP privée ou invalide).")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

# --- MODULE 2 : VRAI SCAN DE PORTS (TCP SOCKET) ---
elif menu == "Scan de Ports Réel":
    st.subheader("🔍 Vrai Scan de Ports (TCP)")
    st.write("Teste si des services spécifiques répondent réellement sur une cible autorisée.")
    
    ip_cible = st.text_input("Adresse IP ou Domaine cible (ex: scanme.nmap.org)", "scanme.nmap.org")
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

# --- MODULE 3 : OSINT TÉLÉPHONE RÉEL ---
elif menu == "OSINT Téléphone (Réel)":
    st.subheader("📱 Analyse OSINT Réelle d'un Numéro")
    st.write("Analyse l'indicatif international pour extraire les vraies métadonnées de la ligne.")
    
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
