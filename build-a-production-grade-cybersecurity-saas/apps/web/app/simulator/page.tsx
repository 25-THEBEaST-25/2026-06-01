"use client";

import { useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { ArrowUpRight, Check, SlidersHorizontal } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { simulateRiskImprovement } from "@/lib/api";
import type { Finding, RiskSimulationResponse } from "@/lib/types";

const currentScore = 62;

const simulatorFindings: Finding[] = [
  {
    category: "email_security",
    key: "dmarc",
    status: "fail",
    severity: "high",
    message: "DMARC is not enforcing quarantine or reject policy.",
    evidence: {}
  },
  {
    category: "ssl",
    key: "ssl_certificate",
    status: "fail",
    severity: "high",
    message: "SSL certificate is expired or not trusted.",
    evidence: {}
  },
  {
    category: "asset_discovery",
    key: "open_ports",
    status: "warn",
    severity: "medium",
    message: "Port 21 is exposed publicly and should be closed.",
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

const defaultSelected = ["dmarc", "ssl_certificate", "open_ports"];

export default function SimulatorPage() {
  const [selected, setSelected] = useState<string[]>(defaultSelected);
  const [simulation, setSimulation] = useState<RiskSimulationResponse | null>(null);
  const projected = useMemo(
    () =>
      simulation ?? {
        current_score: currentScore,
        predicted_score: 84,
        improvement: 22,
        improvement_percentage: 35.5,
        estimated_risk_reduction: 22,
        selected_finding_keys: selected,
        top_fixes: [
          {
            finding_key: "dmarc",
            title: "Enable DMARC enforcement",
            category: "email_security",
            severity: "high" as const,
            score_impact: 12,
            risk_reduction: 12
          },
          {
            finding_key: "ssl_certificate",
            title: "Renew SSL certificate",
            category: "ssl",
            severity: "high" as const,
            score_impact: 8,
            risk_reduction: 8
          },
          {
            finding_key: "open_ports",
            title: "Close Port 21",
            category: "asset_discovery",
            severity: "medium" as const,
            score_impact: 6,
            risk_reduction: 6
          }
        ],
        comparison: [
          { label: "Current", score: currentScore },
          { label: "Predicted", score: 84 }
        ]
      },
    [selected, simulation]
  );

  function toggleFinding(key: string) {
    setSelected((existing) =>
      existing.includes(key) ? existing.filter((item) => item !== key) : [...existing, key]
    );
  }

  async function runSimulation() {
    setSimulation(await simulateRiskImprovement(currentScore, simulatorFindings, selected));
  }

  return (
    <div className="grid gap-6">
      <section className="grid gap-4 xl:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle>Current Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">{projected.current_score}</div>
            <p className="mt-1 text-sm text-muted-foreground">Existing risk posture</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Predicted Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-primary">{projected.predicted_score}</div>
            <p className="mt-1 text-sm text-muted-foreground">After selected fixes</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Improvement</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2 text-4xl font-bold">
              +{projected.improvement}
              <ArrowUpRight className="h-7 w-7 text-primary" />
            </div>
            <p className="mt-1 text-sm text-muted-foreground">
              {projected.improvement_percentage}% score improvement
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Risk Reduction</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">{projected.estimated_risk_reduction}</div>
            <p className="mt-1 text-sm text-muted-foreground">Estimated reduction points</p>
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1fr_420px]">
        <Card>
          <CardHeader>
            <CardTitle>Before vs After</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={projected.comparison}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="label" tickLine={false} axisLine={false} />
                  <YAxis domain={[0, 100]} tickLine={false} axisLine={false} />
                  <Tooltip />
                  <Bar dataKey="score" fill="#0ea5a8" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Simulate Fixes</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3">
            {simulatorFindings.map((finding) => {
              const checked = selected.includes(finding.key);
              return (
                <button
                  className="flex items-start gap-3 rounded-md border p-3 text-left transition hover:bg-muted"
                  key={finding.key}
                  onClick={() => toggleFinding(finding.key)}
                >
                  <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded border bg-background">
                    {checked ? <Check className="h-3.5 w-3.5 text-primary" /> : null}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="flex flex-wrap items-center gap-2">
                      <span className="font-medium">{fixLabel(finding.key)}</span>
                      <Badge tone={finding.severity}>{finding.severity}</Badge>
                    </span>
                    <span className="mt-1 block text-sm text-muted-foreground">{finding.message}</span>
                  </span>
                </button>
              );
            })}
            <Button onClick={runSimulation}>
              <SlidersHorizontal className="h-4 w-4" />
              Run Simulation
            </Button>
          </CardContent>
        </Card>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Top Recommended Fixes by Score Impact</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3">
          {projected.top_fixes.map((fix) => (
            <div className="grid gap-3 rounded-md border p-3 md:grid-cols-[1fr_160px]" key={fix.finding_key}>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <p className="font-medium">{fix.title}</p>
                  <Badge tone={fix.severity}>{fix.severity}</Badge>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">
                  {fix.category.replaceAll("_", " ")} risk reduction estimate
                </p>
              </div>
              <div className="text-left md:text-right">
                <div className="text-2xl font-bold text-primary">+{fix.score_impact}</div>
                <p className="text-sm text-muted-foreground">score impact</p>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}

function fixLabel(key: string) {
  const labels: Record<string, string> = {
    dmarc: "Enable DMARC",
    ssl_certificate: "Renew SSL Certificate",
    open_ports: "Close Port 21",
    content_security_policy: "Add CSP Header"
  };
  return labels[key] ?? `Fix ${key.replaceAll("_", " ")}`;
}
