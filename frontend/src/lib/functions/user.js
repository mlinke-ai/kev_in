import { accessLevel, startPage } from "../../stores";
import { accessLevels } from "../types";

export function getAccessLevel() {
    return accessLevels.admin 
    //just for test cases
    //change later back to .default
}

export function setupUserSettings(level) {
    accessLevel.set(level);
    switch (level) {
      case accessLevels.default:
        break;
      case accessLevels.user:
        startPage.set("/profile");
        break;
      case accessLevels.admin:
        startPage.set("/admin-dashboard");
    }
}