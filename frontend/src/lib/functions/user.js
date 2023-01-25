import { userName, userMail, accessLevel, startPage } from "../../stores";
import { accessLevels } from "../types";

export const getUserData = async () => {
    await fetch("/user", { method: "GET" }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          userName.set(data["1"].user_name);
          userMail.set(data["1"].user_mail);
          accessLevel.set(accessLevels.admin);
        });
      }
    });
  };

  export function setupUserSettings() {
    let level;
    const unsubscribe = accessLevel.subscribe(value => {
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
  }