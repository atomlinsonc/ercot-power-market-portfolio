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
    status: "Upcoming",
    description:
      "Repeatable daily report that summarizes prices, spreads, load forecast error, spike alerts, and items to watch.",
    skills: ["Automation", "Markdown reports", "Desk workflow"],
    links: {
      report: "#",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio",
    },
  },
  {
    title: "Price Spike Event Studies",
    status: "Upcoming",
    description:
      "Event-study workflow for identifying abnormal intervals and documenting possible drivers around high-price periods.",
    skills: ["Event studies", "Alerts", "Market commentary"],
    links: {
      report: "#",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio",
    },
  },
  {
    title: "Battery Arbitrage Simulator",
    status: "Upcoming",
    description:
      "Simple storage dispatch model to estimate charging, discharging, and gross margin under selected price assumptions.",
    skills: ["Optimization", "Python", "Energy storage"],
    links: {
      report: "#",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio",
    },
  },
  {
    title: "ERCOT Market Rules Tracker",
    status: "Upcoming",
    description:
      "Structured tracker for ERCOT market rule changes, NPRRs, key dates, and analyst notes on possible market impact.",
    skills: ["Research", "Documentation", "Market rules"],
    links: {
      report: "#",
      github: "https://github.com/atomlinsonc/ercot-power-market-portfolio",
    },
  },
];
