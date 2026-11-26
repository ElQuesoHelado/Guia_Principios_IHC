"""Construye el HTA v8 en PDF y DOCX desde contenido.json, sin tocar el v7.

Respeta la estructura del PDF v7. Requiere pdflatex. El DOCX usa OOXML estándar y solo stdlib.
"""
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, re, struct, subprocess, tempfile, textwrap
from html import escape

BASE=Path(__file__).resolve().parent.parent
SOURCE=BASE/'docs/hta_v8'
STEM='HTA_correo_vocabulario_v8'

def flatten(node):
    yield node
    for child in node.get('children',[]):yield from flatten(child)

def references(text):
    found=set(re.findall(r'\b[CV]\d+(?:\.\d+)*',text))
    # Incluye los términos intermedios de rangos como C3.2.1–C3.2.3.
    for a,b in re.findall(r'\b([CV]\d+(?:\.\d+)*)[–-]([CV]\d+(?:\.\d+)*)',text):
        pa,_,na=a.rpartition('.');pb,_,nb=b.rpartition('.')
        if pa==pb and na.isdigit() and nb.isdigit():
            found.update(f'{pa}.{i}' for i in range(int(na),int(nb)+1))
        elif re.fullmatch(r'[CV]\d+',a) and a[0]==b[0]:
            found.update(f'{a[0]}{i}' for i in range(int(a[1:]),int(b[1:])+1))
    return found

def validate(data):
    roots=[r['node'] for r in data['roots']]
    assert [r['id'] for r in roots]==['C0','V0'], 'Se requieren exactamente dos raíces.'
    nodes=[n for root in roots for n in flatten(root)]
    ids={n['id'] for n in nodes}
    assert len(ids)==len(nodes),'Identificador repetido.'
    parents=[n for n in nodes if n.get('children')]
    assert all(n.get('plan') for n in parents),'Nodo descompuesto sin plan.'
    for node in nodes:
        assert not re.search('simulaci[oó]n|conversaci[oó]n',node['title'],re.I),node['id']
        for child in node.get('children',[]):
            if node['id'] not in ['C0','V0']:assert child['id'].startswith(node['id']+'.')
        if 'plan' in node:
            refs=references(node['plan'])
            assert refs<=ids,(node['id'],refs-ids)
            child_ids={c['id'] for c in node.get('children',[])}
            assert child_ids<=refs,('Plan sin un hijo explícito',node['id'],child_ids-refs)
    original=BASE/data['original']
    assert hashlib.sha256(original.read_bytes()).hexdigest()==data['original_sha256'],'El original cambió.'
    return nodes,parents

def display_refs(text,scope):
    def convert(m):
        letter,number=m.groups()
        if letter==scope:return number
        task='1' if letter=='C' else '2'
        return f'raíz 0 de la tarea {task}' if number=='0' else f'{number} de la tarea {task}'
    return re.sub(r'\b([CV])(\d+(?:\.\d+)*)',convert,text)


def blocks(data):
    """Mismo orden que v7: usuarios, ficha, árbol, planes, evidencias."""
    b=[('label',('Alumnos:',data['authors'])),
       ('h1','1. Análisis de potenciales grupos de usuarios (Usuarios objetivo)'),
       ('p','Estudiante universitario de 18 a 25 años con nivel B1-B2 de inglés.'),
       ('h2','Características generales del usuario objetivo')]
    b.extend(('p',f'{chr(97+i)}) {label}: {text}') for i,(label,text) in enumerate(data['users_legacy_format']))
    b += [('h2','Enfoque del análisis'),('p',data['learning_focus'])]
    for i,root in enumerate(data['roots']):
        node=root['node'];scope=node['id'][0]
        b += [('page',None),('h1',f'Tarea {i+1}. {data["legacy_format"]["task_titles"][i]}'),
              ('p','Objetivo de aprendizaje: '+root['objective']),('h2','Precondiciones')]
        b.extend(('bullet',p) for p in data['legacy_format']['preconditions'][i])
        b.extend([('label',('Frecuencia:',root['frequency'])),('label',('Restricciones:',data['legacy_format']['restrictions'][i])),
                  ('label',('Excepciones:',root['exceptions'])),('h2','Análisis jerárquico de tareas')])
        def walk(n,depth):
            b.append(('node',(depth,n['id'][1:],display_refs(n['title'],scope))))
            for child in n.get('children',[]):walk(child,depth+1)
        walk(node,0)
        b.append(('h2','Planes de aprendizaje'))
        for n in flatten(node):
            if n.get('plan'):b.append(('label',('Plan '+n['id'][1:]+':',display_refs(n['plan'],scope))))
        b += [('h2','Evidencias de aprendizaje'),('p',data['legacy_format']['evidences'][i]),('p',root['closure'])]
    return b


