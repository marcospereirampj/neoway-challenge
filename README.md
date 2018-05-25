# Data integration challenge

Welcome to Data Integration challenge.

## Original challenge

See [Data Integration challenge in NeowayLabs](https://github.com/NeowayLabs/data-integration-challenge).

## Stack 

- ElasticSearch - Version 6.2.4 (see [Install Elasticsearch with Debian Package](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html));
- Python - Version 3.6;
- Flask (and dependencies);
- Swagger.


## Project's Structure
```

| - api \
    \ - config
        \ - default.py
        \ - app_module.py
        \ - doc_module.py
    \ - controller 
        \ - custom
            \ - __init__.py
            \ - custom_api_error.py
        \ - swagger
            \ - data_api_controller_get.yml
            \ - data_api_controller_post.yml
            \ - data_api_controller_put.yml
        \ - tests
            \ - __init__.py
            \ - data_api_controller_test.py
        \ - __init__.py
        \ - data_api_controller.py
    \ - integration
        \ - tests
            \ - data_process_test.py
        \ - __init__.py
        \ - data_process.py
    \ - __init__.py
    \ - requeriments.txt
    \ - run.py
| - README.md
| - Makefile

```

## Install Requirements (Python Libraries)

```
   pip install -r api/requirements.txt
```


## Running API

```
    cd api/
    python run.py
```

## Running Tests


```
   python -m unittest discover -s api -p "*_test.py"
```

## Design

* DataProcess: class responsible to process the CSV file. It's responsible for load initial data in the database,
update and retrieve data.

* DataApiController: class responsible for API. Process HTTP requests. 

## Strategy

1. When you insert a new object into the database, a hash code (SHA256) is created 
from the data (name and addresszip fields). This hash code will serve to identify the object on the future.

2. To update an object, the hash code (from name and addresszip fields) is used. 

3. To retrieve objects, it's possible to use 'search' (query string) for filter objects.


## Examples

* POST
```
curl -X POST \
  http://0.0.0.0:5000/data-integration \
  -H 'content-type: multipart/form-data' \
  -F file=@./data/q1_catalog.csv
```

* PUT 
```
curl -X PUT \
  http://0.0.0.0:5000/data-integration \
  -H 'content-type: multipart/form-data' \
  -F file=@data/q2_clientData.csv
```

* GET 

```
curl -X GET \
  http://0.0.0.0:5000/data-integration \
  -H 'Content-Type: application/json'
```

* GET (with search for name='redbox') 

```
curl -X GET \
  'http://0.0.0.0:5000/data-integration?name=redbox' \
  -H 'Content-Type: application/json'
```

* GET (with search for name='group' and zip='78229') 

```
curl -X GET \
  'http://0.0.0.0:5000/data-integration?name=group&zip=78229' \
  -H 'Content-Type: application/json'
```