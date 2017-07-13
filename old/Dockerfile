# Copyright 2014-16 Joseph Wolff & eRacks Systems

#FROM phusion/baseimage
# based on dockerfile/ubuntu:
#FROM dockerfile/supervisor

#FROM ubuntu:xenial
FROM ubuntu:trusty

MAINTAINER Joseph Wolff, joe@eracks.com

ENV TERM linux

#RUN locale-gen en_US.UTF-8
#RUN update-locale LANG=en_US.UTF-8


RUN apt-get -y update && apt-get -y install wget git  # curl mc
RUN wget --version

RUN wget -O - https://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -
RUN echo deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest trusty main >/etc/apt/sources.list.d/salt.list
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install salt-minion
RUN python --version
RUN salt-call --version

#RUN git clone git@github.com:jowolf/eracks11.git
#RUN git checkout brahms

#VOLUME /eracks11
#RUN cd /eracks11
#RUN ls -l eracks
#RUN ls -l conf
#RUN cd conf
#RUN pwd

RUN ls -l
RUN ls -l /home
#RUN ls -l /vagrant/


#RUN apt-get update && apt-get upgrade -y
# -o DPkg::Options::=--force-confold

#VOLUME ['/etc/salt/minion.d', ]
#ADD etc/salt/minion.d/minion.conf /etc/salt/minion.d/
#ADD etc/salt/pki/ /etc/salt/pki/



#EXPOSE 22 2222 80 8080 8000 443

#CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
#CMD ['/bin/bash']
#CMD ['/usr/local/bin/bash']
#nope CMD ['ls /bin/']
#CMD ['/bin/sh']
