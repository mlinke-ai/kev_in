import { writable } from "svelte/store";

export const accessLevel = writable(-1);
export const userID = writable<number>();
export const userName = writable("");
export const userMail = writable("");

export const startPage = writable("#/")
