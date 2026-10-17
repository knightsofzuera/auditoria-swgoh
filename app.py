import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# Configuración de página
st.set_page_config(page_title="Auditoría de Reclutamiento SWGOH", page_icon="📊", layout="wide")

st.title("📊 Auditoría de Reclutamiento - SWGOH")
st.write("Introduce el código de aliado o el enlace de swgoh.gg del candidato para analizar su inventario:")

ally_input = st.text_input("Código de Aliado (ej: 736-231-314) o URL del perfil:", "")

if st.button("🔍 Generar Informe de Auditoría"):
    clean_input = ally_input.strip()
    
    # Extraer código de aliado si se introdujo una URL completa
    if "swgoh.gg" in clean_input:
        match = re.search(r'/p/(\d+)', clean_input)
        if match:
            ally_code = match.group(1)
        else:
            ally_code = re.sub(r'\D', '', clean_input)
    else:
        ally_code = re.sub(r'\D', '', clean_input)

    if not ally_code:
        st.error("Por favor, introduce un Código de Aliado o enlace válido.")
    else:
        with st.spinner("Analizando perfil del candidato en swgoh.gg..."):
            profile_url = f"https://swgoh.gg/p/{ally_code}/characters/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            try:
                response = requests.get(profile_url, headers=headers, timeout=15)
                
                if response.status_code != 200:
                    st.error(f"No se pudo acceder al perfil (Error HTTP {response.status_code}). Verifica que el código de aliado ({ally_code}) esté registrado en swgoh.gg.")
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraer el nombre del jugador
                    name_elem = soup.select_one('.profile-portrait-name, h2, title')
                    player_name = name_elem.text.strip().replace(" · Characters", "").replace(" | SWGOH.GG", "") if name_elem else f"Jugador {ally_code}"
                    
                    st.success("¡Perfil cargado con éxito!")
                    st.markdown("---")
                    st.markdown(f"## 📊 INFORME DE AUDITORÍA: {player_name}")
                    st.markdown(f"🔗 **Perfil SWGOH.GG:** [{profile_url}]({profile_url})")
                    
                    # Mapear unidades y sus niveles de reliquia o nivel
                    units_data = {}
                    char_items = soup.select('.collection-char, .media-list-item')
                    
                    for item in char_items:
                        name_node = item.select_one('.collection-char-name-link, .media-list-item-title')
                        relic_node = item.select_one('.relic-badge')
                        if name_node:
                            c_name = name_node.text.strip().lower()
                            r_text = f"R{relic_node.text.strip()}" if relic_node else "G12 / Desbloqueado"
                            units_data[c_name] = r_text

                    # 1. Clones Luminosos
                    st.markdown("### 🪖 Clones Luminosos (Mínimo R7 Exigido)")
                    clones = [
                        ("Captain Rex", "Captain Rex"),
                        ("CT-5555 \"Fives\"", "CT-5555 'Fives'"),
                        ("ARC Trooper", "ARC Trooper"),
                        ("CT-21-0408 \"Echo\"", "CT-21-0408 'Echo'"),
                        ("CT-7567 \"Rex\"", "CT-7567 'Rex'"),
                        ("CC-2224 \"Cody\"", "CC-2224 'Cody'")
                    ]
                    for key_name, display_name in clones:
                        estado = units_data.get(key_name.lower(), "❌ No Desbloqueado / Menor a R7")
                        st.write(f"- **{display_name}:** `{estado}`")

                    # 2. Requisitos RoTE
                    st.markdown("### 🏛️ Requisitos RoTE (Rise of the Empire)")
                    st.markdown("**Requisitos R5+:**")
                    rote_r5 = [("Qi'ra", "Qi'ra"), ("Young Han Solo", "Joven Han Solo")]
                    for key_name, display_name in rote_r5:
                        estado = units_data.get(key_name.lower(), "❌ No Desbloqueado / Menor a R5")
                        st.write(f"- **{display_name}:** `{estado}`")
                        
                    st.markdown("**Requisitos R7+:**")
                    rote_r7 = [
                        ("Jedi Knight Cal Kestis", "Caballero Jedi Cal Kestis (JKCK)"),
                        ("Cere Junda", "Cere Junda"),
                        ("Grand Inquisitor", "Gran Inquisidor"),
                        ("Bo-Katan (Mand'alor)", "Bo-Katan (Mand'alor)"),
                        ("Merrin", "Merrin"),
                        ("Saw Gerrera", "Saw Gerrera"),
                        ("Luthen Rael", "Luthen Rael")
                    ]
                    for key_name, display_name in rote_r7:
                        estado = units_data.get(key_name.lower(), "❌ No Desbloqueado / Menor a R7")
                        st.write(f"- **{display_name}:** `{estado}`")

            except Exception as e:
                st.error(f"Error al procesar la información: {str(e)}")
