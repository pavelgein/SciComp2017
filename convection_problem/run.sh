#!/bin/bash

rm square_tri2.*.vtk
python simple.py heat_equation.py
python postproc.py square_tri2.*.vtk -b --wireframe --ffmpeg-options="-r 1" 

