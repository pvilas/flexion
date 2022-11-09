# flexion

Pluralizar y singularizar nombres en castellano (español) para python3.

El ![proyecto original](https://github.com/bermi/Python-Inflector) de Bermí Ferrer es más genérico y en python2. Sólo he sacado lo imprescindible para singularizar y pluralizar en python3 en español.

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
