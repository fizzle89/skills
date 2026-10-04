// Pillar Trace client for Node 20+. No dependencies. Silent no-op without OBS_TOKEN.
const URL_ = (process.env.OBS_URL || 'https://pillar-fabric.onrender.com').replace(/\/$/, '');
const TOKEN = process.env.OBS_TOKEN || '';
const SKIP = ['/health', '/favicon.ico', '/robots.txt', '/sitemap.xml', '/llms.txt', '/style.css', '/app.js'];
let q = [];
const rid = n => [...Array(n)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');
async function flush() {
  if (!TOKEN || !q.length) return;
  const spans = q.splice(0, 200);
  try { await fetch(URL_ + '/api/obs/ingest', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + TOKEN }, body: JSON.stringify({ spans }), signal: AbortSignal.timeout(15000) }); }
  catch { if (q.length < 1000) q.unshift(...spans); }
}
if (TOKEN) setInterval(flush, 3000).unref();
export default function pillarObs(req, res, next) {
  if (!TOKEN || SKIP.includes(req.path)) return next();
  const start = Date.now();
  res.on('finish', () => {
    if (q.length > 2000) return;
    q.push({ trace_id: rid(16), span_id: rid(8), name: `${req.method} ${req.path}`, kind: 'http', start: start / 1000, duration_ms: Date.now() - start, status: res.statusCode >= 500 ? 'error' : 'ok', attrs: { status_code: res.statusCode } });
  });
  next();
};
