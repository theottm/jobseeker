#!/bin/bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
usr=usr
verbose=0

while getopts "h?vu:" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  verbose=1
        ;;
    u)  usr=$OPTARG
        ;;
    esac
done

shift $((OPTIND-1))

[ "${1:-}" = "--" ] && shift


time=$(date +"%y%m%d-%H%M")
dest="../../../data/$usr/$time"
mkdir -p $dest
cp -r output/done/* $dest
echo $dest
ls -lhsS $dest
while true; do
    read -p "Do you want to delete the original data?" yn
    case $yn in
        [Yy]* ) rm -f output/done/*; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
