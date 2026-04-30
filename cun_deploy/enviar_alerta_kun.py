"""
CUN – Alerta automática: Días KUN (Coworking Chapinero)
Envía recordatorio 1 día antes de cada Día KUN.
"""

import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────

REMITENTE = os.environ.get("EMAIL_REMITENTE", "")
PASSWORD  = os.environ.get("EMAIL_PASSWORD", "")

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

DESTINATARIOS = [
    ("Andrés Camilo Vásquez Blanco",      "andres_vasquez@cun.edu.co"),
    ("Aura María Osorio",                 "johana_caicedo@cun.edu.co"),
    ("Julio Andrés Pamplona Llanos",      "julio_pamplona@cun.edu.co"),
    ("Ángela Rocío Camargo Puerto",       "angela_camargop@cun.edu.co"),
    ("Cristian Felipe Galindo Acero",     "cristian_galindoa@cun.edu.co"),
    ("Elkin Ignacio Rodríguez Carrero",   "elkin_rodriguezca@cun.edu.co"),
    ("Gillyam Germán Martínez Bernal",    "gillyam_martinez@cun.edu.co"),
    ("Heidy Johanna Quiroga Aguilar",     "heidy_quiroga@cun.edu.co"),
    ("Laura Daniela Gómez Arenas",        "laura_gomeza@cun.edu.co"),
    ("Leidy Laura Díazgranados Blanco",   "leidy_diazgranados@cun.edu.co"),
    ("Maira Alejandra Doncel Largo",      "maira_doncel@cun.edu.co"),
    ("Mónica Esperanza Pachón Gordillo",  "monica_pachon@cun.edu.co"),
    ("William Estrada Santis",            "william_estrada@cun.edu.co"),
    ("Yureines María Sánchez Moreno",     "yureines_sanchez@cun.edu.co"),
]

# ── LÓGICA ────────────────────────────────────────────────────────────────────

def dia_kun_manana():
    """Retorna el Día KUN de mañana si existe, si no None."""
    hoy = date.today()
    for d in DIAS_KUN:
        diff = (d["fecha"] - hoy).days
        if diff == 1:
            return d
    return None

def construir_asunto(dia_kun):
    return f"📍 MAÑANA es el Día KUN #{dia_kun['num']} – {dia_kun['dia']} {dia_kun['fecha'].strftime('%d/%m/%Y')}"

def construir_cuerpo_html(nombre, dia_kun):
    fecha_str = dia_kun['fecha'].strftime('%d/%m/%Y')
    return f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:30px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:16px;overflow:hidden;
                      border:1px solid #e2e8f0;max-width:600px;width:100%;">

          <!-- Banner -->
          <tr>
            <td style="background:#1e3a5f;padding:24px 30px;border-bottom:3px solid #3b82f6;">
              <p style="margin:0;font-size:0.75rem;text-transform:uppercase;
                        letter-spacing:0.15em;color:#93c5fd;">
                CUN · Coworking Chapinero
              </p>
              <h1 style="margin:10px 0 0 0;font-size:1.5rem;color:#ffffff;font-weight:700;">
                📍 Recordatorio: Día KUN #{dia_kun['num']}
              </h1>
            </td>
          </tr>

          <!-- Cuerpo -->
          <tr>
            <td style="padding:28px 30px;">
              <p style="color:#64748b;font-size:0.9rem;margin:0 0 6px 0;">Estimado/a,</p>
              <p style="color:#1e293b;font-size:1rem;font-weight:600;margin:0 0 20px 0;">{nombre}</p>

              <!-- Alerta -->
              <div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:10px;
                          padding:16px 20px;margin-bottom:24px;">
                <p style="margin:0;color:#1e40af;font-size:1rem;">
                  🗓️ <strong>Mañana</strong> es el <strong>Día KUN #{dia_kun['num']}</strong>.
                  ¡Recuerda asistir al Coworking Chapinero!
                </p>
              </div>

              <!-- Detalles -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f8fafc;border:1px solid #e2e8f0;
                            border-radius:10px;overflow:hidden;margin-bottom:24px;">
                <tr style="background:#eff6ff;">
                  <td colspan="2" style="padding:10px 16px;font-size:0.7rem;color:#1d4ed8;
                      text-transform:uppercase;letter-spacing:0.1em;font-weight:700;
                      border-bottom:1px solid #e2e8f0;">Información del evento</td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;width:35%;">Día KUN</td>
                  <td style="padding:10px 16px;color:#1e293b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;font-weight:600;">
                    #{dia_kun['num']} de 8
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;">Fecha</td>
                  <td style="padding:10px 16px;color:#1e293b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;font-weight:700;">
                    {dia_kun['dia']} {fecha_str}
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;">Horario</td>
                  <td style="padding:10px 16px;color:#1e293b;font-size:0.85rem;
                             border-bottom:1px solid #f1f5f9;">
                    8:00 AM – 6:00 PM
                  </td>
                </tr>
                <tr>
                  <td style="padding:10px 16px;color:#64748b;font-size:0.85rem;">Lugar</td>
                  <td style="padding:10px 16px;color:#1e293b;font-size:0.85rem;font-weight:600;">
                    Coworking Chapinero
                  </td>
                </tr>
              </table>

              <p style="color:#94a3b8;font-size:0.82rem;margin:0;line-height:1.6;">
                Este mensaje es generado automáticamente por el sistema de calendarios CUN.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f8fafc;padding:14px 30px;border-top:1px solid #e2e8f0;text-align:center;">
              <p style="margin:0;color:#cbd5e1;font-size:0.75rem;">
                CUN – Sistema de Calendarios Académicos · Días KUN
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

def enviar_correos_kun():
    hoy = date.today()
    dia_kun = dia_kun_manana()

    print(f"📅 Hoy: {hoy}")

    if not dia_kun:
        print("✅ No hay Día KUN mañana. Sin alertas.")
        return

    print(f"📧 Mañana es Día KUN #{dia_kun['num']} – {dia_kun['fecha']}. Enviando alertas...")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(REMITENTE, PASSWORD)

        enviados = errores = 0
        for nombre, correo in DESTINATARIOS:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = construir_asunto(dia_kun)
                msg["From"]    = f"CUN Calendarios <{REMITENTE}>"
                msg["To"]      = correo
                msg.attach(MIMEText(construir_cuerpo_html(nombre, dia_kun), "html", "utf-8"))
                server.sendmail(REMITENTE, correo, msg.as_string())
                print(f"  ✅ {nombre} <{correo}>")
                enviados += 1
            except Exception as e:
                print(f"  ❌ Error {correo}: {e}")
                errores += 1

        server.quit()
        print(f"\n📊 Resultado: {enviados} enviados, {errores} errores.")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación.")
    except Exception as e:
        print(f"❌ Error SMTP: {e}")

if __name__ == "__main__":
    enviar_correos_kun()
