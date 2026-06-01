"use client";

import { useState } from "react";
import { Download } from "lucide-react";

import { Button } from "@/components/ui/button";

export function ReportDownload() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function download() {
    setLoading(true);
    setError("");
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
      const token = window.localStorage.getItem("cyber-risk-radar-token");
      const response = await fetch(`${baseUrl}/reports/domain`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ domain: "example.com" })
      });
      if (!response.ok) {
        throw new Error("Report generation failed");
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "example.com-risk-report.pdf";
      anchor.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Sign in to generate reports from the API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-2">
      <Button onClick={download} disabled={loading}>
        <Download className="h-4 w-4" />
        {loading ? "Generating" : "Generate PDF"}
      </Button>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
    </div>
  );
}