def tex(t):
    repl={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','→':r' $\rightarrow$ ','–':'--','—':'---','“':'``','”':"''",'…':r'\ldots{}','·':r'\textperiodcentered{}'}
    return ''.join(repl.get(c,c) for c in str(t))


def pdf(data,content):
    out=[r'''\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[left=1.8cm,right=1.8cm,top=2.06cm,bottom=1.8cm,headsep=24.3pt]{geometry}
\usepackage{xcolor,titlesec,hyperref,fancyhdr}
\definecolor{heading}{HTML}{0D4268}
\hypersetup{pdftitle={Lingua IA - HTA de correo y vocabulario v8}}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small Lingua IA \textperiodcentered{} Análisis de tareas}
\fancyhead[R]{\small HTA \textperiodcentered{} Correo y vocabulario}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{12pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\setlength{\emergencystretch}{3em}
\titleformat{\section}{\Large\bfseries\color{heading}}{}{0pt}{}
\titleformat{\subsection}{\large\bfseries\color{heading}}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{10.66pt}{5.13pt}
\newcommand{\HTAline}[3]{\par\noindent\hspace*{#1cm}\begin{minipage}{\dimexpr\linewidth-#1cm\relax}#3 #2\end{minipage}\par}
\begin{document}''']
    out.append(r'\hypersetup{pdfauthor={'+tex(data['authors'])+'}}')
    for kind,value in content:
        if kind in ['h1','h2']:out.append(('\\section*{' if kind=='h1' else '\\subsection*{')+tex(value)+'}')
        elif kind=='p':out.append(tex(value)+r'\par')
        elif kind=='page':out.append(r'\clearpage')
        elif kind=='bullet':out.append(r'{\setlength{\parskip}{2pt}\textbullet\ '+tex(value)+r'\par}')
        elif kind=='label':label,text=value;out.append(r'\textbf{'+tex(label)+r'} '+tex(text)+r'\par')
        elif kind=='node':
            depth,code,text=value
            title=tex(text)+(r'.' if depth>0 and not text.endswith(('.',':','?','!')) else '')
            if depth<2:paragraph=r'\textbf{'+tex(code)+'. '+title+'}'
            elif depth==2:paragraph=r'\textbf{'+tex(code)+'.} '+title
            else:paragraph=tex(code)+'. '+title
            out.append(r'\HTAline{'+str(max(0,depth-1)*.4)+'}{'+paragraph+'}{}')
    out.append(r'\end{document}')
    source=SOURCE/f'{STEM}.tex';source.write_text('\n'.join(out))
    with tempfile.TemporaryDirectory(prefix='lingua-hta-format-v7-') as temp:
        for _ in range(2):
            r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',temp,str(source)],capture_output=True,text=True,errors='replace')
            if r.returncode:raise RuntimeError(r.stdout[-3500:])
        (BASE/f'{STEM}.pdf').write_bytes((Path(temp)/f'{STEM}.pdf').read_bytes())
        (SOURCE/'compilacion.log').write_text(r.stdout)
        assert 'Overfull \\hbox' not in r.stdout,'Hay texto que rebasa el ancho.'


W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS='xmlns:w="'+W+'" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


def run(text,bold=False):return '<w:r>'+('<w:rPr><w:b/></w:rPr>' if bold else '')+'<w:t xml:space="preserve">'+escape(str(text))+'</w:t></w:r>'


def paragraph(text='',style=None,indent=0,bold=False,runs=None):
    props=(f'<w:pStyle w:val="{style}"/>' if style else '')+(f'<w:ind w:left="{indent}"/>' if indent else '')
    return '<w:p><w:pPr>'+props+'</w:pPr>'+(runs if runs is not None else run(text,bold))+'</w:p>'


def docx(data,content):
    parts={};body=[]
    for kind,value in content:
        if kind in ['h1','h2','p']:
            body.append(paragraph(value,{'h1':'Heading1','h2':'Heading2'}.get(kind)))
        elif kind=='page':body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
        elif kind=='bullet':body.append(paragraph('• '+value,'Bullet'))
        elif kind=='label':label,text=value;body.append(paragraph(runs=run(label+' ',True)+run(text)))
        elif kind=='node':
            depth,code,text=value
            suffix='.' if depth>0 and not text.endswith(('.',':','?','!')) else ''
            if depth<2:runs=run(code+'. '+text+suffix,True)
            elif depth==2:runs=run(code+'. ',True)+run(text+suffix)
            else:runs=run(code+'. '+text+suffix)
            body.append(paragraph(indent=round(max(0,depth-1)*.4/2.54*1440),runs=runs))
    sect='<w:sectPr><w:headerReference w:type="default" r:id="header"/><w:footerReference w:type="default" r:id="footer"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1168" w:right="1020" w:bottom="1020" w:left="1020" w:header="440" w:footer="440"/></w:sectPr>'
    parts['word/document.xml']='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '+NS+'><w:body>'+''.join(body)+sect+'</w:body></w:document>'
    # La familia serif y los tamaños siguen el documento de referencia; el PDF
    # conserva las fuentes Computer Modern originales de TeX.
    styles=[('Normal',20,'000000',False,False),('Heading1',29,'0D4268',True,True),('Heading2',24,'0D4268',True,True),('Header',18,'000000',False,False),('Bullet',20,'000000',False,False)]
    xml='<w:styles xmlns:w="'+W+'"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/><w:lang w:val="es-PE"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
    for name,size,color,bold,keep in styles:
        xml+=f'<w:style w:type="paragraph" w:styleId="{name}"'+(' w:default="1"' if name=='Normal' else '')+f'><w:name w:val="{name}"/>'+('' if name=='Normal' else '<w:basedOn w:val="Normal"/>')+'<w:pPr>'+('<w:keepNext/>' if keep else '')+('<w:spacing w:before="200" w:after="120"/>' if name.startswith('Heading') else '')+('<w:outlineLvl w:val="'+str(int(name[-1])-1)+'"/>' if name.startswith('Heading') else '')+'</w:pPr><w:rPr><w:sz w:val="'+str(size)+'"/><w:color w:val="'+color+'"/>'+('<w:b/>' if bold else '')+'</w:rPr></w:style>'
    parts['word/styles.xml']=xml+'</w:styles>'
    rels=[('styles','styles','styles.xml'),('header','header','header1.xml'),('footer','footer','footer1.xml')]
    parts['word/_rels/document.xml.rels']='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{kind}" Target="{target}"/>' for i,kind,target in rels)+'</Relationships>'
    parts['_rels/.rels']='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="document" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    header=paragraph(runs=run(data['legacy_format']['header_left'])+'<w:r><w:tab/></w:r>'+run(data['legacy_format']['header_right']),style='Header')
    header=header.replace('<w:pPr>','<w:pPr><w:tabs><w:tab w:val="right" w:pos="9866"/></w:tabs><w:pBdr><w:bottom w:val="single" w:sz="4" w:color="000000"/></w:pBdr>')
    parts['word/header1.xml']='<w:hdr '+NS+'>'+header+'</w:hdr>'
    parts['word/footer1.xml']='<w:ftr '+NS+'><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:fldSimple w:instr="PAGE">'+run('1')+'</w:fldSimple></w:p></w:ftr>'
    types=[('document','application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'),('styles','application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'),('header1','application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml'),('footer1','application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml')]
    parts['[Content_Types].xml']='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'+''.join(f'<Override PartName="/word/{part}.xml" ContentType="{kind}"/>' for part,kind in types)+'</Types>'
    with ZipFile(BASE/f'{STEM}.docx','w',ZIP_DEFLATED) as z:
        for name,value in parts.items():z.writestr(name,value.encode('utf-8'))
    with ZipFile(BASE/f'{STEM}.docx') as z:
        assert z.testzip() is None
        for name in z.namelist():
            if name.endswith(('.xml','.rels')):ET.fromstring(z.read(name))


