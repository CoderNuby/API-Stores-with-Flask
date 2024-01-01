# API-Stores-with-Flask
REST API with Python Flask
# API-Stores-with-Flask

## How to run the Dockerfile locally
```
docker run -dp 5000:80 -w /app -v "${PWD}:/app" IMAGE_NAME sh -c "/bin/bash docker-entrypoint.sh"
```

## Remember create a .env file and create the following variable
```
DATABASE_URL=
```

## Run email
```
docker run -w /app rest-api-recording-email sh -c "rq worker -u rediss://red-cm8hfj8cmk4c73921vi0:FKFO7pToDW9OeEo2lpvH2hdGzMupS1io@oregon-redis.render.com:6379 emails"
```