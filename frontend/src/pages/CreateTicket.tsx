import React, { useContext, useEffect, useState } from "react";
import api from "../api";
import { AuthContext } from "../context/Auth";
import { useNavigate } from "react-router-dom";

const CreateTicketPage: React.FC = () => {
  const { user, loading } = useContext(AuthContext);
  const [ticketData, setTicketData] = useState({
    event: "",
    price: "",
    owner: null,
    sector: "",
    row: "",
    seat: "",
    isReserved: false,
  });

  const navigate = useNavigate();
  useEffect(() => {
    if (!loading && !user) {
      navigate("/");
    }
  });

  const [message, setMessage] = useState<string>("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setTicketData({ ...ticketData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await api.post("api/ticket/", ticketData);
      setMessage("Ticket created successfully!");
    } catch (error) {
      setMessage("Failed to create ticket. Please try again.");
      console.error(error);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Create Ticket</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-sm">
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Event ID
          </label>
          <input
            type="text"
            name="name"
            id="name"
            value={ticketData.event}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Price
          </label>
          <textarea
            name="description"
            id="description"
            value={ticketData.price}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            rows={4}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="category" className="block text-sm font-medium text-gray-700">
            Sector
          </label>
          <input
            type="text"
            name="category"
            id="category"
            value={ticketData.sector}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="start_datetime" className="block text-sm font-medium text-gray-700">
            Row
          </label>
          <input
            type="datetime-local"
            name="start_datetime"
            id="start_datetime"
            value={ticketData.row}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="end_datetime" className="block text-sm font-medium text-gray-700">
            Seat
          </label>
          <input
            type="datetime-local"
            name="end_datetime"
            id="end_datetime"
            value={ticketData.seat}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition"
        >
          Create Ticket
        </button>
      </form>
      {message && <div className="mt-4 text-lg">{message}</div>}
    </div>
  );
};

export default CreateTicketPage;
