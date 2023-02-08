import { userID, userName, userMail, accessLevel } from "../../stores";
import { accessLevels } from "../constants";

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
        console.log(data.user_role);
        accessLevel.set(accessLevels.admin);
      });
    } else {
      accessLevel.set(accessLevels.default);
    }
  });
};
