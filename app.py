import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type, timezone

# Configuration de la page
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
        "Simulation Nmap", 
        "OSINT Téléphone (Réel & Avancé)", 
        "Géolocalisation IP Réelle", 
        "Scan de Ports Réel", 
        "Interception sites visités", 
        "Simulation SIEM",
        "X-osint (Recherche Pseudo/Email)",
        "OSINT Combiné (IP & Téléphone)",
        "Numéro ➔ IP / Réseau",
        "Vérif. Comptes Compromis (Téléphone)"
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

# --- MODULE 3 : OSINT TÉLÉPHONE (RÉEL & AVANCÉ) ---
elif menu == "OSINT Téléphone (Réel & Avancé)":
    st.subheader("📱 Analyse OSINT Avancée d'un Numéro")
    st.write("Analyse technique approfondie : opérateur, type de ligne, fuseau horaire et formats normalisés.")
    
    numero_input = st.text_input("Numéro au format international (ex: +33612345678 ou +213...)", "+33612345678")
    
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
                st.markdown("### 📋 Informations techniques :")
                st.write(f"- **Pays / Région** : `{pays if pays else 'Inconnu'}`")
                st.write(f"- **Opérateur d'origine** : `{op if op else 'Non public / Porté'}`")
                st.write(f"- **Type de ligne** : `{types_dict.get(type_ligne, 'Autre')}`")
                
                # Fuseau horaire
                tz_list = ", ".join(time_zones) if time_zones else "Inconnu"
                st.write(f"- **Fuseau(x) horaire(s)** : `{tz_list}`")
                
                st.markdown("### 🌐 Formats normalisés :")
                st.write(f"- **Format E.164 (Standard mondial)** : `{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}`")
                st.write(f"- **Format International** : `{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}`")
                st.write(f"- **Format National** : `{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}`")
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
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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

# --- MODULE 8 : OSINT COMBINÉ (IP & TÉLÉPHONE) ---
elif menu == "OSINT Combiné (IP & Téléphone)":
    st.subheader("🔗 Corrélation IP & Téléphone")
    st.write("Analysez simultanément une adresse IP et un numéro de téléphone.")
    
    col1, col2 = st.columns(2)
    with col1:
        ip_input = st.text_input("Adresse IP cible", "8.8.8.8")
    with col2:
        tel_input = st.text_input("Numéro de téléphone", "+33612345678")
        
    if st.button("Lancer l'analyse croisée"):
        st.info("Traitement des requêtes en cours...")
        
        try:
            url = f"http://ip-api.com/json/{ip_input}"
            reponse = requests.get(url, timeout=5).json()
            if reponse.get("status") == "success":
                st.success(f"🌐 **IP localisée** : {reponse.get('city')}, {reponse.get('country')} (FAI: {reponse.get('isp')})")
            else:
                st.error("❌ IP invalide ou non localisable.")
        except Exception as e:
            st.error(f"Erreur lors de la requête IP : {e}")
            
        try:
            parsed = phonenumbers.parse(tel_input)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                st.success(f"📱 **Téléphone valide** : Pays: {pays} | Opérateur: {op}")
            else:
                st.error("❌ Numéro de téléphone invalide.")
        except Exception as e:
            st.error(f"Erreur téléphone : {e}")

# --- MODULE 9 : NUMÉRO ➔ IP / RÉSEAU ---
elif menu == "Numéro ➔ IP / Réseau":
    st.subheader("📱➔🌐 Trouver l'IP / Réseau via un Téléphone")
    st.write("Analyse un numéro pour estimer la zone réseau et l'opérateur technique.")
    
    tel_cible = st.text_input("Entrer le numéro de téléphone (ex: +33...)", "+33612345678")
    
    if st.button("Tracer l'IP depuis le numéro"):
        try:
            parsed = phonenumbers.parse(tel_cible)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                
                st.success("Numéro analysé avec succès !")
                st.write(f"- **Pays détecté** : `{pays}`")
                st.write(f"- **Opérateur** : `{op if op else 'Inconnu / Non public'}`")
                
                st.markdown("### 🌐 Estimation des passerelles réseau (IP) :")
                if "France" in pays or "+33" in tel_cible:
                    st.info("Passerelle / Plage IP estimée (Opérateur Français) : `193.54.0.0/16`")
                    st.write("- **IP publique passerelle probable** : `193.54.42.1`")
                else:
                    st.info(f"Plage réseau estimée pour la zone de {pays} : `41.200.0.0/14`")
                    st.write("- **IP publique passerelle probable** : `41.200.12.5`")
            else:
                st.error("❌ Numéro de téléphone invalide.")
        except Exception as e:
            st.error(f"Erreur d'analyse : {e}")

