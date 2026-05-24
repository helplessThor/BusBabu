// Routing logic ported from kolkata-bus-route and optimized for Vite/Module environment

export class BusRouter {
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

  async loadData() {
    try {
      const response = await fetch('/busdata.json');
      const data = await response.json();
      
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
      
      this.stops.forEach(s => { 
        if (s.lat != null) this.coords[s.name] = [s.lat, s.lng]; 
      });
      
      this.stopNames = this.stops.map(s => s.name).sort();
      this.isReady = true;
      return true;
    } catch (error) {
      console.error("Failed to load bus data:", error);
      return false;
    }
  }

  idx(r, s) {
    return this.routes[r].stops.indexOf(s);
  }

  seg(r, a, b) {
    const i = this.idx(r, a);
    const j = this.idx(r, b);
    const st = this.routes[r].stops;
    return i <= j ? st.slice(i, j + 1) : st.slice(j, i + 1).reverse();
  }

  shared(r1, r2) {
    const out = []; 
    this.routeSet[r1].forEach(s => { 
      if (this.routeSet[r2].has(s)) out.push(s); 
    }); 
    return out;
  }

  bestTransfer(r1, r2, o, d) {
    let best = null, bc = 1e9;
    this.shared(r1, r2).forEach(t => {
      const c = Math.abs(this.idx(r1, o) - this.idx(r1, t)) + Math.abs(this.idx(r2, t) - this.idx(r2, d));
      if (c < bc) { best = t; bc = c; }
    });
    return [best, bc];
  }

  leg(r, a, b) {
    return { 
      route: this.routes[r].code, 
      kind: this.routes[r].kind, 
      from: a, 
      to: b, 
      stops: this.seg(r, a, b) 
    };
  }

  find(o, d) {
    const res = { origin: o, dest: d, direct: [], one: [], two: [] };
    if (!this.stopRoutes[o] || !this.stopRoutes[d]) { 
      res.error = true; 
      return res; 
    }
    
    const start = this.stopRoutes[o];
    const end = new Set(this.stopRoutes[d]);

    // direct
    start.filter(r => end.has(r))
         .sort((a, b) => Math.abs(this.idx(a, o) - this.idx(a, d)) - Math.abs(this.idx(b, o) - this.idx(b, d)))
         .forEach(r => res.direct.push({
           legs: [this.leg(r, o, d)], 
           cost: Math.abs(this.idx(r, o) - this.idx(r, d))
         }));

    // one transfer
    const seen = new Set(), c1 = [];
    start.forEach(r1 => {
      this.routeAdj[r1].forEach(r2 => {
        if (r1 === r2 || !end.has(r2)) return;
        const key = [this.routes[r1].code, this.routes[r2].code].sort().join('|');
        if (seen.has(key)) return;
        const [t, cost] = this.bestTransfer(r1, r2, o, d);
        if (t == null || t === o || t === d) return;
        seen.add(key); 
        c1.push({ cost, r1, r2, t });
      });
    });
    
    c1.sort((a, b) => a.cost - b.cost).slice(0, 10).forEach(x => {
      res.one.push({ 
        legs: [this.leg(x.r1, o, x.t), this.leg(x.r2, x.t, d)], 
        cost: x.cost 
      });
    });

    // two transfers (only when the easy options are thin)
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
              const cc = Math.abs(this.idx(r1, o) - this.idx(r1, a)) 
                       + Math.abs(this.idx(r2, a) - this.idx(r2, b))
                       + Math.abs(this.idx(r3, b) - this.idx(r3, d));
              if (cc < bc) { bc = cc; bt = [a, b]; }
            }));
            if (!bt) return;
            seen2.add(key); 
            c2.push({ cost: bc, r1, r2, r3, a: bt[0], b: bt[1] });
          });
        });
      });
      
      c2.sort((a, b) => a.cost - b.cost).slice(0, 6).forEach(x => {
        res.two.push({ 
          legs: [this.leg(x.r1, o, x.a), this.leg(x.r2, x.a, x.b), this.leg(x.r3, x.b, d)], 
          cost: x.cost 
        });
      });
    }
    
    return res;
  }
}
