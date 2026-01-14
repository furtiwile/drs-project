import type { Gender } from "../enums/Gender";

export interface RegisterDto {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  birth_date: string;
  gender: Gender;
  country: string;
  city: string;
  street: string;
  house_number: number;
  profile_picture?: string;
}
