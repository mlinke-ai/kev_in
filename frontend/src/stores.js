import { writable } from "svelte/store";
import { accessLevels } from "./lib/types";

// User Storage
export const accessLevel = writable(-1)
export const userName = writable("");
export const userMail = writable("");

export const startPage = writable("#/")