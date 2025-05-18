#!/bin/bash
mkdir -p data
wget -O "data/original.csv" "https://hub.arcgis.com/api/v3/datasets/92842dceac234b9ca1a8266fcfd57de7_50/downloads/data?format=csv&spatialRefId=3857&where=1%3D1"
