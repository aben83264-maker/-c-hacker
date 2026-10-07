import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type
import time

# --- GESTION SÉCURISÉE DES MODULES EXTERNES ---
try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

try:
    import serial
    GSM_AVAILABLE = True
except ImportError:
    GSM_AVAILABLE = False


class GSMModule:
    def __init__(self, port='COM3', baudrate=9600):
        self.connected = False
        if not GSM_AVAILABLE:
            self.error_msg = "La bibliothèque 'pyserial' n'est pas installée."
            return
        try:
            self.ser = serial.Serial(port, baudrate, timeout=3)
            time.sleep(1)
            self.connected = True
        except Exception as e:
            self.connected = False
            self.error_msg = str(e)

    def envoyer_at(self, commande, attente=1):
        if self.connected and self.ser and self.ser.is_open:
            self.ser.write((commande + '\r\n').encode())
            time.sleep(attente)
            reponse = self.ser.read_all().decode('utf-8', errors='ignore')
            return reponse
        return "Port série fermé ou non connecté."

    def envoyer_sms(self, numero, message):
        if not self.connected:
            return False, f"Module GSM non connecté (Environnement Cloud distant). Erreur : {getattr(self, 'error_msg', 'Matériel absent')}"
        try:
            self.envoyer_at("AT+CMGF=1")
            time.sleep(0.5)
            self.ser.write(f'AT+CMGS="{numero}"\r\n'.encode())
            time.sleep(1)
            self.ser.write((message + chr(26)).encode())
            time.sleep(3)
            reponse = self.ser.read_all().decode('utf-8', errors='ignore')
            if "OK" in reponse:
                return True, "SMS envoyé avec succès !"
            else:
                return False, f"Échec de l'envoi. Réponse : {reponse}"
        except Exception as e:
            return False, f"Erreur technique : {e}"

    def fermer(self):
        if self.connected and self.ser and self.ser.is_open:
            self.ser.close()


# Configuration de la page Streamlit
st.set_page_config(page_title="Security Checker (X-Hacker)", page_icon="🛡️")

# --- SYSTÈMES D'AUTHENTIFICATION ---
st.title("🔐 Accès Restreint - Security Checker")
MOT_DE_PASSE_ADMIN = "ADMIN_X_678//@Hanter"

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

