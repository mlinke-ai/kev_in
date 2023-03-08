interface MDCThemeVars {
    "mdc-theme-primary": string;	// The theme primary color
    "mdc-theme-secondary": string;	    // The theme secondary color
    "mdc-theme-background": string;	// The theme background color
    "mdc-theme-surface": string;	    // The theme surface color
    "mdc-theme-on-primary": string | null;	// Text color on top of a primary background
    "mdc-theme-on-secondary": string | null;	// Text color on top of a secondary background
    "mdc-theme-on-surface": string | null;	// Text color on top of a surface background
}

interface CustomThemeVars extends MDCThemeVars{
    [key: string]: string | null;
}

export interface ThemeInterface {
    name: string;
    light: CustomThemeVars;
    dark: CustomThemeVars;
}
