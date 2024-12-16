import { useNavigate } from "react-router-dom";
import { EventProps } from "../props/EventProps";

const EventCard = ({ id, name, category, start_datetime, location }: EventProps) => {
  const eventDate = new Date(start_datetime);
  const formattedDate = eventDate.toLocaleDateString("en-US", {
    day: "2-digit",
  });
  const formattedMonth = eventDate.toLocaleDateString("en-US", {
    month: "short",
  });
  const formattedDay = eventDate.toLocaleDateString("en-US", {
    weekday: "short",
  });
  const formattedTime = eventDate.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
  const navigate = useNavigate();

  return (
    <div className="flex border-b py-4 items-center hover:bg-gray-50 transition">
      <div className="w-20 text-center">
        <div className="text-sm font-semibold text-gray-500">{formattedMonth}</div>
        <div className="text-2xl font-bold text-gray-800">{formattedDate}</div>
      </div>

      <div className="flex-1 ml-6">
        <div className="flex items-center gap-2">
          <span className="text-xs px-2 py-1 bg-blue-100 text-blue-600 font-semibold rounded-md">
            {category}
          </span>
        </div>
        <div className="flex items-center gap-2 mt-2">
          <span className="text-sm text-gray-500">
            {formattedDay} • {formattedTime}
          </span>
        </div>
        <div className="text-lg font-bold text-gray-800 mt-1">{name}</div>
        <div className="text-sm text-gray-600 mt-1">
          {location.city}, {location.country} • {location.venue}
        </div>
      </div>

      <div className="mr-8">
        <button
          onClick={() => navigate(`/event/${id}/`)}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded hover:bg-blue-700 transition"
        >
          Find Tickets
        </button>
      </div>
    </div>
  );
};

export default EventCard;
