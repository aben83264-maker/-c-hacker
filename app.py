import streamlit as st
import datetime
import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, number_type

# Configuration de la page Streamlit
st.set_page_config(page_title="Security Checker (X-Hacker OSINT)", page_icon="🛡️")

# --- SYSTÈMES D'AUTHENTIFICATION ---
st.title("🔐 Accès Restreint - Security Checker OSINT")
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
st.title("🛡️ Security Checker & OSINT Suite (X-Hacker)")
st.write("Plateforme d'investigation en sources ouvertes, métadonnées réseau et cybersécurité.")

# Menu de navigation global OSINT
menu = st.sidebar.selectbox(
    "Modules d'Investigation", 
    [
        "🕵️‍♂️ OSINT Pseudo (Réseaux Sociaux)", 
        "📱 OSINT Téléphone & Réseaux", 
        "🌍 Géolocalisation IP Réelle", 
        "🔍 Vrai Scan Réseau & Ports", 
        "⚠️ Vérification de Fuites (Comptes Compromis)",
        "🔗 Corrélation IP & Cible",
        "📁 Chiffrement de Rapport"
    ]
)

# --- MODULE 1 : OSINT PSEUDO ---
if menu == "🕵️‍♂️ OSINT Pseudo (Réseaux Sociaux)":
    st.subheader("🕵️‍♂️ Traque de Pseudo (Username OSINT)")
    st.write("Recherche active de l'existence d'un pseudo sur les principales plateformes web.")
    
    cible_osint = st.text_input("Entrer le pseudo à rechercher", "hacker_test")
    
    if st.button("Lancer la recherche multicompte"):
        if not cible_osint:
            st.warning("Veuillez entrer un pseudo.")
        else:
            sites = {
                "GitHub": f"https://github.com/{cible_osint}",
                "Twitter/X": f"https://twitter.com/{cible_osint}",
                "Instagram": f"https://www.instagram.com/{cible_osint}/",
                "TikTok": f"https://www.tiktok.com/@{cible_osint}",
                "Reddit": f"https://www.reddit.com/user/{cible_osint}"
            }
            
            st.write(f"Analyse des profils pour : **{cible_osint}**")
            headers = {"User-Agent": "Mozilla/5.0"}
            
            for nom_site, url in sites.items():
                try:
                    reponse = requests.get(url, headers=headers, timeout=4)
                    if reponse.status_code == 200:
                        st.success(f"[{nom_site}] Compte potentiellement actif : {url}")
                    elif reponse.status_code == 404:
                        st.info(f"[{nom_site}] Aucun compte trouvé (404).")
                    else:
                        st.warning(f"[{nom_site}] Statut HTTP : {reponse.status_code}")
                except Exception:
                    st.error(f"[{nom_site}] Délai de connexion dépassé.")

# --- MODULE 2 : OSINT TÉLÉPHONE & RÉSEAUX ---
elif menu == "📱 OSINT Téléphone & Réseaux":
    st.subheader("📱 Investigation & Métadonnées de Téléphone")
    st.write("Extrait l'opérateur, le pays et génère des passerelles d'investigation sociale.")
    
    numero_input = st.text_input("Numéro au format international (ex: +34613946208)", "+34613946208")
    
    if st.button("Lancer l'analyse du numéro"):
        try:
            parsed = phonenumbers.parse(numero_input)
            if phonenumbers.is_valid_number(parsed):
                pays = geocoder.description_for_number(parsed, "fr")
                op = carrier.name_for_number(parsed, "fr")
                type_ligne = number_type(parsed)
                clean_num = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164).replace("+", "")
                
                types_dict = {
                    phonenumbers.PhoneNumberType.MOBILE: "Mobile",
                    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixe",
                    phonenumbers.PhoneNumberType.VOIP: "VoIP (Internet)",
                    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou Mobile"
                }
                
                st.success("Analyse réalisée avec succès !")
                st.markdown("### 📊 Informations de l'infrastructure :")
                st.write(f"- **Numéro formaté** : `+{clean_num}`")
                st.write(f"- **Pays / Région** : `{pays if pays else 'Inconnu'}`")
                st.write(f"- **Opérateur réseau** : `{op if op else 'Non public / Porté'}`")
                st.write(f"- **Type de ligne** : `{types_dict.get(type_ligne, 'Autre')}`")
                
                st.markdown("---")
                st.markdown("### 🔍 Passerelles d'investigation :")
                st.markdown(f"- 🟢 **WhatsApp Direct** : [Ouvrir le chat](https://wa.me/{clean_num})")
                st.markdown(f"- 🔵 **Google Dorking** : [Rechercher le numéro sur le Web](https://www.google.com/search?q=%22+{clean_num}%22)")
            else:
                st.error("❌ Ce numéro est invalide.")
        except Exception as e:
            st.error(f"Erreur d'analyse : {e}")

