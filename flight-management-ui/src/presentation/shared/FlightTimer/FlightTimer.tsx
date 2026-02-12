import { useEffect, useState } from 'react';
import './FlightTimer.css';

interface FlightTimerProps {
  arrivalTime: string; // ISO 8601 format
  onComplete?: () => void;
}

export const FlightTimer = ({ arrivalTime, onComplete }: FlightTimerProps) => {
  const [timeRemaining, setTimeRemaining] = useState<string>('');
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    const updateTimer = () => {
      const now = new Date().getTime();
      const arrival = new Date(arrivalTime).getTime();
      const difference = arrival - now;

      if (difference <= 0) {
        setTimeRemaining('Landing soon');
        setIsCompleted(true);
        if (onComplete) {
          onComplete();
        }
        return;
      }

      const hours = Math.floor(difference / (1000 * 60 * 60));
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((difference % (1000 * 60)) / 1000);

      if (hours > 0) {
        setTimeRemaining(`${hours}h ${minutes}m remaining`);
      } else if (minutes > 0) {
        setTimeRemaining(`${minutes}m ${seconds}s remaining`);
      } else {
        setTimeRemaining(`${seconds}s remaining`);
      }
    };

    updateTimer();
    const intervalId = setInterval(updateTimer, 1000);

    return () => clearInterval(intervalId);
  }, [arrivalTime, onComplete]);

  return (
    <div className={`flight-timer ${isCompleted ? 'completed' : ''}`}>
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
      <span>{timeRemaining}</span>
    </div>
  );
};