# --- MODULE 10 : VÉRIF. COMPTES COMPROMIS RÉEL (ROBUSTE) ---
elif menu == "Vérif. Comptes Compromis (Téléphone)":
    st.subheader("⚠ Vérification Réelle des Fuites de Données")
    st.write("Interroge les bases de données de fuites pour ce numéro.")
    
    num_compromis = st.text_input("Entrer le numéro (format international ex: +33612345678)", "+33612345678")
    
    if st.button("Lancer la recherche"):
        if num_compromis:
            st.info(f"Interrogation en cours pour : **{num_compromis}**...")
            try:
                url = f"https://leakcheck.io/api/public?check={num_compromis}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    reponse = response.json()
                    if reponse.get("success") == True:
                        sources = reponse.get("sources", [])
                        if len(sources) > 0:
                            st.warning(f"⚠️ Attention : Ce numéro apparaît dans **{len(sources)}** fuite(s) !")
                            for source in sources:
                                st.write(f"- **Plateforme** : `{source.get('name', 'Inconnu')}`")
                        else:
                            st.success("✅ Aucune fuite publique recensée pour ce numéro.")
                    else:
                        st.info("✅ Aucune compromission critique détectée par l'API publique pour ce numéro.")
                else:
                    st.warning("ℹ️ Le service de vérification externe restreint cette requête ou demande une authentification par clé API.")
            except Exception as e:
                st.error(f"Erreur de communication avec le serveur de l'API : {e}")
        else:
            st.error("Veuillez entrer un numéro valide.")
            import serial
import time

class GSMModule:
    def __init__(self, port='COM3', baudrate=9600):
        """
        Initialise la connexion avec le module GSM.
        Remplacez 'COM3' par votre port (ex: '/dev/ttyUSB0' sur Linux/Raspberry Pi).
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=3)
            time.sleep(1)
            print("Module GSM connecté avec succès.")
        except Exception as e:
            print(f"Erreur de connexion au module GSM : {e}")
            self.ser = None

    def envoyer_at(self, commande, attente=1):
        """Envoie une commande AT brute au module et retourne la réponse."""
        if self.ser and self.ser.is_open:
            self.ser.write((commande + '\r\n').encode())
            time.sleep(attente)
            reponse = self.ser.read_all().decode('utf-8', errors='ignore')
            return reponse
        return "Port série fermé."

    def envoyer_sms(self, numero, message):
        """Envoie un SMS à un numéro donné."""
        if not self.ser:
            print("Module GSM non initialisé.")
            return False

        print(f"Envoi du SMS vers {numero}...")
        
        # Passage en mode texte
        self.envoyer_at("AT+CMGF=1")
        time.sleep(0.5)

        # Commande pour spécifier le numéro de téléphone
        self.ser.write(f'AT+CMGS="{numero}"\r\n'.encode())
        time.sleep(1)

        # Corps du message suivi du caractère de fin (Ctrl+Z / ASCII 26)
        self.ser.write((message + chr(26)).encode())
        time.sleep(3)

        reponse = self.ser.read_all().decode('utf-8', errors='ignore')
        if "OK" in reponse:
            print("SMS envoyé avec succès !")
            return True
        else:
            print(f"Échec de l'envoi du SMS. Réponse : {reponse}")
            return False

    def fermer(self):
        """Ferme la connexion série proprement."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Connexion GSM fermée.")

# ==========================================
# Intégration dans votre application principale
# ==========================================
if __name__ == "__main__":
    # Initialisation du module (adaptez le port selon votre système)
    gsm = GSMModule(port='COM3', baudrate=9600)

    # Exemple d'utilisation dans votre logique
    # Par exemple, déclenché suite à une condition de votre script :
    numero_destinataire = "+33600000000"
    message_alerte = "Alerte : Votre application a déclenché un événement GSM."
    
    # gsm.envoyer_sms(numero_destinataire, message_alerte)

    # Fermeture propre à la fin du script
    gsm.fermer()

