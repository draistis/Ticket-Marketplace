import React, { useCallback, useEffect, useState } from "react";
import EventCard from "../components/Event";
import api from "../api";
import { Event, Location, EventWithLocation } from "../types/Props";
import SearchBar from "../components/eventSearchBar";

const Home: React.FC = () => {
  const [events, setEvents] = useState<EventWithLocation[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [filters, setFilters] = useState({
    eventName: "",
    location: "",
    date: "",
  });

  useEffect(() => {
    getLocations();
    getEvents(filters);
  });

  const getEvents = useCallback(async (filters: { eventName: string; location: string; date: string }) => {
    try {
      const { eventName, location, date } = filters;
      const queryParams: Record<string, string> = {};

      if (eventName) queryParams.query = eventName;
      if (date) queryParams.start_datetime = date;

      const eventResponse = await api.get("api/event/", { params: queryParams });
      const eventData: Event[] = eventResponse.data;

      const eventsWithLocation: EventWithLocation[] = eventData
        .map((event: Event) => {
          const eventLocation = locations.find((location) => location.id === event.location);
          return eventLocation
            ? {
                ...event,
                city: eventLocation.city,
                country: eventLocation.country,
                venue: eventLocation.name,
              }
            : null;
        })
        .filter((event) => event !== null) as EventWithLocation[];

      if (location) {
        const [city, country] = location.split(",").map((str) => str.trim());
        setEvents(
          eventsWithLocation.filter(
            (event) =>
              (city && event.city.toLowerCase().includes(city.toLowerCase())) ||
              (country && event.country.toLowerCase().includes(country.toLowerCase())),
          ),
        );
      } else {
        setEvents(eventsWithLocation);
      }
    } catch (error) {
      console.error(error);
    }
  }, [locations]);

  useEffect(() => {
    getEvents(filters);
  }, [filters, getEvents]);

  async function getLocations() {
    try {
      const locationResponse = await api.get("api/location/");
      setLocations(locationResponse.data);
    } catch (error) {
      console.error(error);
    }
  }

  const handleSearch = (filters: { eventName: string; location: string; date: string }) => {
    setFilters(filters);
  };

  return (
    <>
      <SearchBar onSearch={handleSearch} />
      <div className="container mx-auto p-6">
        <div className="max-w-screen-lg mx-auto">
          <h1 className="text-2xl font-bold text-gray-800 mb-6">Upcoming Events</h1>
          <div className="bg-white border rounded-lg shadow-sm">
            {events.length > 0 ? (
              events.map((event) => <EventCard key={event.id} {...event} />)
            ) : (
              <p>No events found.</p>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
