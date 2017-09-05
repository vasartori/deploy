#!/usr/bin/env bash

R=${REPO:-"vasartori/deploy"}
V=${VERSION:-"latest"}

usage(){
    echo "REPO=repository... VERSION=latest $0 <OPTIONS>"
    echo "REPO = Registry to push the image [OPTIONAL]"
    echo "VERSION = Docker Image Tag [OPTIONAL]"
    echo "Options: "
    echo "  tests - Execute unit tests"
    echo "  build - Build the docker image"
    echo "  push - Push the docker image to registry"
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
    docker build -t $R:$V .
}

push(){
    docker push $R:$V
    if [ $? -ne 0 ]; then
        echo "Did you login on registry? Try: docker login $R"
        exit 1
    fi

}


case $1 in
    tests) tests ;;
    build) build ;;
    push) push ;;
    all) tests;build;push ;;
    help) usage ;;
    *) usage ;;
esac
