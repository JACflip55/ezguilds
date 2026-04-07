import { useState, useEffect, useRef } from "react";

export function usePolling<T>(
  fetcher: () => Promise<T>,
  intervalMs: number,
  shouldPoll: boolean
) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval>>(undefined);

  useEffect(() => {
    if (!shouldPoll) {
      if (timerRef.current) clearInterval(timerRef.current);
      return;
    }

    const poll = async () => {
      try {
        const result = await fetcher();
        setData(result);
        setError(null);
      } catch (e) {
        setError(e as Error);
      }
    };

    poll(); // immediate first fetch
    timerRef.current = setInterval(poll, intervalMs);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [shouldPoll]);

  return { data, error };
}
