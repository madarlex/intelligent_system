# intelligent_system

This repository contains the code and resources for the Intelligent System project, which is part of the Master's program at Bach Khoa University. The project focuses on developing and implementing intelligent systems using various AI and machine learning techniques.

## Getting Started

To get started with the project, clone the repository and follow the instructions provided in the respective directories.

## Prerequisites

- Python 3.11.9
- Required libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```sh
   cd intelligent_system
   ```
3. Create virtual env
   ```sh
   python -m venv .venv
   Window: .venv/Scripts/activate
   MacOs: source .venv/bin/activate
   ```
4. Install the required libraries:
   ```sh
   pip install -r requirements.txt
   ```
5. install postgres with pgAdmin 4 and create empty database
6. Go into is/settings.py, change this configuration into yours:
   DATABASES = {
   "default": {
   "ENGINE": "django.db.backends.postgresql",
   "NAME": "is", # Database name
   "USER": "postgres", # Username
   "PASSWORD": "31081989", # Password
   "HOST": "localhost", # Set to 'localhost' if the database is on the same machine
   "PORT": "5432", # Default PostgreSQL port
   }
   }
7. Run this for migration: python manage.py migrate
8. Run this for starting apps: python manage.py runserver

# Data Folder

## Dataset

1. Raw file: book_all_best_001_050.jl
2. Clean All Genres: genres.json => data for vectorizing (Read more about OneHotEncoding, Bag of words, There is code example and example result)
3. Book Data for Apps: book_data.json, books_data_with_recommendations.json (The finalize one is books_data_with_recommendations containing vectors and recommended_books)

## Jupyter Files

1. first_preprocessing_data.ipynb:

   - There are some methods I test: Vectorized, Embedded -> Please run and see the results
   - Testing KNN models
   - Get all unique genres and export into genres.json
   - Get 100 first records (100 books) then preprocessing it

2. add_recommending_books.ipynb:

   - Update 100 first book records with gern_vectors and recommending books

3. evaluate_result.ipynb
   - Add labels for dataset by using jaccard distance
   - Calculate Precision, Recall, Accuracy

# Report

1. Identification of stakeholders involved in the project and the potential benefits they can derive from it.
   (Look for this in https://docs.google.com/spreadsheets/d/17k9YMtYijzNDNHLohyPkmVNE9H2Fgma089dQRBNVlyY/edit?gid=334669440#gid=334669440, and add more)

2. Theory of the algorithms used
   (KNN)

3. System design.
   (https://drive.google.com/drive/my-drive?hl=vi)

4. Description of the dataset used and preprocessing steps.
   (Read Dataset and Jupter Files to do this)

5. Details of AI pipeline for data training and deployment
   (Read in books/admin.py)

6. Evaluation results with clear metrics provided.
   - Read code in file evaluate_result.ipynb
   - Use Jaccard distance to get 15 similar books as labels
   - Compare result of KNN with Jaccard, to calculate FP, TP, FN, TN
   - Then calculate precision, recall, accuracy
