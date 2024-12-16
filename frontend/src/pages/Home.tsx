import React from "react";
import EventCard from "../components/Event";
import events from "../testData/event_data";

const Home: React.FC = () => {
  return (
    <div className="container mx-auto p-6 bg-white">
      <div className="max-w-screen-lg mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Upcoming Events</h1>
        <div className="border rounded-lg shadow-sm">
          {events.map((event, index) => (
            <EventCard key={index} {...event} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
