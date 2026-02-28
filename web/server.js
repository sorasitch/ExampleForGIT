"use strict";

const express = require("express");
const path = require("path");
const fs = require("fs");
const rateLimit = require("express-rate-limit");

const app = express();
const PORT = process.env.PORT || 3000;

// Rate-limit API requests (100 req / 15 min per IP)
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});
app.use("/api/", apiLimiter);

// Serve static assets (images, CSS, JS)
app.use(express.static(path.join(__dirname, "public")));

// Load chart metadata once at startup
const chartsMetaPath = path.join(__dirname, "charts_meta.json");
let chartsMeta;
try {
  chartsMeta = JSON.parse(fs.readFileSync(chartsMetaPath, "utf8"));
} catch (err) {
  console.error(
    `ERROR: Could not load charts_meta.json at ${chartsMetaPath}\n` +
    "Run 'npm run generate' (python3 ../python/generate_charts.py) first.\n" +
    err.message
  );
  process.exit(1);
}

// API endpoint – returns chart metadata as JSON
app.get("/api/charts", (_req, res) => {
  res.json(chartsMeta);
});

// Home route – serves the main page
app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`🚀  Futuristic Dashboard running at http://localhost:${PORT}`);
});
