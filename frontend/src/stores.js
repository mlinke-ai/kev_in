import { writable } from "svelte/store";
import { accessLevels } from "./lib/types";

export const accessLevel = writable(accessLevels.default)

// User Storage
export const userLoggedIn = writable(false)
export const userName = writable("");
export const userIsAdmin = writable(false);
export const userLevel = writable(0);

export const startPage = writable("#/")