#!/usr/bin/env bash

R=${REPO:-"vasartori/deploy"}
V=${VERSION:-"latest"}
VENV=${VENV_PATH:-"/tmp/deploy-venv"}

usage(){
    echo "REPO=repository... VERSION=latest ${0} <OPTIONS>"
    echo "REPO = Registry to push the image [OPTIONAL]"
    echo "VERSION = Docker Image Tag [OPTIONAL]"
    echo "VENV_PATH = Path to install virtualenv"
    echo "Options: "
    echo "  tests - Execute unit tests"
    echo "  build - Build the docker image"
    echo "  push - Push the docker image to registry"
    echo "  create-venv - Create python virtualenv and install required deps"
    echo "  all - Run a test, if pass, make a build, and push"
    exit 0
}

tests(){
    echo "Running unit tests...."
    python -m unittest tests/unit_test.py

    if [ $? -ne 0 ]; then
        exit 1
    fi
}

build(){
    docker build -t ${R}:${V} .
}

push(){
    docker push ${R}:${V}
    if [ $? -ne 0 ]; then
        echo "Did you login on registry? Try: docker login ${R}"
        exit 1
    fi

}

activate_venv(){
    if [ -e ${VENV}/bin/activate ]; then
        source ${VENV}/bin/activate
    else
        create_environment
    fi
    source ${VENV}/bin/activate
}

create_environment(){
    if [ $(uname) == "Linux" ]; then
        sudo apt-get install python3-venv || sudo dnf install python3-virtualenv
        if [ $? -ne 0 ]; then
            echo "Apt-get failed or missing. You need install manually python3 virtualenv"
            exit 1
        fi
    elif [ $(uname) == "Darwin" ]; then
        python3 -m pip install virtualenv
        if [ $? -ne 0 ]; then
            echo "python3 pip install virtualenv failed!"
        fi
    fi
    python3 -m venv ${VENV}
    source ${VENV}/bin/activate
    pip install wheel -r requirements.txt 2>&1 > /dev/null
    echo "Virtualenv installed on $VENV"
}

case $1 in
    tests) activate_venv; tests ;;
    build) build ;;
    push) push ;;
    create-venv) create_environment ;;
    all) activate_venv; tests; build; push ;;
    help) usage ;;
    *) usage ;;
esac
