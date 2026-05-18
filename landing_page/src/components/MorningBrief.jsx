import { AlertTriangle, ClipboardList, FileText, Gauge } from "lucide-react";
import { sampleErcotMarketData } from "../data/sampleErcotMarketData.js";

function average(values) {
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function formatCurrency(value) {
  const sign = value < 0 ? "-" : "";
  return `${sign}$${Math.abs(value).toLocaleString(undefined, {
    maximumFractionDigits: 2,
  })}/MWh`;
}

function formatTimestamp(value) {
  return new Date(value.replace(" ", "T")).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
  });
}

function groupBy(rows, key) {
  return rows.reduce((groups, row) => {
    const groupKey = row[key];
    groups[groupKey] = groups[groupKey] || [];
    groups[groupKey].push(row);
    return groups;
  }, {});
}

function summarizeSettlementPoints(rows) {
  return Object.entries(groupBy(rows, "settlement_point"))
    .map(([settlementPoint, pointRows]) => ({
      settlementPoint,
      averagePrice: average(pointRows.map((row) => row.real_time_price)),
      maxPrice: Math.max(...pointRows.map((row) => row.real_time_price)),
      averageSpread: average(pointRows.map((row) => row.da_rt_spread)),
      averageLoadError: average(pointRows.map((row) => row.load_forecast_error_mw)),
    }))
    .sort((a, b) => b.maxPrice - a.maxPrice);
}

function Stat({ icon: Icon, label, value, note }) {
  return (
    <div className="brief-stat">
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

export default function MorningBrief() {
  const threshold = 150;
  const settlementSummary = summarizeSettlementPoints(sampleErcotMarketData);
  const spikes = [...sampleErcotMarketData]
    .filter((row) => row.real_time_price >= threshold)
    .sort((a, b) => b.real_time_price - a.real_time_price);
  const largestSpreads = [...sampleErcotMarketData]
    .sort((a, b) => Math.abs(b.da_rt_spread) - Math.abs(a.da_rt_spread))
    .slice(0, 4);
  const topLoadError = [...sampleErcotMarketData].sort(
    (a, b) => Math.abs(b.load_forecast_error_mw) - Math.abs(a.load_forecast_error_mw),
  )[0];
  const topPoint = settlementSummary[0];
  const averageSpread = average(sampleErcotMarketData.map((row) => row.da_rt_spread));

  return (
    <section className="brief-section" id="morning-brief">
      <div className="brief-shell">
        <div className="section-header">
          <p className="eyebrow">Project 3 automation</p>
          <h2>Automated morning market brief.</h2>
          <p>
            A desk-style Markdown report generated from mock ERCOT-style data:
            price summary, spike alerts, DA/RT misses, load forecast error, and items to watch.
          </p>
        </div>

        <div className="brief-stat-grid">
          <Stat
            icon={Gauge}
            label="Highest RT price"
            value={formatCurrency(topPoint.maxPrice)}
            note={topPoint.settlementPoint}
          />
          <Stat
            icon={AlertTriangle}
            label="Spike intervals"
            value={spikes.length.toLocaleString()}
            note={`At or above ${formatCurrency(threshold)}`}
          />
          <Stat
            icon={ClipboardList}
            label="Avg DA/RT spread"
            value={formatCurrency(averageSpread)}
            note="Day-ahead minus real-time"
          />
          <Stat
            icon={FileText}
            label="Largest load miss"
            value={`${Math.round(topLoadError.load_forecast_error_mw).toLocaleString()} MW`}
            note={topLoadError.settlement_point}
          />
        </div>

        <div className="brief-grid">
          <article className="brief-panel brief-copy-panel">
            <p className="brief-label">Mock-data morning note</p>
            <h3>Executive Summary</h3>
            <p>
              {topPoint.settlementPoint} recorded the highest real-time price in the sample at{" "}
              {formatCurrency(topPoint.maxPrice)}. {spikes.length} intervals cleared above the
              selected spike threshold. The average DA/RT spread was{" "}
              {formatCurrency(averageSpread)}, with the largest load forecast miss at{" "}
              {topLoadError.settlement_point}.
            </p>
            <h3>Items to Watch</h3>
            <ul>
              <li>Review whether high-price intervals are local or broad across ERCOT zones.</li>
              <li>Compare the largest negative DA/RT spreads against spike intervals.</li>
              <li>Check whether actual load exceeded forecast during elevated-price periods.</li>
            </ul>
          </article>

          <article className="brief-panel">
            <div className="chart-header">
              <h3>Largest DA/RT misses included in the brief</h3>
            </div>
            <div className="brief-list">
              {largestSpreads.map((row) => (
                <div className="brief-list-row" key={`${row.timestamp}-${row.settlement_point}`}>
                  <div>
                    <strong>{row.settlement_point}</strong>
                    <span>{formatTimestamp(row.timestamp)}</span>
                  </div>
                  <b>{formatCurrency(row.da_rt_spread)}</b>
                </div>
              ))}
            </div>
          </article>
        </div>
      </div>
    </section>
  );
}
