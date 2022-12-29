# Frontend Development Framework

Short setup guide to get started.

## Features

- Svelte for fast and easy development

- Vite for instant preview in the browser

- Integration of SMUI for prebuilt components, styles and theming

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

1. Create new pages like this: **src/routes/PageName.svelte**
   
   To add new pages to the routing system:
   
   1. Add your page definitions to `src/routes/routes/index.js`
   2. Copy Example page template from `src/routes/Example.svelte`
   3. Change `<Page Title>` to desired title
   4. Place all html content inside the `Page` component, no body tag required
   5. To add a page to navigation bar add it to `src/lib/components/Navbar/config.js`
      
      in the json data under `default -> links` 
      
      or for admin only pages `admin -> links`
   
   

2. Create additional components like this: **src/lib/components/ComponentName.svelte**
   
   
