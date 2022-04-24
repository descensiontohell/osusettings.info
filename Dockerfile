FROM python:3.9-bullseye
RUN mkdir quiz
RUN apt-get update
RUN apt-get -y install postgresql-client
WORKDIR ./quiz/
COPY . ./
EXPOSE 8080
ENV POSTGRES_DB dev_osu
ENV POSTGRES_USER elle_dev
ENV POSTGRES_PASSWORD dev_elle_pass
RUN pip3 install -r requirements.txt
CMD ["/quiz/setup.sh"]