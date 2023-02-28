import { ThemeInterface } from "./types";

export function getTheme() {
  return (localStorage.getItem("preferredTheme") as unknown as number)
}

export function setTheme(index: number, darkMode?: boolean) {
  let theme: ThemeInterface = themes[index]
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
    name: "Ocean",
    light: {
      "mdc-theme-primary": "#005f50",
      "mdc-theme-secondary": "#D79922",
      "mdc-theme-background": "#fff",
      "mdc-theme-surface": "#eee",
      "mdc-theme-on-primary": null,
      "mdc-theme-on-secondary": null,
      "mdc-theme-on-surface": null,
      "console-color": "blue",
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
      "console-color": "blue",
      "console-background": "#000",
    },
  },
  {
    name: "Autumn",
    light: {
      "mdc-theme-primary": "#75663b",
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
      "mdc-theme-primary": "#75663b",
      "mdc-theme-secondary": "#81BDF5",
      "mdc-theme-background": "#3D1E06",
      "mdc-theme-surface": "#1A0F02",
      "mdc-theme-on-primary": null,
      "mdc-theme-on-secondary": null,
      "mdc-theme-on-surface": null,
      "console-color": "#7cfc00",
      "console-background": "#000",
    },
  },
];
