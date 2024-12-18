import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/Auth";
import React from "react";

interface FormProps {
  route: string;
  method: "Login" | "Register";
}

function Form({ route, method }: FormProps) {
  const { login } = React.useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    setLoading(true);
    e.preventDefault();
    try {
      if (method === "Register") {
        if (password !== confirmPassword) {
          alert("Passwords do not match");
          return;
        }
        const response = await api.post(route, { name, email, password });
        if (response.status === 201) {
          alert("Registration successful");
          navigate("/login");
        } else {
          alert("Registration failed");
        }
      }
      if (method === "Login") {
        const success = await login(email, password);
        if (success) {
          navigate("/");
        } else {
          alert("Login failed");
        }
        setLoading(false);
      }
    } catch (error) {
      alert("An error occurred. Please try again.");
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <>
      {loading && <div>Loading...</div>}

      <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-semibold text-center mb-6">{method}</h1>

        {method === "Register" && (
          <input
            className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            type="text"
            value={name}
            placeholder="Name"
            onChange={(e) => setName(e.target.value)}
          />
        )}

        <input
          className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          type="email"
          value={email}
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          type="password"
          value={password}
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        {method === "Register" && (
          <input
            className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            type="password"
            value={confirmPassword}
            placeholder="Confirm Password"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        )}

        <button
          type="submit"
          className="w-full p-3 mt-4 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          {method}
        </button>
      </form>
    </>
  );
}

export default Form;
