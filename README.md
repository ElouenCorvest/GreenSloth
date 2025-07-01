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

You first have to install [nvm](https://github.com/nvm-sh/nvm) and the latest version of [NodeJS](https://nodejs.org/en/download) and npm. Then clone this git repository and in the [website](./website/) directory you can find a bash-script to start hosting the website locally using [Vite](https://vite.dev/). This script will automatically install all the required npm packages and start it.

```console
bash startlocal.sh
```

***Note:** As the website automatically takes infromation from this git repo, however from the server database and not locally, you still need to have an internet connection to be able to use it.*

## How to for the devs

### Easy way

If you have rights to access the WebDAV of the website and want to add to it please use `vite build`, by running the following `bash` script.

```console
bash startpublic.sh <optional/out/path>
```

This script has an optional argument that is the `outDir`, where the build will be generated. If you leave it blank, it will create a new directory called `public` inside the `website` directory. If you give it a path, it will build it there. Therefore, if you already have mounted the WebDAV to your file system you can automatically let it build in there and dont have to manually move the content (**and only the content**) of the `public` directory.

If the script already finds a directory called `public` it will remove it before adding the new one, as this has produced an issue in the past. But you will be prompted to agree before it does it.

### Not so Easy Way

If you do not wish to use the bash script, you may build it yourself. To do that, run the following:

```console
npm run build
```

This will create a `public` directory, which its contents can be uploaded to the website's WebDAV. To get access to the WebDAV, please ask the owner of this GitHub. Please remember to **only** copy the contents of the `public` directory.

If you already have access to the WebDAV and have also mounted it to your file system, you may also wish to directly build into it. You can also use the `vite build` script, however you need to specify a new `outDir`. You can do that with the following, please take care of the extra `--` in the middle, as these are essential and are not a typo.

```console
npm run build -- --outDir <path/to/WebDAV>
```

If you have already run the empty script and therefore created a public directory here, you may encounter an error when wanting to choose a new `outDir`. To fix this, you must first delete the `public` folder beforehand.