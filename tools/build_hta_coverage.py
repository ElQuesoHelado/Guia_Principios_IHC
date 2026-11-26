"""Publica la correspondencia por nodo desde el catálogo de cobertura v8."""
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent.parent

def main():
    catalog=json.loads((BASE/'docs/hta-v8-coverage.json').read_text())
    rows=['# Correspondencia por nodo · HTA v8','',
          'Fuente: [HTA_correo_vocabulario_v8.pdf](../HTA_correo_vocabulario_v8.pdf), sin modificaciones. Esta tabla usa extractos breves como rótulos; el texto completo y los planes están en la fuente.', '',
          'Los 29 planes y las 80 hojas se relacionan con un escenario ejecutable del mock. No se crea un control por cada identificador. Las consultas externas se registran sin fingir conexiones ni verificación; los ejemplos internos son preparados. La cobertura técnica no certifica aprendizaje ni aprobación docente.', '',
          'Prueba: [test_hta_complete.py](../tools/test_hta_complete.py). El test ejecuta interacciones y condiciones y comprueba que no falte ningún identificador del [catálogo](hta-v8-coverage.json).', '']
    for kind,title in [('plan','Planes y nodos descompuestos'),('action','Hojas: acciones y decisiones')]:
        rows += ['## '+title,'','| ID | Extracto identificador de la fuente | Apoyo / comportamiento | Selector de acceso | Escenario de prueba |','|---|---|---|---|---|']
        for node in catalog['nodes']:
            if node['kind']!=kind:continue
            values=[node['id'],node['source_excerpt'],node['behavior'],'`'+node['selector']+'`','`'+node['scenario']+'`']
            rows.append('| '+' | '.join(str(v).replace('|','\\|').replace('\n',' ') for v in values)+' |')
        rows.append('')
    (BASE/'docs/HTA_V8_COBERTURA.md').write_text('\n'.join(rows))
    print('Matriz publicada:',catalog['plans'],'planes y',catalog['actions'],'hojas.')

if __name__=='__main__':main()
