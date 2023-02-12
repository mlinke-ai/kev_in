import { userID, userName, userMail, accessLevel } from "../../stores";
import { accessLevels } from "../constants";

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
    await setupUserSettings().then(() => {
      location.reload();
    });
    return true;
  } else if (response.status == 401) {
    return false;
  }
};

export const logout = async() => {
  await fetch("/logout", { method: "POST" }).then(() => {
    window.location.replace("/")
  });
};

export const setupUserSettings = async () => {
  await fetch("/user", { method: "GET" }).then((response) => {
    if (response.status == 200) {
      response.json().then((data) => {
        userID.set(data.user_id);
        userName.set(data.user_name);
        userMail.set(data.user_mail);
        accessLevel.set(accessLevels.admin);
      });
    } else {
      accessLevel.set(accessLevels.default);
    }
  });
};
