import api from "@/services/api";
import { useState, useCallback } from "react";

export interface InsightsReport {
  [key: string]: any;
}

export function useInsights() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [insights, setInsights] = useState<InsightsReport | null>(null);

  const fetchInsights = useCallback(async (applicant: any) => {
    setLoading(true);
    setError(null);
    setInsights(null);
    try {
      const response = await api.post("/insights/generate", applicant);
      setInsights(response.data.insights);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to fetch insights");
    } finally {
      setLoading(false);
    }
  }, []);

  return { insights, loading, error, fetchInsights };
}
