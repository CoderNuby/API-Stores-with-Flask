FROM python:3.10.13
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
# CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]
CMD ["/bin/bash", "docker-entrypoint.sh"]