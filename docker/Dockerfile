FROM ubuntu:16.04

MAINTAINER DIDARUL "Didarul"

RUN apt -y update &&\
    apt -y install python3 python3-pip &&\
    apt -y install libgtk2.0-dev 


RUN python3 -m pip install --upgrade pip

ADD ./python_requirements.txt /
RUN python3 -m pip install -r python_requirements.txt

# ADD ../scripts /
ENTRYPOINT ["bash","/scripts/start_flask.sh"]


