"use client";

import { useEffect, useState } from "react";
import { BriefcaseBusiness, IndianRupee, TrendingUp } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { estimateBusinessImpact } from "@/lib/api";
import type { BusinessImpactResponse, Finding } from "@/lib/types";

const findings: Finding[] = [
  {
    category: "ssl",
    key: "ssl_certificate",
    status: "fail",
    severity: "medium",
    message: "Expired SSL certificate",
    evidence: {}
  },
  {
    category: "email_security",
    key: "dmarc",
    status: "fail",
    severity: "high",
    message: "DMARC is not enforcing quarantine or reject policy.",
    evidence: {}
  },
  {
    category: "asset_discovery",
    key: "open_ports",
    status: "warn",
    severity: "medium",
    message: "Port 21 is exposed publicly.",
    evidence: { ports: [21] }
  },
  {
    category: "security_headers",
    key: "content_security_policy",
    status: "fail",
    severity: "medium",
    message: "Content-Security-Policy header is missing.",
    evidence: {}
  }
];

export default function ImpactPage() {
  const [impact, setImpact] = useState<BusinessImpactResponse | null>(null);

  useEffect(() => {
    estimateBusinessImpact("example.com", findings).then(setImpact);
  }, []);

  return (
    <div className="grid gap-6">
      <section className="grid gap-4 xl:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Business Exposure</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <BriefcaseBusiness className="h-8 w-8 text-primary" />
              <div>
                <div className="text-3xl font-bold">{impact?.estimates.length ?? findings.length}</div>
                <p className="text-sm text-muted-foreground">findings with business impact estimates</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Highest Likelihood</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <TrendingUp className="h-8 w-8 text-primary" />
              <div>
                <div className="text-3xl font-bold">High</div>
                <p className="text-sm text-muted-foreground">DMARC and exposed ports need priority review</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Estimated Range</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <IndianRupee className="h-8 w-8 text-primary" />
              <div>
                <div className="text-3xl font-bold">₹10k+</div>
                <p className="text-sm text-muted-foreground">per finding depending on severity and exposure</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-4">
        {(impact?.estimates ?? []).map((estimate) => (
          <Card key={estimate.finding_key}>
            <CardHeader>
              <div className="flex flex-wrap items-center justify-between gap-3">
                <CardTitle>{estimate.finding_title}</CardTitle>
                <div className="flex flex-wrap gap-2">
                  <Badge tone={riskTone(estimate.technical_risk)}>{estimate.technical_risk} technical risk</Badge>
                  <Badge tone={likelihoodTone(estimate.likelihood_of_exploitation)}>
                    {estimate.likelihood_of_exploitation} likelihood
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent className="grid gap-4 lg:grid-cols-[1.2fr_1fr_1fr]">
              <div>
                <p className="text-sm font-medium">Business Impact</p>
                <ul className="mt-2 grid gap-2 text-sm text-muted-foreground">
                  {estimate.business_impact.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="text-sm font-medium">Estimated Impact</p>
                <p className="mt-2 text-2xl font-bold text-primary">{estimate.financial_impact_range}</p>
              </div>
              <div>
                <p className="text-sm font-medium">Operational Impact</p>
                <p className="mt-2 text-sm text-muted-foreground">{estimate.operational_impact}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </section>
    </div>
  );
}

function riskTone(risk: string): "high" | "medium" | "low" {
  const value = risk.toLowerCase();
  if (value === "critical" || value === "high") {
    return "high";
  }
  if (value === "medium") {
    return "medium";
  }
  return "low";
}

function likelihoodTone(likelihood: string): "high" | "medium" | "low" {
  const value = likelihood.toLowerCase();
  if (value.includes("high")) {
    return "high";
  }
  if (value.includes("medium")) {
    return "medium";
  }
  return "low";
}
