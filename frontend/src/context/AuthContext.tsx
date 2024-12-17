import React, { createContext, useState, useEffect, ReactNode } from "react";
import api from "../api";
import { User, AuthContextType } from "../types/AuthTypes";

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  user: null,
  logout: async () => {},
  login: async () => false,
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await api.post("api/auth/verify/");
        if (response.status !== 200) {
          throw new Error("User not authenticated");
        } else {
          setUser(null);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error("User not authenticated:", error);
        setUser(null);
        setIsAuthenticated(false);
      }
    };

    checkAuthStatus();
  }, []);

  const logout = async () => {
    try {
      const response = await api.post("api/logout/");
      if (response.status !== 204) {
        throw new Error("Logout failed");
      }
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post("api/auth/", { email, password });
      setUser({
        id: response.data.id,
        name: response.data.name,
        email: response.data.email,
      });
      setIsAuthenticated(true);
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      setUser(null);
      setIsAuthenticated(false);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, logout, login }}>
      {children}
    </AuthContext.Provider>
  );
};
