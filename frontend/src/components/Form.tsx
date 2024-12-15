import { useState } from "react";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";
import "../styles/Form.css";

interface FormProps {
  route: string;
  method: "Login" | "Register";
}

function Form({ route, method }: FormProps) {
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
      if (method === "Register" && password !== confirmPassword) {
        alert("Passwords do not match");
        return;
      }
      const response = await api.post(route, { name, email, password });
      if (method === "Login" && response.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access);
        localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
        navigate("/");
      } else if (method === "Register" && response.status === 201) {
        navigate("/login");
      }
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md"
    >
      <h1 className="text-2xl font-semibold text-center mb-6">{method}</h1>

      {/* Name field (only for Register method) */}
      {method === "Register" && (
        <input
          className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          type="text"
          value={name}
          placeholder="Name"
          onChange={(e) => setName(e.target.value)}
        />
      )}

      {/* Email field */}
      <input
        className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        type="email"
        value={email}
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      {/* Password field */}
      <input
        className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        type="password"
        value={password}
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      {/* Confirm Password field (only for Register method) */}
      {method === "Register" && (
        <input
          className="w-full p-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          type="password"
          value={confirmPassword}
          placeholder="Confirm Password"
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      )}

      {/* Submit Button */}
      <button
        type="submit"
        className="w-full p-3 mt-4 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
      >
        {method}
      </button>
    </form>
  );
}

export default Form;
