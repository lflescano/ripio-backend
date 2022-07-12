# Set the base image to use to Ubuntu
FROM python:3.8.9-slim-buster

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/rp_kyc
ENV COLUMNS=80

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y build-essential autoconf libtool pkg-config
RUN apt-get install -y python3-dev
RUN apt-get install -y gcc
RUN apt-get install -y g++
RUN apt-get install -y git
RUN apt-get install -y curl
# RUN apt-get install -y locales
RUN apt-get install -y gettext

# Configure timezone and locale
# ENV TZ=Brazil/Acre
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir media static logs
VOLUME ["$DOCKYARD_SRVHOME/logs/"]

RUN mkdir $DOCKYARD_SRVPROJ
ADD requirements.txt $DOCKYARD_SRVPROJ/
WORKDIR $DOCKYARD_SRVPROJ
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn[gevent] requests[security]

ADD . $DOCKYARD_SRVPROJ

# Port to expose
EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN python manage.py compilemessages

# Copy entrypoint script into the image
COPY ./docker-entrypoint.sh /
RUN ["chmod", "+x", "/docker-entrypoint.sh"]

ENTRYPOINT ["/docker-entrypoint.sh"]

