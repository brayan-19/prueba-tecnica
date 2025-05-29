import instaloader
import pandas as pd
import re
import time

# Crear instancia sin iniciar sesión
L = instaloader.Instaloader()

# Cuentas a analizar (deben ser públicas)
usernames = ["elcorteingles", "mercadona", "carrefoures"]

datos_perfiles = []

# Función para extraer enlaces de otras redes sociales
def extraer_redes(biografia):
    redes = []
    patrones = {
        'Facebook': r"(facebook\.com\/[^\s]+)",
        'Twitter': r"(twitter\.com\/[^\s]+)",
        'TikTok': r"(tiktok\.com\/[^\s]+)",
        'YouTube': r"(youtube\.com\/[^\s]+)",
        'LinkedIn': r"(linkedin\.com\/[^\s]+)"
    }
    for red, patron in patrones.items():
        encontrados = re.findall(patron, biografia)
        for link in encontrados:
            redes.append(f"{red}: {link}")
    return redes

for username in usernames:
    print(f"\n🔍 Analizando @{username}")
    try:
        profile = instaloader.Profile.from_username(L.context, username)

        bio = profile.biography
        correos = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", bio)
        telefonos = re.findall(r"\+?\d[\d\s().-]{7,}", bio)
        redes = extraer_redes(bio)

        # Intentar obtener la primera publicación
        try:
            publicaciones = list(profile.get_posts())
            primera_fecha = publicaciones[-1].date if publicaciones else "Sin publicaciones"
            ultima_fecha = publicaciones[0].date if publicaciones else "Sin publicaciones"
        except Exception:
            primera_fecha = "No disponible"
            ultima_fecha = "No disponible"

        datos_perfiles.append({
            "Cuenta": username,
            "Nombre Completo": profile.full_name,
            "Biografía": bio,
            "Correo(s)": ", ".join(correos) if correos else "No encontrados",
            "Teléfono(s)": ", ".join(telefonos) if telefonos else "No encontrados",
            "Otras Redes": ", ".join(redes) if redes else "No encontradas",
            "Primera Publicación": primera_fecha,
            "Última Publicación": ultima_fecha
        })

        time.sleep(2)  # Evita ser bloqueado

    except Exception as e:
        print(f"❌ Error accediendo a @{username}: {e}")

# Guardar en Excel
if datos_perfiles:
    df = pd.DataFrame(datos_perfiles)
    df.to_excel("perfiles_instagram_publicos.xlsx", index=False)
    print("\n✅ Archivo 'perfiles_instagram_publicos.xlsx' creado correctamente.")
else:
    print("\n❌ No se pudo extraer información de los perfiles.")
