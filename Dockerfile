FROM ubuntu

# Non-root user
ARG USERNAME

# ENV TZ=Europe/Kiev
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update &&\
    apt-get install -y --no-install-recommends curl git sudo &&\
    useradd --create-home --shell /bin/bash $USERNAME &&\
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME &&\
    chmod 0440 /etc/sudoers.d/$USERNAME &&\
    rm -rf /var/lib/apt/lists/*

RUN apt-get -qq update && apt-get -y --no-install-recommends install wget python3 &&\
    apt-get -y install python3-pip

USER ${USERNAME}


COPY . /home/${USERNAME}/

RUN cd /home/${USERNAME}/ && pip install -r requirements.txt 

WORKDIR /home/${USERNAME}/

