import { useState, useEffect, createContext, useContext } from "react";
import {
  User,
  onAuthStateChanged,
  signInWithPopup,
  signOut,
  GoogleAuthProvider,
} from "firebase/auth";
import { auth } from "../firebase";

interface AuthState {
  user: User | null;
  loading: boolean;
  signIn: () => Promise<void>;
  logOut: () => Promise<void>;
  getToken: () => Promise<string>;
}

export const AuthContext = createContext<AuthState>(null!);

export function useAuthProvider(): AuthState {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    return onAuthStateChanged(auth, (u) => {
      setUser(u);
      setLoading(false);
    });
  }, []);

  const signIn = async () => {
    await signInWithPopup(auth, new GoogleAuthProvider());
  };

  const logOut = async () => {
    await signOut(auth);
  };

  const getToken = async () => {
    if (!user) throw new Error("Not authenticated");
    return user.getIdToken();
  };

  return { user, loading, signIn, logOut, getToken };
}

export function useAuth() {
  return useContext(AuthContext);
}
