from subprocess import call

# NOTE: Add sphinx_autodoc_typehints when ReadTheDocs supports it.
call('pip install six ..', shell=True)

from simple_rpc import _get_metadata


author = _get_metadata('Author')
copyright = _get_metadata('Author')
project = _get_metadata('Name')
release = _get_metadata('Version')

autoclass_content = 'both'
# NOTE: Add sphinx_autodoc_typehints when ReadTheDocs supports it.
extensions = ['sphinx.ext.autodoc']
master_doc = 'index'
