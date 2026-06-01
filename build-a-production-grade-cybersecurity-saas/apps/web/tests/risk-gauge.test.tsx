import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RiskGauge } from "@/components/dashboard/risk-gauge";

describe("RiskGauge", () => {
  it("renders the provided score", () => {
    render(<RiskGauge score={82} />);
    expect(screen.getByText("82")).toBeTruthy();
  });
});
