import { writable } from "svelte/store";

// User Storage
export const userLoggedIn = writable(false)
export const userName = writable("");
export const userIsAdmin = writable(false);
export const userLevel = writable(0);