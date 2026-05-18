import { BarChart3, Clock, LineChart, Target } from "lucide-react";
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

function buildSettlementSummary(rows) {
  return Object.entries(groupBy(rows, "settlement_point"))
    .map(([settlementPoint, pointRows]) => ({
      settlementPoint,
      averageSpread: average(pointRows.map((row) => row.da_rt_spread)),
      averageAbsoluteSpread: average(pointRows.map((row) => Math.abs(row.da_rt_spread))),
      maxPositiveSpread: Math.max(...pointRows.map((row) => row.da_rt_spread)),
      maxNegativeSpread: Math.min(...pointRows.map((row) => row.da_rt_spread)),
    }))
    .sort((a, b) => b.averageAbsoluteSpread - a.averageAbsoluteSpread);
}

function buildHourlySummary(rows) {
  return Object.entries(
    rows.reduce((groups, row) => {
      const hour = new Date(row.timestamp.replace(" ", "T")).getHours();
      groups[hour] = groups[hour] || [];
      groups[hour].push(row);
      return groups;
    }, {}),
  )
    .map(([hour, hourRows]) => ({
      hour: Number(hour),
      averageAbsoluteSpread: average(hourRows.map((row) => Math.abs(row.da_rt_spread))),
      averageSpread: average(hourRows.map((row) => row.da_rt_spread)),
    }))
    .sort((a, b) => b.averageAbsoluteSpread - a.averageAbsoluteSpread);
}

function Stat({ icon: Icon, label, value, note }) {
  return (
    <div className="spread-stat">
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

export default function SpreadAnalysis() {
  const settlementSummary = buildSettlementSummary(sampleErcotMarketData);
  const hourlySummary = buildHourlySummary(sampleErcotMarketData);
  const largestMisses = [...sampleErcotMarketData]
    .sort((a, b) => Math.abs(b.da_rt_spread) - Math.abs(a.da_rt_spread))
    .slice(0, 5);
  const averageSpread = average(sampleErcotMarketData.map((row) => row.da_rt_spread));
  const averageAbsoluteSpread = average(
    sampleErcotMarketData.map((row) => Math.abs(row.da_rt_spread)),
  );
  const topPoint = settlementSummary[0];
  const topHour = hourlySummary[0];
  const maxBar = topPoint.averageAbsoluteSpread;
  const maxHourBar = topHour.averageAbsoluteSpread;

  return (
    <section className="spread-section" id="spread-analysis">
      <div className="spread-shell">
        <div className="section-header">
          <p className="eyebrow">Project 2 analysis</p>
          <h2>Day-ahead versus real-time spread analysis.</h2>
          <p>
            A focused mock-data workflow for ranking ERCOT market misses by
            settlement point and operating hour before live public data is connected.
          </p>
        </div>

        <div className="spread-stat-grid">
          <Stat
            icon={LineChart}
            label="Average DA/RT spread"
            value={formatCurrency(averageSpread)}
            note="Day-ahead minus real-time"
          />
          <Stat
            icon={Target}
            label="Average absolute spread"
            value={formatCurrency(averageAbsoluteSpread)}
            note="Across all sample intervals"
          />
          <Stat
            icon={BarChart3}
            label="Highest avg abs spread"
            value={topPoint.settlementPoint}
            note={formatCurrency(topPoint.averageAbsoluteSpread)}
          />
          <Stat
            icon={Clock}
            label="Highest spread hour"
            value={`${String(topHour.hour).padStart(2, "0")}:00`}
            note={formatCurrency(topHour.averageAbsoluteSpread)}
          />
        </div>

        <div className="spread-grid">
          <div className="spread-panel">
            <div className="chart-header">
              <h3>Settlement points ranked by average absolute spread</h3>
            </div>
            <div className="spread-bars">
              {settlementSummary.slice(0, 6).map((row) => (
                <div className="spread-bar-row" key={row.settlementPoint}>
                  <span>{row.settlementPoint}</span>
                  <div className="spread-bar-track">
                    <i style={{ width: `${(row.averageAbsoluteSpread / maxBar) * 100}%` }} />
                  </div>
                  <strong>{formatCurrency(row.averageAbsoluteSpread)}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="spread-panel">
            <div className="chart-header">
              <h3>Operating hours with largest average misses</h3>
            </div>
            <div className="spread-bars">
              {hourlySummary.slice(0, 6).map((row) => (
                <div className="spread-bar-row" key={row.hour}>
                  <span>{String(row.hour).padStart(2, "0")}:00</span>
                  <div className="spread-bar-track">
                    <i style={{ width: `${(row.averageAbsoluteSpread / maxHourBar) * 100}%` }} />
                  </div>
                  <strong>{formatCurrency(row.averageAbsoluteSpread)}</strong>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="spread-panel spread-table-panel">
          <div>
            <h3>Largest DA/RT market misses</h3>
            <p>
              Negative spread means real-time settled above day-ahead. Values are
              from mock ERCOT-style sample data.
            </p>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Settlement point</th>
                  <th>DA price</th>
                  <th>RT price</th>
                  <th>DA/RT spread</th>
                  <th>Load error</th>
                </tr>
              </thead>
              <tbody>
                {largestMisses.map((row) => (
                  <tr key={`${row.timestamp}-${row.settlement_point}`}>
                    <td>{formatTimestamp(row.timestamp)}</td>
                    <td>{row.settlement_point}</td>
                    <td>{formatCurrency(row.day_ahead_price)}</td>
                    <td>{formatCurrency(row.real_time_price)}</td>
                    <td>{formatCurrency(row.da_rt_spread)}</td>
                    <td>{Math.round(row.load_forecast_error_mw).toLocaleString()} MW</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
