# Metastock

## Environment

Since **`poetry`** helps us manage environments, we no longer need to use Python virtualenv.

When creating a new project and using it with PyCharm, it will be fully integrated with the default mechanism. This will create a new isolated environment in the `/.cache/pypoetry/` folder.

Lúc đó, chỉ còn trường hợp xảy ra là mình muốn thay đổi version của python. For more info, visit [link](https://python-poetry.org/docs/managing-environments/)

```bash
pyenv install 3.9.8
pyenv local 3.9.8  # Activate Python 3.9 for the current project
poetry install
```

## Refer:
- Create a package https://typer.tiangolo.com/tutorial/package/