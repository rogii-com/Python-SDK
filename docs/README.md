## Документации Python SDK
Используется Sphinx + Sphinx AutoAPI.

### Как обновить артефакты документации
При добавлении нового файла с документацией объектов в `\src` необходимо добавить его руками в `\docs\_templates\autoapi\index.rst` и в `\docs\custom_stuff\python_doc_names.py`

Для запуска генерации локально:
```cmd
$ cd docs
$ python -m sphinx.cmd.build -M clean . ..\syntax_folder
$ python -m sphinx.cmd.build -b html . ..\syntax_folder
```
На выходе должна создаться\обновиться папка `syntax_folder` в корне `docs`.

Для копирования документации в докер и создания ссылки:
```
добавить .env в docs
добавить в hosts DOCS_DOMAIN из .env (127.0.0.1 python.solo.cloud)
docker-compose down --volumes
docker-compose build --no-cache
docker-compose up
```
На выходе должна создаться ссылка http://python.solo.cloud/autoapi/index.html.


### Полезные ссылки:
- https://www.sphinx-doc.org/
- https://sphinx-autoapi.readthedocs.io/
- https://bylr.info/articles/2022/05/10/api-doc-with-sphinx-autoapi/
- https://www.aahilm.com/blog/documenting-large-projects-with-sphinx
- https://sphinx-intro-tutorial.readthedocs.io/en/latest/
- https://software.belle2.org/sphinx/light-2205-abys/framework/doc/atend-doctools.html
