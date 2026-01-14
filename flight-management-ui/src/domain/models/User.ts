import type { Gender } from "../enums/Gender";
import type { Role } from "../enums/Role";

export interface User {
  user_id: number;
  first_name: string;
  last_name: string;
  email: string;
  birth_date: string;
  gender: Gender;
  country: string;
  city: string;
  street: string;
  house_number: number;
  account_balance: number;
  role: Role;
  profile_picture: string;
}
