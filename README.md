#Fabrique

Доп задания:
простые тесты, docker-compose, swagger, обработка ошибок сервиса, временные рамки для отправки, admin интерфейс

## Installation with docker-compose


1. Clone repository
```
git clone git@gitlab.com:tests8273328/Fabrique.git
```
2. Go into project dir
3. In file .evn: ```TOKEN = '<your token>'```
4. Launch 
``` 
sudo docker-compose up -d
 ```
5. Stop 
```
sudo docker-compose stop
```


***
```http://0.0.0.0:8000/api/```

```http://0.0.0.0:8000/api/clients/```

```http://0.0.0.0:8000/api/mailings/```

```http://0.0.0.0:8000/api/mailings/fullinfo/```

```http://0.0.0.0:8000/api/mailings/<pk>/info/```

```http://0.0.0.0:8000/api/messages/```

```http://0.0.0.0:8000/admin/```

```http://0.0.0.0:8000/docs/``` - docs

```http://0.0.0.0:5555``` - celery flower

***
