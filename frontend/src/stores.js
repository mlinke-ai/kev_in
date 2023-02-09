import { writable } from "svelte/store";

// User Storage
export const accessLevel = writable(-1);
export const userID = writable(0);
export const userName = writable("");
export const userMail = writable("");
