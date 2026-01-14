export const Role = {
  USER: "USER",
  MANAGER: "MANAGER",
  ADMINISTRATOR: "ADMINISTRATOR"
} as const;

export type Role = typeof Role[keyof typeof Role];
