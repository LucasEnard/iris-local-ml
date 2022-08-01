FROM intersystemsdc/iris-community:latest as build

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

FROM build

USER root
# ADD https://www.cyberciti.biz/files/sticker/sticker_book.pdf /output.pdf
# ADD /output.pdf /irisdev/app/model/output.pdf

# RUN apt-get update
# RUN apt-get install -y curl
# RUN curl https://the-eye.eu/public/AI/GPT-J-6B/step_383500_slim.tar.zstd \
#   | tar -xjC --use-compress-program=unzstd /irisdev/app/model/ step_383500_slim.tar.zstd \
#   && make -C /irisdev/app/model/ step_383500_slim.tar.zstd

WORKDIR /irisdev/app
RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /irisdev/app
USER ${ISC_PACKAGE_MGRUSER}


COPY Installer.cls .
COPY src src
COPY iris.script /tmp/iris.script

USER root
RUN apt-get update
USER ${ISC_PACKAGE_MGRUSER}

RUN iris start IRIS \
	&& iris session IRIS < /tmp/iris.script \
    && iris stop IRIS quietly

ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD "SYS"
ENV IRISNAMESPACE "IRISAPP"