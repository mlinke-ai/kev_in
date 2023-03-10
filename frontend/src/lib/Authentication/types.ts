export interface GetUser {
  user_id: number;
  user_mail: string;
  user_name: string;
  user_role_name: string;
  user_role_value: number;
}

export interface GetUserArgs{
  user_id?: number;
  user_name?: string;
  user_mail?: string;
  user_role?: number;
  user_page?: number;
  user_limit?: number;
}