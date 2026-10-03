/**
 * BusBabu Benchmark Script
 * Measures query latency, graph construction time, memory usage, and routing coverage.
 */
import { readFileSync } from 'fs';
import { performance } from 'perf_hooks';

// Load data
const raw = JSON.parse(readFileSync('./public/busdata.json', 'utf-8'));

class BusRouter {
  constructor() {
    this.routes = [];
    this.stops = [];
    this.stopNames = [];
    this.stopRoutes = {};
    this.routeAdj = [];
    this.routeSet = [];
    this.coords = {};
    this.isReady = false;
  }
  
  loadSync(data) {
    this.routes = data.routes;
    this.stops = data.stops;
    this.routeSet = this.routes.map(r => new Set(r.stops));
    this.routes.forEach((r, i) => {
      new Set(r.stops).forEach(s => {
        (this.stopRoutes[s] = this.stopRoutes[s] || []).push(i);
      });
    });
    this.routeAdj = this.routes.map(() => new Set());
    Object.values(this.stopRoutes).forEach(rs => {
      for (let a = 0; a < rs.length; a++) {
        for (let b = a + 1; b < rs.length; b++) {
          this.routeAdj[rs[a]].add(rs[b]);
          this.routeAdj[rs[b]].add(rs[a]);
        }
      }
    });
    this.stops.forEach(s => { if (s.lat != null) this.coords[s.name] = [s.lat, s.lng]; });
    this.stopNames = this.stops.map(s => s.name).sort();
    this.isReady = true;
  }
  
  idx(r, s) { return this.routes[r].stops.indexOf(s); }
  routePriority(r) {
    if (this.routes[r].kind === 'metro') return -2;
    if (this.routes[r].kind === 'auto') return -1;
    return 0;
  }
  seg(r, a, b) {
    const i = this.idx(r, a), j = this.idx(r, b), st = this.routes[r].stops;
    return i <= j ? st.slice(i, j + 1) : st.slice(j, i + 1).reverse();
  }
  shared(r1, r2) { const out = []; this.routeSet[r1].forEach(s => { if (this.routeSet[r2].has(s)) out.push(s); }); return out; }
  bestTransfer(r1, r2, o, d) {
    let best = null, bc = 1e9;
    this.shared(r1, r2).forEach(t => {
      const c = Math.abs(this.idx(r1, o) - this.idx(r1, t)) + Math.abs(this.idx(r2, t) - this.idx(r2, d));
      if (c < bc) { best = t; bc = c; }
    });
    return [best, bc];
  }
  leg(r, a, b) { return { route: this.routes[r].code, kind: this.routes[r].kind, from: a, to: b, stops: this.seg(r, a, b) }; }
  
  find(o, d) {
    const res = { origin: o, dest: d, direct: [], one: [], two: [] };
    if (!this.stopRoutes[o] || !this.stopRoutes[d]) { res.error = true; return res; }
    const start = this.stopRoutes[o];
    const end = new Set(this.stopRoutes[d]);
    start.filter(r => end.has(r)).sort((a, b) => {
      const pA = this.routePriority(a), pB = this.routePriority(b);
      if (pA !== pB) return pA - pB;
      return Math.abs(this.idx(a, o) - this.idx(a, d)) - Math.abs(this.idx(b, o) - this.idx(b, d));
    }).forEach(r => res.direct.push({ legs: [this.leg(r, o, d)], cost: Math.abs(this.idx(r, o) - this.idx(r, d)) }));
    
    const seen = new Set(), c1 = [];
    start.forEach(r1 => {
      this.routeAdj[r1].forEach(r2 => {
        if (r1 === r2 || !end.has(r2)) return;
        const key = [this.routes[r1].code, this.routes[r2].code].sort().join('|');
        if (seen.has(key)) return;
        const [t, cost] = this.bestTransfer(r1, r2, o, d);
        if (t == null || t === o || t === d) return;
        seen.add(key); c1.push({ cost, r1, r2, t });
      });
    });
    c1.sort((a, b) => {
      const pA = this.routePriority(a.r1) + this.routePriority(a.r2);
      const pB = this.routePriority(b.r1) + this.routePriority(b.r2);
      if (pA !== pB) return pA - pB;
      return a.cost - b.cost;
    }).slice(0, 10).forEach(x => {
      res.one.push({ legs: [this.leg(x.r1, o, x.t), this.leg(x.r2, x.t, d)], cost: x.cost });
    });
    
    if (res.direct.length + res.one.length < 3) {
      const seen2 = new Set(), c2 = [];
      start.forEach(r1 => {
        this.stopRoutes[d].forEach(r3 => {
          if (r3 === r1) return;
          this.routeAdj[r1].forEach(r2 => {
            if (r2 === r1 || r2 === r3 || !this.routeAdj[r3].has(r2)) return;
            if (end.has(r2) || start.includes(r2)) return;
            const key = this.routes[r1].code + '|' + this.routes[r2].code + '|' + this.routes[r3].code;
            if (seen2.has(key)) return;
            const s12 = this.shared(r1, r2), s23 = this.shared(r2, r3);
            let bt = null, bc = 1e9;
            s12.forEach(a => s23.forEach(b => {
              if (new Set([o, a, b, d]).size < 4) return;
              const cc = Math.abs(this.idx(r1, o) - this.idx(r1, a)) + Math.abs(this.idx(r2, a) - this.idx(r2, b)) + Math.abs(this.idx(r3, b) - this.idx(r3, d));
              if (cc < bc) { bc = cc; bt = [a, b]; }
            }));
            if (!bt) return;
            seen2.add(key); c2.push({ cost: bc, r1, r2, r3, a: bt[0], b: bt[1] });
          });
        });
      });
      c2.sort((a, b) => {
        const pA = this.routePriority(a.r1) + this.routePriority(a.r2) + this.routePriority(a.r3);
        const pB = this.routePriority(b.r1) + this.routePriority(b.r2) + this.routePriority(b.r3);
        if (pA !== pB) return pA - pB;
        return a.cost - b.cost;
      }).slice(0, 6).forEach(x => {
        res.two.push({ legs: [this.leg(x.r1, o, x.a), this.leg(x.r2, x.a, x.b), this.leg(x.r3, x.b, d)], cost: x.cost });
      });
    }
    return res;
  }
}

