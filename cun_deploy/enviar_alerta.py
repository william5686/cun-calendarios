"""
CUN – Script de alerta automática: Cierre de Notas 25P06 · T06 · V06
Se ejecuta todos los días via GitHub Actions.
Envía correo los 3 días previos al cierre (26, 27, 28 y 29 de marzo de 2026).
"""

import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────

FECHA_CIERRE = date(2026, 3, 29)
DIAS_ALERTA  = 3   # Enviar desde 3 días antes hasta el día del cierre

REMITENTE = os.environ.get("EMAIL_REMITENTE", "")
PASSWORD  = os.environ.get("EMAIL_PASSWORD", "")

DESTINATARIOS = [
    ("Andrés Camilo Vásquez Blanco",    "andres_vasquez@cun.edu.co"),
    ("Aura María Escamilla Ospina",     "aura_escamilla@cun.edu.co"),
    ("Johana Alfonsina Caicedo Osorio", "johana_caicedo@cun.edu.co"),
    ("Julio Andrés Pamplona Llanos",    "julio_pamplona@cun.edu.co"),
    ("Ángela Rocío Camargo Puerto",     "angela_camargop@cun.edu.co"),
    ("Cristian Felipe Galindo Acero",   "cristian_galindoa@cun.edu.co"),
    ("Elkin Ignacio Rodríguez Carrero", "elkin_rodriguezca@cun.edu.co"),
    ("Gillyam Germán Martínez Bernal",  "gillyam_martinez@cun.edu.co"),
    ("Heidy Johanna Quiroga Aguilar",   "heidy_quiroga@cun.edu.co"),
    ("Laura Daniela Gómez Arenas",      "laura_gomeza@cun.edu.co"),
    ("Maira Alejandra Doncel Largo",    "maira_doncel@cun.edu.co"),
    ("William Estrada Santis",          "william_estrada@cun.edu.co"),
]

# ── LÓGICA ────────────────────────────────────────────────────────────────────

def dias_restantes():
    return (FECHA_CIERRE - date.today()).days

def debe_enviar():
    dr = dias_restantes()
    return 0 <= dr <= DIAS_ALERTA

def construir_asunto(dr):
    if dr == 0:
        return "🔴 HOY es el Cierre de Notas – 25P06 · T06 · V06 Bloque 2"
    elif dr == 1:
        return "🟠 MAÑANA es el Cierre de Notas – 25P06 · T06 · V06 Bloque 2"
    else:
        return f"🟡 Faltan {dr} días para el Cierre de Notas – 25P06 · T06 · V06 Bloque 2"

