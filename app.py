import streamlit as st
import requests
import re

st.set_page_config(page_title="Auditoría de Reclutamiento SWGOH", page_icon="📊", layout="wide")

st.title("📊 Auditoría de Reclutamiento - SWGOH")
st.write("Introduce el **Código de Aliado** del candidato para extraer los datos directamente de la API JSON de swgoh.gg:")

ally_input = st.text_input("Código de Aliado (ej: 469339749):", "469339749")

if st.button("🔍 Extraer y Auditar JSON"):
    code_clean = re.sub(r'\D', '', ally_input)
    
    if not code_clean:
        st.error("Por favor, introduce un código de aliado válido.")
    else:
        with st.spinner("Conectando con la API de SWGOH.GG..."):
            api_url = f"https://swgoh.gg/api/player/{code_clean}/"
            
            # Cabeceras avanzadas para evitar bloqueos básicos
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://swgoh.gg/"
            }
            
            try:
                # Petición directa a la API
                response = requests.get(api_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    player_data = data.get("data", {})
                    player_name = player_data.get("name", f"Jugador {code_clean}")
                    guild_name = player_data.get("guild_name", "Sin Gremio")
                    units_list = data.get("units", [])
                    
                    # Diccionario rápido de unidades del jugador (clave: base_id)
                    units = {}
                    for u in units_list:
                        u_data = u.get("data", {})
                        base_id = u_data.get("base_id")
                        if base_id:
                            units[base_id] = u_data

                    st.success(f"¡JSON cargado correctamente para **{player_name}** (Gremio: {guild_name})!")
                    st.markdown("---")
                    st.markdown(f"## 📋 INFORME DE AUDITORÍA: {player_name}")
                    
                    # Función auxiliar para leer reliquia o nivel de equipo del JSON
                    def get_unit_status(base_id, min_relic=7):
                        unit = units.get(base_id)
                        if not unit:
                            return "❌ No Desbloqueado", 0
                        
                        # En la API de swgoh.gg, relic_tier: 1 es G12, 2 es G13, 3 es R1, 4 es R2... por lo que R7 es relic_tier 9
                        relic_tier = unit.get("relic_tier", 1)
                        gear_level = unit.get("gear_level", 1)
                        
                        if relic_tier > 2:
                            r_val = relic_tier - 2
                            status = "✅ APTO" if r_val >= min_relic else f"❌ Requiere R{min_relic}+"
                            return f"R{r_val}", status
                        else:
                            return f"G{gear_level}", f"❌ Requiere R{min_relic}+"

                    col1, col2 = st.columns(2)

                    with col1:
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
                            r_str, status = get_unit_status(cid, min_relic=7)
                            st.write(f"* **{cname}:** `{r_str}` ➔ {status}")

                    with col2:
                        st.markdown("### 🏛️ Requisitos RoTE clave")
                        rote_units = [
                            ("QIRA", "Qi'ra", 5),
                            ("YOUNGHAN", "Joven Han Solo", 5),
                            ("JKCAL", "Cal Kestis", 7),
                            ("CEREJUNDA", "Cere Junda", 7),
                            ("GRANDINQUISITOR", "Gran Inquisidor", 7),
                            ("BOKATANMANDALOR", "Bo-Katan (Mand'alor)", 7),
                            ("MERRIN", "Merrin", 7),
                            ("SAWGERRERA", "Saw Gerrera", 7),
                            ("LUTHENRAEL", "Luthen Rael", 7)
                        ]
                        for cid, cname, req in rote_units:
                            r_str, status = get_unit_status(cid, min_relic=req)
                            st.write(f"* **{cname}:** `{r_str}` ➔ {status}")

                elif response.status_code == 403:
                    st.error("Cloudflare ha bloqueado la petición directa desde Streamlit (Error 403). Como alternativa si esto ocurre, recuerda que podemos usar un proxy intermedio en la URL.")
                else:
                    st.error(f"Error al conectar con la API (Código HTTP {response.status_code}). Comprueba que el código de aliado sea correcto.")

            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
