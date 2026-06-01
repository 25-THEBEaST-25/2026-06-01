import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const assets = [
  { host: "www.acme.example", services: "80, 443", posture: "monitored" },
  { host: "api.acme.example", services: "443", posture: "monitored" },
  { host: "vpn.acme.example", services: "443, 500, 4500", posture: "review" }
];

export default function AssetsPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Asset Discovery</CardTitle>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="w-full min-w-[620px] text-sm">
          <thead className="text-left text-muted-foreground">
            <tr>
              <th className="py-2">Asset</th>
              <th className="py-2">Public Services</th>
              <th className="py-2">Posture</th>
            </tr>
          </thead>
          <tbody>
            {assets.map((asset) => (
              <tr className="border-t" key={asset.host}>
                <td className="py-3 font-medium">{asset.host}</td>
                <td className="py-3">{asset.services}</td>
                <td className="py-3">
                  <Badge tone={asset.posture === "review" ? "medium" : "pass"}>{asset.posture}</Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
