from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os, json

TZ = ZoneInfo("America/Guayaquil")

class GoogleService:
    def __init__(self, creds_file: str = "credentials.json"):

        creds_env = os.getenv("GOOGLE_CREDENTIALS_JSON")

        if creds_env:
            try:
                creds_env = creds_env.replace("\\n", "\n")
                info = json.loads(creds_env)

                creds = service_account.Credentials.from_service_account_info(
                    info,
                    scopes=["https://www.googleapis.com/auth/calendar"]
                )
                print("🔐 Credenciales cargadas desde GOOGLE_CREDENTIALS_JSON.")
            except Exception as e:
                raise Exception(f"❌ Error leyendo GOOGLE_CREDENTIALS_JSON: {e}")

        else:
            try:
                creds = service_account.Credentials.from_service_account_file(
                    creds_file,
                    scopes=["https://www.googleapis.com/auth/calendar"]
                )
                print("📄 Usando credentials.json local.")
            except Exception as e:
                raise Exception(
                    f"❌ Error cargando credentials.json:\n{e}\n"
                    f"Si estás en producción debes usar GOOGLE_CREDENTIALS_JSON."
                )

        self.service = build("calendar", "v3", credentials=creds)

    def crear_evento(self, calendar_id, resumen, descripcion, inicio, fin, timezone="America/Guayaquil"):
        try:
            evento = {
                "summary": resumen,
                "description": descripcion,
                "start": {"dateTime": inicio.isoformat(), "timeZone": timezone},
                "end": {"dateTime": fin.isoformat(), "timeZone": timezone},
            }

            self.service.events().insert(calendarId=calendar_id, body=evento).execute()
            print(f"✅ Evento creado correctamente: {resumen}")

        except Exception as e:
            raise Exception(f"❌ Error creando evento en Google Calendar: {e}")

