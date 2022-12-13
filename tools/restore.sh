#!/bin/bash -x
FROM=$1
TO=$2
cp $FROM/*.py $FROM/*.json $FROM/token $TO/
sync