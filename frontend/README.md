# Frontend Development Framework

Short setup guide to get started.

## Features

- Svelte for fast and easy multi-page development

- Vite for instant preview in the browser

- Integration of SMUI for prebuilt components, styles and theming

- ~~Support for SASS~~ (TODO)

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

 

## Development

#### Folder Structure

1. Create new pages in **src/routes**
   
   The pages are svelte components that can be imported to `App.svelte` to be included in the website.

2. Create additional components in **src/lib/components**
   
   Components should be named like this: `ComponentName.svelte`


