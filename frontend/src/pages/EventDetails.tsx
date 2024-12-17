import React, { useEffect } from "react";
import api from "../api";
import { Location, Event, Ticket } from "../types/Props";
import { useParams } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const EventDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [eventDetails, setEventDetails] = React.useState<Event | null>(null);
  const [tickets, setTickets] = React.useState<Ticket[]>([]);
  const [location, setLocation] = React.useState<Location | null>(null);
  const [loading, setLoading] = React.useState(false);
  const { isAuthenticated } = React.useContext(AuthContext);

  useEffect(() => {
    getEventDetails();
    getTickets();
  }, []);

  async function getEventDetails() {
    try {
      const eventRes = await api.get(`api/event/${id}/`);
      setEventDetails(eventRes.data);
      const locationRes = await api.get(`api/location/${eventRes.data.location}/`);
      setLocation(locationRes.data);
    } catch (error) {
      alert("Failed to fetch event details. Please try again.");
      console.error(error);
    }
  }
  async function getTickets() {
    try {
      setLoading(true);
      const ticketRes = await api.get(`api/event/${id}/tickets/`);
      setTickets(ticketRes.data);
    } catch (error) {
      alert("Failed to fetch tickets. Please try again.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 flex gap-8">
      <div className="w-3/5">
        {eventDetails ? (
          <>
            <div className="bg-white p-6 rounded-lg shadow-md h-min">
              <h1 className="text-3xl font-bold mb-4">{eventDetails.name}</h1>
              <p className="text-gray-700 mb-2">{eventDetails.description}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md h-min mt-4">
              <h2 className="text-2xl font-semibold mb-4">Date & Time</h2>
              <p className="text-gray-600">
                {new Date(eventDetails.start_datetime).toLocaleString()}
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md h-min mt-4">
              <h2 className="text-2xl font-semibold mb-4">Location</h2>
              <p className="text-gray-600">
                {location?.name}, {location?.city}, {location?.country}
              </p>
            </div>
          </>
        ) : (
          <p>Loading event details...</p>
        )}
      </div>

      <div className="w-2/5 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">Available Tickets</h2>
        {tickets.length > 0 ? (
          <ul>
            {tickets.map((ticket) => (
              <li
                key={ticket.id}
                className="flex justify-between p-4 mb-2 border rounded-md shadow-sm"
              >
                <div>
                  <p className="text-gray-800">
                    Sector: {ticket.sector}, Row: {ticket.row}, Seat: {ticket.seat}
                  </p>
                  <p className="text-gray-600">Price: ${ticket.price}</p>
                </div>
                <button className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">
                  Buy Ticket
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No tickets available yet.</p>
        )}
        {loading && <p>Loading more tickets...</p>}
      </div>
    </div>
  );
};

export default EventDetailsPage;
