import React, { useEffect, useState } from "react";
import EventCard from "../components/Event";
import api from "../api";
import { Event, Location, EventWithLocation } from "../props/Props";

const Home: React.FC = () => {
  const [events, setEvents] = useState<EventWithLocation[]>([]);

  useEffect(() => {
    getEvents();
  }, []);

  async function getEvents() {
    try {
      const [eventResponse, locationResponse] = await Promise.all([
        api.get("api/event/"),
        api.get("api/location/"),
      ]);
      const eventData: Event[] = eventResponse.data;
      const locationData: Location[] = locationResponse.data;

      const locationMap: Record<number, Location> = {};
      locationData.forEach((location) => {
        locationMap[location.id] = location;
      });

      const eventsWithLocation = eventData.map((event: Event) => ({
        ...event,
        city: locationMap[event.location].city,
        country: locationMap[event.location].country,
        venue: locationMap[event.location].name,
      }));

      setEvents(eventsWithLocation);
    } catch (error) {
      alert("Failed to fetch events or locations. Please try again.");
      console.error(error);
    }
  }

  return (
    <div className="container mx-auto p-6">
      <div className="max-w-screen-lg mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Upcoming Events</h1>
        <div className="bg-white border rounded-lg shadow-sm">
          {events.map((event) => (
            <EventCard key={event.id} {...event} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
