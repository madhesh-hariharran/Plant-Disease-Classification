# Plant Disease Classification

## Overview
This repository contains all the necessary components for training and deploying a plant disease classification model. The dataset used is a custom modified version of the PlantVillage dataset.

## Backend

### Model
The trained model files are stored in this directory. The following files are included:

- `variables`: This file contains information related to model variables.
- `fingerprint.pb`: The fingerprint protocol buffer file.
- `keras_metadata.pb`: The keras metadata protocol buffer file.
- `saved_model.pb`: The saved model protocol buffer file.

### Output
This directory contains output files generated during or after model training.

### Training Code
The following Jupyter notebooks are essential for building and training the plant disease classificatiom model:

1. `Plant_Disease_Model_Building.ipynb`: This notebook focuses on constructing the disease classification model.
2. `Plant_Disease_Training.ipynb`: Use this notebook to train the model. After training, the model is saved as `saved_model.pb` in the 'model' directory.

### Dataset
Includes a custom modified version of the PlantVillage dataset tailored for this specific plant disease classification task.

## Frontend
Holds all assets and code necessary for setting up the webpage frontend that interacts with our trained model.
