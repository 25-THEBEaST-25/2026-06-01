import type * as React from "react";

import { cn } from "@/lib/utils";

const tones = {
  critical: "bg-red-500/15 text-red-600 dark:text-red-300",
  high: "bg-orange-500/15 text-orange-700 dark:text-orange-300",
  medium: "bg-amber-500/15 text-amber-700 dark:text-amber-300",
  low: "bg-cyan-500/15 text-cyan-700 dark:text-cyan-300",
  info: "bg-slate-500/15 text-slate-700 dark:text-slate-300",
  pass: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
  fail: "bg-red-500/15 text-red-600 dark:text-red-300",
  warn: "bg-amber-500/15 text-amber-700 dark:text-amber-300"
};

export function Badge({
  tone = "info",
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & { tone?: keyof typeof tones }) {
  return (
    <span
      className={cn("inline-flex items-center rounded-md px-2 py-1 text-xs font-medium", tones[tone], className)}
      {...props}
    />
  );
}
