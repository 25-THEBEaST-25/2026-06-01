import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const users = [
  { email: "admin@cyberriskradar.dev", role: "admin", status: "active" },
  { email: "analyst@acme.example", role: "analyst", status: "active" },
  { email: "viewer@acme.example", role: "viewer", status: "invited" }
];

export default function AdminPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Admin Dashboard</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-3">
        {users.map((user) => (
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-md border p-3" key={user.email}>
            <div>
              <p className="font-medium">{user.email}</p>
              <p className="text-sm text-muted-foreground">{user.role}</p>
            </div>
            <Badge tone={user.status === "active" ? "pass" : "low"}>{user.status}</Badge>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
