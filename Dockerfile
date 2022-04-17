FROM python:3.9-bullseye
RUN mkdir quiz
RUN apt-get update
RUN apt-get -y install postgresql-client
WORKDIR ./quiz/
COPY . ./
ENV CONFIGPATH=/quiz/config.yml
EXPOSE 8080
ENV POSTGRES_DB dev_osu
ENV POSTGRES_USER elle_dev
ENV POSTGRES_PASSWORD dev_elle_pass
RUN python3 -m venv venv
RUN pip install -r requirements.txt
RUN alembic init alembic
COPY env.py ./alembic/
CMD ["/quiz/setup.sh"]