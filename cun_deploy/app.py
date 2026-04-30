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
.stApp { background: #ffffff; color: #1a1a2e; }

.header {
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 2rem;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #1a1a2e;
}
.header-title span { color: #059669; }
.header-sub {
    color: #64748b;
    font-size: 0.9rem;
    margin-top: 0.3rem;
    font-weight: 300;
}

.fecha-hoy {
    display: inline-block;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-size: 0.82rem;
    color: #1d4ed8;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 0.8rem;
}

/* Cards principales */
.bloque-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    cursor: pointer;
}
.bloque-card:hover { border-color: #059669; }
.bloque-card.activo  { border-left: 4px solid #059669; }
.bloque-card.proximo { border-left: 4px solid #2563eb; }
.bloque-card.finalizado { border-left: 4px solid #cbd5e1; opacity: 0.6; }

.bloque-nombre {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #1a1a2e;
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
.badge-activo     { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
.badge-proximo    { background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }
.badge-finalizado { background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; }

/* Sub-bloques */
.sub-bloques {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-top: 0.8rem;
}
.sub-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.9rem 1rem;
}
.sub-card.activo-sub   { border-color: #6ee7b7; background: #f0fdf4; }
.sub-card.proximo-sub  { border-color: #93c5fd; background: #eff6ff; }
.sub-card.done-sub     { opacity: 0.45; }

.sub-titulo {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.sub-titulo.t-act  { color: #059669; }
.sub-titulo.t-prox { color: #2563eb; }
.sub-titulo.t-done { color: #94a3b8; }

.sub-fechas {
    font-size: 0.88rem;
    color: #64748b;
}
.sub-fechas strong { color: #1e293b; font-weight: 500; }

.dias-restantes {
    margin-top: 0.4rem;
    font-size: 0.78rem;
    font-weight: 600;
}
.dr-act  { color: #059669; }
.dr-prox { color: #2563eb; }
.dr-done { color: #94a3b8; }

/* Selector */
[data-testid="stSelectbox"] > div > div {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}
label { color: #64748b !important; font-size: 0.82rem !important; }

/* Divider */
.divider { border: none; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }

/* Tabla de actividades */
.act-section { margin-top: 1.8rem; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; }
.act-header { background: #eff6ff; padding: 0.9rem 1.2rem; font-family: 'Syne', sans-serif;
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em;
    color: #1d4ed8; border-bottom: 1px solid #e2e8f0; }
.corte-label { background: #f0f9ff; padding: 0.6rem 1.2rem; font-family: 'Syne', sans-serif;
    font-size: 0.78rem; font-weight: 700; color: #0369a1; text-transform: uppercase;
    letter-spacing: 0.08em; border-bottom: 1px solid #e2e8f0;
    display: flex; justify-content: space-between; align-items: center; }
.corte-pct { background: #dbeafe; color: #1d4ed8; padding: 0.15rem 0.6rem;
    border-radius: 999px; font-size: 0.72rem; }
.act-row { display: grid; grid-template-columns: 50px 95px 95px 1fr 55px;
    gap: 0.5rem; padding: 0.65rem 1.2rem; border-bottom: 1px solid #f1f5f9;
    font-size: 0.83rem; align-items: center; background: #ffffff; }
.act-row:last-child { border-bottom: none; }
.act-row.vigente { background: #f0fdf4; }
.act-row.proxima { background: #eff6ff; }
.act-row.done    { opacity: 0.45; }
.act-semana { color: #94a3b8; font-weight: 600; text-align: center; }
.act-fecha  { color: #64748b; font-size: 0.78rem; }
.act-nombre strong { color: #1e293b; display: block; }
.act-nombre span   { color: #94a3b8; font-size: 0.78rem; }
.act-pct    { color: #059669; font-weight: 600; font-size: 0.8rem; text-align: center; }
.col-headers { display: grid; grid-template-columns: 50px 95px 95px 1fr 55px;
    gap: 0.5rem; padding: 0.5rem 1.2rem; border-bottom: 1px solid #e2e8f0;
    font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;
    letter-spacing: 0.08em; font-weight: 600; background: #f8fafc; }

/* Resumen hoy */
.hoy-box {
    background: #f0fdf4;
    border: 1px solid #6ee7b7;
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
    color: #059669;
    margin-bottom: 0.8rem;
}
.hoy-item {
    display: flex;
    justify-content: space-between;
    padding: 0.35rem 0;
    border-bottom: 1px solid #d1fae5;
    font-size: 0.88rem;
}
.hoy-item:last-child { border-bottom: none; }
.hoy-bloque { font-family: 'Syne', sans-serif; font-weight: 700; color: #1a1a2e; }
.hoy-sub    { color: #059669; font-size: 0.8rem; }
.hoy-fecha  { color: #2563eb; font-size: 0.8rem; }
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
              "I":  None,
              "II": (date(2026,2,2), date(2026,5,24))},

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


# ── DATOS BE ─────────────────────────────────────────────────────────────────
PERIODOS_BE = {
    "26I01": {"label": "26I01 · 26PI1", "actividades": [
        {"act": "Emisión de recibo de matrícula",  "ini": date(2025,12,1),  "fin": date(2026,1,28)},
        {"act": "Activación de saldo",              "ini": date(2025,12,1),  "fin": date(2026,2,2)},
        {"act": "Retiros y aplazamientos",          "ini": date(2026,2,2),   "fin": date(2026,2,17)},
        {"act": "Inicio de clases",                 "ini": date(2026,2,2),   "fin": date(2026,2,2)},
        {"act": "Novedades de matrícula",           "ini": date(2026,2,2),   "fin": date(2026,2,13)},
        {"act": "Cierre de actividades",            "ini": date(2026,3,22),  "fin": date(2026,3,22)},
        {"act": "Reporte de novedades de notas",    "ini": date(2026,3,23),  "fin": date(2026,3,25)},
        {"act": "Cierre de periodo académico",      "ini": date(2026,3,29),  "fin": date(2026,3,29)},
    ]},
    "26I02": {"label": "26I02 · 25PI2", "actividades": [
        {"act": "Emisión de recibo de matrícula",        "ini": date(2026,2,2),   "fin": date(2026,3,25)},
        {"act": "Activación de saldo",                   "ini": date(2026,2,2),   "fin": date(2026,3,30)},
        {"act": "Matrícula prueba Reconocimiento Saberes","ini": date(2026,2,2),   "fin": date(2026,3,10)},
        {"act": "Retiros y aplazamientos",               "ini": date(2026,3,30),  "fin": date(2026,4,14)},
        {"act": "Inicio de clases",                      "ini": date(2026,3,30),  "fin": date(2026,3,30)},
        {"act": "Novedades de matrícula",                "ini": date(2026,3,30),  "fin": date(2026,4,10)},
        {"act": "Cierre de actividades",                 "ini": date(2026,5,17),  "fin": date(2026,5,17)},
        {"act": "Reporte de novedades de notas",         "ini": date(2026,5,18),  "fin": date(2026,5,20)},
        {"act": "Cierre de periodo académico",           "ini": date(2026,5,24),  "fin": date(2026,5,24)},
    ]},
    "26I03": {"label": "26I03 · 25PI3", "actividades": [
        {"act": "Emisión de recibo de matrícula",        "ini": date(2026,3,30),  "fin": date(2026,5,20)},
        {"act": "Activación de saldo",                   "ini": date(2026,3,30),  "fin": date(2026,5,25)},
        {"act": "Prueba de Reconocimiento de Saberes",   "ini": date(2026,3,30),  "fin": date(2026,5,5)},
        {"act": "Retiros y aplazamientos",               "ini": date(2026,5,25),  "fin": date(2026,6,9)},
        {"act": "Inicio de clases",                      "ini": date(2026,5,25),  "fin": date(2026,5,25)},
        {"act": "Novedades de matrícula",                "ini": date(2026,5,25),  "fin": date(2026,6,5)},
        {"act": "Cierre de actividades",                 "ini": date(2026,7,12),  "fin": date(2026,7,12)},
        {"act": "Reporte de novedades de notas",         "ini": date(2026,7,20),  "fin": date(2026,7,24)},
        {"act": "Cierre de periodo académico",           "ini": date(2026,7,19),  "fin": date(2026,7,19)},
    ]},
    "26I04": {"label": "26I04 · 25PI4", "actividades": [
        {"act": "Emisión de recibo de matrícula",        "ini": date(2026,5,25),  "fin": date(2026,7,29)},
        {"act": "Activación de saldo",                   "ini": date(2026,5,25),  "fin": date(2026,8,3)},
        {"act": "Prueba de Reconocimiento de Saberes",   "ini": date(2026,5,25),  "fin": date(2026,7,14)},
        {"act": "Retiros y aplazamientos",               "ini": date(2026,8,3),   "fin": date(2026,8,18)},
        {"act": "Inicio de clases",                      "ini": date(2026,8,3),   "fin": date(2026,8,3)},
        {"act": "Novedades de matrícula",                "ini": date(2026,8,3),   "fin": date(2026,8,14)},
        {"act": "Cierre de actividades",                 "ini": date(2026,9,20),  "fin": date(2026,9,20)},
        {"act": "Reporte de novedades de notas",         "ini": date(2026,9,21),  "fin": date(2026,9,25)},
        {"act": "Cierre de periodo académico",           "ini": date(2026,9,27),  "fin": date(2026,9,27)},
    ]},
    "26I05": {"label": "26I05 · 25PI5", "actividades": [
        {"act": "Emisión de recibo de matrícula",        "ini": date(2026,8,3),   "fin": date(2026,9,23)},
        {"act": "Activación de saldo",                   "ini": date(2026,8,3),   "fin": date(2026,9,28)},
        {"act": "Prueba de Reconocimiento de Saberes",   "ini": date(2026,8,3),   "fin": date(2026,9,8)},
        {"act": "Retiros y aplazamientos",               "ini": date(2026,9,28),  "fin": date(2026,10,13)},
        {"act": "Inicio de clases",                      "ini": date(2026,9,28),  "fin": date(2026,9,28)},
        {"act": "Novedades de matrícula",                "ini": date(2026,9,28),  "fin": date(2026,10,9)},
        {"act": "Cierre de actividades",                 "ini": date(2026,11,15), "fin": date(2026,11,15)},
        {"act": "Reporte de novedades de notas",         "ini": date(2026,11,16), "fin": date(2026,11,20)},
        {"act": "Cierre de periodo académico",           "ini": date(2026,11,22), "fin": date(2026,11,22)},
    ]},
    "26I06": {"label": "26I06 · 25PI6", "actividades": [
        {"act": "Emisión de recibo de matrícula",        "ini": date(2026,9,28),  "fin": date(2026,11,18)},
        {"act": "Activación de saldo",                   "ini": date(2026,9,28),  "fin": date(2026,11,23)},
        {"act": "Prueba de Reconocimiento de Saberes",   "ini": date(2026,9,28),  "fin": date(2026,11,3)},
        {"act": "Retiros y aplazamientos",               "ini": date(2026,11,23), "fin": date(2026,12,8)},
        {"act": "Inicio de clases",                      "ini": date(2026,11,23), "fin": date(2026,11,23)},
        {"act": "Novedades de matrícula",                "ini": date(2026,11,23), "fin": date(2026,12,4)},
        {"act": "Cierre de actividades",                 "ini": date(2027,1,10),  "fin": date(2027,1,10)},
        {"act": "Reporte de novedades de notas",         "ini": date(2027,1,11),  "fin": date(2027,1,15)},
        {"act": "Cierre de periodo académico",           "ini": date(2027,1,17),  "fin": date(2027,1,17)},
    ]},
}

PLACEMENT_BE = {
    "26I32": {"label": "26I32", "actividades": [
        {"act": "Matrícula de estudiantes",         "ini": date(2026,2,2),   "fin": date(2026,3,25)},
        {"act": "Toma de Placement test",           "ini": date(2026,3,30),  "fin": date(2026,5,8)},
        {"act": "Cargue de notas y homologaciones", "ini": date(2026,5,11),  "fin": date(2026,5,17)},
        {"act": "Cierre de periodo académico",      "ini": date(2026,5,24),  "fin": date(2026,5,24)},
    ]},
    "26I33": {"label": "26I33", "actividades": [
        {"act": "Matrícula de estudiantes",         "ini": date(2026,3,30),  "fin": date(2026,5,20)},
        {"act": "Toma de Placement test",           "ini": date(2026,5,25),  "fin": date(2026,7,3)},
        {"act": "Cargue de notas y homologaciones", "ini": date(2026,7,6),   "fin": date(2026,7,17)},
        {"act": "Cierre de periodo académico",      "ini": date(2026,7,19),  "fin": date(2026,7,19)},
    ]},
    "26I34": {"label": "26I34", "actividades": [
        {"act": "Matrícula de estudiantes",         "ini": date(2026,5,25),  "fin": date(2026,7,29)},
        {"act": "Toma de Placement test",           "ini": date(2026,8,3),   "fin": date(2026,9,11)},
        {"act": "Cargue de notas y homologaciones", "ini": date(2026,9,14),  "fin": date(2026,9,25)},
        {"act": "Cierre de periodo académico",      "ini": date(2026,9,27),  "fin": date(2026,9,27)},
    ]},
    "26I35": {"label": "26I35", "actividades": [
        {"act": "Matrícula de estudiantes",         "ini": date(2026,8,3),   "fin": date(2026,9,23)},
        {"act": "Toma de Placement test",           "ini": date(2026,9,28),  "fin": date(2026,11,6)},
        {"act": "Cargue de notas y homologaciones", "ini": date(2026,11,9),  "fin": date(2026,11,21)},
        {"act": "Cierre de periodo académico",      "ini": date(2026,11,22), "fin": date(2026,11,22)},
    ]},
    "26I36": {"label": "26I36", "actividades": [
        {"act": "Matrícula de estudiantes",         "ini": date(2026,9,28),  "fin": date(2026,11,18)},
        {"act": "Toma de Placement test",           "ini": date(2026,11,23), "fin": date(2027,1,1)},
        {"act": "Cargue de notas y homologaciones", "ini": date(2027,1,4),   "fin": date(2027,1,15)},
        {"act": "Cierre de periodo académico",      "ini": date(2027,1,17),  "fin": date(2027,1,17)},
    ]},
}

NIVELATORIO_BE = {
    "26I11": {"label": "26I11", "actividades": [
        {"act": "Venta de la prueba nivelatoria",           "ini": date(2025,12,11),"fin": date(2026,1,12)},
        {"act": "Verificación de estudiantes matriculados", "ini": date(2026,1,12), "fin": date(2026,1,14)},
        {"act": "Corrección de novedades de matrícula",     "ini": date(2026,1,14), "fin": date(2026,1,16)},
        {"act": "Tutorías",                                 "ini": date(2026,1,14), "fin": date(2026,1,28)},
        {"act": "Prueba nivelatoria",                       "ini": date(2026,1,19), "fin": date(2026,1,28)},
        {"act": "Verificación de notas",                    "ini": date(2026,1,29), "fin": date(2026,2,5)},
        {"act": "Cargue de notas",                          "ini": date(2026,2,5),  "fin": date(2026,2,13)},
        {"act": "Cierre del periodo",                       "ini": date(2026,2,13), "fin": date(2026,2,13)},
    ]},
    "26I12": {"label": "26I12", "actividades": [
        {"act": "Venta de la prueba nivelatoria",           "ini": date(2026,1,13), "fin": date(2026,2,9)},
        {"act": "Verificación de estudiantes matriculados", "ini": date(2026,2,9),  "fin": date(2026,2,11)},
        {"act": "Corrección de novedades de matrícula",     "ini": date(2026,2,11), "fin": date(2026,2,13)},
        {"act": "Tutorías",                                 "ini": date(2026,2,11), "fin": date(2026,2,25)},
        {"act": "Prueba nivelatoria",                       "ini": date(2026,2,16), "fin": date(2026,2,25)},
        {"act": "Verificación de notas",                    "ini": date(2026,2,26), "fin": date(2026,3,5)},
        {"act": "Cargue de notas",                          "ini": date(2026,3,5),  "fin": date(2026,3,13)},
        {"act": "Cierre del periodo",                       "ini": date(2026,3,13), "fin": date(2026,3,13)},
    ]},
    "26I13": {"label": "26I13", "actividades": [
        {"act": "Venta de la prueba nivelatoria",           "ini": date(2026,2,10), "fin": date(2026,3,9)},
        {"act": "Verificación de estudiantes matriculados", "ini": date(2026,3,9),  "fin": date(2026,3,11)},
        {"act": "Corrección de novedades de matrícula",     "ini": date(2026,3,11), "fin": date(2026,3,13)},
        {"act": "Tutorías",                                 "ini": date(2026,3,11), "fin": date(2026,3,25)},
        {"act": "Prueba nivelatoria",                       "ini": date(2026,3,16), "fin": date(2026,3,25)},
        {"act": "Verificación de notas",                    "ini": date(2026,3,26), "fin": date(2026,4,2)},
        {"act": "Cargue de notas",                          "ini": date(2026,4,2),  "fin": date(2026,4,10)},
        {"act": "Cierre del periodo",                       "ini": date(2026,4,10), "fin": date(2026,4,10)},
    ]},
    "26I14": {"label": "26I14", "actividades": [
        {"act": "Venta de la prueba nivelatoria",           "ini": date(2026,3,10), "fin": date(2026,4,13)},
        {"act": "Verificación de estudiantes matriculados", "ini": date(2026,4,13), "fin": date(2026,4,15)},
        {"act": "Corrección de novedades de matrícula",     "ini": date(2026,4,15), "fin": date(2026,4,17)},
        {"act": "Tutorías",                                 "ini": date(2026,4,15), "fin": date(2026,4,29)},
        {"act": "Prueba nivelatoria",                       "ini": date(2026,4,20), "fin": date(2026,4,29)},
        {"act": "Verificación de notas",                    "ini": date(2026,4,30), "fin": date(2026,5,7)},
        {"act": "Cargue de notas",                          "ini": date(2026,5,7),  "fin": date(2026,5,15)},
        {"act": "Cierre del periodo",                       "ini": date(2026,5,15), "fin": date(2026,5,15)},
    ]},
    "26I15": {"label": "26I15", "actividades": [
        {"act": "Venta de la prueba nivelatoria",           "ini": date(2026,4,14), "fin": date(2026,5,11)},
        {"act": "Verificación de estudiantes matriculados", "ini": date(2026,5,11), "fin": date(2026,5,13)},
        {"act": "Corrección de novedades de matrícula",     "ini": date(2026,5,13), "fin": date(2026,5,15)},
        {"act": "Tutorías",                                 "ini": date(2026,5,13), "fin": date(2026,5,27)},
        {"act": "Prueba nivelatoria",                       "ini": date(2026,5,18), "fin": date(2026,5,27)},
        {"act": "Verificación de notas",                    "ini": date(2026,5,28), "fin": date(2026,6,4)},
        {"act": "Cargue de notas",                          "ini": date(2026,6,4),  "fin": date(2026,6,12)},
        {"act": "Cierre del periodo",                       "ini": date(2026,6,12), "fin": date(2026,6,12)},
    ]},
    "26I16": {"label": "26I16", "actividades": [
        {"act": "Venta de la prueba nivelatoria",           "ini": date(2026,5,12), "fin": date(2026,6,8)},
        {"act": "Verificación de estudiantes matriculados", "ini": date(2026,6,8),  "fin": date(2026,6,10)},
        {"act": "Corrección de novedades de matrícula",     "ini": date(2026,6,10), "fin": date(2026,6,12)},
        {"act": "Tutorías",                                 "ini": date(2026,6,10), "fin": date(2026,6,24)},
        {"act": "Prueba nivelatoria",                       "ini": date(2026,6,15), "fin": date(2026,6,24)},
        {"act": "Verificación de notas",                    "ini": date(2026,6,25), "fin": date(2026,7,2)},
        {"act": "Cargue de notas",                          "ini": date(2026,7,2),  "fin": date(2026,7,10)},
        {"act": "Cierre del periodo",                       "ini": date(2026,7,10), "fin": date(2026,7,10)},
    ]},
}

def estado_be(ini, fin):
    hoy = date.today()
    if hoy < ini: return "proximo"
    if hoy > fin: return "finalizado"
    return "activo"

def mostrar_tabla_be(periodos):
    hoy = date.today()
    for codigo, data in periodos.items():
        actos = data["actividades"]
        ini_periodo = min(a["ini"] for a in actos)
        fin_periodo = max(a["fin"] for a in actos)
        est = estado_be(ini_periodo, fin_periodo)
        em  = {"activo":"🟢","proximo":"🔵","finalizado":"⬛"}.get(est,"⬛")
        bor = {"activo":"#6ee7b7","proximo":"#93c5fd","finalizado":"#e2e8f0"}.get(est,"#e2e8f0")

        with st.expander(f"{em} **{data['label']}**  —  {fmt(ini_periodo)} → {fmt(fin_periodo)}", expanded=(est=="activo")):
            for a in actos:
                ini_a, fin_a = a["ini"], a["fin"]
                if ini_a <= hoy <= fin_a:
                    row_bg = "#f0fdf4"; txt_col = "#065f46"; dot = "🟢"
                elif ini_a > hoy:
                    row_bg = "#eff6ff"; txt_col = "#1e40af"; dot = "🔵"
                else:
                    row_bg = "#f8fafc"; txt_col = "#94a3b8"; dot = "⬛"
                fin_str = fmt(fin_a) if fin_a != ini_a else ""
                rng_str = f"{fmt(ini_a)} → {fin_str}" if fin_str else fmt(ini_a)
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            background:{row_bg};border-radius:8px;padding:0.5rem 0.9rem;
                            margin-bottom:0.3rem;border-left:3px solid {bor};">
                    <span style="color:{txt_col};font-size:0.85rem;">{dot} {a['act']}</span>
                    <span style="color:#64748b;font-size:0.78rem;font-family:'Syne',sans-serif;">{rng_str}</span>
                </div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab_be = st.tabs(["🔍 Buscar bloque", "📋 Todos los bloques", "🌐 Calendario BE"])

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
        <span style="font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:800; color:#1a1a2e">
            {data['label']}
        </span>
        <span class="bloque-badge {badge_cls[est_gral]}">{badge_txt[est_gral]}</span>
    </div>
    <div style="color:#64748b; font-size:0.83rem; margin-bottom:1.2rem;">
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
                        <span style="color:#cbd5e1"> → </span>
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
                    st.markdown(f"<div style='margin-top:.5rem; color:#64748b; font-size:.78rem;'>Bloque {sub_key}: {fmt(rng[0])} → {fmt(rng[1])}</div>", unsafe_allow_html=True)
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
            color = {"activo":"#059669","proximo":"#2563eb","finalizado":"#94a3b8"}.get(est2,"#94a3b8")
            sub_html += f"""
            <span style="display:inline-block; margin-right:1.5rem; font-size:0.82rem;">
                <span style="color:#94a3b8; font-weight:600; text-transform:uppercase;
                             font-size:0.7rem; letter-spacing:.08em;">{sub_label} </span>
                <span style="color:#1e293b">{fmt(rng[0])} → {fmt(rng[1])}</span>
                <span style="color:{color}; font-size:0.75rem; margin-left:.4rem">· {dr}</span>
            </span>"""

        st.markdown(f"""
        <div class="bloque-card {card_cls[est_gral]}">
            <div class="bloque-nombre">
                {data['label']}
                <span class="bloque-badge {badge_cls2[est_gral]}">{badge_txt2[est_gral]}</span>
            </div>
            <div style="color:#64748b; font-size:0.78rem; margin-bottom:.6rem">
                {' · '.join(data['modalidades'])}
            </div>
            <div>{sub_html}</div>
        </div>""", unsafe_allow_html=True)

# ══ TAB BE ═══════════════════════════════════════════════════════════════════
with tab_be:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:12px;
                padding:1rem 1.4rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:0.75rem;font-weight:700;
                    text-transform:uppercase;letter-spacing:.12em;color:#7c3aed;margin-bottom:.3rem;">
            🌐 Área Bilingüe — BE
        </div>
        <div style="color:#64748b;font-size:0.85rem;">
            Calendarios de Períodos BE, Placement y Nivelatorio. Los períodos activos aparecen expandidos automáticamente.
        </div>
    </div>
    """, unsafe_allow_html=True)

    be_sub1, be_sub2, be_sub3 = st.tabs(["📘 Períodos BE", "🔤 Placement", "📝 Nivelatorio"])

    with be_sub1:
        st.markdown("<br>", unsafe_allow_html=True)
        mostrar_tabla_be(PERIODOS_BE)

    with be_sub2:
        st.markdown("<br>", unsafe_allow_html=True)
        mostrar_tabla_be(PLACEMENT_BE)

    with be_sub3:
        st.markdown("<br>", unsafe_allow_html=True)
        mostrar_tabla_be(NIVELATORIO_BE)

DIAS_KUN = [
    {"num": 1, "dia": "Jueves",    "fecha": date(2026, 5,  7)},
    {"num": 2, "dia": "Lunes",     "fecha": date(2026, 5, 25)},
    {"num": 3, "dia": "Jueves",    "fecha": date(2026, 6,  4)},
    {"num": 4, "dia": "Martes",    "fecha": date(2026, 6, 16)},
    {"num": 5, "dia": "Miércoles", "fecha": date(2026, 6, 24)},
    {"num": 6, "dia": "Lunes",     "fecha": date(2026, 7,  6)},
    {"num": 7, "dia": "Miércoles", "fecha": date(2026, 7, 15)},
    {"num": 8, "dia": "Lunes",     "fecha": date(2026, 7, 27)},
]

with tab_kun:
    st.markdown("<br>", unsafe_allow_html=True)

    # Banner
    st.markdown("""
    <div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:12px;
                padding:1rem 1.4rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:0.75rem;font-weight:700;
                    text-transform:uppercase;letter-spacing:.12em;color:#1d4ed8;margin-bottom:.3rem;">
            📍 Días KUN — Coworking Chapinero
        </div>
        <div style="color:#64748b;font-size:0.85rem;">
            8:00 AM – 6:00 PM · Se envía recordatorio automático 1 día antes de cada fecha.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tarjetas de cada día KUN
    for d in DIAS_KUN:
        diff = (d["fecha"] - hoy).days
        if diff < 0:
            est_kun = "finalizado"
            em_kun  = "⬛"
            bg      = "#f8fafc"
            borde   = "#e2e8f0"
            txt     = "#94a3b8"
            badge_bg = "#f1f5f9"; badge_txt = "#64748b"
            etiqueta = "Finalizado"
        elif diff == 0:
            est_kun = "hoy"
            em_kun  = "🟢"
            bg      = "#f0fdf4"
            borde   = "#6ee7b7"
            txt     = "#065f46"
            badge_bg = "#d1fae5"; badge_txt = "#065f46"
            etiqueta = "¡HOY!"
        elif diff == 1:
            est_kun = "manana"
            em_kun  = "🟡"
            bg      = "#fefce8"
            borde   = "#fde68a"
            txt     = "#92400e"
            badge_bg = "#fef3c7"; badge_txt = "#92400e"
            etiqueta = "¡MAÑANA!"
        else:
            est_kun = "proximo"
            em_kun  = "🔵"
            bg      = "#eff6ff"
            borde   = "#93c5fd"
            txt     = "#1e40af"
            badge_bg = "#dbeafe"; badge_txt = "#1e40af"
            etiqueta = f"En {diff} días"

        st.markdown(f"""
        <div style="background:{bg};border:1px solid {borde};border-left:4px solid {borde};
                    border-radius:12px;padding:1rem 1.4rem;margin-bottom:0.7rem;
                    display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:700;
                             text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;">
                    Día KUN #{d['num']}
                </span><br>
                <span style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                             color:{txt};">
                    {em_kun} {d['dia']} {d['fecha'].strftime('%d/%m/%Y')}
                </span>
                <span style="color:#94a3b8;font-size:0.82rem;margin-left:0.5rem;">
                    · 8:00 AM – 6:00 PM · Coworking Chapinero
                </span>
            </div>
            <div>
                <span style="background:{badge_bg};color:{badge_txt};padding:0.3rem 0.8rem;
                             border-radius:999px;font-size:0.75rem;font-weight:700;
                             font-family:'Syne',sans-serif;">
                    {etiqueta}
                </span>
            </div>
        </div>""", unsafe_allow_html=True)
