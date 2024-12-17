interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  logout: () => Promise<void>;
  login: (email: string, password: string) => Promise<boolean>;
}

export type { User, AuthContextType };
