"""
CUN – Analizador de Calendarios Académicos
Los PDFs se cargan automáticamente desde la carpeta /pdfs
"""

import os, re, io
import pdfplumber
import pandas as pd
import streamlit as st
from datetime import date

# ── Configuración ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CUN – Calendarios Académicos",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0f1117; color: #e8e8e8; }
[data-testid="stSidebar"] { background: #161b27 !important; border-right: 1px solid #2a2f3e; }
.titulo { font-family:'Space Mono',monospace; font-size:2rem; font-weight:700;
          background:linear-gradient(135deg,#00d4aa,#0099ff);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.sub    { color:#6b7280; font-size:0.9rem; font-family:'Space Mono',monospace; margin-bottom:1.5rem; }
.card   { border-radius:12px; padding:1.2rem 1.4rem; margin-bottom:.8rem; border:1px solid; }
.c-act  { background:#0a2e1f; border-color:#00d4aa; }
.c-prox { background:#0a1f3a; border-color:#0099ff; }
.c-fin  { background:#2a1515; border-color:#ff4b4b; }
.c-unk  { background:#1e1e2e; border-color:#555; }
.clbl   { font-family:'Space Mono',monospace; font-size:.72rem; text-transform:uppercase;
          letter-spacing:.1em; color:#6b7280; margin-bottom:.2rem; }
.cval   { font-size:1.4rem; font-weight:700; font-family:'Space Mono',monospace; }
.t-act  { color:#00d4aa; } .t-prox { color:#0099ff; } .t-fin { color:#ff4b4b; }
.pill   { display:inline-block; padding:.18rem .65rem; border-radius:999px; font-size:.76rem;
          font-weight:500; margin:.1rem; }
.p-virt { background:#0a1f3a; color:#60b3ff; border:1px solid #0099ff44; }
.p-pres { background:#1a2a0a; color:#8bde6a; border:1px solid #4caf5044; }
.p-bach { background:#2a1f0a; color:#ffc46b; border:1px solid #ff990044; }
.p-335  { background:#2a0a2a; color:#d06bff; border:1px solid #9c27b044; }
.row-act{ background:#0a2e1f; border-left:3px solid #00d4aa; border-radius:7px;
          padding:.6rem 1rem; margin-bottom:.4rem; display:flex;
          justify-content:space-between; align-items:center; }
.row-fut{ background:#0d1520; border-left:3px solid #0099ff44; border-radius:7px;
          padding:.6rem 1rem; margin-bottom:.4rem; display:flex;
          justify-content:space-between; align-items:center; }
</style>
""", unsafe_allow_html=True)

# ── Constantes ────────────────────────────────────────────────────────────────
PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")

MESES = {"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
          "julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}

MODALIDAD_MAP = {"BACHILLER":"Bachilleresitario","PRESENCIAL":"Presencial",
                 "335":"Modalidad 335","VIRTUAL":"Virtual"}

PAT_ES  = re.compile(r'(?:lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo),\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', re.I)
PAT_ANG = re.compile(r'(?:lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo),\s+(\w+)\s+(\d{1,2}),?\s+(\d{4})', re.I)
PAT_ANY = re.compile(r'(?:lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo),\s+\d{1,2}\s+(?:de\s+)?\w+(?:\s+de\s+|\s+)\d{4}', re.I)
PAT_BLQ = [re.compile(r'^(2[56])(T|V|P)(0[1-9]|[1-9]\d)$', re.I),
            re.compile(r'^20(2[56])[A-D]$', re.I)]

# ── Funciones de extracción ───────────────────────────────────────────────────
def parsear_fecha(txt):
    m = PAT_ES.search(txt or "")
    if m:
        mes = MESES.get(m.group(2).lower())
        if mes:
            try: return date(int(m.group(3)), mes, int(m.group(1)))
            except: pass
    m = PAT_ANG.search(txt or "")
    if m:
        mes = MESES.get(m.group(1).lower())
        if mes:
            try: return date(int(m.group(3)), mes, int(m.group(2)))
            except: pass
    return None

def es_bloque(txt):
    t = txt.strip().upper().replace(" ","")
    return any(p.match(t) for p in PAT_BLQ)

def detectar_bloque(texto):
    for linea in [l.strip() for l in texto.split("\n") if l.strip()][:15]:
        norm = "".join(c for i,c in enumerate(linea) if i==0 or c!=linea[i-1])
        if es_bloque(norm.strip().upper().replace(" ","")):
            return norm.strip().upper().replace(" ","")
    return None

def detectar_modalidad(texto, nombre):
    src = (texto+" "+nombre).upper()
    for k,v in MODALIDAD_MAP.items():
        if k in src: return v
    return "Virtual"

def limpiar(txt):
    for p in [r'Proceso de Ingreso.*',r'Fechas de Pago.*',r'Novedades de.*',
              r'Procesos Acad[eé]micos.*',r'Estudiantes Nuevos.*']:
        txt = re.sub(p,'',txt,flags=re.I).strip()
    return txt.strip()

def extraer(texto):
    acts = []
    for linea in texto.split("\n"):
        linea = linea.strip()
        fechas = PAT_ANY.findall(linea)
        if len(fechas)>=2:
            nombre = limpiar(linea[:linea.index(fechas[0])])
            if len(nombre)>=4: acts.append({"actividad":nombre,"ini":fechas[0],"fin":fechas[1]})
        elif len(fechas)==1:
            nombre = limpiar(linea[:linea.index(fechas[0])])
            if len(nombre)>=4: acts.append({"actividad":nombre,"ini":fechas[0],"fin":fechas[0]})
    return acts

def leer_pdf(ruta):
    registros = []
    nombre = os.path.basename(ruta)
    try:
        with pdfplumber.open(ruta) as pdf:
            for pag in pdf.pages:
                texto = pag.extract_text() or ""
                if not texto.strip(): continue
                bloque = detectar_bloque(texto)
                if not bloque: continue
                modalidad = detectar_modalidad(texto, nombre)
                for a in extraer(texto):
                    ini = parsear_fecha(a["ini"])
                    fin = parsear_fecha(a["fin"])
                    if ini is None and fin is None: continue
                    registros.append({"bloque":bloque,"modalidad":modalidad,
                                      "actividad":a["actividad"],"inicio":ini,"fin":fin})
    except Exception as e:
        st.warning(f"⚠ Error en {nombre}: {e}")
    return registros

# ── Carga de datos (cacheada) ─────────────────────────────────────────────────
@st.cache_data(show_spinner="📂 Leyendo calendarios…")
def cargar_datos():
    archivos = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    todos = []
    for f in archivos:
        todos.extend(leer_pdf(os.path.join(PDF_DIR, f)))
    if not todos:
        return pd.DataFrame(columns=["bloque","modalidad","actividad","inicio","fin"])
    df = pd.DataFrame(todos).drop_duplicates(
        subset=["bloque","modalidad","actividad","inicio","fin"]).reset_index(drop=True)
    return df

# ── Análisis ──────────────────────────────────────────────────────────────────
def estado_bloque(df_b):
    hoy = date.today()
    per = df_b[df_b["actividad"].str.contains("Periodo.Acad",case=False,na=False,regex=True)]
    src = per if not per.empty else df_b
    ini, fin = src["inicio"].dropna().min(), src["fin"].dropna().max()
    if pd.isna(ini) or pd.isna(fin): return "DESCONOCIDO"
    if hoy < ini:  return "PRÓXIMO"
    if hoy > fin:  return "FINALIZADO"
    return "ACTIVO"

def fmt(d):
    if d is None or (isinstance(d,float) and pd.isna(d)): return "—"
    return d.strftime("%d/%m/%Y") if isinstance(d,date) else str(d)

def pill(m):
    cls = {"Virtual":"p-virt","Presencial":"p-pres","Bachilleresitario":"p-bach","Modalidad 335":"p-335"}.get(m,"")
    return f'<span class="pill {cls}">{m}</span>'

# ── Cargar datos ──────────────────────────────────────────────────────────────
df = cargar_datos()
hoy = date.today()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="titulo" style="font-size:1.2rem;">📅 CUN Calendarios</div>
    <div class="sub" style="font-size:.75rem;">Corporación Unificada Nacional</div>
    """, unsafe_allow_html=True)

    if not df.empty:
        bloques = sorted(df["bloque"].unique())
        activos  = sum(1 for b in bloques if estado_bloque(df[df["bloque"]==b])=="ACTIVO")
        proximos = sum(1 for b in bloques if estado_bloque(df[df["bloque"]==b])=="PRÓXIMO")

        st.markdown("#### 📊 Resumen")
        c1,c2 = st.columns(2)
        c1.metric("Bloques",   len(bloques))
        c2.metric("🟢 Activos",  activos)
        c1.metric("🔵 Próximos", proximos)
        c2.metric("Registros", len(df))
        st.markdown(f"<div style='color:#555;font-size:.75rem;margin-top:.5rem'>Hoy: {hoy.strftime('%d/%m/%Y')}</div>",
                    unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo">Calendarios Académicos CUN</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Consulta el estado de cualquier bloque académico en tiempo real</div>',
            unsafe_allow_html=True)

if df.empty:
    st.error("No se encontraron PDFs en la carpeta /pdfs. Verifica que los archivos estén incluidos.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Buscar bloque", "📋 Todos los bloques", "📅 Activos hoy"])

# ══ TAB 1 ════════════════════════════════════════════════════════════════════
with tab1:
    bloques_list = sorted(df["bloque"].unique())
    ca, cb = st.columns([2,2])
    with ca:
        sel = st.selectbox("Selecciona un bloque", [""]+bloques_list,
                           format_func=lambda x: "— elige un bloque —" if x=="" else x)
    with cb:
        mods_all = ["Todas"] + sorted(df["modalidad"].unique())
        mod_f = st.selectbox("Modalidad", mods_all)

    if not sel:
        st.info("👆 Selecciona un bloque para ver su información")
        st.stop()

    df_b = df[df["bloque"]==sel].copy()
    if mod_f != "Todas":
        df_b = df_b[df_b["modalidad"]==mod_f]
    if df_b.empty:
        st.warning(f"No hay datos para {sel} con esa modalidad.")
        st.stop()

    est = estado_bloque(df_b)
    mods = sorted(df_b["modalidad"].unique())
    info = {"ACTIVO":("🟢","c-act","t-act"),"PRÓXIMO":("🔵","c-prox","t-prox"),
            "FINALIZADO":("🔴","c-fin","t-fin"),"DESCONOCIDO":("⚪","c-unk","")}.get(est,("⚪","c-unk",""))

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="card {info[1]}"><div class="clbl">Estado</div>'
                    f'<div class="cval {info[2]}">{info[0]} {est}</div></div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card c-unk"><div class="clbl">Inicio bloque</div>'
                    f'<div class="cval" style="font-size:1rem;color:#e8e8e8">'
                    f'{fmt(df_b["inicio"].dropna().min())}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card c-unk"><div class="clbl">Fin bloque</div>'
                    f'<div class="cval" style="font-size:1rem;color:#e8e8e8">'
                    f'{fmt(df_b["fin"].dropna().max())}</div></div>', unsafe_allow_html=True)
    with c4:
        pills_html = " ".join(pill(m) for m in mods)
        st.markdown(f'<div class="card c-unk"><div class="clbl">Modalidades</div>'
                    f'<div style="margin-top:.5rem">{pills_html}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Vigentes hoy
    vigentes = df_b[(df_b["inicio"]<=hoy)&(df_b["fin"]>=hoy)].sort_values("inicio")
    if not vigentes.empty:
        st.markdown("#### 🟢 En curso hoy")
        for _,row in vigentes.iterrows():
            st.markdown(f'<div class="row-act"><span style="color:#e8e8e8;font-weight:500">'
                        f'{row["actividad"]}</span>'
                        f'<span style="color:#00d4aa;font-family:Space Mono,monospace;font-size:.82rem">'
                        f'{fmt(row["inicio"])} → {fmt(row["fin"])}</span></div>',
                        unsafe_allow_html=True)
        st.markdown("")

    # Tabla completa
    st.markdown("#### 📋 Todas las actividades")
    busq = st.text_input("🔎 Buscar actividad", placeholder="ej: matrícula, parcial…")

    filas = []
    for _,row in df_b.sort_values("inicio").iterrows():
        ini_r, fin_r = row["inicio"], row["fin"]
        if pd.notna(ini_r) and pd.notna(fin_r):
            if ini_r<=hoy<=fin_r: e2="🟢 Hoy"
            elif ini_r>hoy:       e2="⏳ Próxima"
            else:                 e2="✅ Finalizada"
        else: e2="—"
        filas.append({"Actividad":row["actividad"],"Modalidad":row["modalidad"],
                      "Inicio":fmt(ini_r),"Fin":fmt(fin_r),"Estado":e2})

    df_show = pd.DataFrame(filas)
    if busq:
        df_show = df_show[df_show["Actividad"].str.contains(busq,case=False,na=False)]

    st.dataframe(df_show, use_container_width=True, hide_index=True,
                 height=min(420, 55+len(df_show)*36))

# ══ TAB 2 ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### 📋 Todos los bloques")
    fa, fb = st.columns(2)
    with fa:
        f_est = st.multiselect("Estado", ["ACTIVO","PRÓXIMO","FINALIZADO"],
                               default=["ACTIVO","PRÓXIMO"])
    with fb:
        f_mod = st.multiselect("Modalidad", sorted(df["modalidad"].unique()))

    filas2 = []
    for b in sorted(df["bloque"].unique()):
        db = df[df["bloque"]==b]
        e  = estado_bloque(db)
        if f_est and e not in f_est: continue
        ms = sorted(db["modalidad"].unique())
        if f_mod and not any(m in f_mod for m in ms): continue
        fut = db[db["fin"]>=hoy].sort_values("inicio")
        prox = fut.iloc[0]["actividad"][:40] if not fut.empty else "—"
        em = {"ACTIVO":"🟢","PRÓXIMO":"🔵","FINALIZADO":"🔴"}.get(e,"⚪")
        filas2.append({"Bloque":b,"Estado":f"{em} {e}","Modalidades":", ".join(ms),
                       "Inicio":fmt(db["inicio"].dropna().min()),
                       "Fin":fmt(db["fin"].dropna().max()),
                       "Próxima actividad":prox,"Actividades":len(db)})

    if filas2:
        st.dataframe(pd.DataFrame(filas2), use_container_width=True, hide_index=True,
                     height=min(600, 55+len(filas2)*38))
    else:
        st.info("No hay bloques con esos filtros.")

# ══ TAB 3 ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"#### 📅 En curso hoy — {hoy.strftime('%d/%m/%Y')}")
    df_hoy = df[(df["inicio"]<=hoy)&(df["fin"]>=hoy)].sort_values(["bloque","inicio"])

    if df_hoy.empty:
        st.info("No hay actividades en curso hoy.")
    else:
        for b in sorted(df_hoy["bloque"].unique()):
            dbh = df_hoy[df_hoy["bloque"]==b]
            ms  = ", ".join(sorted(dbh["modalidad"].unique()))
            with st.expander(f"**{b}** — {ms} ({len(dbh)} actividad{'es' if len(dbh)>1 else ''})", expanded=True):
                for _,row in dbh.iterrows():
                    st.markdown(f'<div class="row-fut">'
                                f'<span style="color:#e0e0e0">{row["actividad"]}</span>'
                                f'<span style="color:#60b3ff;font-size:.82rem;font-family:Space Mono,monospace">'
                                f'hasta {fmt(row["fin"])}</span></div>', unsafe_allow_html=True)
