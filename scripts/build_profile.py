"""Genera el README y sus fichas SVG desde datos locales; solo biblioteca estándar."""
from pathlib import Path
from html import escape
import json
from design import hero_card, architecture_card

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

def picture(name, alt):
    return [
        '<picture>',
        f'  <source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.svg">',
        f'  <img src="./assets/{name}-light.svg" width="1100" alt="{escape(alt)}">',
        '</picture>', '',
    ]


def experience_block(experience):
    lines = [
        f'### {experience["project"]} · {experience["role"]}', '',
        f'**{experience["organization"]}** · {experience["period"]}', '',
        experience['summary'], '',
    ]
    lines += ['- '+bullet for bullet in experience['bullets']]
    return lines + ['', '**Stack / enfoque:** '+ ' · '.join(experience['tags'])+'.', '']


def project_image(project, width=440):
    image = f'<img src="./{project["thumbnail"]}" width="{width}" alt="Captura de {escape(project["name"])}">'
    return f'<a href="{escape(project["url"])}">{image}</a>' if project['url'] else image


def markdown():
    contact = {row['label']:row for row in DATA['card']}
    current = DATA['experiences'][0]
    featured = DATA['projects'][:2]
    lines = ['<!-- Generado con python scripts/build_profile.py. Editar profile.json para actualizar los datos. -->']
    lines += picture('hero', f'{DATA["name"]} — Ingeniero en software. Full stack y arquitectura. Retrato ASCII propio y trabajo actual en Equipo ARIES.')
    lines += [
        f'**[↗ Portafolio y código]({DATA["portfolio_url"]})** &nbsp; / &nbsp; [LinkedIn]({contact["LinkedIn"]["url"]}) &nbsp; / &nbsp; [Email]({contact["Email"]["url"]}) &nbsp; / &nbsp; [CV actualizado (PDF)]({DATA["cv_url"]})', '',
        DATA['about'], '',
        '> **Ahora, en Equipo ARIES:** desarrollo frontend, migración y evolución de la arquitectura, con pruebas automatizadas en Cypress.', '',
        '## `$ ls ./work --selected`', '',
        '| '+ ' | '.join(f'[{project["name"]}]({project["url"]})' for project in featured)+' |',
        '| :--- | :--- |',
        '| '+ ' | '.join(project_image(project) for project in featured)+' |',
        '| '+ ' | '.join(project['description'] for project in featured)+' |',
        '| '+ ' | '.join(' · '.join(f'`{tag}`' for tag in project['tags']) for project in featured)+' |',
        '| '+ ' | '.join(f'[↗ Explorar el código]({project["url"]})' for project in featured)+' |', '',
    ]
    for project in featured:
        lines += ['<details>', f'<summary>{escape(project["name"])}: decisiones de arquitectura</summary>', '', project['architecture'], '']
        lines += [f'[{link["label"]}]({link["url"]})' for link in project['related']]
        lines += ['', '</details>', '']
    lines += ['<details>', '<summary>+ Explorar otros 3 proyectos: gestión académica, negocio y aplicaciones web</summary>', '', '| Proyecto | Qué construí | Tecnologías |', '| --- | --- | --- |']
    for project in DATA['projects'][2:]:
        name = f'[{project["name"]}]({project["url"]})' if project['url'] else project['name']+' *(sin enlace público al código)*'
        lines.append(f'| {project_image(project,190)}<br>{name} | {project["description"]} | {", ".join(project["tags"])} |')
    lines += ['', '</details>', '', '## `$ inspect architecture`', '']
    lines += picture('architecture','Mi enfoque full stack: frontend, APIs, dominio y datos; calidad transversal con Cypress y herramientas de desarrollo.')
    lines += [DATA['approach'], '']
    for area in DATA['expertise']:
        lines.append(f'- **{area["name"]}:** {area["description"]}')
    lines += ['', '<details>', '<summary>stack.conf — herramientas por área</summary>', '', '| Área | Herramientas |', '| --- | --- |']
    lines += [f'| {group["name"]} | {", ".join(group["tools"])} |' for group in DATA['stack']]
    lines += ['', '</details>', '', '## `$ tail experiencia.log`', '']
    lines += experience_block(current)
    lines += ['<details>', '<summary>Experiencia anterior — desarrollo backend y sistemas académicos</summary>', '']
    for experience in DATA['experiences'][1:]:
        lines += experience_block(experience)
    lines += ['</details>', '']
    education = DATA['education']
    lines += ['<details>', '<summary>Formación y reconocimientos — Universidad Veracruzana</summary>', '', f'**{education["degree"]} · {education["organization"]}**', '', f'{education["period"]} · Promedio global de la carrera: **{education["average"]}**.', '', education['recognition'], '']
    lines += [f'- [{source["label"]}]({source["url"]})' for source in education['sources']]
    lines += ['', '</details>', '', '<details>', '<summary>neofetch --full — ficha completa del perfil</summary>', '']
    lines += picture('profile',f'{DATA["name"]}: ficha neofetch con perfil, tecnologías, formación y contacto.')
    lines += ['</details>', '', '## `$ ./contacto.sh`', '', f'¿Un proyecto, un reto técnico o una oportunidad? Escríbeme a **[{contact["Email"]["value"]}]({contact["Email"]["url"]})**.', '', f'[GitHub]({contact["GitHub"]["url"]}) · [LinkedIn]({contact["LinkedIn"]["url"]}) · [Descargar CV]({DATA["cv_url"]})', '']
    return '\n'.join(lines)

for theme in PALETTES:
    (ROOT / f'assets/profile-{theme}.svg').write_text(svg_card(theme),encoding='utf-8')
    (ROOT / f'assets/hero-{theme}.svg').write_text(hero_card(theme,PALETTES[theme],PORTRAIT,DATA),encoding='utf-8')
    (ROOT / f'assets/architecture-{theme}.svg').write_text(architecture_card(theme,PALETTES[theme]),encoding='utf-8')
(ROOT / 'README.md').write_text(markdown(),encoding='utf-8')
print('Generados: README, portadas, diagramas de arquitectura y fichas neofetch en ambos temas.')
