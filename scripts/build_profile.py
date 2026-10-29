"""Genera el README y sus fichas SVG desde datos locales; solo biblioteca estándar."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
PORTRAIT = (ROOT / 'assets/portrait-ascii.txt').read_text(encoding='utf-8').splitlines()
PALETTES = {
    'dark': {'background':'#161b22','chrome':'#0d1117','line':'#303844','dots':'#56616f','text':'#d4d9e0','muted':'#8b949e','label':'#eeb880','value':'#9ccdf2','portrait':'#a4b3c3'},
    'light': {'background':'#ffffff','chrome':'#f6f7f9','line':'#d0d7df','dots':'#b0bac6','text':'#27313b','muted':'#637080','label':'#98510b','value':'#215b88','portrait':'#617285'},
}

def svg_card(theme):
    color = PALETTES[theme]
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="610" viewBox="0 0 1100 610" role="img" aria-labelledby="title description">',
        '<title id="title">Miguel Camo · Ingeniero en software · Perfil neofetch</title>',
        '<desc id="description">Retrato ASCII de Miguel Camo junto a su perfil full stack, tecnologías y contacto. La misma información está disponible como texto en el README.</desc>',
        f'<rect x="1" y="1" width="1098" height="608" rx="8" fill="{color["background"]}" stroke="{color["line"]}"/>',
        f'<path d="M9 1h1082a8 8 0 0 1 8 8v30H1V9a8 8 0 0 1 8-8Z" fill="{color["chrome"]}"/>',
        f'<path d="M1 39h1098" stroke="{color["line"]}"/>',
        '<g font-family="Consolas, Liberation Mono, Menlo, monospace" font-size="12">',
    ]
    def text(x,y,value,fill='text',size=None,anchor=None):
        attrs = f' x="{x}" y="{y}" fill="{color[fill]}"'
        if size: attrs += f' font-size="{size}"'
        if anchor: attrs += f' text-anchor="{anchor}"'
        elements.append(f'<text{attrs} xml:space="preserve">{escape(str(value))}</text>')
    for index,fill in enumerate(['#cf8177','#d8b778','#96b98b']):
        elements.append(f'<circle cx="{23+index*11}" cy="21" r="3" fill="{fill}"/>')
    text(67,25,'miguel@camo: ~','muted',10)
    text(1073,25,'portfolio / profile','muted',10,'end')
    text(27,70,'miguel@camo:~$','label',12)
    text(137,70,'neofetch --profile','text',12)
    for index,line in enumerate(PORTRAIT):
        text(24,106 + index*11.7,line,'portrait',9.7)
    text(181,552,'Miguel Camo / retrato en ASCII','muted',9,'middle')
    text(388,103,'miguel@camo','label',14)
    elements.append(f'<path d="M494 99H1073" stroke="{color["dots"]}" stroke-dasharray="3 4"/>')
    cursor = 132
    for index,row in enumerate(DATA['card']):
        if index in (6,12):
            cursor += 17
            heading = 'Tecnologías' if index == 6 else 'Contacto'
            text(388,cursor,'─ '+heading,'text',12)
            elements.append(f'<path d="M497 {cursor-4}H1073" stroke="{color["dots"]}"/>')
            cursor += 27
        label = row['label']
        value = row['value'].removesuffix(' ↗')
        # Dots behind masks allow variable label/value widths without external fonts.
        dots_start = 390 + len(label)*7.25 + 9
        dots_end = 1073 - len(value)*7.25 - 10
        if dots_end > dots_start:
            elements.append(f'<path d="M{dots_start:.2f} {cursor-3}H{dots_end:.2f}" stroke="{color["dots"]}" stroke-dasharray="1 4"/>')
        text(388,cursor,label,'label',12)
        text(1073,cursor,value,'value',12,'end')
        cursor += 22
    elements.append(f'<path d="M388 555H1073" stroke="{color["line"]}"/>')
    text(388,577,f'Proyectos: {len(DATA["projects"]):02d}   Formación: {DATA["education"]["average"]}','muted',10)
    text(1073,577,'# de la interfaz a la arquitectura.','muted',10,'end')
    elements.extend(['</g>','</svg>'])
    return '\n'.join(elements)+'\n'

def markdown():
    contact = {row['label']:row for row in DATA['card']}
    lines = [
        '<!-- Generado con python scripts/build_profile.py. Editar profile.json para actualizar los datos. -->',
        '<picture>',
        '  <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-dark.svg">',
        f'  <img src="./assets/profile-light.svg" width="1100" alt="{escape(DATA["name"])} — Ingeniero en software, desarrollo full stack y arquitectura. Retrato ASCII y ficha neofetch.">',
        '</picture>', '',
        f'[GitHub]({contact["GitHub"]["url"]}) · [LinkedIn]({contact["LinkedIn"]["url"]}) · [Email]({contact["Email"]["url"]}) · [Portafolio y código]({DATA["portfolio_url"]}) · [CV actualizado (PDF)]({DATA["cv_url"]})', '',
        '## `$ cat sobre_mí.md`', '',
        f'**{DATA["name"]}** · Ingeniería en software · Xalapa, Veracruz, México.', '',
        DATA['about'], '', DATA['approach'], '',
    ]
    for area in DATA['expertise']:
        lines.append(f'- **{area["name"]}:** {area["description"]}')
    lines += ['', '## `$ less experiencia.log`', '']
    for experience in DATA['experiences']:
        lines += [f'### {experience["project"]} · {experience["role"]}', '', f'**{experience["organization"]}** · {experience["period"]}', '', experience['summary'], '']
        lines += ['- '+bullet for bullet in experience['bullets']]
        lines += ['', '**Stack / enfoque:** '+ ' · '.join(experience['tags'])+'.', '']
    lines += ['## `$ ls -la ./proyectos`', '', '| Proyecto | Qué construí | Tecnologías |', '| --- | --- | --- |']
    for project in DATA['projects']:
        name = f'[{project["name"]}]({project["url"]})' if project['url'] else project['name']+' *(sin enlace público al código)*'
        lines.append(f'| {name} | {project["description"]} | {", ".join(project["tags"])} |')
    lines.append('')
    for project in DATA['projects']:
        if not project['architecture']: continue
        lines += ['<details>', f'<summary>{escape(project["name"])}: una mirada a la arquitectura</summary>', '', project['architecture'], '']
        lines += [f'[{link["label"]}]({link["url"]})' for link in project['related']]
        lines += ['', '</details>', '']
    lines += ['## `$ cat stack.conf`', '', '| Área | Herramientas |', '| --- | --- |']
    lines += [f'| {group["name"]} | {", ".join(group["tools"])} |' for group in DATA['stack']]
    education = DATA['education']
    lines += ['', '## `$ cat formación.md`', '', f'**{education["degree"]} · {education["organization"]}**', '', f'{education["period"]} · Promedio global de la carrera: **{education["average"]}**.', '', education['recognition'], '']
    lines += [f'- [{source["label"]}]({source["url"]})' for source in education['sources']]
    lines += ['', '## `$ ./contacto.sh`', '', f'¿Un proyecto, un reto técnico o una oportunidad? Escríbeme a [{contact["Email"]["value"]}]({contact["Email"]["url"]}).', '', f'[Mi trabajo en GitHub]({contact["GitHub"]["url"]}) · [LinkedIn]({contact["LinkedIn"]["url"]}) · [Descargar CV]({DATA["cv_url"]})', '']
    return '\n'.join(lines)

for theme in PALETTES:
    (ROOT / f'assets/profile-{theme}.svg').write_text(svg_card(theme),encoding='utf-8')
(ROOT / 'README.md').write_text(markdown(),encoding='utf-8')
print('Generados: README.md, assets/profile-dark.svg y assets/profile-light.svg.')
