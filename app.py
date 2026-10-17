import streamlit as st
import requests
import json
import re

st.set_page_config(page_title="Auditoría de Reclutamiento SWGOH", page_icon="📊", layout="wide")

st.title("📊 Auditoría de Reclutamiento - SWGOH")
st.write("Herramienta oficial de auditoría para **Knights of Zuera**.")

tab1, tab2 = st.tabs(["🌐 Vía Código de Aliado / API", "📋 Vía Pegar Datos Directos"])

# --- MATRIZ DE OMICRONES DEL GREMIO ---
MATRIZ_OMICRONES_P1 = [
    ("GENERALSYNDULLA", "General Syndulla", "Único omi"),
    ("PADAWANSABINE", "Padawan Sabine Wren", "Único omi"),
    ("FULCRUMAHSOKA", "Ahsoka Tano (Fulcrum)", "Único omi"),
    ("CALKESTIS", "Cal Kestis", "Único omi"),
    ("BRUTUS", "Brutus", "Único omi"),
    ("SM33", "SM-33", "First Mate of the Onyx Cinder"),
    ("EMBO", "Embo", "Único omi"),
    ("DISGUISEDCLONETROOPER", "Soldado clon disfrazado", "Único omi"),
    ("GREATMOTHERS", "Grandes Madres", "Threads of Destiny (Líder)"),
    ("GREATMOTHERS", "Grandes Madres", "To The Old Ways (Única)"),
    ("KELLERANBEQ", "Kelleran Beq", "Único omi"),
    ("MASTERQUIGON", "Maestro Qui-Gon", "Único omi"),
    ("BOSSNASS", "Jefe Nass", "Único omi"),
    ("MAULHATEFUELED", "Maul (Alimentado por Odio)", "Hatred Sustains (Única)"),
    ("SHINHATI", "Shin Hati", "Único omi"),
]

MATRIZ_OMICRONES_P2 = [
    ("SM33", "SM-33", "Limb From Limb (Esp 1)"),
    ("CINTA", "Cinta Kas", "Omi secundario"),
    ("GRANDINQUISITOR", "Gran Inquisidor", "Ready to Die? (Líder)"),
    ("MARAJADE", "Mara Jade", "Omi secundario"),
    ("MAULHATEFUELED", "Maul (Alimentado por Odio)", "Relentless Malice (Esp 1)"),
    ("MOFFGIDEONS3", "Soldado Oscuro Moff Gideon", "Shadow Contingency (Líder)"),
]

# --- FUNCIONES DE PROCESAMIENTO ---

def process_player_data(data):
    player_data = data.get("data", {})
    player_name = player_data.get("name", "Candidato")
    guild_name = player_data.get("guild_name", "Sin Gremio")
    units_list = data.get("units", [])
    units = {u["data"]["base_id"]: u["data"] for u in units_list if "data" in u}

    st.success(f"¡Datos cargados con éxito para **{player_name}** ({guild_name})!")
    st.markdown("---")
    st.markdown(f"## 📋 INFORME DE AUDITORÍA: {player_name}")
    st.markdown(f"**Gremio Actual:** `{guild_name}`")

    def get_relic(base_id):
        unit = units.get(base_id)
        if not unit:
            return "❌ No Desbloqueado", 0
        r_level = unit.get("relic_tier", 1) - 2
        if r_level > 0:
            return f"R{r_level}", r_level
        g_level = unit.get("gear_level", 1)
        return f"G{g_level}", 0

    col1, col2 = st.columns(2)

    with col1:
        # 1. Leyendas Galácticas
        st.markdown("### 👑 Leyendas Galácticas (GLs)")
        gls = [
            ("SUPREMELEADERKEYLO REN", "Kylo Ren (GL)"),
            ("REY", "Rey (GL)"),
            ("JEDIMASTERCURTIS", "Maestro Jedi Luke"),
            ("SITHPALPATINE", "Sith Eterno"),
            ("JEDIMASTERKENOBI", "Maestro Jedi Kenobi"),
            ("LORDVADER", "Lord Vader"),
            ("JABBA", "Jabba el Hutt"),
            ("JEDIKNIGHTCAL", "Caballero Jedi Cal Kestis"),
            ("AHSOKATANO", "Ahsoka Tano (GL)")
        ]
        for gid, gname in gls:
            r_str, r_num = get_relic(gid)
            st.write(f"* **{gname}:** `{r_str}`")

        # 2. Clones Luminosos
        st.markdown("### 🪖 Clones Luminosos (Mínimo R7)")
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
            status = "✅ APTO" if r_num >= 7 else "❌ REQUIERE R7+"
            st.write(f"* **{cname}:** `{r_str}` ➔ {status}")

    with col2:
        # 3. Requisitos RoTE
        st.markdown("### 🏛️ Requisitos RoTE")
        st.markdown("**Mínimo R5:**")
        for rid, rname in [("QIRA", "Qi'ra"), ("YOUNGHAN", "Joven Han Solo")]:
            r_str, r_num = get_relic(rid)
            status = "✅ APTO" if r_num >= 5 else "❌ REQUIERE R5+"
            st.write(f"* **{rname}:** `{r_str}` ➔ {status}")

        st.markdown("**Mínimo R7:**")
        rote_r7 = [
            ("JKCAL", "JKCK"),
            ("CEREJUNDA", "Cere Junda"),
            ("GRANDINQUISITOR", "Gran Inquisidor"),
            ("BOKATANMANDALOR", "Bo-Katan (Mand'alor)"),
            ("MERRIN", "Merrin"),
            ("SAWGERRERA", "Saw Gerrera"),
            ("LUTHENRAEL", "Luthen Rael")
        ]
        for rid, rname in rote_r7:
            r_str, r_num = get_relic(rid)
            status = "✅ APTO" if r_num >= 7 else "❌ REQUIERE R7+"
            st.write(f"* **{rname}:** `{r_str}` ➔ {status}")

    st.markdown("---")
    st.markdown("### 🔮 Matriz de Omicrones Exigidos")
    
    col_omi1, col_omi2 = st.columns(2)
    with col_omi1:
        st.markdown("**Prioridad 1 (OBLIGATORIOS):**")
        for base_id, name, desc in MATRIZ_OMICRONES_P1:
            r_str, _ = get_relic(base_id)
            st.write(f"* **{name}** ({desc}): `{r_str}`")

    with col_omi2:
        st.markdown("**Prioridad 2 (SECUNDARIOS):**")
        for base_id, name, desc in MATRIZ_OMICRONES_P2:
            r_str, _ = get_relic(base_id)
            st.write(f"* **{name}** ({desc}): `{r_str}`")

