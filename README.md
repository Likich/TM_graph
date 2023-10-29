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

## Getting Started

To get started with TM_graph, follow these steps:

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/Likich/TM_graph.git
   ```

2. Install the required dependencies using pip. You can use the provided requirements.txt file:


```
pip install -r requirements.txt
```

3. Run the server by executing app.py:

```
python app.py
```


4. Open a web browser and access the server as per the provided instructions.

## Usage
1. Load your text data into the server using the web interface.
2. Choose your preferred topic modeling method (e.g., BERT or LDA) and the number of topics.
3. Analyze and visualize your text data based on the selected method.
4. Explore the topics in the graph.

## Multilingual Support
The server provides multilingual support. It can automatically detect the language of the input text and select the appropriate model (DeepPavlov for Russian or multilingual BERT for other languages).

## Code Structure
Make_graph_from_TM.py: Python script for creating the topic graph.<br>
TM.py: Contains the code for topic modeling and text analysis.<br>
app.py: The main server application script.<br>
Preprocess.py: Supports preprocessing for text analysis.<br>
lemmatizator_stem.py: Provides lemmatization support.<br>
static/ and templates/: Contain static files and HTML templates for the web 


## Author
Likich

Feel free to use and modify this server for your text analysis needs!

Note: Ensure that you have the required Python libraries installed before running the server. You may need to set up additional configurations or install additional resources based on your specific environment and requirements.
