"""Composición vectorial del perfil; sin scripts ni recursos externos en los SVG."""
from html import escape

FONT = 'Consolas, Liberation Mono, Menlo, monospace'


class Drawing:
    def __init__(self, width, height, color, title, description):
        self.width, self.height, self.color = width, height, color
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="description">{escape(description)}</desc>',
            f'<g font-family="{FONT}">',
        ]

    def rect(self, x, y, width, height, fill='background', stroke=None, radius=0):
        attrs = f' x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{self.color.get(fill, fill)}"'
        if stroke:
            attrs += f' stroke="{self.color.get(stroke, stroke)}"'
        self.parts.append(f'<rect{attrs}/>')

    def path(self, path, color='line', opacity=1, dashed=None):
        attrs = f' d="{path}" fill="none" stroke="{self.color.get(color, color)}" opacity="{opacity}"'
        if dashed:
            attrs += f' stroke-dasharray="{dashed}"'
        self.parts.append(f'<path{attrs}/>')

    def text(self, x, y, text, color='text', size=14, weight=400, anchor=None, length=None):
        attrs = f' x="{x}" y="{y}" fill="{self.color.get(color, color)}" font-size="{size}" font-weight="{weight}"'
        if anchor:
            attrs += f' text-anchor="{anchor}"'
        if length:
            attrs += f' textLength="{length:.2f}" lengthAdjust="spacingAndGlyphs"'
        self.parts.append(f'<text{attrs} xml:space="preserve">{escape(str(text))}</text>')

    def finish(self):
        return '\n'.join(self.parts + ['</g>', '</svg>'])+'\n'


def hero_card(theme, color, portrait, data):
    drawing = Drawing(
        1100, 610, color,
        'Miguel Camo · Software engineer · Full stack y arquitectura',
        'Retrato ASCII de Miguel Camo. Ingeniero en software, desarrollador full stack; actualmente frontend y QA en Equipo ARIES. Xalapa, Veracruz. La información completa está en el README.',
    )
    drawing.rect(1,1,1098,608,'background','line',8)
    drawing.rect(2,2,1096,36,'chrome',radius=7)
    drawing.path('M1 39H1099')
    drawing.text(24,25,'~/migcamo', 'label',11)
    drawing.text(1075,25,'README.md  /  UTF-8  /  LF','muted',10,anchor='end')

    # El retrato mantiene un avance fijo de carácter en diferentes plataformas.
    drawing.rect(22,63,355,500,'chrome','line',3)
    for x in range(42,370,22):
        drawing.path(f'M{x} 84V541','dots',.12)
    for y in range(86,542,22):
        drawing.path(f'M38 {y}H362','dots',.12)
    drawing.text(39,87,'01 / IDENTITY', 'muted',10)
    for index, line in enumerate(portrait):
        drawing.text(34,110+index*12.0,line,'portrait',10.5,length=len(line)*5.6)
    drawing.path('M34 113V99H48M352 99H366V113M34 523V537H48M352 537H366V523','label')
    drawing.text(200,552,'miguel@camo:~$ whoami','label',10,anchor='middle')

    drawing.text(410,88,'ENGINEERING / FULL STACK', 'value',12)
    drawing.text(404,165,'MIGUEL','text',66,700)
    drawing.text(404,236,'CAMO','label',66,700)
    drawing.rect(591,225,28,8,'value')
    drawing.text(410,281,'Ingeniero en software','text',23)
    drawing.text(410,313,'De la interfaz a la arquitectura.','value',17)
    drawing.path('M410 340H1072')
    drawing.text(410,368,'ACTUALMENTE / UNIVERSIDAD VERACRUZANA','muted',10)
    drawing.text(410,399,'Equipo ARIES','text',23,600)
    drawing.rect(869,375,202,31,'chrome','line',3)
    drawing.text(970,395,'FRONTEND + QA','label',12,anchor='middle')
    drawing.text(410,430,'Desarrollo frontend, migración y arquitectura.','muted',14)
    drawing.text(410,452,'Pruebas automatizadas con Cypress.','muted',14)
    drawing.path('M410 475H1072')
    drawing.text(410,505,'XALAPA, VERACRUZ / MX','value',12)
    drawing.text(410,531,'GitHub: @MigCamo','muted',12)
    drawing.text(1071,531,f'{len(data["projects"]):02d} proyectos · {len(data["experiences"]):02d} experiencias','muted',11,anchor='end')
    drawing.path('M22 579H1072')
    drawing.text(24,598,'RESPONSABILIDADES CLARAS  /  CÓDIGO MANTENIBLE  /  CALIDAD','muted',10)
    drawing.text(1072,598,'software con criterio_','label',10,anchor='end')
    return drawing.finish()


def architecture_card(theme, color):
    drawing = Drawing(
        1100, 310, color,
        'Cómo abordo un sistema: frontend, APIs, dominio y datos',
        'Esquema conceptual de mi enfoque full stack: interfaces, servicios, responsabilidades del dominio y persistencia. Calidad transversal con Cypress y herramientas de desarrollo. No describe la implementación de un proyecto concreto.',
    )
    drawing.rect(1,1,1098,308,'background','line',5)
    drawing.text(26,30,'02 / SYSTEMS THINKING','label',11)
    drawing.text(26,69,'Una visión de extremo a extremo.','text',27,600)
    drawing.text(1072,30,'$ inspect architecture','muted',10,anchor='end')
    drawing.path('M26 91H1072')
    nodes = [
        (26,'01 / UI','Frontend','Angular · React · Vue.js','value'),
        (301,'02 / API','Servicios','.NET · Spring Boot · Node.js','label'),
        (576,'03 / CORE','Dominio','SOLID · Patrones · UML','value'),
        (851,'04 / DATA','Datos','SQL Server · MySQL','label'),
    ]
    for x, label, title, tools, accent in nodes:
        drawing.rect(x,116,223,104,'chrome','line',3)
        drawing.rect(x,116,3,104,accent)
        drawing.text(x+17,141,label,'muted',10)
        drawing.text(x+17,172,title,accent,21,600)
        drawing.text(x+17,199,tools,'muted',10)
        if x < 851:
            drawing.path(f'M{x+233} 168H{x+266}m-7-5 7 5-7 5','dots')
    drawing.path('M26 242H1072')
    drawing.text(26,271,'[ CALIDAD TRANSVERSAL ]','label',12)
    drawing.text(26,293,'Cypress · Git · Docker · Podman · Postman','muted',11)
    drawing.text(1072,275,'diseñar → construir → probar → evolucionar','value',12,anchor='end')
    return drawing.finish()
