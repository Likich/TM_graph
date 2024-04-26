# Topic Modeling Graph 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license](https://img.shields.io/github/license/SpirinEgor/gulag)](https://github.com/Likich/frog/blob/master/LICENSE)


## Overview

This repository contains a Python script for performing topic modeling on multilingual text data. It supports both Russian (using the DeepPavlov model) and other languages (using a multilingual BERT model). The code can automatically detect the language of the input text and choose the appropriate model for topic modeling.

## Features

- Supports text analysis using different topic modeling techniques.
- Multilingual support for both Russian and other languages.
- User-friendly web interface for easy interaction.
- Visualization of topics in a graph format.

## Getting Started with Docker

To get started with TM_graph using Docker, follow these steps:

1. Clone this repository to your local machine:


1. Clone this repository to your local machine:
   ```
   git clone https://github.com/Likich/TM_graph.git
   ```


2. Navigate to the directory containing the Dockerfile of the cloned repository:

```
cd TM_graph
```


3. Build the Docker image:

```
docker build -t tm_graph .
```


4. Run the container from the image:

```
docker run -d -p 5000:8080 --name tm_graph_container tm_graph
```


5. Open a web browser and access the server at `http://localhost:5000`.

Note: The above command assumes that the application runs on port 5000 within the container. Adjust the port mappings as necessary.

## Usage
1. Load your text data into the server using the web interface.
2. Choose your preferred topic modeling method (e.g., BERT or LDA) and the number of topics.
3. Analyze and visualize your text data based on the selected method.
4. Explore the topics in the graph.

## Multilingual Support
The server provides multilingual support. It can automatically detect the language of the input text and select the appropriate model (DeepPavlov for Russian or multilingual BERT for other languages).

## Code Structure
- `Make_graph_from_TM.py`: Python script for creating the topic graph.
- `TM.py`: Contains the code for topic modeling and text analysis.
- `app.py`: The main server application script.
- `Preprocess.py`: Supports preprocessing for text analysis.
- `lemmatizator_stem.py`: Provides lemmatization support.
- `static/` and `templates/`: Contain static files and HTML templates for the web interface.

## Docker Support
The application is fully Dockerized for easy setup and deployment. Follow the Docker instructions above to build and run the application inside a Docker container.

## Author
Likich

Feel free to use and modify this server for your text analysis needs!

Note: Ensure that Docker is installed and running on your machine before building and running the Docker container.


