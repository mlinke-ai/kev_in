import { ThemeInterface } from "./types";

export let themes: Array<ThemeInterface> = [
  {
    name: "TU",
    light: {
      mdc: {
        "--mdc-theme-primary": "#005f50",
        "--mdc-theme-secondary": "#D79922",
        "--mdc-theme-background": "#fff",
        "--mdc-theme-surface": "#eee",
      },
      custom: {
        "--console-color": "#7cfc00",
        "--console-background": "#000",
      },
    },
    dark: {
      mdc: {
        "--mdc-theme-primary": "#005f50",
        "--mdc-theme-secondary": "#D79922",
        "--mdc-theme-background": "#000",
        "--mdc-theme-surface": "#001a16",
      },
      custom: {
        "--console-color": "#7cfc00",
        "--console-background": "#000",
      },
    },
  },
];
