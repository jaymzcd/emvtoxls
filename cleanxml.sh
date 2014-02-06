#!/bin/bash

# So far it seems EMVs 'XML' is invalid not doing clean up on entities
# like ampersands in particular, convert in place if the parser is unable
# to read the input file as valid. We can't skip as we need to use
# iterparse for large file perfomance

sed -i 's/&/&amp;/g' $1;

