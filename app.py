import streamlit as st
import requests
import json
import re

st.set_page_config(page_title="Auditoría de Reclutamiento SWGOH", page_icon="📊", layout="wide")

st.title("📊 Auditoría de Reclutamiento - SWGOH")
st.write("Elige la forma en la que quieres auditar al candidato:")

tab1, tab2 = st.tabs(["🌐 Vía Código de Aliado / API", "📋 Vía Pegar Datos Directos"])

# --- TAB 1: CÓDIGO DE ALIADO ---
with tab1:
    st.subheader("Búsqueda Automática")
    ally_input = st.text_input("Código de Aliado (ej: 883-313-486):", "", key="ally_code_input")
    
    if st.button("🔍 Auditar por Código de Aliado", key="btn_code"):
        code_clean = re.sub(r'\D', '', ally_input)
        if not code_clean:
            st.error("Por favor, introduce un código de aliado válido.")
        else:
            with st.spinner("Consultando datos del jugador..."):
                target_url = f"https://swgoh.gg/api/player/{code_clean}/"
                # Usamos un proxy CORS alternativo y rápido (corsproxy.io)
                proxy_url = f"https://corsproxy.io/?{target_url}"
                
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(proxy_url, headers=headers, timeout=25)
                    
                    if response.status_code == 200:
                        data = response.json()
                        process_player_data(data)
                    else:
                        st.error(f"No se pudo obtener la información automáticamente (HTTP {response.status_code}). Prueba la pestaña 'Vía Pegar Datos Directos'.")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}. Te recomendamos usar la pestaña 'Vía Pegar Datos Directos'.")

# --- TAB 2: PEGAR TEXTO DIRECTO ---
with tab2:
    st.subheader("Auditoría Instantánea (Sin Bloqueos)")
    st.write("Abre la página de personajes del jugador en `swgoh.gg`, pulsa `Ctrl + A` (seleccionar todo), `Ctrl + C` (copiar) y pégalo todo abajo:")
    raw_text = st.text_area("Pega aquí el contenido de la página de swgoh.gg:", height=200)
    
    if st.button("⚡ Auditar Texto Pegado", key="btn_text"):
        if not raw_text.strip():
            st.error("El campo de texto está vacío.")
        else:
            process_raw_text(raw_text)

# --- FUNCIONES DE PROCESAMIENTO ---
def process_player_data(data):
    player_data = data.get("data", {})
    player_name = player_data.get("name", "Candidato")
    guild_name = player_data.get("guild_name", "Sin Gremio")
    units_list = data.get("units", [])
    units = {u["data"]["base_id"]: u["data"] for u in units_list if "data" in u}

    st.success(f"¡Datos cargados con éxito para **{player_name}** ({guild_name})!")
    st.markdown("---")
    st.markdown(f"## 📊 INFORME DE AUDITORÍA: {player_name}")
    
    def get_relic(base_id):
        unit = units.get(base_id)
        if not unit:
            return "❌ No Desbloqueado", 0
        r_level = unit.get("relic_tier", 1) - 2
        if r_level > 0:
            return f"R{r_level}", r_level
        g_level = unit.get("gear_level", 1)
        return f"G{g_level}", 0

    st.markdown("### 🪖 Clones Luminosos (Mínimo R7 Exigido)")
    clones = [
        ("CAPTAINREX", "Captain Rex"),
        ("CT5555", "CT-5555 'Fives'"),
        ("ARCTROOPER", "ARC Trooper"),
        ("CT210408", "CT-21-0408 'Echo'"),
        ("CT7567", "CT-7567 'Rex'"),
        ("CC2224", "CC-2224 'Cody'")
    ]
    for cid, cname in clones:
        r_str, r_num = get_relic(cid)
        status = "✅ **APTO**" if r_num >= 7 else "❌ **NO APTO (Requiere R7+)**"
        st.write(f"* **{cname}:** `{r_str}` ➔ {status}")

    st.markdown("### 🏛️ Requisitos RoTE (Rise of the Empire)")
    st.markdown("**Requisitos R5+:**")
    for rid, rname in [("QIRA", "Qi'ra"), ("YOUNGHAN", "Joven Han Solo")]:
        r_str, r_num = get_relic(rid)
        status = "✅ Cumple" if r_num >= 5 else "❌ NO CUMPLE (Mínimo R5)"
        st.write(f"* **{rname}:** `{r_str}` ➔ {status}")

    st.markdown("**Requisitos R7+:**")
    rote_r7 = [
        ("JKCAL", "Caballero Jedi Cal Kestis (JKCK)"),
        ("CEREJUNDA", "Cere Junda"),
        ("GRANDINQUISITOR", "Gran Inquisidor"),
        ("BOKATANMANDALOR", "Bo-Katan (Mand'alor)"),
        ("MERRIN", "Merrin"),
        ("SAWGERRERA", "Saw Gerrera"),
        ("LUTHENRAEL", "Luthen Rael")
    ]
    for rid, rname in rote_r7:
        r_str, r_num = get_relic(rid)
        status = "✅ Cumple" if r_num >= 7 else "❌ NO CUMPLE (Mínimo R7)"
        st.write(f"* **{rname}:** `{r_str}` ➔ {status}")

def process_raw_text(text):
    st.success("¡Texto procesado correctamente!")
    st.markdown("---")
    st.markdown("## 📊 INFORME DE AUDITORÍA (Análisis de Texto)")
    
    lines = text.split("\n")
    text_lower = text.lower()
    
    st.markdown("### 🪖 Clones Luminosos")
    clones = ["Captain Rex", "CT-5555", "ARC Trooper", "Echo", "Rex", "CC-2224"]
    for c in clones:
        match = re.search(rf"{c}.*?(R\d+|G\d+)", text, re.IGNORECASE)
        val = match.group(1) if match else "No detectado en el texto pegado"
        st.write(f"* **{c}:** `{val}`")