// --- BENCHMARK ---
const router = new BusRouter();

// 1. Graph construction time
const t0 = performance.now();
router.loadSync(raw);
const constructTime = performance.now() - t0;

console.log('=== GRAPH CONSTRUCTION ===');
console.log(`Routes: ${router.routes.length}`);
console.log(`Stops: ${router.stops.length}`);
console.log(`Stop names: ${router.stopNames.length}`);
console.log(`Graph build time: ${constructTime.toFixed(2)} ms`);
console.log(`Dataset file size: ${(readFileSync('./public/busdata.json').length / 1024).toFixed(1)} KB`);

// Compute graph density
let totalAdj = 0;
router.routeAdj.forEach(s => totalAdj += s.size);
console.log(`Avg route adjacency: ${(totalAdj / router.routes.length).toFixed(1)}`);
console.log(`GPS-mapped stops: ${Object.keys(router.coords).length}`);

// 2. Benchmark queries — representative pairs
const queryPairs = [
  ['Esplanade', 'Howrah Station'],
  ['Gariahat', 'Sealdah Station'],
  ['Dunlop', 'Tollygunge'],
  ['Howrah Station', 'Salt Lake'],
  ['Baranagar', 'Jadavpur'],
  ['Ruby', 'Shyambazar'],
  ['Rashbehari', 'Ultadanga'],
  ['Behala', 'Dum Dum'],
  ['New Market', 'Barrackpore'],
  ['Saltlake Sector V', 'Kalighat'],
  ['Garia', 'Dakshineswar'],
  ['Ballygunge', 'Belgharia'],
  ['Santragachi', 'Park Circus'],
  ['Liluah', 'Rabindra Sadan'],
  ['Naihati', 'Babughat'],
  ['Howrah Station', 'Gariahat'],
  ['Esplanade', 'Dum Dum'],
  ['Behala', 'Sealdah Station'],
  ['Ultadanga', 'Tollygunge'],
  ['New Market', 'Jadavpur'],
];

console.log('\n=== QUERY BENCHMARKS ===');
const latencies = [];
const results = [];
queryPairs.forEach(([o, d]) => {
  const runs = [];
  // warm-up run
  router.find(o, d);
  // timed runs
  for (let i = 0; i < 50; i++) {
    const t = performance.now();
    const res = router.find(o, d);
    runs.push(performance.now() - t);
    if (i === 0) results.push({ o, d, res });
  }
  runs.sort((a, b) => a - b);
  const med = runs[Math.floor(runs.length / 2)];
  const p95 = runs[Math.floor(runs.length * 0.95)];
  const avg = runs.reduce((s, v) => s + v, 0) / runs.length;
  latencies.push({ o, d, avg, med, p95 });
});

latencies.forEach(l => {
  console.log(`${l.o} -> ${l.d}: avg=${l.avg.toFixed(3)}ms  med=${l.med.toFixed(3)}ms  p95=${l.p95.toFixed(3)}ms`);
});

const allAvg = latencies.reduce((s, l) => s + l.avg, 0) / latencies.length;
const allMed = latencies.map(l => l.med).sort((a, b) => a - b);
const globalMed = allMed[Math.floor(allMed.length / 2)];
const maxP95 = Math.max(...latencies.map(l => l.p95));
console.log(`\nOverall: mean=${allAvg.toFixed(3)}ms  median=${globalMed.toFixed(3)}ms  worst-p95=${maxP95.toFixed(3)}ms`);

// 3. Routing coverage
console.log('\n=== ROUTING COVERAGE ===');
results.forEach(r => {
  const { o, d, res } = r;
  const total = res.direct.length + res.one.length + res.two.length;
  console.log(`${o} -> ${d}: direct=${res.direct.length} 1-change=${res.one.length} 2-change=${res.two.length} total=${total}${res.error ? ' ERROR' : ''}`);
});

// 4. Full random sample reachability
console.log('\n=== REACHABILITY (Random 200 pairs) ===');
const allStops = Object.keys(router.stopRoutes);
let reachable = 0, unreachable = 0, sampleSize = 200;
const rng = (max) => Math.floor(Math.abs(Math.sin(max * 9301 + 49297) * 233280) % max);
for (let i = 0; i < sampleSize; i++) {
  const a = allStops[rng(allStops.length + i * 7) % allStops.length];
  const b = allStops[rng(allStops.length + i * 13 + 3) % allStops.length];
  if (a === b) { sampleSize++; continue; }
  const r = router.find(a, b);
  if (r.direct.length + r.one.length + r.two.length > 0) reachable++;
  else unreachable++;
}
console.log(`Reachable (<=2 transfers): ${reachable}/${reachable+unreachable} (${(reachable*100/(reachable+unreachable)).toFixed(1)}%)`);

// 5. Memory estimate
const mem = process.memoryUsage();
console.log(`\n=== MEMORY ===`);
console.log(`Heap used: ${(mem.heapUsed / 1024 / 1024).toFixed(2)} MB`);
console.log(`RSS: ${(mem.rss / 1024 / 1024).toFixed(2)} MB`);
