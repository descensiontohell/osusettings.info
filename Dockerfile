FROM python:3.9-bullseye
RUN mkdir osusettings
RUN apt-get update
RUN apt-get -y install postgresql-client
WORKDIR ./osusettings/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . ./
EXPOSE 8080
ENV IS_IN_DOCKER Yes
ENV POSTGRES_DB dev_osu
ENV POSTGRES_USER elle_dev
ENV POSTGRES_PASSWORD dev_elle_pass
ENTRYPOINT ["/osusettings/setup.sh"]
