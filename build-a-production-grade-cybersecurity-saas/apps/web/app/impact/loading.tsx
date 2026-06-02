import { Skeleton } from "@/components/ui/skeleton";

export default function ImpactLoading() {
  return (
    <div className="grid gap-6">
      <div className="grid gap-4 xl:grid-cols-3">
        <Skeleton className="h-36" />
        <Skeleton className="h-36" />
        <Skeleton className="h-36" />
      </div>
      <Skeleton className="h-80" />
    </div>
  );
}
