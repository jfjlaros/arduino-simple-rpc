from importlib.metadata import metadata


_package_metadata = metadata('arduino_simple_rpc')

html_theme = 'sphinx_rtd_theme'
author = _package_metadata['Author']
copyright = '2019, {}'.format(author)
project = _package_metadata['Name']
release = _package_metadata['Version']

autoclass_content = 'both'
extensions = [
  'sphinx.ext.autodoc', 'sphinx_autodoc_typehints', 'sphinxarg.ext']
master_doc = 'index'