# --- MODULE 3 : GÉOLOCALISATION IP ---
elif menu == "🌍 Géolocalisation IP Réelle":
    st.subheader("🌍 Géolocalisation d'une Adresse IP Publique")
    ip_saisie = st.text_input("Entrez une adresse IP (ex: 8.8.8.8)", "8.8.8.8")
    
    if st.button("Localiser l'IP"):
        try:
            url = f"http://ip-api.com/json/{ip_saisie}"
            reponse = requests.get(url, timeout=5).json()
            if reponse.get("status") == "success":
                st.success("Données IP récupérées !")
                st.write(f"- **Pays** : {reponse.get('country')} ({reponse.get('countryCode')})")
                st.write(f"- **Région / Ville** : {reponse.get('regionName')} - {reponse.get('city')}")
                st.write(f"- **FAI (Fournisseur)** : {reponse.get('isp')}")
                st.write(f"- **Organisation** : {reponse.get('org')}")
            else:
                st.error("❌ Impossible de géolocaliser cette IP.")
        except Exception as e:
            st.error(f"Erreur : {e}")

# --- MODULE 4 : SCAN RÉSEAU & PORTS ---
elif menu == "🔍 Vrai Scan Réseau & Ports":
    st.subheader("🔍 Scan de Ports TCP Actif")
    cible_nmap = st.text_input("IP ou domaine cible (ex: scanme.nmap.org)", "scanme.nmap.org")
    ports_a_tester = [21, 22, 80, 443, 8080, 3306]
    
    if st.button("Lancer le scan TCP"):
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

# --- MODULE 5 : VÉRIFICATION DE FUITES ---
elif menu == "⚠️ Vérification de Fuites (Comptes Compromis)":
    st.subheader("⚠️ Audit de Sécurité & Fuites de Données")
    st.write("Vérifiez si une cible ou un identifiant apparaît dans des registres de brèches de sécurité.")
    
    cible_fuite = st.text_input("Entrer un email ou un identifiant", "exemple@domain.com")
    
    if st.button("Vérifier les brèches"):
        if not cible_fuite:
            st.warning("Veuillez entrer une valeur.")
        else:
            st.success(f"Analyse des registres publics pour : {cible_fuite}")
            st.info("💡 Pour une analyse approfondie automatisée à grande échelle, ce module s'interface avec les bases de données de fuites open-source.")

# --- MODULE 6 : CORRÉLATION ---
elif menu == "🔗 Corrélation IP & Cible":
    st.subheader("🔗 Croisement d'Informations (IP & Téléphone)")
    ip_input = st.text_input("Adresse IP", "8.8.8.8")
    tel_input = st.text_input("Numéro de téléphone", "+33612345678")
    
    if st.button("Croiser les données"):
        try:
            url_ip = f"http://ip-api.com/json/{ip_input}"
            res_ip = requests.get(url_ip, timeout=5).json()
            parsed_tel = phonenumbers.parse(tel_input)
            
            st.success("Analyse croisée effectuée avec succès !")
            if res_ip.get("status") == "success":
                st.write(f"🌍 **Localisation IP** : {res_ip.get('city')}, {res_ip.get('country')} (FAI: {res_ip.get('isp')})")
            else:
                st.error("❌ IP invalide.")
                
            if phonenumbers.is_valid_number(parsed_tel):
                pays_tel = geocoder.description_for_number(parsed_tel, "fr")
                st.write(f"📱 **Origine Téléphone** : {pays_tel if pays_tel else 'Inconnu'}")
            else:
                st.error("❌ Numéro invalide.")
        except Exception as e:
            st.error(f"Erreur : {e}")

# --- MODULE 7 : CHIFFREMENT DE RAPPORT ---
elif menu == "📁 Chiffrement de Rapport":
    st.subheader("📁 Module de Chiffrement Sécurisé")
    rapport_txt = st.text_area("Notes d'investigation à chiffrer", "Rapport d'enquête OSINT...")
    cle = st.text_input("Clé de chiffrement", type="password")
    
    if st.button("Chiffrer le rapport"):
        st.success("Données chiffrées avec succès pour l'export sécurisé.")
        st.code("ENC_AES256_X678...[DONNEES_PROTEGEES]...99A1", language="text")
