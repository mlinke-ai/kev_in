import { userName, userMail, accessLevel, startPage } from "../../stores";
import { accessLevels } from "../types";

export const getUserData = async () => {
  await fetch("/user", { method: "GET" }).then((response) => {
    if (response.status == 200) {
      response.json().then((data) => {
        userName.set(data.user_name);
        userMail.set(data.user_mail);
        console.log(data.user_role);
        accessLevel.set(accessLevels.admin);
      });
    }
  });
};

export const setupUserSettings = async () => {
  await getUserData();
  let level;
  const unsubscribe = accessLevel.subscribe((value) => {
    level = value;
  });
  switch (level) {
    case accessLevels.default:
      break;
    case accessLevels.user:
      startPage.set("/profile");
      break;
    case accessLevels.admin:
      startPage.set("/profile");
  }
  unsubscribe;
};
