import { CheckCircle2 } from "lucide-react";

import { AlertsList } from "@/components/dashboard/alerts-list";
import { RiskGauge } from "@/components/dashboard/risk-gauge";
import { RiskTrend } from "@/components/dashboard/risk-trend";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getDashboard } from "@/lib/api";

export default async function DashboardPage() {
  const dashboard = await getDashboard();

  return (
    <div className="grid gap-6">
      <section className="grid gap-6 xl:grid-cols-[360px_1fr]">
        <Card>
          <CardHeader>
            <CardTitle>Security Posture</CardTitle>
          </CardHeader>
          <CardContent>
            <RiskGauge score={dashboard.risk_score} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Risk Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <RiskTrend data={dashboard.trend} />
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Active Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <AlertsList alerts={dashboard.active_alerts} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Security Recommendations</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3">
            {dashboard.recommendations.map((recommendation) => (
              <div className="rounded-md border p-3" key={recommendation.finding_key}>
                <div className="flex items-center justify-between gap-3">
                  <p className="font-medium">{recommendation.title}</p>
                  <Badge tone={recommendation.priority}>{recommendation.priority}</Badge>
                </div>
                <p className="mt-2 text-sm text-muted-foreground">{recommendation.remediation}</p>
              </div>
            ))}
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <CheckCircle2 className="h-4 w-4 text-primary" />
              Recommendations update after every scan.
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
