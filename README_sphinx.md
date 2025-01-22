# Sphinx Documentation Generator


## Installation

Use the package manager to install sphinx and the read-the-docs theme.

```bash
poetry add --group dev sphinx, sphinx-rtd-theme
```

## Generating first documentation

1. Create docs folder where output will end up
2. in docs folder execute
     ```bash
    mkdir docs
    cd docs
    sphinx-quickstart
    ```
    Select `y` for separate source and build directories
    (creates files in the docs folder)

3. enter settings, project name etc.

4. In the docs folder execute one of the following (whether in sphinx-quickstart you 
chose to create separate directories for source and build or not):
    ```bash
    sphinx-apidoc -o  ./source ../<package_name>
    ```
    (creates even more files in the docs folder)

5. add "modules" (without quotes) to index.rst below contents followed by "Indices and tables", i.e.

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

6. adjust source/conf.py: in Project Information add
```python
import os
import sys

sys.path.insert(0, os.path.abspath('../../<package_name>/'))
```
7. adjust source/conf.py: in general configuration & options for HTML output:
```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    # "sphinx.ext.todo",
    # "sphinx.ext.viewcode",
]
```
8. adjust source/conf.py: in general configuration & options for HTML output:
```python
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
```
9. in docs execute
 ```bash
sphinx-build -b html ./source build/html
 ```

## Update documentation

1. update docstrings etc.
2. in docs folder execute step 9.

### If module structure changes
```bash
find source -name '*.rst' -not -name 'index.rst' -delete
```
```powershell
Get-ChildItem -Path . -Filter *.rst -Exclude index.rst -Recurse | Remove-Item -Force
```
Then repeat step 4.

## Testing documentation

In the docs folder, run
```bash
sphinx-build -b doctest ./source build/doctest
```
This will run the code examples in the documentation and check if they work as expected.
To check for syntax errors, use
```bash
sphinx-build -b html -W ./source build/html 
```