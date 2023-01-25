# Frontend Development Framework

Short setup guide to get started.

## Features

- Svelte for fast and easy development

- Vite for instant preview in the browser

- Integration of SMUI for prebuilt components, styles, fonts and theming

- hash-based single page routing for maximum performance

- Support for SASS

## Get started

1. Install required tools:

   - [git](https://github.com/git-guides/install-git)

   - [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

   - [Visual Studio Code](https://code.visualstudio.com/download) (recommended)

2. Set up local repository for frontend development

```bash
# clone the repo
git clone https://github.com/mlinke-ai/kev.in.git

# cd into repo
cd kev.in

# change to the dev-svelte-frontend branch
git checkout remotes/origin/dev-frontend

# cd into frontend directory
cd frontend

# install required dependencies
npm install

# start the vite live server
npm run dev -- --open
```

> To open VS Code in the current directory, run `code .`



## Development Guidelines

#### Folder Structure

##### `src/lib/components`

Here is where to move new svelte components. If you have multiple components that depend on each other, consider creating a new folder for them inside this directory.

> Components should start with a capital letter in CamelCase style



##### `src/lib/functions`

If you have any piece of code that looks to big for a component or is used by many components, create a JavaScript file here.



##### `src/routes`

To create new pages for the website, use the `Example.svelte` file as a template.

To add your pages to the routing system, you have to add it to `index.js` inside of the routes directory.

If you need to add pages to the navigation bar, add them to `src/lib/components/Navbar/config.js`

> Every page has to be inside a  `<Page />` component. It provides smooth transitions when switching pages, enables you to set a title in the browser and protect pages from unauthorized access.
