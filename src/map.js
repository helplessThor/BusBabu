export class BusMap {
  constructor(containerId) {
    this.map = null;
    this.layerGroup = null;
    this.containerId = containerId;
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    
    // Default Kolkata Coordinates
    this.map = L.map(this.containerId, {
      center: [22.5726, 88.3639],
      zoom: 12,
      zoomControl: false
    });
    
    L.control.zoom({ position: 'bottomright' }).addTo(this.map);

    // Using CartoDB Positron for a clean look matching our aesthetics
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      maxZoom: 19
    }).addTo(this.map);

    this.layerGroup = L.layerGroup().addTo(this.map);
    this.initialized = true;
  }

  clear() {
    if (this.layerGroup) {
      this.layerGroup.clearLayers();
    }
  }

  plotJourney(journey, coordsDict) {
    if (!this.initialized) this.init();
    this.clear();

    const colors = ['#1f6f4a', '#0f5c78', '#8a4b12']; // Default bus theme leg colors
    let bounds = L.latLngBounds();
    let hasValidPoints = false;
    let plotted = 0;
    let missing = 0;

    // Check current theme colors from computed style if possible, but fallback to array
    const root = document.documentElement;
    const computed = getComputedStyle(root);
    const leg1 = computed.getPropertyValue('--leg-1').trim() || colors[0];
    const leg2 = computed.getPropertyValue('--leg-2').trim() || colors[1];
    const leg3 = computed.getPropertyValue('--leg-3').trim() || colors[2];
    const legColors = [leg1, leg2, leg3];

    journey.legs.forEach((leg, i) => {
      const lineCoords = [];
      
      leg.stops.forEach(stopName => {
        if (coordsDict[stopName]) {
          plotted++;
          const [lat, lng] = coordsDict[stopName];
          lineCoords.push([lat, lng]);
          bounds.extend([lat, lng]);
          hasValidPoints = true;

          // Add simple circle marker for each stop
          L.circleMarker([lat, lng], {
            radius: 3,
            color: legColors[i],
            fillColor: '#fff',
            fillOpacity: 1,
            weight: 2
          }).addTo(this.layerGroup).bindTooltip(stopName, { direction: 'top', className: 'pin' });
        } else {
          missing++;
        }
      });

      if (lineCoords.length > 1) {
        L.polyline(lineCoords, {
          color: legColors[i],
          weight: 4,
          opacity: 0.8
        }).addTo(this.layerGroup);
      }
    });

    // Add Start and End markers
    const marks = [{ s: journey.legs[0].from, t: 'A' }];
    journey.legs.slice(0, -1).forEach(l => marks.push({ s: l.to, t: '~' }));
    marks.push({ s: journey.legs[journey.legs.length - 1].to, t: 'B' });

    marks.forEach(m => {
      const c = coordsDict[m.s];
      if (!c) return;
      const isBig = m.t !== '~';
      const color = isBig ? leg1 : leg2;
      L.marker(c, {
        icon: L.divIcon({
          className: '',
          html: `<div style="background:${color};color:#fff;
            width:${isBig ? 28 : 20}px;height:${isBig ? 28 : 20}px;border-radius:50%;
            display:flex;align-items:center;justify-content:center;
            border:2px solid #fff;box-shadow:0 2px 5px rgba(0,0,0,.3);
            font:700 ${isBig ? 14 : 12}px sans-serif;">${m.t === '~' ? '⇄' : m.t}</div>`,
          iconSize: [isBig ? 28 : 20, isBig ? 28 : 20],
          iconAnchor: [isBig ? 14 : 10, isBig ? 14 : 10]
        })
      }).addTo(this.layerGroup).bindTooltip(m.s, { direction: 'top', className: 'pin' });
    });

    if (hasValidPoints) {
      this.map.fitBounds(bounds, { padding: [30, 30], maxZoom: 14 });
    }

    return { plotted, missing };
  }
}
