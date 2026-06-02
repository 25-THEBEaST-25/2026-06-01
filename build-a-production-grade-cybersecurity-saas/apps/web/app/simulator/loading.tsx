import { Skeleton } from "@/components/ui/skeleton";

export default function SimulatorLoading() {
  return (
    <div className="grid gap-6">
      <div className="grid gap-4 xl:grid-cols-4">
        <Skeleton className="h-36" />
        <Skeleton className="h-36" />
        <Skeleton className="h-36" />
        <Skeleton className="h-36" />
      </div>
      <Skeleton className="h-96" />
    </div>
  );
}
