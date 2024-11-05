# Project Structure

## Overview

This project contains several directories and files, organized to streamline the development process and make it easier to navigate the codebase. This document provides a general overview of the structure and purpose of each key component. Additionally, note that the `data/` and `model/` directories are mounted to the Docker container for seamless integration during development.

## Directory Structure

### `data/` directory

This directory is used to store the data files needed for the project. The content might vary based on the stage of the project (e.g., training, validation, or testing data). The `data/` directory is mounted to the Docker container, allowing the containerized environment to access the data seamlessly.

### `doc/` directory

Contains the project documentation in Markdown format. Below are the key files:

* `baseline_model.md`: Details regarding the baseline model used in this project.
* `data_acquisition.md`: Information on how data is sourced and preprocessed.
* `docker_guide.md`: A guide on setting up and using Docker for this project.
* `evaluation_criteria.md`: Documentation on the metrics and criteria used to evaluate the model's performance.
* `project_structure.md`: The document explaining the project's structure (this file).

### `model/` directory

The `model/` directory contains the code, files, and assets related to the machine learning model. This folder is also mounted to the Docker container. The model's weights, configuration files, and other assets used during training and inference may reside here.

### `notebooks/` directory

Jupyter Notebooks used for interactive code development, analysis, and experimentation. Notebooks included:

* `baseline_model.ipynb`: Implementation and (some) analysis of the baseline segmentation model.
* `data_preparation.ipynb`: Steps and code for preparing the dataset.
* `dataset_analysis.ipynb`: Exploratory data analysis to better understand the dataset's characteristics.
* `download_dataset.ipynb`: Notebook containing the original code to download the dataset.
* `initial_model.ipynb`: Notebook for working on the ensemble model implementation using the [MONAI](https://monai.io/) framework.

### `src/` directory

This is the core source code directory for the project. The files in this directory are essential for data management and model execution. The key components include:

* `model/`: Directory containing code related to model implementation.
  * `__init__.py`: This file makes the `src/model/` directory a package.
  * `common.py`: Provides a wrapper class for all `nn.Module` models, encapsulating shared functionality.
  * `ensemble.py`: Implements a class for generating ensemble predictions by aggregating outputs from multiple models.
* `__init__.py`: This file makes the `src/` directory a Python package.
* `dataloader.py`: Contains the code responsible for loading the dataset into memory, preprocessing it, and preparing it for model training and evaluation.
* `download_dataset.py`: Script to download the dataset from a specified source and organize it into the appropriate directory structure.
* `main.py`: Some sample code to make sure that the container works.
* `metrics.py`: Custom metric implementations based on criteria in the [`evaluation_criteria.md`](evaluation_criteria.md) document. Initially used for evaluating the baseline model, but later replaced by metrics in the MONAI framework.
* `util.py`: Contains utility functions, such as checking if an integer is a power of two, to support various tasks across the project.

### Root directory

The root directory contains several configuration files and scripts that are essential for setting up, running, and managing the project environment. These files primarily handle Docker containerization, dependency management, and project documentation. Below is a breakdown of each file:

* `build_and_run.sh`: Shell script to build and run the Docker container.
* `build.sh`: Script used for building the Docker container.
* `Dockerfile`: The Docker configuration file, outlining the container's environment and dependencies.
* `entrypoint.sh`: Entry point script for the Docker container.
* `pyproject.toml`: Configuration file for [Poetry](https://python-poetry.org/).
* `README.md`: An overview of the project, with links to all other documentations.
* `requirements.txt`: List of Python dependencies required for the project.
* `run.sh`: Script to start up the built Docker image.
