import { Skeleton } from "@/components/ui/skeleton";

export default function DomainsLoading() {
  return (
    <div className="grid gap-6">
      <Skeleton className="h-32" />
      <Skeleton className="h-96" />
    </div>
  );
}
