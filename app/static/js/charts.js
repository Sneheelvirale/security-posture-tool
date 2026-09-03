/**
 * SecurePosture — Chart.js Helper Functions
 * Reusable chart generators matching the application theme.
 */

const ChartTheme = {
  primary: '#1a1a2e',
  primaryLight: '#16213e',
  secondary: '#0f3460',
  accent: '#e94560',
  success: '#53a653',
  warning: '#f0a500',
  info: '#4ea8de',
  gridColor: 'rgba(0, 0, 0, 0.06)',
  scoreColors: ['#dc3545', '#e74c3c', '#f39c12', '#f1c40f', '#7dcea0', '#27ae60'],
  functionColors: {
    Identify: 'rgba(30, 64, 175, 0.7)',
    Protect:  'rgba(6, 95, 70, 0.7)',
    Detect:   'rgba(146, 64, 14, 0.7)',
    Respond:  'rgba(153, 27, 27, 0.7)',
    Recover:  'rgba(91, 33, 182, 0.7)',
  }
};

/**
 * Radar Chart for NIST CSF Functions (pentagon)
 * @param {string} canvasId - Canvas element ID
 * @param {string[]} labels - Function names (Identify, Protect, etc.)
 * @param {number[]} data - Current scores (0-5 scale)
 * @param {number[]|null} targetData - Optional target scores
 * @param {string} title - Chart title
 * @returns {Chart}
 */
function createRadarChart(canvasId, labels, data, targetData = null, title = 'NIST CSF Maturity by Function') {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const datasets = [
    {
      label: 'Current Score',
      data: data,
      backgroundColor: 'rgba(15, 52, 96, 0.2)',
      borderColor: ChartTheme.secondary,
      pointBackgroundColor: ChartTheme.secondary,
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: ChartTheme.secondary,
      pointRadius: 4,
      borderWidth: 2,
    }
  ];

  if (targetData) {
    datasets.push({
      label: 'Target (Defined / Level 3)',
      data: targetData,
      backgroundColor: 'rgba(83, 166, 83, 0.1)',
      borderColor: ChartTheme.success,
      borderDash: [5, 5],
      pointBackgroundColor: ChartTheme.success,
      pointBorderColor: '#fff',
      pointRadius: 3,
      borderWidth: 1.5,
    });
  }

  return new Chart(ctx, {
    type: 'radar',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: !!title, text: title, font: { size: 14, weight: 'bold' } },
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)} / 5.0`
          }
        }
      },
      scales: {
        r: {
          min: 0,
          max: 5,
          ticks: { stepSize: 1, backdropColor: 'transparent' },
          grid: { color: ChartTheme.gridColor },
          angleLines: { color: ChartTheme.gridColor },
          pointLabels: { font: { size: 12, weight: '600' } }
        }
      }
    }
  });
}

/**
 * Bar Chart for Maturity / Score Distributions
 * @param {string} canvasId - Canvas element ID
 * @param {string[]} labels - Bar labels
 * @param {number[]} data - Values
 * @param {string} title - Chart title
 * @param {string[]} colors - Optional custom colors array
 * @returns {Chart}
 */
function createBarChart(canvasId, labels, data, title = '', colors = null) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const bgColors = colors || data.map((_, i) => ChartTheme.scoreColors[i % ChartTheme.scoreColors.length]);

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Controls',
        data: data,
        backgroundColor: bgColors,
        borderColor: bgColors.map(c => c.replace(/[\d.]+\)$/g, '1)')),
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: !!title, text: title, font: { size: 14, weight: 'bold' } },
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.raw} control${ctx.raw === 1 ? '' : 's'}`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, precision: 0 },
          grid: { color: ChartTheme.gridColor }
        }
      }
    }
  });
}

/**
 * Doughnut Chart for Evidence Status Distribution
 * @param {string} canvasId - Canvas element ID
 * @param {string[]} labels - ['None', 'Partial', 'Full']
 * @param {number[]} data - Counts
 * @param {string} title - Chart title
 * @returns {Chart}
 */
