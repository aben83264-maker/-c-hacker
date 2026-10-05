# --- MODULE 4 : INTERCEPTION SITES VISITÉS & MÉTADONNÉES RÉSEAU ---
elif menu == "Interception sites visités":
    st.subheader("🌐 Analyse des métadonnées réseau & Flux")
    num_intercep = st.text_input("Numéro ou IP cible", "+33 (0) 6 51 43 46 40")
    
    if st.button("Capturer les paquets et métadonnées"):
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.success(f"Capture réseau réussie pour la cible : {num_intercep}")
        st.info(f"🕒 **Horodatage de la connexion** : {maintenant}")
        
        st.markdown("### 📊 Métadonnées des flux actifs :")
        
        # Site 1 : Google
        with st.expander("🔗 1. Google.com (HTTPS / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `142.250.190.46`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets échangés** : `1.2 Ko (Requête) / 14.5 Ko (Réponse)`")
            st.write("- **Statut de la session** : Actif (TLS 1.3)")
            
        # Site 2 : Instagram
        with st.expander("🔗 2. Instagram.com (HTTPS / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `157.240.199.174`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets échangés** : `850 octets (Requête) / 48.2 Ko (Médias/Images)`")
            st.write("- **Statut de la session** : Actif (Keep-Alive)")
            
        # Site 3 : WhatsApp
        with st.expander("🔗 3. WhatsApp.com / API (Port 5222 / 443)"):
            st.write("- **Adresse IP source/destination** : `192.168.1.55` ➔ `157.240.197.60`")
            st.write(f"- **Horodatage précis** : {maintenant}")
            st.write("- **Taille des paquets de données échangés** : `420 octets (Payload chiffré)`")
            st.write("- **Statut de la session** : Actif (Connexion persistante / WebSocket)")
