import React, { useState, useEffect, ReactNode } from "react";
import api from "../api";
import { User } from "../types/AuthTypes";
import { AuthContext } from "./Auth";

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    console.log(user);
  }, [user]);

  useEffect(() => {
    const checkAuthStatus = async () => {
      setLoading(true);
      try {
        const response = await api.post("api/auth/verify/");
        if (response.status !== 200) {
          throw new Error("User not authenticated");
        } else {
          setUser({
            id: response.data.id,
            name: response.data.name,
            email: response.data.email,
            is_superuser: response.data.is_superuser,
            is_organizer: response.data.is_organizer,
          });
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error("User not authenticated:", error);
        setUser(null);
        setIsAuthenticated(false);
      }
      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  const logout = async () => {
    setLoading(true);
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
    setLoading(false);
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await api.post("api/auth/", { email, password });
      setUser({
        id: response.data.id,
        name: response.data.name,
        email: response.data.email,
        is_superuser: response.data.is_superuser,
        is_organizer: response.data.is_organizer,
      });
      setIsAuthenticated(true);
      setLoading(false);
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      setUser(null);
      setIsAuthenticated(false);
      setLoading(false);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, logout, login, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
