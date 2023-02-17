import { userID, userName, userMail, accessLevel } from "../../stores";
import { accessLevels } from "../constants";

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
    storeUser(<GetUser>(await getUser()));
    location.reload();
    return true;
  } else if (response.status == 401) {
    return false;
  }
};

// function to make the server log out the client
export const logout = async () => {
  await fetch("/logout", { method: "POST" }).then(() => {
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

// function to store user data
export function storeUser(user: GetUser) {
  userID.set(user.user_id);
  userName.set(user.user_name);
  userMail.set(user.user_mail);
  accessLevel.set(accessLevels.admin);
}
