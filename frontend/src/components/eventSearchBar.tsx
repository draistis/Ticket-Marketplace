import React, { useState } from "react";

interface SearchBarProps {
  onSearch: (filters: {
    eventName: string;
    location: string;
    date: string;
  }) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState({
    eventName: "",
    location: "",
    date: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm({
      ...searchTerm,
      [e.target.name]: e.target.value,
    });
  };

  const handleSearch = () => {
    onSearch(searchTerm);
  };

  return (
    <div className="bg-white shadow-md border-b">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
          <input
            type="text"
            name="eventName"
            value={searchTerm.eventName}
            onChange={handleChange}
            placeholder="Search by event name"
            className="px-4 py-2 border border-gray-300 rounded-lg w-full sm:w-1/3 focus:outline-none focus:ring-2 focus:ring-purple-600"
          />
          <input
            type="text"
            name="location"
            value={searchTerm.location}
            onChange={handleChange}
            placeholder="Search by location (city, country)"
            className="px-4 py-2 border border-gray-300 rounded-lg w-full sm:w-1/3 focus:outline-none focus:ring-2 focus:ring-purple-600"
          />
          <input
            type="date"
            name="date"
            value={searchTerm.date}
            onChange={handleChange}
            className="px-4 py-2 border border-gray-300 rounded-lg w-full sm:w-1/3 focus:outline-none focus:ring-2 focus:ring-purple-600"
          />
          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-600 transition"
          >
            Search
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
