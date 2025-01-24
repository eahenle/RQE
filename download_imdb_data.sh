#!/bin/bash
mkdir -p data
if [ ! -f ./data/db.zip ]; then
  echo "Downloading IMDB data..."
  curl -L -o ./data/db.zip\
  https://www.kaggle.com/api/v1/datasets/download/priy998/imdbsqlitedataset
else
  echo "IMDB data already downloaded."
fi
