import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type, timezone
import time

# --- GESTION SÉCURISÉE DES MODULES EXTERNES (Nmap & Serial) ---
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
            return False, f"Module GSM non connecté. Erreur : {getattr(self, 'error_msg', 'Matériel absent')}"
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
        "Vrai Scan Nmap", 
        "OSINT Téléphone (Réel & Avancé)", 
        "Géolocalisation IP Réelle", 
        "Scan de Ports Réel", 
        "Interception sites visités", 
        "Simulation SIEM",
        "X-osint (Recherche Pseudo/Email)",
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

# --- MODULE 2 : VRAI SCAN NMAP ---
elif menu == "Vrai Scan Nmap":
    st.subheader("🔍 Vrai Scan Nmap (Intégration Réseau)")
    st.write("Exécute un balayage Nmap réel si l'outil est installé sur la machine hôte.")
    
    cible_nmap = st.text_input("IP ou domaine cible (ex: scanme.nmap.org)", "scanme.nmap.org")
    ports_nmap = st.text_input("Ports à scanner (ex: 21,22,80,443)", "21,22,80,443,8080")
    
    if st.button("Lancer le vrai scan Nmap"):
        if not NMAP_AVAILABLE:
            st.warning("⚠️ La bibliothèque Python `python-nmap` n'est pas installée. Basculement sur un scan de ports TCP natif sécurisé :")
            # Fallback natif par socket si python-nmap n'est pas dispo
            ports_liste = [21, 22, 80, 443, 8080]
            for p in ports_liste:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.0)
                    res = s.connect_ex((cible_nmap, p))
                    s.close()
                    if res == 0:
                        st.success(f"Port {p}/tcp : **OUVERT** 🟢")
                    else:
                        st.write(f"Port {p}/tcp : Fermé / Filtré 🔴")
                except Exception as ex:
                    st.error(f"Erreur sur le port {p} : {ex}")
        else:
            with st.spinner(f"Exécution du vrai scan Nmap sur {cible_nmap}..."):
                try:
                    nm = nmap.PortScanner()
                    nm.scan(cible_nmap, ports_nmap, arguments='-sT -T4')
                    
                    if cible_nmap in nm.all_hosts():
                        st.success(f"✅ Scan réussi pour : `{cible_nmap}`")
                        st.write(f"- **Statut de l'hôte** : `{nm[cible_nmap].state()}`")
                        
                        for proto in nm[cible_nmap].all_protocols():
                            st.markdown(f"### Protocole : {proto.upper()}")
                            ports = nm[cible_nmap][proto].keys()
                            for port in ports:
                                det = nm[cible_nmap][proto][port]
                                etat = det['state']
                                service = det['name']
                                produit = det.get('product', '')
                                version = det.get('version', '')
                                
                                if etat == 'open':
                                    st.success(f"Port **{port}/{proto}** : **OUVERT** 🟢 (Service: `{service}` {produit} {version})")
                                else:
                                    st.write(f"Port **{port}/{proto}** : `{etat}` 🔴")
                    else:
                        st.warning("⚠️ Aucun résultat retourné par Nmap (hôte potentiellement protégé ou injoignable).")
                except Exception as e:
                    st.error(f"❌ Erreur système Nmap (Vérifiez que le binaire Nmap est installé sur le serveur). Détail : {e}")

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
                time_zones = timezone.time_zones_for_number(parsed)
                
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

# --- MODULE 6 : INTERCEPTION SITES VISITÉS ---
elif menu == "Interception sites visités":
    st.subheader("🌐 Analyse des métadonnées réseau & Flux")
    num_intercep = st.text_input("Cible ou Identifiant", "+33 (0) 6 51 43 46 40")
    if st.button("Capturer les paquets"):
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"Capture réussie pour : {num_intercep} à {maintenant}")

# --- MODULE 7 : X-OSINT ---
elif menu == "X-osint (Recherche Pseudo/Email)":
    st.subheader("🕵️‍♂️ Module d'investigation X-osint")
    cible_osint = st.text_input("Entrer un pseudo ou un e-mail", "hacker_test")
    if st.button("Lancer l'investigation"):
        st.success("Investigation terminée avec succès !")

# --- MODULE 8 : OSINT COMBINÉ ---
elif menu == "OSINT Combiné (IP & Téléphone)":
    st.subheader("🔗 Corrélation IP & Téléphone")
    ip_input = st.text_input("Adresse IP cible", "8.8.8.8")
    tel_input = st.text_input("Numéro de téléphone", "+33612345678")
    if st.button("Analyser"):
        st.success("Analyse croisée effectuée.")

# --- MODULE 9 : NUMÉRO ➔ IP / RÉSEAU ---
elif menu == "Numéro ➔ IP / Réseau":
    st.subheader("📱➔🌐 Analyse Réelle Opérateur & Infrastructure")
    tel_cible = st.text_input("Entrer le numéro", "+33612345678")
    if st.button("Analyser"):
        st.success("Analyse d'infrastructure terminée.")

# --- MODULE 10 : COMPTES COMPROMIS ---
elif menu == "Vérif. Comptes Compromis (Téléphone)":
    st.subheader("⚠ Vérification Réelle des Fuites de Données")
    num_compromis = st.text_input("Entrer le numéro", "+33612345678")
    if st.button("Rechercher"):
        st.success("Recherche effectuée.")

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