def construir_cuerpo_html(nombre, dr):
    if dr == 0:
        urgencia = "🔴 <strong>HOY es el último día</strong> para el registro de notas."
        color_banner = "#7f1d1d"
        color_borde  = "#ef4444"
    elif dr == 1:
        urgencia = "🟠 <strong>Mañana vence</strong> el plazo para el registro de notas."
        color_banner = "#78350f"
        color_borde  = "#f97316"
    else:
        urgencia = f"🟡 Quedan <strong>{dr} días</strong> para el cierre de notas."
        color_banner = "#1e3a5f"
        color_borde  = "#3b82f6"

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alerta Cierre de Notas</title>
</head>
<body style="margin:0;padding:0;background:#0f1117;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:30px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#0d1120;border-radius:16px;overflow:hidden;
                      border:1px solid #1a2035;max-width:600px;width:100%;">

          <!-- Banner superior -->
          <tr>
            <td style="background:{color_banner};padding:20px 30px;
                       border-bottom:3px solid {color_borde};">
              <p style="margin:0;font-size:0.75rem;text-transform:uppercase;
                        letter-spacing:0.15em;color:#94a3b8;">
                Corporación Unificada Nacional de Educación Superior
              </p>
              <h1 style="margin:8px 0 0 0;font-size:1.4rem;color:#f8fafc;font-weight:700;">
                ⚠️ Alerta: Cierre de Notas
              </h1>
            </td>
          </tr>

          <!-- Cuerpo -->
          <tr>
            <td style="padding:28px 30px;">
              <p style="color:#94a3b8;font-size:0.9rem;margin:0 0 8px 0;">
                Estimado/a,
              </p>
              <p style="color:#e2e8f0;font-size:1rem;font-weight:600;margin:0 0 20px 0;">
                {nombre}
              </p>

              <!-- Alerta principal -->
              <div style="background:{color_banner};border:1px solid {color_borde};
                          border-radius:10px;padding:16px 20px;margin-bottom:24px;">
                <p style="margin:0;color:#f8fafc;font-size:1rem;">
                  {urgencia}
                </p>
              </div>

              <!-- Detalles del bloque -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#080c14;border:1px solid #1a2035;
                            border-radius:10px;overflow:hidden;margin-bottom:24px;">
                <tr style="background:#0a1829;">
                  <td colspan="2" style="padding:10px 16px;font-size:0.7rem;
                      color:#3b82f6;text-transform:uppercase;letter-spacing:0.1em;
                      font-weight:700;border-bottom:1px solid #1a2035;">
                    Información del Bloque
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #0f1520;width:40%;">Bloques</td>
                  <td style="padding:10px 16px;color:#e2e8f0;font-size:0.85rem;
                             border-bottom:1px solid #0f1520;font-weight:600;">
                    25P06 · 25T06 · 25V06 — Bloque 2<br>
                    26V01 · 26P01 · 26T01 — Bloque 1
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #0f1520;">Actividad</td>
                  <td style="padding:10px 16px;color:#e2e8f0;font-size:0.85rem;
                             border-bottom:1px solid #0f1520;font-weight:600;">
                    Cierre de Notas — Semana 8
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #0f1520;">Período</td>
                  <td style="padding:10px 16px;color:#e2e8f0;font-size:0.85rem;
                             border-bottom:1px solid #0f1520;">
                    23/03/2026 – <strong style="color:{color_borde};">29/03/2026</strong>
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;">
                    Días restantes</td>
                  <td style="padding:10px 16px;font-size:1rem;font-weight:700;
                             color:{color_borde};">
                    {"HOY es el último día" if dr == 0 else f"{dr} día{'s' if dr != 1 else ''}"}
                  </td>
                </tr>
              </table>

              <p style="color:#64748b;font-size:0.82rem;margin:0;line-height:1.6;">
                Por favor asegúrese de registrar las notas del Tercer Corte antes del
                <strong style="color:#e2e8f0;">29 de marzo de 2026</strong>.
                Este mensaje es generado automáticamente por el sistema de calendarios CUN.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#080c14;padding:16px 30px;
                       border-top:1px solid #1a2035;text-align:center;">
              <p style="margin:0;color:#1e2a3a;font-size:0.75rem;">
                CUN – Sistema de Calendarios Académicos · Notificación automática
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

def enviar_correos():
    dr = dias_restantes()
    print(f"📅 Hoy: {date.today()} | Cierre: {FECHA_CIERRE} | Días restantes: {dr}")

    if not debe_enviar():
        print("✅ No es necesario enviar alerta hoy.")
        return

    print(f"📧 Enviando alertas a {len(DESTINATARIOS)} destinatarios...")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(REMITENTE, PASSWORD)

        enviados = 0
        errores  = 0

        for nombre, correo in DESTINATARIOS:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = construir_asunto(dr)
                msg["From"]    = f"CUN Calendarios <{REMITENTE}>"
                msg["To"]      = correo

                cuerpo_html = construir_cuerpo_html(nombre, dr)
                msg.attach(MIMEText(cuerpo_html, "html", "utf-8"))

                server.sendmail(REMITENTE, correo, msg.as_string())
                print(f"  ✅ Enviado a {nombre} <{correo}>")
                enviados += 1

            except Exception as e:
                print(f"  ❌ Error enviando a {correo}: {e}")
                errores += 1

        server.quit()
        print(f"\n📊 Resultado: {enviados} enviados, {errores} errores.")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación. Verifica EMAIL_REMITENTE y EMAIL_PASSWORD en los secretos de GitHub.")
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")

if __name__ == "__main__":
    enviar_correos()
