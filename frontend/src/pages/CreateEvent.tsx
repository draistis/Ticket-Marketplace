import React, { useContext, useEffect, useState } from "react";
import api from "../api";
import { AuthContext } from "../context/Auth";
import { useNavigate } from "react-router-dom";

const CreateEventPage: React.FC = () => {
  const { user, loading } = useContext(AuthContext);
  const [eventData, setEventData] = useState({
    name: "",
    description: "",
    category: "",
    start_datetime: "",
    end_datetime: "",
    location: "",
    organizer: "",
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
    setEventData({ ...eventData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await api.post("api/event/", eventData);
      setMessage("Event created successfully!");
    } catch (error) {
      setMessage("Failed to create event. Please try again.");
      console.error(error);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Create Event</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-sm">
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Event Name
          </label>
          <input
            type="text"
            name="name"
            id="name"
            value={eventData.name}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            name="description"
            id="description"
            value={eventData.description}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            rows={4}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="category" className="block text-sm font-medium text-gray-700">
            Category
          </label>
          <input
            type="text"
            name="category"
            id="category"
            value={eventData.category}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="start_datetime" className="block text-sm font-medium text-gray-700">
            Start Date & Time
          </label>
          <input
            type="datetime-local"
            name="start_datetime"
            id="start_datetime"
            value={eventData.start_datetime}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="end_datetime" className="block text-sm font-medium text-gray-700">
            End Date & Time
          </label>
          <input
            type="datetime-local"
            name="end_datetime"
            id="end_datetime"
            value={eventData.end_datetime}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="location" className="block text-sm font-medium text-gray-700">
            Location ID
          </label>
          <input
            type="text"
            name="location"
            id="location"
            value={eventData.location}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="organizer" className="block text-sm font-medium text-gray-700">
            Organizer
          </label>
          <input
            type="text"
            name="organizer"
            id="organizer"
            value={eventData.organizer}
            onChange={handleInputChange}
            className="mt-1 p-2 border border-gray-300 rounded w-full"
            required
          ></input>
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition"
        >
          Create Event
        </button>
      </form>
      {message && <div className="mt-4 text-lg">{message}</div>}
    </div>
  );
};

export default CreateEventPage;
