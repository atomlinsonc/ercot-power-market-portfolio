export const projects = [
  {
    title: "ERCOT Real-Time Market Dashboard",
    status: "Active",
    description:
      "Streamlit dashboard for monitoring real-time prices, day-ahead comparisons, DA/RT spreads, load forecast error, and spike intervals.",
    skills: ["Python", "Streamlit", "pandas", "Plotly", "Market reporting"],
    links: {
      dashboard: "#dashboard",
      report: "#",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/projects/01_realtime_market_dashboard",
    },
  },
  {
    title: "Day-Ahead vs Real-Time Spread Analysis",
    status: "Active",
    description:
      "Python analysis workflow for ranking ERCOT DA/RT market misses by settlement point, operating hour, and abnormal spread intervals.",
    skills: ["Python", "pandas", "Time series", "Spread analysis"],
    links: {
      report: "#spread-analysis",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/projects/02_da_rt_spread_analysis",
    },
  },
  {
    title: "Automated Morning Market Brief",
    status: "Active",
    description:
      "Repeatable daily report that summarizes prices, spreads, load forecast error, spike alerts, and items to watch.",
    skills: ["Python", "Automation", "Markdown reports", "Desk workflow"],
    links: {
      report: "#morning-brief",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/projects/03_automated_morning_market_brief",
    },
  },
  {
    title: "Price Spike Event Studies",
    status: "Active",
    description:
      "Event-study workflow for identifying abnormal intervals and documenting possible drivers around high-price periods.",
    skills: ["Python", "Event studies", "Alerts", "Market commentary"],
    links: {
      report: "#price-spike-events",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/projects/04_price_spike_event_studies",
    },
  },
  {
    title: "Battery Arbitrage Simulator",
    status: "Active",
    description:
      "Transparent storage dispatch model that estimates charge/discharge behavior, state of charge, and gross margin from ERCOT-style prices.",
    skills: ["Python", "Storage analytics", "Time series", "Asset optimization"],
    links: {
      report: "#battery-arbitrage",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/projects/05_battery_arbitrage_simulator",
    },
  },
  {
    title: "ERCOT Market Rules Tracker",
    status: "Active",
    description:
      "Source-linked NPRR watchlist for tracking rule status, priority, impact areas, and analyst notes for market commentary.",
    skills: ["Research", "NPRR tracking", "Documentation", "Market rules"],
    links: {
      report: "#market-rules",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio/tree/main/projects/06_ercot_market_rules_tracker",
    },
  },
];
