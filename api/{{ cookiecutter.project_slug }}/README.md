# {{ cookiecutter.project_slug }}
## First Setup
```bash
    ln -sf ${PWD}/.githooks/* ${PWD}/.git/hooks/
```
## Install
```bash
  poetry install
```
## Run
```bash
  poetry run python -m app
```
## Env Config
```.env
  APP_PORT=<APP_PORT>
  LOG_JSON_FORMAT=<LOG_JSON_FORMAT>
  LOG_LEVEL=<LOG_LEVEL>

```