def main():
    data=json.loads((SOURCE/'contenido.json').read_text())
    nodes,parents=validate(data);content=blocks(data)
    pdf(data,content);docx(data,content)
    pdf_text=subprocess.run(['pdftotext','-layout',str(BASE/f'{STEM}.pdf'),'-'],capture_output=True,text=True,check=True).stdout
    # Verifica cada título, hoja y plan en su tarea, sin depender de los prefijos
    # internos C/V, que no forman parte de la numeración del formato anterior.
    def norm(t):return re.sub(r'\s+',' ',t).replace('–','-').strip()
    assert norm(data['authors']) in norm(pdf_text),'Faltan los alumnos en el PDF.'
    sections=re.split(r'Tarea [12]\. ',pdf_text)
    assert len(sections)==3,'Deben existir solo dos tareas.'
    for root,section in zip(data['roots'],sections[1:]):
        for node in flatten(root['node']):
            label=node['id'][1:]
            assert re.search(r'(?m)^\s*'+re.escape(label)+r'\. ',section),node['id']
            if node.get('plan'):assert 'Plan '+label+':' in section,node['id']
    with ZipFile(BASE/f'{STEM}.docx') as z:
        root=ET.fromstring(z.read('word/document.xml'));docx_text=' '.join(e.text or '' for e in root.iter('{'+W+'}t'))
        assert not root.findall('.//{'+W+'}tbl'),'No se añaden tablas al formato anterior.'
        assert not any(name.startswith('word/media/') for name in z.namelist())
    assert all(display_refs(n['title'],n['id'][0]) in docx_text for n in nodes)
    assert data['authors'] in docx_text,'Faltan los alumnos en el DOCX.'
    assert not re.search('simulaci[oó]n|conversaci[oó]n',pdf_text,re.I)
    validate(data)
    summary={'roots':[r['node']['id'] for r in data['roots']],'display_numbering':'0, 1, 1.1, 1.1.1 por tarea','nodes':len(nodes),'plans':len(parents),'format_reference':data['original'],'original_sha256':data['original_sha256'],'original_unchanged':True,'pdf_content_verified':True,'docx_zip_xml_and_content_verified':True,'docx_external_render_verified':False,'layout':'Usuarios; ficha de tarea; árbol numerado; planes al final; evidencias. Sin portada, gráficos ni tablas.'}
    (SOURCE/'verificacion.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
