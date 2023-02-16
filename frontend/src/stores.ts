import { writable } from "svelte/store";
import { accessLevels } from "./lib/constants";

// User Storage
export const accessLevel = writable(accessLevels.undefined);
export const userID = writable<bigint>();
export const userName = writable<string>();
export const userMail = writable<string>();

export const startPage = writable("#/")

// UI
export const renderNavbar = writable(true)