function createDoughnutChart(canvasId, labels, data, title = 'Evidence Status') {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const defaultColors = [ChartTheme.accent, ChartTheme.warning, ChartTheme.success];

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: defaultColors,
        borderWidth: 2,
        borderColor: '#fff',
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        title: { display: !!title, text: title, font: { size: 14, weight: 'bold' } },
        legend: { position: 'bottom', labels: { boxWidth: 14, padding: 12 } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
              const pct = total ? ((ctx.raw / total) * 100).toFixed(1) : 0;
              return `${ctx.label}: ${ctx.raw} (${pct}%)`;
            }
          }
        }
      }
    }
  });
}

/**
 * Gap Heatmap — Draws a grid of control maturity blocks on a raw canvas
 * @param {string} canvasId - Canvas element ID
 * @param {Array<{ref: string, score: number, function: string}>} data
 */
function createGapHeatmap(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();

  canvas.width = rect.width * dpr;
  canvas.height = (Math.ceil(data.length / 10) * 44 + 40) * dpr;
  canvas.style.height = `${Math.ceil(data.length / 10) * 44 + 40}px`;
  ctx.scale(dpr, dpr);

  const cols = Math.min(10, data.length);
  const padding = 6;
  const cellSize = Math.floor((rect.width - (cols + 1) * padding) / cols);

  ctx.clearRect(0, 0, rect.width, rect.height);

  data.forEach((item, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = padding + col * (cellSize + padding);
    const y = padding + row * (cellSize + padding);

    const score = Math.min(5, Math.max(0, Math.round(item.score)));
    ctx.fillStyle = ChartTheme.scoreColors[score];

    // Rounded rectangle
    const r = 4;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + cellSize - r, y);
    ctx.quadraticCurveTo(x + cellSize, y, x + cellSize, y + r);
    ctx.lineTo(x + cellSize, y + cellSize - r);
    ctx.quadraticCurveTo(x + cellSize, y + cellSize, x + cellSize - r, y + cellSize);
    ctx.lineTo(x + r, y + cellSize);
    ctx.quadraticCurveTo(x, y + cellSize, x, y + cellSize - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
    ctx.fill();

    // Ref text
    ctx.fillStyle = score >= 2 && score <= 3 ? '#222' : '#fff';
    ctx.font = 'bold 9px "Segoe UI", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(item.ref, x + cellSize / 2, y + cellSize / 2 - 5);

    // Score text
    ctx.font = '8px "Segoe UI", sans-serif';
    ctx.fillText(`L${score}`, x + cellSize / 2, y + cellSize / 2 + 7);
  });
}

/**
 * Score Gauge — Circular arc indicating overall posture score
 * @param {string} canvasId - Canvas element ID
 * @param {number} score - 0 to 5 (or 0 to 100)
 * @param {number} maxScore - default 5
 * @param {string} label - sub-label below score
 * @returns {Chart}
 */
function createScoreGauge(canvasId, score, maxScore = 5, label = 'Maturity Score') {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const normalized = Math.min(maxScore, Math.max(0, score));
  const pct = (normalized / maxScore) * 100;
  const scoreIndex = Math.min(5, Math.max(0, Math.round((normalized / maxScore) * 5)));
  const fillColor = ChartTheme.scoreColors[scoreIndex];

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Score', 'Remaining'],
      datasets: [{
        data: [normalized, maxScore - normalized],
        backgroundColor: [fillColor, '#e9ecef'],
        borderWidth: 0,
        circumference: 240,
        rotation: 240,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '78%',
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false },
      }
    },
    plugins: [{
      id: 'gaugeCenterText',
      afterDraw(chart) {
        const { ctx, chartArea: { top, bottom, left, right } } = chart;
        const cx = (left + right) / 2;
        const cy = (top + bottom) / 2 + 10;

        ctx.save();
        ctx.textAlign = 'center';

        // Score value
        ctx.font = 'bold 2rem "Segoe UI", sans-serif';
        ctx.fillStyle = ChartTheme.primary;
        ctx.fillText(normalized.toFixed(1), cx, cy);

        // Max scale
        ctx.font = '0.8rem "Segoe UI", sans-serif';
        ctx.fillStyle = '#6c757d';
        ctx.fillText(`/ ${maxScore.toFixed(1)}`, cx, cy + 18);

        // Label
        ctx.font = '600 0.85rem "Segoe UI", sans-serif';
        ctx.fillStyle = fillColor;
        ctx.fillText(label, cx, cy + 36);

        ctx.restore();
      }
    }]
  });
}
