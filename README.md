# This Repository was created to house all applicable files, notebooks, and modules necessary to complete my Natural Language Processing project.

# _GitHub Program Language Predictor Project_

![](https://clipart.info/images/ccovers/1499794873github-logo-png.png)




- This project uses a various classification models to predict what programming language a GitHub repository is given the text of the README file.
- In this README I will :
    * Explain what the project is and goals I attempted to reach. 
    * Explain how to reproduce my work. 
    * Contain notes from project planning.

## Goals
- This project aims to predict what programming language a repository is, given the text of the README file  This will be a approached as NLP problem and will try to use various classification models to find the best accuracy score.

## Project Planning
- Trello Board Link:
  - https://trello.com/b/C5zkPkLB/nlp-project

**Deliverables:**
1. README.md file containing overall project information, how to reproduce work, and notes from project planning.
2. Jupyter Notebook Report detailing the pipeline process.
3. One or two google slides suitable for a general audience that summarize your findings. IncludING a well-labelled visualization in my slides.

## Key Findings 
* Majority of the Repositories were in the Python programming language.
* Many of the same words were spread across all the top 5 programming languages making for a unreliable prediction.
* Logistic Regression was my best performing model over all, however I was hoping for a more reliable accuracy.




## Setup this project
* Dependencies
    1. python
    2. pandas
    3. scipy
    4. sklearn
    5. numpy
    6. matplotlib.pyplot
    7. seaborn
    8. wordcloud
    9. requests
* Steps to recreate
    1. Clone this repository
    3. Open `nlp_project_finale.ipynb` and run the cells


## Data Dictionary 

#### Target
Name | Description | Type
:---: | :---: | :---:
language| Primary repository programming language | object

#### Features
Name | Description | Type
:---: | :---: | :---:
repo |  Repository url | object
readme_contents  |  Text found in repository README files | object
