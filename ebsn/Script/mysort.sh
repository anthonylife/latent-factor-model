#!/bin/sh

## This bash script is responsible for one main duty: 1.Sort the lines accroding to the order os the specified field; ...
##
## Input:
##       $1-->number of the field;
##       $2-->data file name;
##       $3-->new file name;


# Specify the separator 
Sep=","

# Root path of the data
Root_Src="/home/zhangwei/Code/Git/latent-factor-model/ebsn/Meetup_network/"
Root_Des="/home/zhangwei/Code/Git/latent-factor-model/ebsn/Sta_Data/"
#Root=""

if [ $# -eq 3 ]; then
    field=$1
    data_file=$Root_Src$2
    new_file=$Root_Des$3
else
    echo "./script field datafile newfile"
    exit 0
fi

# Call awk cammander
#awk -F$Sep '{print $v1}' v1=$field $data_file | sort > $new_file  #Introduce how to pass parameter to Awk interpretor.

# Call sort command
sort -t, -k $field $data_file | uniq >  $new_file
