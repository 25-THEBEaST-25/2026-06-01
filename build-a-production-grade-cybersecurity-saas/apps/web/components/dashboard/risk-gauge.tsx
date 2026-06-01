export function RiskGauge({ score }: { score: number }) {
  const clamped = Math.max(0, Math.min(score, 100));
  const color = clamped >= 85 ? "#10b981" : clamped >= 70 ? "#f59e0b" : "#ef4444";

  return (
    <div className="flex items-center justify-center">
      <div
        className="grid h-44 w-44 place-items-center rounded-full"
        style={{ background: `conic-gradient(${color} ${clamped * 3.6}deg, hsl(var(--muted)) 0deg)` }}
      >
        <div className="grid h-32 w-32 place-items-center rounded-full bg-card">
          <div className="text-center">
            <div className="text-4xl font-bold">{clamped}</div>
            <div className="text-xs uppercase tracking-wide text-muted-foreground">Risk score</div>
          </div>
        </div>
      </div>
    </div>
  );
}
