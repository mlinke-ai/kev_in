import { ThemeInterface } from "./types";

export function setTheme(theme: ThemeInterface, darkMode?: boolean) {
  if (darkMode) {
    for (const variable in theme.dark) {
      if (theme.dark[variable]) {
        document.documentElement.style.setProperty(
          `--${variable}`,
          theme.dark[variable]
        );
        console.log(`--${variable}`, theme.dark[variable]);
      }
    }
  } else {
    for (const variable in theme.light) {
      if (theme.light[variable]) {
        document.documentElement.style.setProperty(
          `--${variable}`,
          theme.light[variable]
        );
      }
    }
  }
}

export let themes: Array<ThemeInterface> = [
  {
    name: "TU",
    light: {
      "mdc-theme-primary": "#005f50",
      "mdc-theme-secondary": "#D79922",
      "mdc-theme-background": "#fff",
      "mdc-theme-surface": "#eee",
      "mdc-theme-on-primary": null,
      "mdc-theme-on-secondary": null,
      "mdc-theme-on-surface": null,
      "console-color": "#7cfc00",
      "console-background": "#000",
    },
    dark: {
      "mdc-theme-primary": "#005f50",
      "mdc-theme-secondary": "#D79922",
      "mdc-theme-background": "#003931",
      "mdc-theme-surface": "#001a16",
      "mdc-theme-on-primary": null,
      "mdc-theme-on-secondary": null,
      "mdc-theme-on-surface": null,
      "console-color": "#7cfc00",
      "console-background": "#000",
    },
  },
  {
    name: "DeepOcean",
    light: {
      "mdc-theme-primary": "#005f50",
      "mdc-theme-secondary": "#D79922",
      "mdc-theme-background": "#fff",
      "mdc-theme-surface": "#eee",
      "mdc-theme-on-primary": null,
      "mdc-theme-on-secondary": null,
      "mdc-theme-on-surface": null,
      "console-color": "#7cfc00",
      "console-background": "#000",
    },
    dark: {
      "mdc-theme-primary": "#1976d2",
      "mdc-theme-secondary": "#D79922",
      "mdc-theme-background": "#070c30",
      "mdc-theme-surface": "#010417",
      "mdc-theme-on-primary": null,
      "mdc-theme-on-secondary": null,
      "mdc-theme-on-surface": null,
      "console-color": "#7cfc00",
      "console-background": "#000",
    },
  },
];
