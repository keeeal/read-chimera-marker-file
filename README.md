# read-chimera-marker-file

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15062882.svg)](https://doi.org/10.5281/zenodo.15062882)
[![PAPER](https://img.shields.io/badge/PAPER-10.1038%2Fs41467--025--58514--x-blue)](https://doi.org/10.1038/s41467-025-58514-x)

This script does the following:

1. Parses a [Chimera marker file](https://www.cgl.ucsf.edu/chimera/docs/ContributedSoftware/volumepathtracer/volumepathtracer.html#markerfiles) and reads the coordinates into a numpy array.
2. Triangulates the coordinates in 3D (i.e. into tetrahedra)
3. Computes and prints the volume of the shape.
4. Computes and prints the surface area of the shape.

## Requirements

```sh
pip install -r requirements.txt
```

## Running

```sh
python read_cmm.py path/to/marker_file.cmm
```
