# GreenSloth

In 2022, Elouen, the creator of GreenSloth, wrote his Bachelor's thesis about comparing the popular and simple steady-state Farquhar, von Caemmerer, and Berry Model (FvCB model) and a kinetic photosynthesis model. While searching for the other model, he searched various public sources for scientific literature and tried to recreate several models. During this time, he arrived at one conclusion: modeling, especially photosynthesis, aims to help others understand more of the essential process of life on Earth. However, the scientific community has not achieved a common way to share its models. This is where the idea of GreenSloth first came into play.

During his further experience with photosynthetic models, he found that this issue was common for experts and amateurs in modelling, which inspired his mind even more to find a solution. He wanted to create a resource that collects popular photosynthesis models and enables an easier summary and accessibility, especially for amateurs in the modelling field. 

With GreenSloth, Elouen hopes to facilitate researchers' access to the modelling world. He believes this is vital to understanding and coping with the complexity of photosynthesis. This website will enable even better scientific transparency.

## How to Use

GreenSloth's main idea is to be made available as a website, however you can also go through this Git Repo, as all the information the website extracts, is located here. Each model can be found in the [models](./models/) directory, with their respective summaries, figure recreation, and model as a package.

## How to Contribute

As this is an open-ource project, it is greatly appreciated if anyone wants to contribute a model to GreenSloth! To do so, you can post an [issue](https://github.com/ElouenCorvest/GreenSloth/issues), where the issue template **New Model** will tell you what to do. In brief, you can submit a proposition for a model to be added to GreenSloth, however you need to formulate it in the same manner as the others models are in this repo. This will eleviate a lot of time for the maintainers, and so they only need to concentrate in perfecting the version of the model for publishing.

## How to locally start the website

*This has been tested with Ubuntu 24.04.02 LTS*

### Installation

You first have to install [nvm](https://github.com/nvm-sh/nvm), the latest version of [NodeJS](https://nodejs.org/en/download), and nvm. Then clone this git repository and in the [website](./website/) directory you can find a bash-script to start hosting the website locally using [Vite](https://vite.dev/). This script will automatically install all the required nvm packages and start it.

```console
bash start.sh
```

***Note:** As the website automatically takes infromation from this git repo, however from the server database and not locally, you still need to have an internet connection to be able to use it.*