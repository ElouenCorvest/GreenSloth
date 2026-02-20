# GreenSloth

In 2022, Elouen, the creator of GreenSloth, wrote his Bachelor's thesis about comparing the popular and simple steady-state Farquhar, von Caemmerer, and Berry Model (FvCB model) and a kinetic photosynthesis model. While searching for the other model, he searched various public sources for scientific literature and tried to recreate several models. During this time, he arrived at one conclusion: modeling, especially photosynthesis, aims to help others understand more of the essential process of life on Earth. However, the scientific community has not achieved a common way to share its models. This is where the idea of GreenSloth first came into play.

During his further experience with photosynthetic models, he found that this issue was common for experts and amateurs in modelling, which inspired his mind even more to find a solution. He wanted to create a resource that collects popular photosynthesis models and enables an easier summary and accessibility, especially for amateurs in the modelling field.

With GreenSloth, Elouen hopes to facilitate researchers' access to the modelling world. He believes this is vital to understanding and coping with the complexity of photosynthesis. This website will enable even better scientific transparency.

## What is this

All the models in the ecosystem of GreenSloth are found in this repository. Each model has its own directory, with a specific structure. The overarching name is the last Name of the first author and the date of publication of the model. This directory is best created using the [GreenSlothUtils](https://github.com/ElouenCorvest/GreenSlothUtils), as it will automatically use the name provided and insert it in the right places. Inside the model directory, you can find the following:

```bash
Corvest2000
├── figures
│   ├── demonstrations.ipynb
│   └── paper_figures.ipynb
├── model  
│   ├── __init__.py
│   ├── derived_quantities.py
│   ├── rates.py
│   └── basic_funcs.py
├── model_info
│   ├── comps.csv
│   ├── derived_comps.csv
│   ├── derived_params.csv
│   ├── params.csv
│   ├── rates.csv
│   ├── model_glosses
│   └── python_written
│       ├── gloss_to_python
│       └── model_to_latex
│ 
└── README_script.py
```

The `figures` directory includes the template Jupyter Notebooks for the recreations of the figures of the original paper and for demonstrations of the model.

The `model` directory includes the Python code of the model, which is seperated into different files for better readability. The `__init__.py` file is the main file, which imports the other files and contains the main function of the model. The `derived_quantities.py` file contains the derived quantities of the model, and the `rates.py` file contains the rates of the model. The `basic_funcs.py` file contains the basic functions of the model, which are used in the other files.

The `model_info` directory contains all the information about the model. The `.csv` files need to be filled with the information of the model, which is used in the README file. The comps and rates can be helped by the addition of the Glossary IDs. The `model_glosses` directory is filled after usage of the `GreenSlothUtils` to create the glossaries extracted from the model. The `python_written` directory contains pointers to be copied over to the README script, which are created by `GreenSlothUtils` from the model. 

The `README_script.py` file is the script that generates the README file of the model, which is the main file that is shown on the website. This script needs to be filled with the python variables, latex equations, summary, figure recreations, and demontrations of the model. The script is then run, which generates the README file.

## How to Contribute

To create a new model directory to be then included here, the best way is to follow the instructions in the [GreenSlothUtils](https://github.com/ElouenCorvest/GreenSlothUtils). This will automatically create the directory with the right structure and also fill in some of the files with the right information. After that, you can fill in the rest of the files with the information of the model. The README script is the most important file, as it generates the README file that is shown on the website. Therefore, it needs to be filled with care and attention to detail.

Once the model directory is created and everything is filled out, you can create a pull request to this repository, which whill then be reviewed and merged by the maintainers of this repository. If your model directory follows the same format as the other model directories, it can be accepted. if it does not follow the same format, it will be sent back to you with comments on what needs to be changed.

After acceptance, the maintainers will then add the model to the website, which can take some time.