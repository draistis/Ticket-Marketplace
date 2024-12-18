interface User {
  id: string;
  name: string;
  email: string;
  is_superuser: boolean;
  is_organizer: boolean;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  logout: () => Promise<void>;
  login: (email: string, password: string) => Promise<boolean>;
  loading: boolean;
}

export type { User, AuthContextType };