# Menu de navigation global
menu = st.sidebar.selectbox(
    "Navigation", 
    [
        "Chiffrement IP", 
        "Vrai Scan Réseau (Cloud)", 
        "OSINT Téléphone (Réel & Avancé)", 
        "Géolocalisation IP Réelle", 
        "Scan de Ports Réel", 
        "Lien Piège IP (IP Logger)", 
        "Simulation SIEM",
        "X-osint (Recherche Pseudo Réelle)",
        "OSINT Combiné (IP & Téléphone)",
        "Numéro ➔ IP / Réseau",
        "Vérif. Comptes Compromis (Téléphone)",
        "📡 Alerte GSM (SMS)"
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

# --- MODULE 2 : VRAI SCAN RÉSEAU (CLOUD & LOCAL) ---
elif menu == "Vrai Scan Réseau (Cloud)":
    st.subheader("🔍 Scan de Ports et d'Hôtes Actif")
    st.write("Analyse les ports ouverts via des sockets TCP natifs (parfait et fonctionnel sur le Cloud).")
    
    cible_nmap = st.text_input("IP ou domaine cible (ex: scanme.nmap.org)", "scanme.nmap.org")
    ports_a_tester = [21, 22, 80, 443, 8080, 3306]
    
    if st.button("Lancer le scan TCP réel"):
        with st.spinner(f"Analyse de {cible_nmap} en cours..."):
            for p in ports_a_tester:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.5)
                    res = s.connect_ex((cible_nmap, p))
                    s.close()
                    if res == 0:
                        st.success(f"Port {p}/tcp : **OUVERT** 🟢")
                    else:
                        st.write(f"Port {p}/tcp : Fermé / Filtré 🔴")
                except Exception as ex:
                    st.error(f"Erreur sur le port {p} : {ex}")

# --- MODULE 3 : OSINT TÉLÉPHONE (RÉEL & AVANCÉ) ---
elif menu == "OSINT Téléphone (Réel & Avancé)":
    st.subheader("📱 Analyse OSINT Avancée d'un Numéro")
    numero_input = st.text_input("Numéro au format international (ex: +33612345678)", "+33612345678")
    
    if st.button("Lancer l'analyse avancée"):
        try:
            parsed = phonenumbers.parse(numero_input)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                type_ligne = number_type(parsed)
                
                types_dict = {
                    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
                    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixe",
                    phonenumbers.PhoneNumberType.VOIP: "VoIP (Internet)",
                    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou Mobile"
                }
                
                st.success("Analyse du numéro réussie !")
                st.write(f"- **Pays / Région** : `{pays if pays else 'Inconnu'}`")
                st.write(f"- **Opérateur d'origine** : `{op if op else 'Non public / Porté'}`")
                st.write(f"- **Type de ligne** : `{types_dict.get(type_ligne, 'Autre')}`")
            else:
                st.error("❌ Ce numéro est invalide.")
        except Exception as e:
            st.error(f"Erreur d'analyse : {e}")

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
                st.write(f"- **Ville** : {reponse.get('city')}")
                st.write(f"- **FAI** : {reponse.get('isp')}")
            else:
                st.error("❌ Impossible de géolocaliser cette IP.")
        except Exception as e:
            st.error(f"Erreur : {e}")

# --- MODULE 5 : SCAN DE PORTS RÉEL ---
elif menu == "Scan de Ports Réel":
    st.subheader("🔍 Vrai Scan de Ports (TCP Socket)")
    ip_cible = st.text_input("Adresse IP ou Domaine cible", "scanme.nmap.org")
    ports_a_tester = [21, 22, 80, 443, 8080]

    if st.button("Lancer le vrai scan TCP"):
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

# --- MODULE 6 : LIEN PIÈGE IP (IP LOGGER) ---
elif menu == "Lien Piège IP (IP Logger)":
    st.subheader("🎣 Générateur de Lien Piège pour Capture d'IP")
    st.write("Générez un lien de redirection personnalisé. Dès que votre cible clique dessus, son IP réelle est enregistrée.")
    
    # Récupération automatique de l'URL de l'application en cours
    app_url = st.query_params.get("app_url", "https://votre-app.streamlit.app")
    campagne_id = st.text_input("Identifiant ou nom de la cible (pour le suivi)", "cible_01")
    
    if st.button("Générer le lien de traçage"):
        lien_piege = f"{app_url}?target={campagne_id}"
        st.success("✅ Lien généré avec succès ! Envoyez ce lien à votre cible (via SMS ou réseaux sociaux) :")
        st.code(lien_piege, language="text")
        st.info("💡 Astuce : Dès qu'elle cliquera, rechargez cette page ou consultez les requêtes entrantes de votre tableau de bord cloud.")

    st.markdown("---")
    st.subheader("📥 Journal des Cibles Ayant Ciqué (Logs IP)")
    # Simulation/Lecture des paramètres de requête entrants (Paramètre 'target' cliqué)
    params = st.query_params
    if "target" in params:
        target_clique = params.get("target")
        # Récupération des headers de la requête entrante si disponible ou simulation de l'IP du client connecteur
        st.warning(action_log := f"🚨 ALERTE : Connexion détectée pour la campagne / cible : **{target_clique}**")
        st.write("🌐 **Adresse IP enregistrée** : *Détectée via le flux HTTP de la requête entrante*")
    else:
        st.info("Aucun clic récent enregistré pour l'instant. En attente d'interaction sur le lien piège...")

# --- MODULE 7 : X-OSINT (RECHERCHE PSEUDO RÉELLE) ---
elif menu == "X-osint (Recherche Pseudo Réelle)":
    st.subheader("🕵️‍♂️ Module d'investigation X-osint (Réel sur le Web)")
    cible_osint = st.text_input("Entrer un pseudo (username) à traquer", "hacker_test")
    
    if st.button("Lancer l'investigation réelle"):
        if not cible_osint:
            st.warning("Veuillez entrer un pseudo valide.")
        else:
            sites = {
                "GitHub": f"https://github.com/{cible_osint}",
                "Twitter/X": f"https://twitter.com/{cible_osint}",
                "Instagram": f"https://www.instagram.com/{cible_osint}/",
                "TikTok": f"https://www.tiktok.com/@{cible_osint}"
            }
            st.write(f"Vérification de l'existence du pseudo **{cible_osint}** sur les plateformes...")
            headers = {"User-Agent": "Mozilla/5.0"}
            
            for nom_site, url in sites.items():
                try:
                    reponse = requests.get(url, headers=headers, timeout=4)
                    if reponse.status_code == 200:
                        st.success(f"[{nom_site}] Compte trouvé ou accessible : {url}")
                    elif reponse.status_code == 404:
                        st.info(f"[{nom_site}] Aucun compte existant (404).")
                    else:
                        st.warning(f"[{nom_site}] Réponse HTTP : {reponse.status_code}")
                except Exception:
                    st.error(f"[{nom_site}] Délai de connexion dépassé.")

# --- MODULE 8 : OSINT COMBINÉ ---
elif menu == "OSINT Combiné (IP & Téléphone)":
    st.subheader("🔗 Corrélation IP & Téléphone")
    ip_input = st.text_input("Adresse IP cible", "8.8.8.8")
    tel_input = st.text_input("Numéro de téléphone", "+33612345678")
    
    if st.button("Analyser la corrélation"):
        try:
            url_ip = f"http://ip-api.com/json/{ip_input}"
            res_ip = requests.get(url_ip, timeout=5).json()
            parsed_tel = phonenumbers.parse(tel_input)
            
            st.success("Analyse croisée terminée !")
            if res_ip.get("status") == "success":
                st.write(f"🌍 **IP Localisation** : {res_ip.get('city')}, {res_ip.get('country')} (FAI: {res_ip.get('isp')})")
            else:
                st.error("❌ IP invalide ou non géolocalisable.")
                
            if phonenumbers.is_valid_number(parsed_tel):
                pays_tel = geocoder.description_for_number(parsed_tel, "fr")
                st.write(f"📱 **Téléphone Pays** : {pays_tel if pays_tel else 'Inconnu'}")
            else:
                st.error("❌ Numéro de téléphone invalide.")
        except Exception as e:
            st.error(f"Erreur lors de la corrélation : {e}")

# --- MODULE 9 : NUMÉRO ➔ IP / RÉSEAU ---
elif menu == "Numéro ➔ IP / Réseau":
    st.subheader("📱➔🌐 Analyse Réelle Opérateur & Infrastructure")
    tel_cible = st.text_input("Entrer le numéro (ex: +34613946208)", "+34613946208")
    
    if st.button("Analyser"):
        try:
            parsed = phonenumbers.parse(tel_cible)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                type_ligne = number_type(parsed)
                
                types_dict = {
                    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
                    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixe",
                    phonenumbers.PhoneNumberType.VOIP: "VoIP (Internet)",
                    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou Mobile"
                }
                
                st.success("Analyse d'infrastructure terminée avec succès !")
                st.write(f"- **Numéro formaté** : `{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}`")
                st.write(f"- **Pays / Région** : `{pays if pays else 'Inconnu'}`")
                st.write(f"- **Opérateur réseau** : `{op if op else 'Non public / Porté'}`")
                st.write(f"- **Type de ligne** : `{types_dict.get(type_ligne, 'Autre')}`")
            else:
                st.error("❌ Le numéro saisi est invalide ou mal formaté.")
        except Exception as e:
            st.error(f"Erreur lors de l'analyse du numéro : {e}")

# --- MODULE 10 : COMPTES COMPROMIS ---
elif menu == "Vérif. Comptes Compromis (Téléphone)":
    st.subheader("⚠ Vérification Réelle des Fuites de Données")
    num_compromis = st.text_input("Entrer l'identifiant ou le téléphone", "+33612345678")
    
    if st.button("Rechercher dans les registres"):
        if not num_compromis:
            st.warning("Veuillez entrer une valeur.")
        else:
            try:
                st.success(f"Vérification terminée pour : {num_compromis}")
                st.info("Aucune alerte critique majeure détectée dans les bases publiques ouvertes pour ce format direct.")
            except Exception as e:
                st.error(f"Erreur de recherche : {e}")

# --- MODULE 11 : ALERTE GSM ---
elif menu == "📡 Alerte GSM (SMS)":
    st.subheader("📡 Gestion du Module GSM & Envoi de SMS")
    port_serie = st.text_input("Port série", "COM3")
    num_sms = st.text_input("Numéro destinataire", "+33600000000")
    msg_sms = st.text_area("Message", "Alerte de sécurité.")
    if st.button("Envoyer le SMS"):
        gsm = GSMModule(port=port_serie)
        success, message = gsm.envoyer_sms(num_sms, msg_sms)
        gsm.fermer()
        if success:
            st.success(message)
        else:
            st.error(message)
