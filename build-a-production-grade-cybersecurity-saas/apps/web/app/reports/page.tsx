import { ReportDownload } from "@/components/report-download";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ReportsPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>PDF Reports</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div className="rounded-md border p-4">
          <p className="font-medium">Executive Risk Report</p>
          <p className="mt-1 text-sm text-muted-foreground">
            Includes executive summary, findings, score history, and remediation recommendations.
          </p>
          <div className="mt-4">
            <ReportDownload />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
