import { writable } from "svelte/store";
import { accessLevels } from "./lib/types";

// User Storage
export const accessLevel = writable(accessLevels.default)
export const userName = writable("");
export const userLevel = writable(0);

export const startPage = writable("#/")