import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Auditoría de Reclutamiento SWGOH", page_icon="📊", layout="wide")

st.title("📊 Auditoría de Reclutamiento - SWGOH")
st.write("Introduce el Código de Aliado del candidato (o la URL de swgoh.gg) para analizar su inventario:")

ally_input = st.text_input("Código de Aliado (ej: 736-231-314 o 883-313-486):", "")

if st.button("🔍 Generar Informe de Auditoría"):
    code_clean = ally_input.replace("-", "").strip()
    # Si introdujo una URL, extraer el código numérico
    if "swgoh.gg" in code_clean:
        import re
        match = re.search(r'(\d{9})', code_clean)
        if match:
            code_clean = match.group(1)

    if not code_clean or not code_clean.isdigit():
        st.error("Por favor, introduce un Código de Aliado válido (9 dígitos).")
    else:
        with st.spinner("Obteniendo datos a través del servicio puente..."):
            # Usar API pública directamente con encabezados
            target_url = f"https://swgoh.gg/api/player/{code_clean}/"
            
            # Intento de petición
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
            
            # Servicio de proxy alternativo en caso de bloqueo de Cloudflare
            proxy_url = f"https://api.allorigins.win/get?url={requests.utils.quote(target_url)}"
            
            try:
                # Probar conexión mediante proxy
                response = requests.get(proxy_url, timeout=15)
                if response.status_code == 200:
                    import json
                    json_raw = response.json().get('contents')
                    data = json.loads(json_raw)
                    
                    player_data = data.get("data", {})
                    player_name = player_data.get("name", f"Jugador {code_clean}")
                    guild_name = player_data.get("guild_name", "Sin Gremio")
                    units_list = data.get("units", [])
                    units = {u["data"]["base_id"]: u["data"] for u in units_list if "data" in u}

                    st.success(f"¡Datos cargados con éxito para **{player_name}** ({guild_name})!")
                    st.markdown("---")
                    st.markdown(f"## 📊 INFORME DE AUDITORÍA: {player_name}")
                    st.markdown(f"**Gremio Actual:** {guild_name}")

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

                    # 1. Clones Luminosos
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

                    # 2. Requisitos RoTE
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

                else:
                    st.error("No se pudo obtener la información a través del servidor proxy.")

            except Exception as e:
                st.error(f"Error en la consulta: {str(e)}")
