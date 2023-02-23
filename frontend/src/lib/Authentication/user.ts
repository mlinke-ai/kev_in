import { userID, userName, userMail, accessLevel, startPage } from "../../stores";
import { accessLevels, startPages, userRoles } from "../common/types";
import { get as getStore } from "svelte/store";
import type { GetUser } from "./types"

// function to send login data to the server
export const login = async (email: string, password: string) => {
  let response = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_mail: email,
      user_pass: password,
    }),
  });

  if (response.status == 200) {
    let userData = await response.json()
    let user: GetUser = {
      user_id: userData.user_id,
      user_mail: userData.user_mail,
      user_name: userData.user_name,
      user_role_name: userData.user_role_name,
      user_role_value: userData.user_role_value
    } 
    storeUser(user);
    window.location.replace(getStore(startPage))
    return true;
  } else if (response.status == 401) {
    return false;
  }
};

// function to make the server log out the client
export const logout = async () => {
  await fetch("/logout", { method: "POST" }).then(() => {
    resetUser()
    window.location.replace(getStore(startPage));
  });
};

// function to fetch user data from the server
export const getUser = async (): Promise<GetUser | null> => {
  try {
    const response = await fetch("/user", { method: "GET" });
    if (!response.ok) {
      return null;
    }
    return await response.json();
  } catch (error) {
    return null;
  }
};

export function getAccessLevel(user_role: string): number {
  let level: number = accessLevels.undefined;
  switch (user_role) {
    case userRoles.default:
      level = accessLevels.default;
      break;
    case userRoles.user:
      level = accessLevels.user;
      break;
    case userRoles.admin:
      level = accessLevels.admin;
      break;
    case userRoles.sadmin:
      level = accessLevels.sadmin;
  }
  return level;
}

export function getStartPage(level: accessLevels): startPages {
  switch (level) {
    case accessLevels.user:
      return startPages.user
    case accessLevels.admin:
      return startPages.admin
    case accessLevels.sadmin:
      return startPages.sadmin
    default:
      return startPages.default
  }
}

// function to store user data
export function storeUser(user: GetUser) {
  let level: number = getAccessLevel(user.user_role_name);
  userID.set(user.user_id);
  userName.set(user.user_name);
  userMail.set(user.user_mail);
  accessLevel.set(level);
  console.log(getStartPage(level))
  startPage.set(getStartPage(level))
}

export function resetUser() {
  const user: GetUser = {
    user_id: 0,
    user_name: "",
    user_role_name: "Default",
    user_role_value: 0,
    user_mail: ""
  }
  storeUser(user)
}