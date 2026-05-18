import { BatteryCharging, CircleDollarSign, Gauge, Zap } from "lucide-react";
import { sampleErcotMarketData } from "../data/sampleErcotMarketData.js";

function formatCurrency(value) {
  const sign = value < 0 ? "-" : "";
  return `${sign}$${Math.abs(value).toLocaleString(undefined, {
    maximumFractionDigits: 0,
  })}`;
}

function formatPrice(value) {
  return `$${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}/MWh`;
}

function formatTimestamp(value) {
  return new Date(value.replace(" ", "T")).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
  });
}

function quantile(values, q) {
  const sorted = [...values].sort((a, b) => a - b);
  const index = (sorted.length - 1) * q;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower);
}

function simulateBattery(rows) {
  const capacity = 100;
  const power = 50;
  const efficiency = Math.sqrt(0.86);
  const prices = rows.map((row) => row.real_time_price);
  const chargeThreshold = quantile(prices, 0.3);
  const dischargeThreshold = quantile(prices, 0.75);
  let stateOfCharge = 50;

  return rows.map((row) => {
    let action = "Hold";
    let margin = 0;
    let dischargeMwh = 0;

    if (row.real_time_price <= chargeThreshold && stateOfCharge < capacity) {
      action = "Charge";
      const energyAdded = Math.min(power, capacity - stateOfCharge);
      margin = -(energyAdded / efficiency) * row.real_time_price;
      stateOfCharge += energyAdded;
    } else if (row.real_time_price >= dischargeThreshold && stateOfCharge > 0) {
      action = "Discharge";
      const energyRemoved = Math.min(power, stateOfCharge);
      dischargeMwh = energyRemoved * efficiency;
      margin = dischargeMwh * row.real_time_price;
      stateOfCharge -= energyRemoved;
    }

    return {
      ...row,
      action,
      intervalMargin: margin,
      dischargeMwh,
      stateOfCharge,
      chargeThreshold,
      dischargeThreshold,
    };
  });
}

function Stat({ icon: Icon, label, value, note }) {
  return (
    <div className="storage-stat">
      <div className="metric-icon">
        <Icon size={18} aria-hidden="true" />
      </div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
        <span>{note}</span>
      </div>
    </div>
  );
}

export default function BatteryArbitrage() {
  const settlementPoint = "HB_NORTH";
  const rows = sampleErcotMarketData
    .filter((row) => row.settlement_point === settlementPoint)
    .sort((a, b) => new Date(a.timestamp.replace(" ", "T")) - new Date(b.timestamp.replace(" ", "T")));
  const dispatch = simulateBattery(rows);
  const grossMargin = dispatch.reduce((sum, row) => sum + row.intervalMargin, 0);
  const dischargeIntervals = dispatch.filter((row) => row.action === "Discharge");
  const chargeIntervals = dispatch.filter((row) => row.action === "Charge");
  const totalDischargeMwh = dischargeIntervals.reduce((sum, row) => sum + row.dischargeMwh, 0);
  const topIntervals = [...dispatch].sort((a, b) => b.intervalMargin - a.intervalMargin).slice(0, 5);
  const maxMargin = Math.max(...topIntervals.map((row) => row.intervalMargin));

  return (
    <section className="storage-section" id="battery-arbitrage">
      <div className="storage-shell">
        <div className="section-header">
          <p className="eyebrow">Project 5 storage analytics</p>
          <h2>Battery arbitrage simulator.</h2>
          <p>
            A transparent mock-data dispatch model that translates ERCOT-style real-time prices
            into charge, hold, discharge, state-of-charge, and gross-margin outputs.
          </p>
        </div>

        <div className="storage-stat-grid">
          <Stat
            icon={CircleDollarSign}
            label="Simulated gross margin"
            value={formatCurrency(grossMargin)}
            note={`${settlementPoint}, before fees and degradation`}
          />
          <Stat
            icon={BatteryCharging}
            label="Charge intervals"
            value={chargeIntervals.length.toLocaleString()}
            note="Lower-price threshold rule"
          />
          <Stat
            icon={Zap}
            label="Discharge intervals"
            value={dischargeIntervals.length.toLocaleString()}
            note={`${Math.round(totalDischargeMwh).toLocaleString()} MWh delivered`}
          />
          <Stat
            icon={Gauge}
            label="Ending state of charge"
            value={`${Math.round(dispatch.at(-1).stateOfCharge)} MWh`}
            note="100 MWh sample battery"
          />
        </div>

        <div className="storage-grid">
          <article className="storage-panel">
            <div>
              <h3>Highest-value discharge intervals</h3>
              <p>Mock ERCOT-style prices, simple threshold dispatch, HB_NORTH.</p>
            </div>
            <div className="storage-bars">
              {topIntervals.map((row) => (
                <div className="storage-bar-row" key={row.timestamp}>
                  <span>{formatTimestamp(row.timestamp)}</span>
                  <div className="storage-bar-track">
                    <i style={{ width: `${(row.intervalMargin / maxMargin) * 100}%` }} />
                  </div>
                  <strong>{formatCurrency(row.intervalMargin)}</strong>
                </div>
              ))}
            </div>
          </article>

          <article className="storage-panel storage-copy-panel">
            <span className="brief-label">Mock-data strategy</span>
            <h3>Analyst takeaway</h3>
            <p>
              This section shows the portfolio workflow, not a trade recommendation: choose a
              settlement point, apply visible storage assumptions, calculate dispatch economics,
              and identify which intervals deserve follow-up.
            </p>
            <ul>
              <li>Next improvement: compare hubs and load zones side by side.</li>
              <li>Add degradation, end-of-day state-of-charge targets, and benchmark optimization.</li>
              <li>Connect live ERCOT/GridStatus prices before treating results as market observations.</li>
            </ul>
          </article>
        </div>
      </div>
    </section>
  );
}
