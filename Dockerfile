FROM intersystemsdc/iris-community:latest as build

RUN pip install --upgrade pip
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip3 install -r requirements.txt
FROM build

USER root

WORKDIR /irisdev/app
RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /irisdev/app
USER ${ISC_PACKAGE_MGRUSER}

USER root
RUN apt-get update
USER ${ISC_PACKAGE_MGRUSER}


RUN \
	--mount=type=bind,src=src,dst=src \
	--mount=type=bind,src=iris.script,dst=/tmp/iris.script \
	--mount=type=bind,src=Installer.cls,dst=Installer.cls \
	iris start IRIS && \
	iris session IRIS < /tmp/iris.script && \
	iris stop iris quietly

ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD "SYS"
ENV IRISNAMESPACE "IRISAPP"