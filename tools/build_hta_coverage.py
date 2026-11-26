"""Relaciona el HTA general vigente con los escenarios ilustrativos del prototipo."""
from pathlib import Path
import json
from build_hta_v8 import flatten
BASE=Path(__file__).resolve().parent.parent

def main():
    path=BASE/'docs/hta-v8-coverage.json'
    prior=json.loads(path.read_text())
    scenario_ids=set(prior.get('scenario_node_ids',[n['id'] for n in prior['nodes']]))
    examples={n['id']:n for n in prior['nodes'] if n['id'] in scenario_ids}
    source=json.loads((BASE/'docs/hta_v8/contenido.json').read_text())
    current=[n for root in source['roots'] for n in flatten(root['node'])]
    rows=[]
    for node in current:
        key=node['id']
        while key not in examples and '.' in key:key=key.rsplit('.',1)[0]
        entry=examples.get(key,examples[node['id'][0]+'0'])
        rows.append({'id':node['id'],'kind':'plan' if node.get('children') else 'action','source_excerpt':node['title'],'behavior':entry['behavior'],'scenario':entry['scenario'],'selector':entry['selector'],'test':entry['test'],'basis_id':entry.get('basis_id',key),'coverage':'Ilustrativa; requiere contraste con la acción general'})
    plans=sum(n['kind']=='plan' for n in rows)
    catalog={'source':'HTA_correo_vocabulario_v8.pdf','source_json':'docs/hta_v8/contenido.json','plans':plans,'actions':len(rows)-plans,'scenario_node_ids':sorted(scenario_ids),'scope':'La presencia de un escenario o un identificador no acredita cobertura total de la tarea general ni aprendizaje. Los escenarios anteriores siguen disponibles; las nuevas acciones se relacionan con el apoyo del grupo correspondiente.','nodes':rows}
    path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    out=['# Correspondencia por nodo · HTA v8','',
         'Alumnos: '+source['authors'],'',
         'Fuente vigente: [HTA en PDF](../HTA_correo_vocabulario_v8.pdf) y [contenido estructurado](hta_v8/contenido.json). Cada título nombra una acción con un verbo inicial.','',
         f'El HTA contiene {plans} descomposiciones con plan y {len(rows)-plans} acciones terminales. El prototipo conserva los escenarios preparados de correo, consultas con retorno, revisión por fragmentos y repaso por contexto. La tabla indica el apoyo relacionado; no afirma que una demostración concreta cubra todos los casos de una tarea general.','',
         'Las pruebas de escenarios verifican comportamiento y persistencia, no adquisición de conocimiento ni aprobación docente. Las consultas externas son aportes sin verificación automática.','']
    for kind,title in [('plan','Nodos descompuestos'),('action','Acciones terminales')]:
        out+=['## '+title,'','| ID | Acción del HTA | Apoyo ilustrativo | Acceso | Escenario | Alcance |','|---|---|---|---|---|---|']
        for n in rows:
            if n['kind']!=kind:continue
            fields=[n['id'],n['source_excerpt'],n['behavior'],'`'+n['selector']+'`','`'+n['scenario']+'`',n['coverage']]
            out.append('| '+' | '.join(v.replace('|','\\|').replace('\n',' ') for v in fields)+' |')
        out.append('')
    (BASE/'docs/HTA_V8_COBERTURA.md').write_text('\n'.join(out).rstrip()+'\n')
    print('Correspondencia actual:',len(rows),'nodos; escenarios ilustrativos conservados:',len(scenario_ids))

if __name__=='__main__':main()