def process_raw_text(text):
    st.success("¡Texto analizado correctamente!")
    st.markdown("---")
    st.markdown("## 📋 INFORME DE AUDITORÍA (Análisis de Texto Pegado)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🪖 Clones Luminosos y RoTE")
        units_to_check = [
            ("Captain Rex", "Captain Rex"),
            ("Fives", "CT-5555 'Fives'"),
            ("ARC Trooper", "ARC Trooper"),
            ("Echo", "CT-21-0408 'Echo'"),
            ("Rex", "CT-7567 'Rex'"),
            ("Cody", "CC-2224 'Cody'"),
            ("Qi'ra", "Qi'ra"),
            ("Young Han", "Joven Han Solo"),
            ("Cal Kestis", "Cal Kestis"),
            ("Cere Junda", "Cere Junda"),
            ("Grand Inquisitor", "Gran Inquisidor"),
            ("Bo-Katan", "Bo-Katan (Mand'alor)"),
            ("Merrin", "Merrin"),
            ("Saw Gerrera", "Saw Gerrera"),
            ("Luthen", "Luthen Rael")
        ]
        for key, name in units_to_check:
            match = re.search(rf"{key}.*?(R\d+|G\d+)", text, re.IGNORECASE)
            status = f"`{match.group(1)}` ✅" if match else "`No detectado / G12` ❌"
            st.write(f"* **{name}:** {status}")

    with col2:
        st.markdown("### 🔮 Verificación de Omicrones en Texto")
        st.write("Verificando presencia de unidades clave de la matriz:")
        for _, name, desc in MATRIZ_OMICRONES_P1[:8]:
            present = "✅ Presente" if name.lower() in text.lower() else "❌ No Detectado"
            st.write(f"* **{name}** ({desc}): {present}")

# --- INTERFAZ PRINCIPAL ---

with tab1:
    st.subheader("Búsqueda Automática")
    ally_input = st.text_input("Código de Aliado (ej: 883313486):", "", key="ally_code_input")
    
    if st.button("🔍 Auditar por Código de Aliado", key="btn_code"):
        code_clean = re.sub(r'\D', '', ally_input)
        if not code_clean:
            st.error("Por favor, introduce un código de aliado válido.")
        else:
            with st.spinner("Consultando datos del jugador..."):
                target_url = f"https://swgoh.gg/api/player/{code_clean}/"
                proxy_url = f"https://corsproxy.io/?{target_url}"
                
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(proxy_url, headers=headers, timeout=20)
                    
                    if response.status_code == 200:
                        data = response.json()
                        process_player_data(data)
                    else:
                        st.error(f"No se pudo obtener la información automáticamente (HTTP {response.status_code}). Prueba la pestaña 'Vía Pegar Datos Directos'.")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}. Prueba la pestaña 'Vía Pegar Datos Directos'.")

with tab2:
    st.subheader("Auditoría Instantánea (Sin Bloqueos)")
    st.write("Abre la página de personajes del jugador en `swgoh.gg`, pulsa `Ctrl + A` (seleccionar todo), `Ctrl + C` (copiar) y pégalo todo abajo:")
    raw_text = st.text_area("Pega aquí el contenido de la página de swgoh.gg:", height=200, key="text_area_input")
    
    if st.button("⚡ Auditar Texto Pegado", key="btn_text"):
        if not raw_text.strip():
            st.error("El campo de texto está vacío.")
        else:
            process_raw_text(raw_text)
