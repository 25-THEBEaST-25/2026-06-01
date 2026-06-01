import { AlertTriangle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import type { DashboardResponse } from "@/lib/types";

export function AlertsList({ alerts }: { alerts: DashboardResponse["active_alerts"] }) {
  return (
    <div className="grid gap-3">
      {alerts.map((alert) => (
        <div className="flex items-start gap-3 rounded-md border p-3" key={`${alert.asset}-${alert.title}`}>
          <AlertTriangle className="mt-0.5 h-4 w-4 text-primary" />
          <div className="min-w-0 flex-1">
            <p className="font-medium">{alert.title}</p>
            <p className="text-sm text-muted-foreground">{alert.asset}</p>
          </div>
          <Badge tone={alert.severity}>{alert.severity}</Badge>
        </div>
      ))}
    </div>
  );
}
