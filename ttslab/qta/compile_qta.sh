#!/bin/bash

cython qta_sylcontour.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o qta_sylcontour.so qta_sylcontour.c
