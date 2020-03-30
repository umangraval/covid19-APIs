#!/bin/bash
#Get servers list
set -f
string=$DEPLOY_SERVER
#Iterate servers for deploy and pull last commit
echo "Deploy project on server "    
ssh -o StrictHostKeyChecking=no covid19@${string} "cd api_management && git pull origin master"