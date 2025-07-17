# Mighty Project Template

This repository contains everything to immediately start building your own Mighty project.

## Installation & Dependencies
We recommend using uv to create a new virtual environment:

```bash
pip install uv
uv venv --python 3.11
source .venv/bin/activate
```

And then installing the basic dependencies of Mighty like this:
```bash
make install
```

To add your own dependencies, simply put them in the 'pyproject.toml' file.

## Repository Content
This repository has:
- Basic runscripts for multiple seeds, HPO and parallel cluster evaluation
- The full set of Mighty config files
- A basic runscript & plotting setup

This way you should be able to implement your extensions and run your experiments immediately. Also check out the Makefile and adjust it to your needs. Currently it features install, format and check commands you can customize and extend.
