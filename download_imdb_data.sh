#!/bin/bash

# specify the dataset to download
DATASET=priy998/imdbsqlitedataset
# specify the database filename (not path)
DB_FILE=movie.sqlite
# set the data directory
DATA_DIR=./data

# resolve the full path of the database file
DB_FILE=$DATA_DIR/$DB_FILE
# resolve the full URL of the dataset
DB_URL=https://www.kaggle.com/api/v1/datasets/download/$DATASET
# resolve the full path of the temporary zip file
TMP_ZIP=$DATA_DIR/db.zip

# create the data directory if it doesn't exist
mkdir -p $DATA_DIR
# download the dataset if it doesn't exist
if [ ! -f $DB_FILE ]; then
  echo "Downloading IMDB data..."
  curl -L -o $TMP_ZIP $DB_URL

  echo "Unzipping IMDB data..."
  unzip $TMP_ZIP -d $DATA_DIR

  echo "Cleaning up..."
  rm -f $TMP_ZIP
else
  echo "IMDB data already downloaded."
fi
