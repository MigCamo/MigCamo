# Generación del perfil

El README, las portadas, los diagramas de arquitectura y las fichas neofetch se generan desde `profile.json` y `assets/portrait-ascii.txt`. Los datos se mantienen en una sola fuente dentro de este repositorio.

```powershell
python scripts/build_profile.py
```

El generador utiliza únicamente la biblioteca estándar de Python 3.9 o superior. No necesita servicios externos ni credenciales. `build_profile.py` organiza el contenido y `design.py` compone la portada y el diagrama. Después de editar los datos, ejecutar el generador y revisar el README y ambas variantes de color antes de hacer commit.

La información y el retrato se sincronizaron con `MigCamo/My-portfolio`, commit `984e6e4739817f4b7dff949412499569a939d812`. Se distinguen el promedio global de la carrera y los promedios por periodo de las notas laudatorias. No se añaden contadores de GitHub, porcentajes de dominio ni logros inferidos.

Los SVG incluyen únicamente texto y formas vectoriales locales: sin scripts, `foreignObject`, fuentes remotas ni imágenes enlazadas. La variante de color se selecciona con `picture`. La información también se presenta como Markdown accesible y los enlaces de contacto se encuentran fuera de la imagen. La terminal interactiva permanece en el portafolio web; el perfil muestra la ficha estática que GitHub admite.

Las cinco capturas de `assets/projects/` proceden del portafolio. Las dos primeras se muestran como proyectos destacados y las restantes se agrupan en una sección desplegable. La experiencia anterior, la formación, el stack completo y la ficha neofetch siguen disponibles en desplegables para facilitar la lectura inicial.

El diagrama representa el enfoque conceptual de Miguel para conectar interfaces, servicios, dominio y datos; no se atribuye esa arquitectura a una implementación concreta de ARIES.

La composición toma como referencia la ficha neofetch de [Andrew6rant](https://github.com/Andrew6rant/Andrew6rant). El retrato y el contenido pertenecen a Miguel Camo. El flujo de contribuciones preexistente se conserva en `.github/workflows/blank.yml`.
