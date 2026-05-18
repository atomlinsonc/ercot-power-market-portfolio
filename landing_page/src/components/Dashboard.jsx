import { useMemo, useState } from "react";
import { AlertTriangle, Activity, Gauge, TrendingUp } from "lucide-react";
import { sampleErcotMarketData } from "../data/sampleErcotMarketData.js";

const dateRangeOptions = [
  { value: "all", label: "7 days" },
  { value: "first3", label: "First 3 days" },
  { value: "last3", label: "Last 3 days" },
];

const colors = {
  rt: "#006a64",
  da: "#235c96",
  spread: "#c47c18",
  load: "#5f4b8b",
  forecast: "#6d7b73",
};

function average(rows, key) {
  if (!rows.length) return 0;
  return rows.reduce((sum, row) => sum + row[key], 0) / rows.length;
}

function formatCurrency(value) {
  return `$${value.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

function formatMw(value) {
  return `${Math.round(value).toLocaleString()} MW`;
}

function formatTimestamp(value) {
  return new Date(value.replace(" ", "T")).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
  });
}

function toTime(value) {
  return new Date(value.replace(" ", "T")).getTime();
}

function buildLine(rows, key, minY, maxY, width, height, pad) {
  if (rows.length < 2) return "";
  const span = Math.max(maxY - minY, 1);
  return rows
    .map((row, index) => {
      const x = pad + (index / (rows.length - 1)) * (width - pad * 2);
      const y = height - pad - ((row[key] - minY) / span) * (height - pad * 2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}

function LineChart({ title, rows, series, unit = "$", zeroBaseline = false }) {
  const width = 760;
  const height = 260;
  const pad = 34;
  const values = rows.flatMap((row) => series.map((item) => row[item.key]));
  const minValue = zeroBaseline ? Math.min(0, ...values) : Math.min(...values);
  const maxValue = Math.max(...values);
  const yPad = Math.max((maxValue - minValue) * 0.12, 5);
  const minY = minValue - yPad;
  const maxY = maxValue + yPad;
  const yTicks = [maxY, (maxY + minY) / 2, minY];

  return (
    <div className="chart-panel">
      <div className="chart-header">
        <h3>{title}</h3>
        <div className="chart-legend">
          {series.map((item) => (
            <span key={item.key}>
              <i style={{ background: item.color }} />
              {item.label}
            </span>
          ))}
        </div>
      </div>
      <svg className="market-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label={title}>
        {yTicks.map((tick) => {
          const y = height - pad - ((tick - minY) / Math.max(maxY - minY, 1)) * (height - pad * 2);
          return (
            <g key={tick}>
              <line x1={pad} x2={width - pad} y1={y} y2={y} className="chart-grid-line" />
              <text x={8} y={y + 4} className="chart-tick">
                {unit === "$" ? formatCurrency(tick) : Math.round(tick).toLocaleString()}
              </text>
            </g>
          );
        })}
        {series.map((item) => (
          <polyline
            key={item.key}
            points={buildLine(rows, item.key, minY, maxY, width, height, pad)}
            fill="none"
            stroke={item.color}
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        ))}
        <text x={pad} y={height - 8} className="chart-tick">
          {formatTimestamp(rows[0].timestamp)}
        </text>
        <text x={width - 150} y={height - 8} className="chart-tick">
          {formatTimestamp(rows[rows.length - 1].timestamp)}
        </text>
      </svg>
    </div>
  );
}

function Metric({ icon: Icon, label, value, note }) {
  return (
    <div className="metric-card">
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

export default function Dashboard() {
  const settlementPoints = useMemo(
    () => [...new Set(sampleErcotMarketData.map((row) => row.settlement_point))],
    [],
  );
  const [settlementPoint, setSettlementPoint] = useState("HB_NORTH");
  const [dateRange, setDateRange] = useState("all");
  const [threshold, setThreshold] = useState(150);

  const rows = useMemo(() => {
    const pointRows = sampleErcotMarketData
      .filter((row) => row.settlement_point === settlementPoint)
      .sort((a, b) => toTime(a.timestamp) - toTime(b.timestamp));

    if (dateRange === "first3") return pointRows.slice(0, 72);
    if (dateRange === "last3") return pointRows.slice(-72);
    return pointRows;
  }, [dateRange, settlementPoint]);

  const latest = rows[rows.length - 1];
  const spikes = rows
    .filter((row) => row.real_time_price >= threshold)
    .sort((a, b) => b.real_time_price - a.real_time_price);
  const maxRow = rows.reduce((best, row) =>
    row.real_time_price > best.real_time_price ? row : best,
  rows[0]);
  const avgRt = average(rows, "real_time_price");
  const avgSpread = average(rows, "da_rt_spread");
  const avgLoadError = average(rows, "load_forecast_error_mw");
  const biggestSpikeText = spikes.length
    ? `${formatTimestamp(spikes[0].timestamp)} at ${formatCurrency(spikes[0].real_time_price)}/MWh`
    : "No intervals above the selected threshold";

  return (
    <section className="dashboard-section" id="dashboard">
      <div className="dashboard-shell">
        <div className="dashboard-title-row">
          <div>
            <p className="eyebrow">Project 1 dashboard</p>
            <h2>ERCOT Real-Time Market Dashboard</h2>
            <p>
              Mock ERCOT-style data for the first portfolio milestone. Live public
              ERCOT/GridStatus integration is the next data-source step.
            </p>
          </div>
          <a className="dashboard-repo-link" href="https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/src/dashboard">
            View Streamlit source
          </a>
        </div>

        <div className="dashboard-controls" aria-label="Dashboard controls">
          <label>
            Hub / load zone
            <select value={settlementPoint} onChange={(event) => setSettlementPoint(event.target.value)}>
              {settlementPoints.map((point) => (
                <option value={point} key={point}>
                  {point}
                </option>
              ))}
            </select>
          </label>
          <label>
            Date range
            <select value={dateRange} onChange={(event) => setDateRange(event.target.value)}>
              {dateRangeOptions.map((option) => (
                <option value={option.value} key={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Spike threshold: {formatCurrency(threshold)}/MWh
            <input
              type="range"
              min="50"
              max="500"
              step="25"
              value={threshold}
              onChange={(event) => setThreshold(Number(event.target.value))}
            />
          </label>
        </div>

        <div className="metric-grid">
          <Metric icon={Gauge} label="Latest RT price" value={`${formatCurrency(latest.real_time_price)}/MWh`} note={formatTimestamp(latest.timestamp)} />
          <Metric icon={Activity} label="Average RT price" value={`${formatCurrency(avgRt)}/MWh`} note={`${rows.length} hourly intervals`} />
          <Metric icon={TrendingUp} label="Max RT price" value={`${formatCurrency(maxRow.real_time_price)}/MWh`} note={formatTimestamp(maxRow.timestamp)} />
          <Metric icon={AlertTriangle} label="Spike intervals" value={spikes.length.toLocaleString()} note={`Threshold: ${formatCurrency(threshold)}/MWh`} />
        </div>

        <div className="dashboard-summary">
          <strong>Auto summary:</strong> Real-time prices exceeded the selected
          threshold during {spikes.length} intervals. The largest spike was
          {` ${biggestSpikeText}`}. Average DA/RT spread was {formatCurrency(avgSpread)}/MWh,
          and average load forecast error was {formatMw(avgLoadError)}.
        </div>

        <div className="chart-grid">
          <LineChart
            title="Real-time price over time"
            rows={rows}
            series={[{ key: "real_time_price", label: "Real-time", color: colors.rt }]}
          />
          <LineChart
            title="Day-ahead vs real-time price"
            rows={rows}
            series={[
              { key: "real_time_price", label: "Real-time", color: colors.rt },
              { key: "day_ahead_price", label: "Day-ahead", color: colors.da },
            ]}
          />
          <LineChart
            title="DA/RT spread over time"
            rows={rows}
            series={[{ key: "da_rt_spread", label: "DA minus RT", color: colors.spread }]}
            zeroBaseline
          />
          <LineChart
            title="Load forecast vs actual load"
            rows={rows}
            unit="MW"
            series={[
              { key: "forecast_load_mw", label: "Forecast", color: colors.forecast },
              { key: "actual_load_mw", label: "Actual", color: colors.load },
            ]}
          />
        </div>

        <div className="spike-table-panel">
          <div>
            <h3>Price Spike Alerts</h3>
            <p>Intervals above the selected real-time price threshold.</p>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Settlement point</th>
                  <th>RT price</th>
                  <th>DA price</th>
                  <th>DA/RT spread</th>
                  <th>Load error</th>
                </tr>
              </thead>
              <tbody>
                {spikes.slice(0, 10).map((row) => (
                  <tr key={`${row.timestamp}-${row.settlement_point}`}>
                    <td>{formatTimestamp(row.timestamp)}</td>
                    <td>{row.settlement_point}</td>
                    <td>{formatCurrency(row.real_time_price)}</td>
                    <td>{formatCurrency(row.day_ahead_price)}</td>
                    <td>{formatCurrency(row.da_rt_spread)}</td>
                    <td>{formatMw(row.load_forecast_error_mw)}</td>
                  </tr>
                ))}
                {!spikes.length && (
                  <tr>
                    <td colSpan="6">No intervals exceeded the selected threshold.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
