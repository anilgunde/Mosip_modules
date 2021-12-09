#!/bin/sh
# Installs Resident service
NS=resident
CHART_VERSION=1.2.0

echo Create namespace
kubectl create ns $NS 

echo Istio label 
kubectl label ns $NS istio-injection=enabled --overwrite
helm repo update

echo Copy configmaps
./copy_cm.sh

echo Installing Resident
helm -n $NS install resident mosip/resident --version $CHART_VERSION