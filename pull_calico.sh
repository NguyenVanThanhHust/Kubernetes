#!/bin/bash
DOCKER_REGISTRY="${1:-10.0.2.15:9004}"
lines=$(cat images-calico.txt)
COUNTER=0
ORIG_IMG=""
NEW_IMG=""

IGreen='\033[0;92m'
NC='\033[0m'

for l in $lines
do
    # new code
    let COUNTER++
    IMG=$l
    ORI_IMG=quay.io/${IMG}
    NEW_IMG=${DOCKER_REGISTRY}/${IMG}
    echo -e "${IGreen}$COUNTER: pushing $ORI_IMG to $NEW_IMG...${NC}" 
    docker pull -q $ORI_IMG
    docker tag $ORI_IMG $NEW_IMG
    docker push -q $NEW_IMG
    docker rmi $NEW_IMG $ORI_IMG
done
