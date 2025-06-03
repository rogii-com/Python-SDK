## Документации Python SDK
Используется Sphinx + Sphinx AutoAPI.

### Как обновить артефакты документации
При добавлении нового файла с документацией объектов в `\src` необходимо добавить его руками в `\docs\_templates\autoapi\index.rst` и в `\docs\custom_stuff\python_doc_names.py`

Документация создаётся в докере. Для создания:
```
добавить .env в docs
docker-compose build --no-cache
docker-compose up -d
```


### Полезные ссылки:
- https://www.sphinx-doc.org/
- https://sphinx-autoapi.readthedocs.io/
- https://bylr.info/articles/2022/05/10/api-doc-with-sphinx-autoapi/
- https://www.aahilm.com/blog/documenting-large-projects-with-sphinx
- https://sphinx-intro-tutorial.readthedocs.io/en/latest/
- https://software.belle2.org/sphinx/light-2205-abys/framework/doc/atend-doctools.html
