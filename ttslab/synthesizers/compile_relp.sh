#!/bin/bash

cython --convert-range relp.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o relp.so relp.c
