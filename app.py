import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="Auditoría de Reclutamiento SWGOH", page_icon="📊", layout="wide")

st.title("📊 Auditoría de Reclutamiento - SWGOH")
st.write("Introduce el código de aliado del candidato para generar el informe automático según la matriz del gremio.")

# Entrada del código de aliado
ally_code = st.text_input("Código de Aliado (ejemplo: 736231314 o 736-231-314):", "")

# Matriz oficial de omicrones del gremio
MATRIZ_OMICRONES_P1 = [
    ("GENERALSYNDULLA", "General Syndulla", "Único omi"),
    ("PADAWANSABINE", "Padawan Sabine Wren", "Único omi"),
    ("FULCRUMAHOOKA", "Ahsoka Tano (Fulcrum)", "Único omi"),
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

if st.button("🔍 Generar Informe de Auditoría"):
    code_clean = ally_code.replace("-", "").strip()
    if not code_clean or not code_clean.isdigit():
        st.error("Por favor, introduce un Código de Aliado válido (solo números).")
    else:
        with st.spinner("Consultando la API de swgoh.gg..."):
            url = f"https://swgoh.gg/api/player/{code_clean}/"
            response = requests.get(url)
            
            if response.status_code != 200:
                st.error("No se pudo obtener la información del jugador. Verifica el Código de Aliado.")
            else:
                data = response.json()
                player_name = data.get("data", {}).get("name", "Desconocido")
                guild_name = data.get("data", {}).get("guild_name", "Sin Gremio")
                units = {u["data"]["base_id"]: u["data"] for u in data.get("units", [])}

                st.success(f"¡Datos cargados con éxito para **{player_name}** ({guild_name})!")
                
                # Resumen Markdown para copiar
                st.subheader("📋 Informe Formateado")
                
                # Función auxiliar de reliquias
                def get_relic(base_id):
                    unit = units.get(base_id)
                    if not unit:
                        return "❌ No Desbloqueado", 0
                    r_level = unit.get("relic_tier", 1) - 2
                    if r_level > 0:
                        return f"R{r_level}", r_level
                    g_level = unit.get("gear_level", 1)
                    return f"G{g_level}", 0

                # Renderizado de Secciones
                st.markdown(f"### 📊 INFORME DE AUDITORÍA: {player_name}")
                st.markdown(f"**Gremio Actual:** {guild_name}")
                
                # 1. Clones Luminosos
                st.markdown("#### 🪖 Clones Luminosos (Mínimo R7 Exigido)")
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
                    status = "✅ APTO" if r_num >= 7 else "❌ NO APTO (Requiere R7+)"
                    st.write(f"- **{cname}:** {r_str} ➔ {status}")
                
                st.info("Tip: Puedes seleccionar todo el texto generado para copiarlo a Discord o WhatsApp.")