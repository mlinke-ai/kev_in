export interface UICardActionInterface {
  icon: string;
  func: () => void;
}

export interface GetMeta{
  next_page?: number;
  next_url?: number;
  prev_page?: number;
  prev_url?: number;
  total?: number;
}

export enum accessLevels {
  undefined = -1,
  default = 0,
  user = 1,
  admin = 2,
  sadmin = 3,
}

export enum startPages {
  default = "/",
  user = "/user",
  admin = "/admin",
  sadmin = "/admin",
}

export enum userRoles {
  undefined = "Undefined",
  default = "Default",
  user = "User",
  admin = "Admin",
  sadmin = "SAdmin",
}

export enum messages {
  neutral = 0,
  success = 1,
  warning = 2,
  error = 3,
}

export enum languages {
  python = "Python",
  java = "Java",
}

export const passwordLength = 8;

export const dashboardPage = "/admin-dashboard";
