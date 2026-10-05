import streamlit as st
import datetime
import random

# Configuration de la page
st.set_page_config(page_title="Security Checker (X-Hacker)", page_icon="🛡️")

st.title("🛡️ Security Checker (X-Hacker)")
st.write("Plateforme interactive de simulation de cybersécurité offensive et défensive.")

# Menu de navigation dans la barre latérale incluant l'interception
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

# --- MODULE 4 : INTERCEPTION SITES VISITÉS ---
elif menu == "Interception sites visités":
    st.subheader("🌐 Interception sites visités (Simulation)")
    num_intercep = st.text_input("Numéro de téléphone cible", "+33 (0) 6 51 43 46 40")
    
    if st.button("Analyser les flux"):
        st.write("🔗 [https://www.google.com](https://www.google.com)")
        st.write("🔗 [https://www.instagram.com](https://www.instagram.com)")
        st.write("🔗 [https://www.whatsapp.com](https://www.whatsapp.com)")

# --- MODULE 5 : SIMULATION SIEM ---
elif menu == "Simulation SIEM":
    st.subheader("📊 Simulation SIEM & Analyse de Logs")
    
    if st.button("Analyser les logs"):
        st.text("192.168.1.55 -- GET /index.php (200)")
        st.text("203.0.113.42 -- POST /login.php (401)")
        st.error("🔴 ALERTE CRITIQUE : Tentative de Brute-Force détectée depuis 203.0.113.42")
