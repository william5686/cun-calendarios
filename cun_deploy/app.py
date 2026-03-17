"""
CUN – Calendarios Académicos
Fechas tomadas directamente del tablero oficial.
"""

import streamlit as st
from datetime import date

st.set_page_config(
    page_title="CUN – Calendarios",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #ffffff; color: #0f1117; }

.header {
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #1a2035;
    margin-bottom: 2rem;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0f1117;
}
.header-title span { color: #22d3a5; }
.header-sub {
    color: #4a5568;
    font-size: 0.9rem;
    margin-top: 0.3rem;
    font-weight: 300;
}

.fecha-hoy {
    display: inline-block;
    background: #0d1829;
    border: 1px solid #1a2e4a;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-size: 0.82rem;
    color: #4a9eff;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 0.8rem;
}

/* Cards principales */
.bloque-card {
    background: #0d1120;
    border: 1px solid #1a2035;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    cursor: pointer;
}
.bloque-card:hover { border-color: #22d3a5; }
.bloque-card.activo  { border-left: 4px solid #22d3a5; }
.bloque-card.proximo { border-left: 4px solid #4a9eff; }
.bloque-card.finalizado { border-left: 4px solid #2a3550; opacity: 0.6; }

.bloque-nombre {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0f0f0;
    margin-bottom: 0.6rem;
}
.bloque-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.badge-activo     { background: #0a2e1f; color: #22d3a5; border: 1px solid #22d3a544; }
.badge-proximo    { background: #0a1f3a; color: #4a9eff; border: 1px solid #4a9eff44; }
.badge-finalizado { background: #1a2035; color: #4a5568; border: 1px solid #2a3550; }

/* Sub-bloques */
.sub-bloques {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-top: 0.8rem;
}
.sub-card {
    background: #0a0f1c;
    border: 1px solid #1a2035;
    border-radius: 10px;
    padding: 0.9rem 1rem;
}
.sub-card.activo-sub   { border-color: #22d3a544; background: #071a12; }
.sub-card.proximo-sub  { border-color: #4a9eff44; background: #071224; }
.sub-card.done-sub     { opacity: 0.45; }

.sub-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.sub-titulo.t-act  { color: #22d3a5; }
.sub-titulo.t-prox { color: #4a9eff; }
.sub-titulo.t-done { color: #2a3a55; }

.sub-fechas {
    font-size: 0.88rem;
    color: #8892a4;
}
.sub-fechas strong { color: #c8d0dc; font-weight: 500; }

.dias-restantes {
    margin-top: 0.4rem;
    font-size: 0.78rem;
    font-weight: 600;
}
.dr-act  { color: #22d3a5; }
.dr-prox { color: #4a9eff; }
.dr-done { color: #2a3a55; }

/* Selector */
[data-testid="stSelectbox"] > div > div {
    background: #0d1120 !important;
    border: 1px solid #1a2035 !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
}
label { color: #4a5568 !important; font-size: 0.82rem !important; }

/* Divider */
.divider { border: none; border-top: 1px solid #1a2035; margin: 1.5rem 0; }

/* Tabla de actividades */
.act-section { margin-top: 1.8rem; border: 1px solid #1a2035; border-radius: 14px; overflow: hidden; }
.act-header { background: #0d1829; padding: 0.9rem 1.2rem; font-family: 'Syne', sans-serif;
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em;
    color: #4a9eff; border-bottom: 1px solid #1a2035; }
.corte-label { background: #0a1829; padding: 0.6rem 1.2rem; font-family: 'Syne', sans-serif;
    font-size: 0.78rem; font-weight: 700; color: #4a9eff; text-transform: uppercase;
    letter-spacing: 0.08em; border-bottom: 1px solid #1a2035;
    display: flex; justify-content: space-between; align-items: center; }
.corte-pct { background: #0d2a4a; color: #4a9eff; padding: 0.15rem 0.6rem;
    border-radius: 999px; font-size: 0.72rem; }
.act-row { display: grid; grid-template-columns: 50px 95px 95px 1fr 55px;
    gap: 0.5rem; padding: 0.65rem 1.2rem; border-bottom: 1px solid #0f1520;
    font-size: 0.83rem; align-items: center; }
.act-row:last-child { border-bottom: none; }
.act-row.vigente { background: #071a12; }
.act-row.proxima { background: #07121f; }
.act-row.done    { opacity: 0.45; }
.act-semana { color: #4a5568; font-weight: 600; text-align: center; }
.act-fecha  { color: #8892a4; font-size: 0.78rem; }
.act-nombre strong { color: #f0f0f0; display: block; }
.act-nombre span   { color: #6b7280; font-size: 0.78rem; }
.act-pct    { color: #22d3a5; font-weight: 600; font-size: 0.8rem; text-align: center; }
.col-headers { display: grid; grid-template-columns: 50px 95px 95px 1fr 55px;
    gap: 0.5rem; padding: 0.5rem 1.2rem; border-bottom: 1px solid #1a2035;
    font-size: 0.7rem; color: #2a3a55; text-transform: uppercase;
    letter-spacing: 0.08em; font-weight: 600; }

/* Resumen hoy */
.hoy-box {
    background: #071a12;
    border: 1px solid #22d3a544;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.5rem;
}
.hoy-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #22d3a5;
    margin-bottom: 0.8rem;
}
.hoy-item {
    display: flex;
    justify-content: space-between;
    padding: 0.35rem 0;
    border-bottom: 1px solid #0a2e1f;
    font-size: 0.88rem;
}
.hoy-item:last-child { border-bottom: none; }
.hoy-bloque { font-family: 'Syne', sans-serif; font-weight: 700; color: #f0f0f0; }
.hoy-sub    { color: #22d3a5; font-size: 0.8rem; }
.hoy-fecha  { color: #4a9eff; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ── DATOS OFICIALES DEL TABLERO ───────────────────────────────────────────────
# Formato: { "CODIGO": { "I": (inicio, fin), "II": (inicio, fin) } }
# Modalidades que comparten fechas: P=Presencial, T=Presencial(T), V=Virtual, 335

CALENDARIOS = {
    # 25P05 / 25T05 / 25V05
    "25P05": {"label": "25P05 · T05 · V05", "modalidades": ["Presencial","Virtual","335"],
              "I":  (date(2025,9,29), date(2025,11,22)),
              "II": (date(2025,11,24), date(2026,1,18))},
    "25T05": {"label": "25T05", "alias": "25P05", "modalidades": ["Bachilleresitario"],
              "I":  (date(2025,9,29), date(2025,11,22)),
              "II": (date(2025,11,24), date(2026,1,18))},
    "25V05": {"label": "25V05", "alias": "25P05", "modalidades": ["Virtual"],
              "I":  (date(2025,9,29), date(2025,11,22)),
              "II": (date(2025,11,24), date(2026,1,18))},

    # 25P06 / 25T06 / 25V06
    "25P06": {"label": "25P06 · T06 · V06", "modalidades": ["Presencial","Virtual","335"],
              "I":  (date(2025,11,24), date(2026,1,18)),
              "II": (date(2026,2,2),   date(2026,3,29))},
    "25T06": {"label": "25T06", "alias": "25P06", "modalidades": ["Bachilleresitario"],
              "I":  (date(2025,11,24), date(2026,1,18)),
              "II": (date(2026,2,2),   date(2026,3,29))},
    "25V06": {"label": "25V06", "alias": "25P06", "modalidades": ["Virtual"],
              "I":  (date(2025,11,24), date(2026,1,18)),
              "II": (date(2026,2,2),   date(2026,3,29))},

    # 2026A (Presencial anual)
    "2026A": {"label": "2026A", "modalidades": ["Presencial"],
              "I": (date(2026,2,2), date(2026,5,24))},

    # 26V01
    "26V01": {"label": "26V01", "modalidades": ["Virtual","335"],
              "I":  (date(2026,2,2),  date(2026,3,29)),
              "II": (date(2026,3,30), date(2026,5,24))},

    # 26P01 / 26T01
    "26P01": {"label": "26P01 · T01", "modalidades": ["Presencial","Bachilleresitario"],
              "I":  (date(2026,2,2),  date(2026,3,29)),
              "II": (date(2026,3,30), date(2026,5,24))},

    # 26V02
    "26V02": {"label": "26V02", "modalidades": ["Virtual","335"],
              "I":  (date(2026,3,30), date(2026,5,24)),
              "II": (date(2026,5,25), date(2026,7,19))},

    # 26P02 / 26T02
    "26P02": {"label": "26P02 · T02", "modalidades": ["Presencial","Bachilleresitario"],
              "I":  (date(2026,3,30), date(2026,5,24)),
              "II": (date(2026,5,25), date(2026,7,19))},

    # 26V03
    "26V03": {"label": "26V03", "modalidades": ["Virtual","335"],
              "I":  (date(2026,5,25), date(2026,7,19)),
              "II": (date(2026,8,3),  date(2026,9,27))},

    # 26P03 / 26T03
    "26P03": {"label": "26P03 · T03", "modalidades": ["Presencial","Bachilleresitario"],
              "I":  (date(2026,5,25), date(2026,7,19)),
              "II": (date(2026,8,3),  date(2026,9,27))},

    # 26V04
    "26V04": {"label": "26V04", "modalidades": ["Virtual","335"],
              "I":  (date(2026,8,3),  date(2026,9,27)),
              "II": (date(2026,9,28), date(2026,11,22))},

    # 26P04 / 26T04
    "26P04": {"label": "26P04 · T04", "modalidades": ["Presencial","Bachilleresitario"],
              "I":  (date(2026,8,3),  date(2026,9,27)),
              "II": (date(2026,9,28), date(2026,11,22))},
}

# ── ACTIVIDADES POR BLOQUE ────────────────────────────────────────────────────
# clave = codigo del bloque + "_" + sub ("I" o "II")
# Aplica a: 25P06/25T06/25V06 Bloque II  Y  26V01/26P01/26T01 Bloque I
# (mismas fechas para ambos según el calendario oficial)

ACTIVIDADES = {
    # 25P06·T06·V06 Bloque II  ==  26V01·P01·T01 Bloque I  (mismas fechas)
    "BLOQUE_VIRTUAL_B2_V1_B1": [
        # Primer Corte (30%)
        {"corte": "Primer Corte", "pct_corte": "30%", "semana": 1,
         "ini": date(2026,2,2),  "fin": date(2026,2,8),
         "nombre": "Introducción – Sesión de clase", "sub": "", "pct_act": ""},
        {"corte": "Primer Corte", "pct_corte": "30%", "semana": 2,
         "ini": date(2026,2,9),  "fin": date(2026,2,15),
         "nombre": "Quiz 1", "sub": "Sesión de Clase", "pct_act": "10%"},
        {"corte": "Primer Corte", "pct_corte": "30%", "semana": 3,
         "ini": date(2026,2,16), "fin": date(2026,2,22),
         "nombre": "Parcial 1", "sub": "Sesión de Clase", "pct_act": "20%"},
        # Segundo Corte (30%)
        {"corte": "Segundo Corte", "pct_corte": "30%", "semana": 4,
         "ini": date(2026,2,23), "fin": date(2026,3,1),
         "nombre": "Quiz 2", "sub": "Sesión de Clase", "pct_act": "10%"},
        {"corte": "Segundo Corte", "pct_corte": "30%", "semana": 5,
         "ini": date(2026,3,2),  "fin": date(2026,3,8),
         "nombre": "Parcial 2", "sub": "Sesión de Clase", "pct_act": "20%"},
        # Tercer Corte (40%)
        {"corte": "Tercer Corte", "pct_corte": "40%", "semana": 6,
         "ini": date(2026,3,9),  "fin": date(2026,3,15),
         "nombre": "ACA – Pitch (Disciplinares–NIP)", "sub": "Sesión de Clase", "pct_act": "34%"},
        {"corte": "Tercer Corte", "pct_corte": "40%", "semana": 7,
         "ini": date(2026,3,16), "fin": date(2026,3,22),
         "nombre": "Quiz 3", "sub": "Sesión de Clase", "pct_act": "2%"},
        {"corte": "Tercer Corte", "pct_corte": "40%", "semana": 7,
         "ini": date(2026,3,16), "fin": date(2026,3,22),
         "nombre": "Coevaluación", "sub": "", "pct_act": "2%"},
        {"corte": "Tercer Corte", "pct_corte": "40%", "semana": 7,
         "ini": date(2026,3,16), "fin": date(2026,3,22),
         "nombre": "Autoevaluación", "sub": "", "pct_act": "2%"},
        {"corte": "Tercer Corte", "pct_corte": "40%", "semana": 8,
         "ini": date(2026,3,23), "fin": date(2026,3,29),
         "nombre": "Cierre de Notas", "sub": "", "pct_act": ""},
    ],
}

# Mapeo: qué clave de actividades usar para cada bloque+sub
ACTIVIDADES_MAP = {
    "25P06_II": "BLOQUE_VIRTUAL_B2_V1_B1",
    "26V01_I":  "BLOQUE_VIRTUAL_B2_V1_B1",
    "26P01_I":  "BLOQUE_VIRTUAL_B2_V1_B1",
}

# ── LÓGICA ────────────────────────────────────────────────────────────────────
def fmt(d):
    return d.strftime("%d/%m/%Y") if d else "—"

def estado_sub(ini, fin):
    hoy = date.today()
    if ini is None or fin is None:
        return "desconocido"
    if hoy < ini:
        return "proximo"
    if hoy > fin:
        return "finalizado"
    return "activo"

def dias_info(ini, fin):
    hoy = date.today()
    if ini is None or fin is None:
        return "", ""
    if hoy < ini:
        dias = (ini - hoy).days
        return "proximo", f"Inicia en {dias} día{'s' if dias!=1 else ''}"
    if hoy > fin:
        return "finalizado", "Finalizado"
    dias = (fin - hoy).days
    return "activo", f"Faltan {dias} día{'s' if dias!=1 else ''}"

def estado_bloque(data):
    hoy = date.today()
    estados = []
    for sub in ["I", "II"]:
        rng = data.get(sub)
        if rng:
            estados.append(estado_sub(rng[0], rng[1]))
    if "activo" in estados:
        return "activo"
    if "proximo" in estados:
        return "proximo"
    return "finalizado"

def mostrar_actividades(actos):
    hoy = date.today()
    st.markdown('<div class="act-section">', unsafe_allow_html=True)
    st.markdown('<div class="act-header">📋 Calendario de Actividades</div>', unsafe_allow_html=True)
    st.markdown('<div class="col-headers"><span>Sem.</span><span>Inicio</span><span>Fin</span><span>Actividad</span><span>%</span></div>', unsafe_allow_html=True)

    corte_actual = None
    for a in actos:
        # Encabezado de corte
        if a["corte"] != corte_actual:
            corte_actual = a["corte"]
            st.markdown(f'<div class="corte-label"><span>{corte_actual}</span><span class="corte-pct">{a["pct_corte"]}</span></div>', unsafe_allow_html=True)

        # Estado de la fila
        if a["ini"] <= hoy <= a["fin"]:
            css_row = "vigente"
            dot = '<span class="act-estado-dot dot-act"></span>'
        elif a["ini"] > hoy:
            css_row = "proxima"
            dot = '<span class="act-estado-dot dot-prox"></span>'
        else:
            css_row = "done"
            dot = '<span class="act-estado-dot dot-done"></span>'

        sub_txt = f'<span>{a["sub"]}</span>' if a["sub"] else ""
        st.markdown(f"""
        <div class="act-row {css_row}">
            <div class="act-semana">{dot}{a['semana']}</div>
            <div class="act-fecha">{a['ini'].strftime('%d/%m/%Y')}</div>
            <div class="act-fecha">{a['fin'].strftime('%d/%m/%Y')}</div>
            <div class="act-nombre"><strong>{a['nombre']}</strong>{sub_txt}</div>
            <div class="act-pct">{a['pct_act']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
hoy = date.today()
st.markdown(f"""
<div class="header">
    <div class="header-title">Calendarios Académicos <span>CUN</span></div>
    <div class="header-sub">Corporación Unificada Nacional de Educación Superior</div>
    <div class="fecha-hoy">📅 HOY: {hoy.strftime("%d/%m/%Y")}</div>
</div>
""", unsafe_allow_html=True)

# ── RESUMEN ACTIVOS HOY ───────────────────────────────────────────────────────
activos_hoy = []
for codigo, data in CALENDARIOS.items():
    if data.get("alias"):
        continue
    for sub in ["I", "II"]:
        rng = data.get(sub)
        if rng and rng[0] <= hoy <= rng[1]:
            activos_hoy.append((data["label"], f"Bloque {sub}", rng[1]))

if activos_hoy:
    st.markdown('<div class="hoy-box"><div class="hoy-titulo">🟢 En curso hoy</div>', unsafe_allow_html=True)
    for lbl, sub, fin_r in activos_hoy:
        st.markdown(f"""
        <div class="hoy-item">
            <span class="hoy-bloque">{lbl} <span class="hoy-sub">— {sub}</span></span>
            <span class="hoy-fecha">hasta {fmt(fin_r)}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🔍 Buscar bloque", "📋 Todos los bloques"])

# ══ TAB 1 ════════════════════════════════════════════════════════════════════
with tab1:
    codigos_principales = [c for c, d in CALENDARIOS.items() if not d.get("alias")]
    opciones = {d["label"]: c for c, d in CALENDARIOS.items() if not d.get("alias")}

    sel_label = st.selectbox(
        "Selecciona un bloque",
        ["— elige un bloque —"] + list(opciones.keys())
    )

    if sel_label == "— elige un bloque —":
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👆 Selecciona un bloque para ver sus fechas")
        st.stop()

    codigo = opciones[sel_label]
    data = CALENDARIOS[codigo]
    est_gral = estado_bloque(data)

    badge_cls = {"activo": "badge-activo", "proximo": "badge-proximo", "finalizado": "badge-finalizado"}
    badge_txt = {"activo": "🟢 ACTIVO", "proximo": "🔵 PRÓXIMO", "finalizado": "⬛ FINALIZADO"}

    st.markdown(f"""
    <div style="margin: 1.2rem 0 1rem 0;">
        <span style="font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#f0f0f0">
            {data['label']}
        </span>
        <span class="bloque-badge {badge_cls[est_gral]}">{badge_txt[est_gral]}</span>
    </div>
    <div style="color:#4a5568; font-size:0.83rem; margin-bottom:1.2rem;">
        {' · '.join(data['modalidades'])}
    </div>
    """, unsafe_allow_html=True)

    # Sub-bloques
    cols = st.columns(2)
    for i, (sub_key, sub_label) in enumerate([("I", "Bloque I"), ("II", "Bloque II")]):
        rng = data.get(sub_key)
        with cols[i]:
            if rng is None:
                st.markdown(f"""
                <div class="sub-card done-sub">
                    <div class="sub-titulo t-done">{sub_label}</div>
                    <div class="sub-fechas">No aplica</div>
                </div>""", unsafe_allow_html=True)
            else:
                est = estado_sub(rng[0], rng[1])
                _, dr_txt = dias_info(rng[0], rng[1])
                css_card  = {"activo":"activo-sub","proximo":"proximo-sub","finalizado":"done-sub"}.get(est,"")
                css_titulo = {"activo":"t-act","proximo":"t-prox","finalizado":"t-done"}.get(est,"")
                css_dr    = {"activo":"dr-act","proximo":"dr-prox","finalizado":"dr-done"}.get(est,"")

                st.markdown(f"""
                <div class="sub-card {css_card}">
                    <div class="sub-titulo {css_titulo}">{sub_label}</div>
                    <div class="sub-fechas">
                        <strong>{fmt(rng[0])}</strong>
                        <span style="color:#2a3a55"> → </span>
                        <strong>{fmt(rng[1])}</strong>
                    </div>
                    <div class="dias-restantes {css_dr}">{dr_txt}</div>
                </div>""", unsafe_allow_html=True)

    # ── Tabla de actividades si existe para este bloque/sub ───────────────────
    for sub_key in ["I", "II"]:
        clave = f"{codigo}_{sub_key}"
        if clave in ACTIVIDADES_MAP:
            rng = data.get(sub_key)
            if rng:
                est_sub = estado_sub(rng[0], rng[1])
                if est_sub in ("activo", "proximo"):
                    actos = ACTIVIDADES[ACTIVIDADES_MAP[clave]]
                    st.markdown(f"<div style='margin-top:.5rem; color:#4a5568; font-size:.78rem;'>Bloque {sub_key}: {fmt(rng[0])} → {fmt(rng[1])}</div>", unsafe_allow_html=True)
                    mostrar_actividades(actos)

# ══ TAB 2 ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    # Filtro
    filtro = st.multiselect(
        "Filtrar por estado",
        ["🟢 Activo", "🔵 Próximo", "⬛ Finalizado"],
        default=["🟢 Activo", "🔵 Próximo"]
    )
    mapa_filtro = {"🟢 Activo": "activo", "🔵 Próximo": "proximo", "⬛ Finalizado": "finalizado"}
    estados_sel = [mapa_filtro[f] for f in filtro]

    for codigo, data in CALENDARIOS.items():
        if data.get("alias"):
            continue
        est_gral = estado_bloque(data)
        if estados_sel and est_gral not in estados_sel:
            continue

        badge_cls2 = {"activo": "badge-activo", "proximo": "badge-proximo", "finalizado": "badge-finalizado"}
        badge_txt2 = {"activo": "🟢 ACTIVO", "proximo": "🔵 PRÓXIMO", "finalizado": "⬛ FIN"}
        card_cls   = {"activo": "activo", "proximo": "proximo", "finalizado": "finalizado"}

        sub_html = ""
        for sub_key, sub_label in [("I","Bloque I"),("II","Bloque II")]:
            rng = data.get(sub_key)
            if rng is None:
                continue
            est2 = estado_sub(rng[0], rng[1])
            _, dr = dias_info(rng[0], rng[1])
            color = {"activo":"#22d3a5","proximo":"#4a9eff","finalizado":"#2a3a55"}.get(est2,"#2a3a55")
            sub_html += f"""
            <span style="display:inline-block; margin-right:1.5rem; font-size:0.82rem;">
                <span style="color:#4a5568; font-weight:600; text-transform:uppercase;
                             font-size:0.7rem; letter-spacing:.08em;">{sub_label} </span>
                <span style="color:#c8d0dc">{fmt(rng[0])} → {fmt(rng[1])}</span>
                <span style="color:{color}; font-size:0.75rem; margin-left:.4rem">· {dr}</span>
            </span>"""

        st.markdown(f"""
        <div class="bloque-card {card_cls[est_gral]}">
            <div class="bloque-nombre">
                {data['label']}
                <span class="bloque-badge {badge_cls2[est_gral]}">{badge_txt2[est_gral]}</span>
            </div>
            <div style="color:#4a5568; font-size:0.78rem; margin-bottom:.6rem">
                {' · '.join(data['modalidades'])}
            </div>
            <div>{sub_html}</div>
        </div>""", unsafe_allow_html=True)
