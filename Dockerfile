FROM python:3.10.13
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN flask db upgrade
CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]