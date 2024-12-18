import { createContext } from "react";
import { AuthContextType } from "../types/AuthTypes";

export const AuthContext = createContext<AuthContextType>({
    isAuthenticated: false,
    user: null,
    logout: async () => {},
    login: async () => false,
    loading: true,
  });