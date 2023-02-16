import { writable } from "svelte/store";

// User Storage
export const accessLevel = writable(-1);
export const userID = writable<bigint>();
export const userName = writable("");
export const userMail = writable("");

export const startPage = writable("#/")

// UI
export const renderNavbar = writable(true)