"""
CUN – Alerta automática: Cierre de Actividades Calendario BE (26I01)
Cierre de actividades: 22/03/2026
Se ejecuta todos los días via GitHub Actions.
Envía correo hoy (prueba) y del 20 al 22 de marzo de 2026.
"""

import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────

FECHA_CIERRE = date(2026, 3, 22)
DIAS_ALERTA  = 3   # Enviar desde 3 días antes hasta el día del cierre

REMITENTE = os.environ.get("EMAIL_REMITENTE", "")
PASSWORD  = os.environ.get("EMAIL_PASSWORD", "")

DESTINATARIOS = [
    ("Maira Doncel",       "maira_doncel@cun.edu.co"),
    ("Laura Gómez",        "laura_gomeza@cun.edu.co"),
    ("Mónica Pachón",      "monica_pachon@cun.edu.co"),
    ("Leidy Díazgranados", "leidy_diazgranados@cun.edu.co"),
    ("Julián Chavista",    "julian_chavista@cun.edu.co"),
    ("William Estrada",    "william_estrada@cun.edu.co"),
]

# ── LÓGICA ────────────────────────────────────────────────────────────────────

def dias_restantes():
    return (FECHA_CIERRE - date.today()).days

def debe_enviar():
    dr = dias_restantes()
    hoy = date.today()
    # Prueba: enviar hoy 20 de marzo
    if hoy == date(2026, 3, 20):
        return True
    # Normal: enviar del 20 al 22 de marzo
    return 0 <= dr <= DIAS_ALERTA

def construir_asunto(dr):
    if dr <= 0:
        return "🔴 HOY es el Cierre de Actividades – Calendario BE 26I01"
    elif dr == 1:
        return "🟠 MAÑANA es el Cierre de Actividades – Calendario BE 26I01"
    else:
        return f"🟡 Faltan {dr} días – Cierre de Actividades Calendario BE 26I01"

def construir_cuerpo_html(nombre, dr):
    if dr <= 0:
        urgencia = "🔴 <strong>HOY es el último día</strong> para el cierre de actividades."
        color_banner = "#7f1d1d"
        color_borde  = "#ef4444"
    elif dr == 1:
        urgencia = "🟠 <strong>Mañana vence</strong> el plazo para el cierre de actividades."
        color_banner = "#78350f"
        color_borde  = "#f97316"
    else:
        urgencia = f"🟡 Quedan <strong>{dr} días</strong> para el cierre de actividades."
        color_banner = "#1e3a5f"
        color_borde  = "#3b82f6"

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:30px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:16px;overflow:hidden;
                      border:1px solid #e2e8f0;max-width:600px;width:100%;">

          <!-- Banner superior -->
          <tr>
            <td style="background:{color_banner};padding:20px 30px;
                       border-bottom:3px solid {color_borde};">
              <p style="margin:0;font-size:0.75rem;text-transform:uppercase;
                        letter-spacing:0.15em;color:#cbd5e1;">
                CUN · Área Bilingüe (BE)
              </p>
              <h1 style="margin:8px 0 0 0;font-size:1.4rem;color:#f8fafc;font-weight:700;">
                ⚠️ Alerta: Cierre de Actividades BE
              </h1>
            </td>
          </tr>

          <!-- Cuerpo -->
          <tr>
            <td style="padding:28px 30px;">
              <p style="color:#64748b;font-size:0.9rem;margin:0 0 6px 0;">Estimado/a,</p>
              <p style="color:#1e293b;font-size:1rem;font-weight:600;margin:0 0 20px 0;">
                {nombre}
              </p>

              <!-- Alerta principal -->
              <div style="background:{color_banner};border:1px solid {color_borde};
                          border-radius:10px;padding:16px 20px;margin-bottom:24px;">
                <p style="margin:0;color:#f8fafc;font-size:1rem;">{urgencia}</p>
              </div>

              <!-- Detalles -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f8fafc;border:1px solid #e2e8f0;
                            border-radius:10px;overflow:hidden;margin-bottom:24px;">
                <tr style="background:#eff6ff;">
                  <td colspan="2" style="padding:10px 16px;font-size:0.7rem;
                      color:#1d4ed8;text-transform:uppercase;letter-spacing:0.1em;
                      font-weight:700;border-bottom:1px solid #e2e8f0;">
                    Información del Período
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;width:40%;">Período</td>
                  <td style="padding:10px 16px;color:#1e293b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;font-weight:600;">
                    26I01 · 26PI1 — Calendario BE
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;">Actividad</td>
                  <td style="padding:10px 16px;color:#1e293b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;font-weight:600;">
                    Cierre de Actividades
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;">Fecha límite</td>
                  <td style="padding:10px 16px;font-size:0.95rem;font-weight:700;
                             color:{color_borde};border-bottom:1px solid #f1f5f9;">
                    22/03/2026
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;">
                    Días restantes</td>
                  <td style="padding:10px 16px;font-size:1rem;font-weight:700;
                             color:{color_borde};">
                    {"HOY es el último día" if dr <= 0 else f"{dr} día{'s' if dr != 1 else ''}"}
                  </td>
                </tr>
              </table>

              <!-- Próximas fechas clave -->
              <div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:10px;
                          padding:14px 18px;margin-bottom:20px;">
                <p style="margin:0 0 8px 0;font-size:0.75rem;font-weight:700;
                           text-transform:uppercase;letter-spacing:.1em;color:#7c3aed;">
                  Próximas fechas clave
                </p>
                <p style="margin:0;color:#4c1d95;font-size:0.85rem;line-height:1.8;">
                  📌 <strong>Cierre de actividades:</strong> 22/03/2026<br>
                  📌 <strong>Reporte de novedades de notas:</strong> 23/03/2026 – 25/03/2026<br>
                  📌 <strong>Cierre de periodo académico:</strong> 29/03/2026
                </p>
              </div>

              <p style="color:#94a3b8;font-size:0.82rem;margin:0;line-height:1.6;">
                Este mensaje es generado automáticamente por el sistema de calendarios CUN.
                Por favor no responda a este correo.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f8fafc;padding:14px 30px;
                       border-top:1px solid #e2e8f0;text-align:center;">
              <p style="margin:0;color:#cbd5e1;font-size:0.75rem;">
                CUN – Sistema de Calendarios Académicos · Área Bilingüe BE
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

def enviar_correos_be():
    dr = dias_restantes()
    print(f"📅 Hoy: {date.today()} | Cierre BE: {FECHA_CIERRE} | Días restantes: {dr}")

    if not debe_enviar():
        print("✅ No es necesario enviar alerta BE hoy.")
        return

    print(f"📧 Enviando alertas BE a {len(DESTINATARIOS)} destinatarios...")

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
                msg["From"]    = f"CUN Calendarios BE <{REMITENTE}>"
                msg["To"]      = correo

                msg.attach(MIMEText(construir_cuerpo_html(nombre, dr), "html", "utf-8"))
                server.sendmail(REMITENTE, correo, msg.as_string())
                print(f"  ✅ Enviado a {nombre} <{correo}>")
                enviados += 1

            except Exception as e:
                print(f"  ❌ Error enviando a {correo}: {e}")
                errores += 1

        server.quit()
        print(f"\n📊 Resultado BE: {enviados} enviados, {errores} errores.")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación. Verifica los secretos EMAIL_REMITENTE y EMAIL_PASSWORD.")
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")

if __name__ == "__main__":
    enviar_correos_be()
