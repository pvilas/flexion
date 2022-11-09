# flexión

Pluralización y singularización de nombres en castellano (español) para python3.

El [proyecto original](https://github.com/bermi/Python-Inflector) de Bermí Ferrer es más genérico pero solo está disponible para python2. He sacado lo imprescindible para singularizar y pluralizar en python3 y en español.

## Uso en jinja

Tan solo es necesario añadir un filtro al entorno tal como

```python3
from flexion import singularizar, pluralizar
from jinja2 import Environment

env = Environment()
env.filters['pluralizar'] = pluralizar
env.filters['singularizar'] = singularizar

tmpl = env.from_string('"flash"|pluralizar')
assert tmpl.render() == 'flashes'
```
