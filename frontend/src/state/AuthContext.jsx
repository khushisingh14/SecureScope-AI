import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("securescope_token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(token));

  useEffect(() => {
    const handleLogout = () => logout();
    window.addEventListener("securescope:logout", handleLogout);
    return () => window.removeEventListener("securescope:logout", handleLogout);
  }, []);

  useEffect(() => {
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    api.get("/auth/me")
      .then((response) => setUser(response.data))
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, [token]);

  const login = async (email, password) => {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);
    const response = await api.post("/auth/login", form);
    localStorage.setItem("securescope_token", response.data.access_token);
    setToken(response.data.access_token);
  };

  const register = async (payload) => {
    await api.post("/auth/register", payload);
    await login(payload.email, payload.password);
  };

  const logout = () => {
    localStorage.removeItem("securescope_token");
    setToken(null);
    setUser(null);
  };

  const value = useMemo(() => ({ token, user, loading, login, register, logout }), [token, user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
