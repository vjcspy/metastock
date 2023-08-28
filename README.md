# Metastock

## Environment

Since **`poetry`** helps us manage environments, we no longer need to use Python virtualenv.

When creating a new project and using it with PyCharm, it will be fully integrated with the default mechanism. This will
create a new isolated environment in the `/.cache/pypoetry/` folder.

Lúc đó, chỉ còn trường hợp xảy ra là mình muốn thay đổi version của python. For more info,
visit [link](https://python-poetry.org/docs/managing-environments/)

```bash
pyenv install 3.9.8
pyenv local 3.9.8  # Activate Python 3.9 for the current project
poetry install
```

## Development

### PM2

In local development, we can use pm2 with command

```shell
pm2 start metastock/bin/start_consumer.py --log-date-format '' --interpreter=/home/wsl/.cache/pypoetry/virtualenvs/metastock-bq6tFdVW-py3.11/bin/python --instances 4 --max-memory-restart 1G -- --name=test_consumer
```

## Production

So far, the significant way is run by pm2. This is the best method that will not consume much time and resources
compared to building a Docker file or Kubernetes.

But, we need create a python file to call metastock module

Ex:

```shell
pm2 start metastock/start_consumer.py --log-date-format '' --interpreter=/home/wsl/.cache/pypoetry/virtualenvs/metastock-bq6tFdVW-py3.11/bin/python --instances 4 --max-memory-restart 1G -- --name=test_consumer
```

## Refer:

- Create a package https://typer.tiangolo.com/tutorial/package/