import { userID, userName, userMail, accessLevel } from "../../stores";
import { accessLevels, userRoles } from "../constants";

interface GetUser {
  user_id: number;
  user_mail: string;
  user_name: string;
  user_role: string;
}

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
    storeUser(<GetUser>await getUser());
    location.reload();
    return true;
  } else if (response.status == 401) {
    return false;
  }
};

// function to make the server log out the client
export const logout = async () => {
  await fetch("/logout", { method: "POST" }).then(() => {
    resetUser()
    window.location.replace("/");
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

// function to store user data
export function storeUser(user: GetUser) {
  userID.set(user.user_id);
  userName.set(user.user_name);
  userMail.set(user.user_mail);
  accessLevel.set(getAccessLevel(user.user_role));
}

export function resetUser() {
  const user: GetUser = {
    user_id: 0,
    user_name: "",
    user_role: "Default",
    user_mail: ""
  }
  storeUser(user)
}