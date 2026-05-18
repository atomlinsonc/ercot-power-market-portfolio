import BatteryArbitrage from "./components/BatteryArbitrage.jsx";
import Contact from "./components/Contact.jsx";
import Dashboard from "./components/Dashboard.jsx";
import Hero from "./components/Hero.jsx";
import MarketRulesTracker from "./components/MarketRulesTracker.jsx";
import MorningBrief from "./components/MorningBrief.jsx";
import PriceSpikeEvents from "./components/PriceSpikeEvents.jsx";
import SpreadAnalysis from "./components/SpreadAnalysis.jsx";

export default function App() {
  return (
    <main>
      <Hero />
      <Dashboard />
      <SpreadAnalysis />
      <MorningBrief />
      <PriceSpikeEvents />
      <BatteryArbitrage />
      <MarketRulesTracker />
      <Contact />
    </main>
  );
}
