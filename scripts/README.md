# Generación del perfil

El README y las dos fichas SVG se generan desde `profile.json` y `assets/portrait-ascii.txt` para mantener una sola fuente de información dentro de este repositorio.

```powershell
python scripts/build_profile.py
```

El generador utiliza únicamente la biblioteca estándar de Python 3.9 o superior. No necesita servicios externos ni credenciales. Después de editar los datos, ejecutarlo y revisar el README y ambas variantes de color antes de hacer commit.

La información y el retrato se sincronizaron con `MigCamo/My-portfolio`, commit `984e6e4739817f4b7dff949412499569a939d812`. Se distinguen el promedio global de la carrera y los promedios por periodo de las notas laudatorias. No se añaden contadores de GitHub, porcentajes de dominio ni logros inferidos.

Los SVG incluyen únicamente texto y formas vectoriales locales: sin scripts, `foreignObject`, fuentes remotas ni imágenes enlazadas. La variante de color se selecciona con `picture`. La información también se presenta como Markdown accesible y los enlaces de contacto se encuentran fuera de la imagen. La terminal interactiva permanece en el portafolio web; el perfil muestra la ficha estática que GitHub admite.

La composición toma como referencia la ficha neofetch de [Andrew6rant](https://github.com/Andrew6rant/Andrew6rant). El retrato y el contenido pertenecen a Miguel Camo. El flujo de contribuciones preexistente se conserva en `.github/workflows/blank.yml`.
