#!/usr/bin/env bash

. ./unimelb-comp90024-2023-grp-72-openrc.sh < secret.txt
ansible-playbook -i hosts instance.yml
