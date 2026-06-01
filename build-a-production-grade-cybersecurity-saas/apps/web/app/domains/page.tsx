"use client";

import { useState } from "react";
import { Search } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { scanDomain } from "@/lib/api";
import type { ScanResponse } from "@/lib/types";

export default function DomainsPage() {
  const [domain, setDomain] = useState("example.com");
  const [scan, setScan] = useState<ScanResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function runScan() {
    setLoading(true);
    try {
      setScan(await scanDomain(domain));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-6">
      <Card>
        <CardHeader>
          <CardTitle>Domain Monitoring</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-3 sm:flex-row">
            <input
              className="h-10 flex-1 rounded-md border bg-background px-3 text-sm"
              value={domain}
              onChange={(event) => setDomain(event.target.value)}
            />
            <Button onClick={runScan} disabled={loading}>
              <Search className="h-4 w-4" />
              {loading ? "Scanning" : "Scan"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {scan ? (
        <Card>
          <CardHeader>
            <CardTitle>{scan.domain} Findings</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3">
            <div className="text-sm text-muted-foreground">Risk score: {scan.risk_score}/100</div>
            {scan.findings.map((finding) => (
              <div className="rounded-md border p-3" key={`${finding.category}-${finding.key}`}>
                <div className="flex flex-wrap items-center gap-2">
                  <Badge tone={finding.status}>{finding.status}</Badge>
                  <Badge tone={finding.severity}>{finding.severity}</Badge>
                  <span className="font-medium">{finding.key.replaceAll("_", " ")}</span>
                </div>
                <p className="mt-2 text-sm text-muted-foreground">{finding.message}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
