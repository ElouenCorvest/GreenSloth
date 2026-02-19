# GreenSloth - Website

In 2022, Elouen, the creator of GreenSloth, wrote his Bachelor's thesis about comparing the popular and simple steady-state Farquhar, von Caemmerer, and Berry Model (FvCB model) and a kinetic photosynthesis model. While searching for the other model, he searched various public sources for scientific literature and tried to recreate several models. During this time, he arrived at one conclusion: modeling, especially photosynthesis, aims to help others understand more of the essential process of life on Earth. However, the scientific community has not achieved a common way to share its models. This is where the idea of GreenSloth first came into play.

During his further experience with photosynthetic models, he found that this issue was common for experts and amateurs in modelling, which inspired his mind even more to find a solution. He wanted to create a resource that collects popular photosynthesis models and enables an easier summary and accessibility, especially for amateurs in the modelling field.

With GreenSloth, Elouen hopes to facilitate researchers' access to the modelling world. He believes this is vital to understanding and coping with the complexity of photosynthesis. This website will enable even better scientific transparency.

## What is this

This branch of the GreenSloth repository is the code for the website, which is built using [Vite](https://vite.dev/) and plain HTML, CSS, and JavaScript. The website is hosted on an official RWTH Aachen site, and only the contact persons have access to upload the content to the WebDAV. However, the content of the website can be edited here, for later upload.

## How to Add Models

Only models that have a full directory in the [models](https://github.com/ElouenCorvest/GreenSloth/tree/main/models) directory of the main branch can be added to the website. To add a model, you need to to two things:

1) Fill the [models.json](./src/js/models.json) file with the new model, following the same format as the other models. You can also add new tags to the model, also new categories, if needed. Please make sure to also add the DOI of the paper, as this is important for the website and also for the users to find the original paper.

```json
"Matuszynska2016": {
        "DOI": "https://doi.org/10.1016/j.bbabio.2016.09.003",
        "tags": {
            "Part of Photosynthesis": ["PSII", "ATP Synthase", "Cytochrome b6f", "PQ Cycle"],
            "Demonstrations": ["Day Simulation", "PAM Simulation", "Photosynthesis MCA", "Fitting of NPQ"]
        }
    },
```

2) Duplicate any of the model HTML files in the [models](./src/html/models/) directory and rename it to the name of the new model.

If the model directory on the main branch is correct, everything will be filled in correctly on the website, as the website automatically takes the information from the GitHub repository. 

# How to add more stuff to the website

This is where it gets complicated. As models need to be easily uploadable, the website is built in a way that it automatically takes the information from the GitHub repository. This means that most pages are created automatically, by JS. So if you wish to add more parts to the website, like new sections to models, or new comparisions, you will need to edit the JS code. Keep in mind that the website should be hands free when adding new models, so the JS code should be written in a way that it automatically takes the information from the GitHub repository, without the need to edit the code for each new model.

## How to locally start the website

*This has been tested with Ubuntu 24.04.02 LTS*

You need to first install [npm](https://www.npmjs.com/) and [Node.js](https://nodejs.org/en/), which are required to run the website locally. After that, you can run the following command in the terminal, in the root directory of the website:

```console
npm install
npm run dev -- --open
```

## How to build for the website

To build the website for upload, you can run the following command in the terminal, in the root directory of the website:

```bash
npm install
npm run build
```

After building it is recommended to preview the build, so no mistakes are uploaded to the WebDAV. You can run the following command in the terminal, in the root directory of the website after building:

```bash
npm run preview
```