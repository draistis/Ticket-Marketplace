interface Location {
  city: string;
  country: string;
  venue: string;
}

interface EventProps {
  id: number;
  name: string;
  category: string;
  start_datetime: string;
  location: Location;
}

export type { EventProps };
