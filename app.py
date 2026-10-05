import streamlit as st
import datetime
import random
import phonenumbers
from phonenumbers import geocoder, carrier, number_type

# Configuration de la page
st.set_page_config(page_title="Security Checker (X-Hacker)", page_icon="🛡️")

# --- SYSTÈME D'AUTHENTIFICATION UNIQUE ---
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

st.title("🛡️ Security Checker (X-Hacker)")
st.write("Plateforme interactive de simulation de cybersécurité offensive et défensive.")

menu = st.sidebar.selectbox(
    "Navigation", 
    ["Chiffrement IP", "Simulation Nmap", "OSINT Téléphone (Réel)", "Interception (Métadonnées)", "Simulation SIEM"]
)

# --- MODULE 1 : CHIFFREMENT D'IP ---
if menu == "Chiffrement IP":
    st.subheader("📁 Créer & Chiffrer un rapport")
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
        st.info("Port 22/tcp : **OUVERT** — Service: SSH")
        st.write("Port 80/tcp : **OUVERT** — Service: HTTP")
        st.info("Port 443/tcp : **OUVERT** — Service: HTTPS")

# --- MODULE 3 : OSINT TÉLÉPHONE (VRAIE ANALYSE TECHNIQUE) ---
elif menu == "OSINT Téléphone (Réel)":
    st.subheader("📱 Analyse OSINT Réelle d'un Numéro")
    st.write("Entre un numéro au format international (ex: `+213562516680` ou `+33612345678`)")
    numero_input = st.text_input("Numéro de téléphone cible", "+213562516680")
    
    if st.button("Lancer l'analyse réelle"):
        try:
            # Analyse réelle du numéro via la bibliothèque phonenumbers
            parsed_number = phonenumbers.parse(numero_input)
            
            if phonenumbers.is_valid_number(parsed_number):
                pays_reel = geocoder.description_for_number(parsed_number, "fr")
                operateur_reel = carrier.name_for_number(parsed_number, "fr")
                type_ligne = number_type(parsed_number)
                
                # Traduction du type de ligne
                types_dict = {
                    phonenumbers.PhoneNumberType.MOBILE: "Téléphone Mobile",
                    phonenumbers.PhoneNumberType.FIXED_LINE: "Ligne Fixe",
                    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou Mobile",
                    phonenumbers.PhoneNumberType.VOIP: "VoIP (Internet)"
                }
                libelle_type = types_dict.get(type_ligne, "Inconnu / Autre")
                
                st.success(f"Analyse réussie pour le numéro : {numero_input}")
                st.markdown("### 📊 Résultats techniques réels :")
                st.write(f"- **Pays / Région d'origine** : `{pays_reel if pays_reel else 'Non spécifié'}`")
                st.write(f"- **Opérateur réseau** : `{operateur_reel if operateur_reel else 'Opérateur non détecté (ou masqué par portabilité)'}`")
                st.write(f"- **Type de ligne** : `{libelle_type}`")
                st.write(f"- **Format international normalisé** : `{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}`")
            else:
                st.error("❌ Ce numéro semble invalide ou mal formaté.")
        except Exception as e:
            st.error(f"Erreur d'analyse : Assure-toi d'inclure l'indicatif du pays (ex: +213...). Détail : {e}")

# --- MODULE 4 : INTERCEPTION (MÉTADONNÉES RÉSEAU) ---
elif menu == "Interception (Métadonnées)":
    st.subheader("🌐 Analyse des métadonnées réseau & Flux")
    num_intercep = st.text_input("Cible", "+213 56 25 16 68 0")
    
    if st.button("Capturer les paquets"):
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"Capture réseau pour : {num_intercep}")
        st.info(f"🕒 **Horodatage** : {maintenant}")
        st.write("- **Adresse IP source** : `192.168.1.55`")
        st.write("- **Taille des paquets de données** : `520 octets (Flux chiffré)`")
        st.write("- **Statut de session** : Actif")

# --- MODULE 5 : SIMULATION SIEM ---
elif menu == "Simulation SIEM":
    st.subheader("📊 Simulation SIEM & Analyse de Logs")
    if st.button("Analyser les logs"):
        st.text("192.168.1.55 -- GET /index.php (200)")
        st.error("🔴 ALERTE CRITIQUE : Tentative de Brute-Force détectée depuis 203.0.113.42")
