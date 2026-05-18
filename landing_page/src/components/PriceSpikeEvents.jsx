import { Activity, Clock, MapPin, Zap } from "lucide-react";
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

function buildEventContext(rows, threshold) {
  return [...rows]
    .filter((row) => row.real_time_price >= threshold)
    .sort((a, b) => b.real_time_price - a.real_time_price)
    .slice(0, 5)
    .map((event, index) => {
      const eventTime = new Date(event.timestamp.replace(" ", "T"));
      const pointRows = rows.filter((row) => row.settlement_point === event.settlement_point);
      const preRows = pointRows.filter((row) => {
        const rowTime = new Date(row.timestamp.replace(" ", "T"));
        const hourDelta = (eventTime - rowTime) / 36e5;
        return hourDelta > 0 && hourDelta <= 2;
      });
      const postRows = pointRows.filter((row) => {
        const rowTime = new Date(row.timestamp.replace(" ", "T"));
        const hourDelta = (rowTime - eventTime) / 36e5;
        return hourDelta > 0 && hourDelta <= 2;
      });

      return {
        ...event,
        eventId: index + 1,
        preAveragePrice: average(preRows.map((row) => row.real_time_price)),
        postAveragePrice: average(postRows.map((row) => row.real_time_price)),
      };
    });
}

function Stat({ icon: Icon, label, value, note }) {
  return (
    <div className="event-stat">
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

export default function PriceSpikeEvents() {
  const threshold = 150;
  const events = buildEventContext(sampleErcotMarketData, threshold);
  const topEvent = events[0];
  const eventWindow = sampleErcotMarketData
    .filter((row) => row.settlement_point === topEvent.settlement_point)
    .filter((row) => {
      const rowTime = new Date(row.timestamp.replace(" ", "T"));
      const eventTime = new Date(topEvent.timestamp.replace(" ", "T"));
      return Math.abs((rowTime - eventTime) / 36e5) <= 2;
    });

  return (
    <section className="event-section" id="price-spike-events">
      <div className="event-shell">
        <div className="section-header">
          <p className="eyebrow">Project 4 event studies</p>
          <h2>Price spike event-study workflow.</h2>
          <p>
            A structured way to review high-price intervals with pre-event and post-event context,
            DA/RT spread, and load forecast error before writing market-observation notes.
          </p>
        </div>

        <div className="event-stat-grid">
          <Stat
            icon={Zap}
            label="Top spike"
            value={formatCurrency(topEvent.real_time_price)}
            note={topEvent.settlement_point}
          />
          <Stat
            icon={Clock}
            label="Event interval"
            value={formatTimestamp(topEvent.timestamp)}
            note="Highest mock-data interval"
          />
          <Stat
            icon={Activity}
            label="DA/RT spread"
            value={formatCurrency(topEvent.da_rt_spread)}
            note="Negative means RT premium"
          />
          <Stat
            icon={MapPin}
            label="Events reviewed"
            value={events.length.toLocaleString()}
            note={`Top intervals above ${formatCurrency(threshold)}`}
          />
        </div>

        <div className="event-grid">
          <article className="event-panel">
            <div>
              <h3>Top spike events</h3>
              <p>Each row is a mock-data interval above the selected threshold.</p>
            </div>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Event</th>
                    <th>Timestamp</th>
                    <th>Point</th>
                    <th>RT price</th>
                    <th>DA/RT spread</th>
                    <th>Load error</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((event) => (
                    <tr key={`${event.timestamp}-${event.settlement_point}`}>
                      <td>{event.eventId}</td>
                      <td>{formatTimestamp(event.timestamp)}</td>
                      <td>{event.settlement_point}</td>
                      <td>{formatCurrency(event.real_time_price)}</td>
                      <td>{formatCurrency(event.da_rt_spread)}</td>
                      <td>{Math.round(event.load_forecast_error_mw).toLocaleString()} MW</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </article>

          <article className="event-panel">
            <div>
              <h3>Top event window</h3>
              <p>Same settlement point, two hours before and after the top spike.</p>
            </div>
            <div className="event-window">
              {eventWindow.map((row) => {
                const rowTime = new Date(row.timestamp.replace(" ", "T"));
                const eventTime = new Date(topEvent.timestamp.replace(" ", "T"));
                const relativeHour = Math.round((rowTime - eventTime) / 36e5);
                return (
                  <div className={relativeHour === 0 ? "event-window-row active" : "event-window-row"} key={row.timestamp}>
                    <span>{relativeHour > 0 ? `+${relativeHour}` : relativeHour}h</span>
                    <strong>{formatCurrency(row.real_time_price)}</strong>
                    <em>{formatCurrency(row.da_rt_spread)}</em>
                  </div>
                );
              })}
            </div>
          </article>
        </div>
      </div>
    </section>
  );
}
