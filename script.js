/* ═══════════════════════════════════════════
   BloodConnect – script.js
   All interactions, data, and dynamic UI
═══════════════════════════════════════════ */

'use strict';

// ── Sample Data ──────────────────────────────
const DONORS = [
  { id:1, name:'Arjun Sharma',     initials:'AS', blood:'O+',  city:'Mumbai',    available:true,  lastDonation:'2024-12-10', donations:8 },
  { id:2, name:'Priya Nair',       initials:'PN', blood:'A+',  city:'Bangalore', available:true,  lastDonation:'2024-11-22', donations:5 },
  { id:3, name:'Rohan Verma',      initials:'RV', blood:'B-',  city:'Delhi',     available:false, lastDonation:'2025-01-05', donations:3 },
  { id:4, name:'Sana Mirza',       initials:'SM', blood:'AB+', city:'Hyderabad', available:true,  lastDonation:'2024-10-30', donations:12 },
  { id:5, name:'Vikram Patel',     initials:'VP', blood:'O-',  city:'Pune',      available:true,  lastDonation:'2024-12-01', donations:20 },
  { id:6, name:'Deepa Krishnan',   initials:'DK', blood:'A-',  city:'Chennai',   available:false, lastDonation:'2025-01-15', donations:6 },
  { id:7, name:'Ankit Joshi',      initials:'AJ', blood:'B+',  city:'Mumbai',    available:true,  lastDonation:'2024-11-10', donations:4 },
  { id:8, name:'Meera Iyer',       initials:'MI', blood:'AB-', city:'Kolkata',   available:true,  lastDonation:'2024-09-20', donations:9 },
  { id:9, name:'Suresh Babu',      initials:'SB', blood:'O+',  city:'Bangalore', available:true,  lastDonation:'2024-12-18', donations:15 },
];

const EMERGENCY_REQUESTS = [
  { id:1, patient:'Ramesh Gupta',   blood:'O-',  hospital:'Apollo Hospital, Mumbai', city:'Mumbai',    units:3, priority:'critical', time:'12 min ago', contact:'+91 9876543210' },
  { id:2, patient:'Fatima Sheikh',  blood:'AB+', hospital:'AIIMS, Delhi',            city:'Delhi',     units:2, priority:'critical', time:'34 min ago', contact:'+91 9123456789' },
  { id:3, patient:'Lalit Rao',      blood:'B+',  hospital:'Fortis, Bangalore',       city:'Bangalore', units:1, priority:'high',     time:'1 hr ago',   contact:'+91 9988776655' },
  { id:4, patient:'Ananya Das',     blood:'A-',  hospital:'Ruby General, Kolkata',   city:'Kolkata',   units:4, priority:'high',     time:'2 hr ago',   contact:'+91 8877665544' },
  { id:5, patient:'Harish Kumar',   blood:'O+',  hospital:'Manipal, Hyderabad',      city:'Hyderabad', units:2, priority:'normal',   time:'3 hr ago',   contact:'+91 7766554433' },
  { id:6, patient:'Ritu Sharma',    blood:'B-',  hospital:'Max Healthcare, Pune',    city:'Pune',      units:1, priority:'normal',   time:'4 hr ago',   contact:'+91 6655443322' },
];

const CAMPS = [
  { id:1, name:'National Blood Drive – Mumbai Chapter', day:'22', month:'JAN', year:'2025', time:'8:00 AM – 4:00 PM', venue:'NSCI Dome, Worli, Mumbai', organizer:'Red Cross Mumbai',    spots:120 },
  { id:2, name:'LifeGive Community Camp 2025',          day:'28', month:'JAN', year:'2025', time:'9:00 AM – 5:00 PM', venue:'Town Hall, Connaught Place, Delhi', organizer:'BloodConnect Delhi', spots:80 },
  { id:3, name:'Tech Park Donation Drive',              day:'05', month:'FEB', year:'2025', time:'10:00 AM – 3:00 PM', venue:'Bagmane Tech Park, Bangalore', organizer:'Infosys CSR',         spots:60 },
  { id:4, name:'City Hospital Mega Camp',               day:'14', month:'FEB', year:'2025', time:'7:00 AM – 7:00 PM', venue:'Gandhi Nagar Community Centre, Hyderabad', organizer:'Yashoda Hospitals', spots:200 },
  { id:5, name:'University Blood Connect',              day:'20', month:'FEB', year:'2025', time:'9:00 AM – 2:00 PM', venue:'IIT Bombay Main Campus', organizer:'NSS IIT Bombay',      spots:150 },
  { id:6, name:'Rotary Club Monthly Drive',             day:'01', month:'MAR', year:'2025', time:'8:30 AM – 4:30 PM', venue:'Rotary Bhavan, Chennai',          organizer:'Rotary International',spots:90 },
];

const DONATION_HISTORY = [
  { date:'15 Dec 2024', title:'Voluntary Donation', hospital:'Apollo Hospital, Mumbai',    type:'Voluntary',  status:'completed' },
  { date:'10 Sep 2024', title:'Emergency Response', hospital:'KEM Hospital, Mumbai',       type:'Emergency',  status:'completed' },
  { date:'20 Jun 2024', title:'Blood Camp Donation', hospital:'NSS Camp, Powai',           type:'Camp',       status:'completed' },
  { date:'03 Mar 2024', title:'Voluntary Donation', hospital:'Lilavati Hospital, Mumbai',  type:'Voluntary',  status:'completed' },
  { date:'18 Nov 2023', title:'Emergency Response', hospital:'Hinduja Hospital, Mumbai',   type:'Emergency',  status:'completed' },
];

const ACHIEVEMENTS = [
  { icon:'🩸', title:'First Drop',    desc:'Made your first donation', unlocked:true  },
  { icon:'🏅', title:'5 Lives',       desc:'Donated 5 times',          unlocked:true  },
  { icon:'🥇', title:'10 Lives',      desc:'Donated 10 times',         unlocked:false },
  { icon:'🦸', title:'Lifesaver',     desc:'Donated 25+ times',        unlocked:false },
  { icon:'⚡', title:'Fast Responder',desc:'Responded in under 1 hr',  unlocked:true  },
  { icon:'🌟', title:'Verified Hero', desc:'Passed medical screening', unlocked:true  },
  { icon:'🎖️', title:'Monthly Donor', desc:'Donated 3 months in a row',unlocked:false },
  { icon:'💎', title:'Legend',        desc:'50+ lifetime donations',   unlocked:false },
];

const HOSPITAL_REQUESTS = [
  { patient:'Kiran Bala',    blood:'A+',  units:2, priority:'critical', status:'pending'  },
  { patient:'Sudhir Mehta',  blood:'O-',  units:3, priority:'critical', status:'active'   },
  { patient:'Uma Devi',      blood:'B+',  units:1, priority:'high',     status:'active'   },
  { patient:'Prakash Singh', blood:'AB+', units:2, priority:'normal',   status:'pending'  },
  { patient:'Nisha Patil',   blood:'A-',  units:1, priority:'high',     status:'active'   },
];

const ADMIN_USERS = [
  { name:'Arjun Sharma',   role:'Donor',    blood:'O+',  city:'Mumbai',    status:'verified', joined:'Jan 2024' },
  { name:'Priya Nair',     role:'Donor',    blood:'A+',  city:'Bangalore', status:'verified', joined:'Feb 2024' },
  { name:'Apollo Hosp.',   role:'Hospital', blood:'—',   city:'Mumbai',    status:'active',   joined:'Mar 2023' },
  { name:'Rohan Verma',    role:'Receiver', blood:'B-',  city:'Delhi',     status:'pending',  joined:'Dec 2024' },
  { name:'Meera Iyer',     role:'Donor',    blood:'AB-', city:'Kolkata',   status:'verified', joined:'Jun 2024' },
  { name:'Sana Mirza',     role:'Donor',    blood:'AB+', city:'Hyderabad', status:'verified', joined:'Aug 2024' },
  { name:'Fortis Hosp.',   role:'Hospital', blood:'—',   city:'Bangalore', status:'active',   joined:'Jan 2024' },
  { name:'Vikram Patel',   role:'Donor',    blood:'O-',  city:'Pune',      status:'verified', joined:'Oct 2023' },
];

const NOTIFICATIONS = [
  { icon:'🆘', title:'Critical Request Near You', text:'Patient needs O− in Mumbai (Apollo Hospital)', time:'5 min ago' },
  { icon:'✅', title:'Donation Verified',          text:'Your Dec 2024 donation is now verified.',        time:'2 hr ago' },
  { icon:'📅', title:'Upcoming Camp',              text:'Blood Drive at NSCI Dome on 22nd Jan.',          time:'1 day ago' },
];

const FAQS = [
  { q:'Who can donate blood?',               a:'Anyone between 18–65 years, weighing over 50 kg, and in good health can donate. Certain medical conditions may affect eligibility — our team can guide you.' },
  { q:'How often can I donate?',             a:'Whole blood donors should wait 90 days between donations. Platelet donors can donate more frequently, typically every 7 days.' },
  { q:'Is donating blood safe?',             a:'Absolutely. All equipment is sterile and single-use. The process is medically supervised and takes about 8–10 minutes.' },
  { q:'How do I get verified as a donor?',   a:'Register with your Aadhaar, upload a recent medical check-up, and our team verifies within 24 hours.' },
  { q:'What if I need blood urgently?',      a:'Use our Emergency Request feature — verified donors near you are alerted instantly. You can also call our 24/7 hotline.' },
];

// Load camps from localStorage or default CAMPS array
function getCampsList() {
  const stored = localStorage.getItem('bloodconnect_camps');
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch (e) {
      console.error("Error parsing stored camps", e);
    }
  }
  return [...CAMPS];
}

// ── Init ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initHamburger();
  initScrollAnimations();
  renderDonors(DONORS);
  renderEmergency(EMERGENCY_REQUESTS);
  renderCamps(getCampsList());
  renderTimeline(DONATION_HISTORY);
  renderAchievements(ACHIEVEMENTS);
  renderHospitalTable(HOSPITAL_REQUESTS);
  renderAdminTable(ADMIN_USERS);
  renderNotifications(NOTIFICATIONS);
  renderFAQs(FAQS);
  initTabs();
  initCounters();
  initCharts();
  initModals();
  initFAQAccordion();
  initAvailToggle();
  initBackendIntegration();
});

// ── Navbar scroll ────────────────────────────
function initNavbar() {
  const nav = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

// ── Hamburger / Mobile Drawer ────────────────
function initHamburger() {
  const hamburger = document.getElementById('hamburger');
  const drawer    = document.getElementById('mobileDrawer');
  const overlay   = document.getElementById('drawerOverlay');
  const close     = document.getElementById('drawerClose');

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    drawer.classList.toggle('open');
    overlay.classList.toggle('visible');
    document.body.style.overflow = drawer.classList.contains('open') ? 'hidden' : '';
  });

  [overlay, close].forEach(el => el.addEventListener('click', closeMobileDrawer));

  document.querySelectorAll('.drawer-link').forEach(link => {
    link.addEventListener('click', closeMobileDrawer);
  });
}

function closeMobileDrawer() {
  document.getElementById('hamburger').classList.remove('open');
  document.getElementById('mobileDrawer').classList.remove('open');
  document.getElementById('drawerOverlay').classList.remove('visible');
  document.body.style.overflow = '';
}

// ── Scroll Animations ────────────────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
}

// ── Counter Animation ────────────────────────
function initCounters() {
  const counters = document.querySelectorAll('.stat-number[data-target]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(c => observer.observe(c));
}

function animateCounter(el) {
  const target   = parseInt(el.dataset.target, 10);
  const duration = 2000;
  const step     = 16;
  const increment = target / (duration / step);
  let current = 0;

  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      el.textContent = formatNumber(target);
      clearInterval(timer);
    } else {
      el.textContent = formatNumber(Math.floor(current));
    }
  }, step);
}

function formatNumber(n) {
  return n >= 1000 ? (n / 1000).toFixed(n >= 10000 ? 0 : 1) + 'K' : n.toString();
}

// ── Scroll to helper ─────────────────────────
function scrollTo(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Render Donors ────────────────────────────
function renderDonors(donors) {
  const container = document.getElementById('donorResults');
  container.innerHTML = '';

  if (donors.length === 0) {
    container.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:60px 24px;color:var(--muted);">
      <div style="font-size:3rem;margin-bottom:12px">🔍</div>
      <p style="font-size:1rem;font-weight:600">No donors found</p>
      <p style="font-size:.85rem;margin-top:6px">Try adjusting your filters.</p>
    </div>`;
    return;
  }

  donors.forEach((donor, i) => {
    const card = document.createElement('div');
    card.className = 'donor-card fade-up';
    card.style.transitionDelay = `${i * 0.07}s`;

    const availLabel = donor.available ? 'Available' : 'Available Soon';
    const dotClass   = donor.available ? 'avail-dot' : 'avail-dot soon';
    const lastDonate = new Date(donor.lastDonation).toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric' });

    card.innerHTML = `
      <div class="donor-header">
        <div class="donor-avatar">${donor.initials}</div>
        <div>
          <div class="donor-name">${donor.name}</div>
          <div class="donor-city">📍 ${donor.city}</div>
        </div>
        <div class="blood-badge">${donor.blood}</div>
      </div>
      <div class="donor-meta">
        <span class="donor-meta-item"><span class="${dotClass}"></span> ${availLabel}</span>
        <span class="donor-meta-item">🗓 ${lastDonate}</span>
        <span class="donor-meta-item">🩸 ${donor.donations} donations</span>
      </div>
      <button class="contact-btn" onclick="handleContact('${donor.name}')">
        📞 Contact Donor
      </button>`;

    container.appendChild(card);

    // Re-observe for animation
    requestAnimationFrame(() => {
      setTimeout(() => card.classList.add('visible'), 50 + i * 70);
    });
  });
}

function showSkeletons() {
  const container = document.getElementById('donorResults');
  container.innerHTML = Array.from({length:6}).map(() => `
    <div class="skeleton-card">
      <div style="display:flex;gap:14px;align-items:center;margin-bottom:14px">
        <div class="skeleton sk-avatar"></div>
        <div style="flex:1">
          <div class="skeleton sk-line" style="width:70%;margin-bottom:8px"></div>
          <div class="skeleton sk-line shorter"></div>
        </div>
      </div>
      <div class="skeleton sk-line" style="width:100%"></div>
      <div class="skeleton sk-line" style="width:60%;margin-top:8px"></div>
    </div>`).join('');
}

function searchDonors() {
  showSkeletons();

  const bg    = document.getElementById('bloodGroupFilter').value;
  const city  = document.getElementById('cityFilter').value;
  const avail = document.getElementById('availFilter').value;

  setTimeout(() => {
    const results = DONORS.filter(d => {
      const bgMatch    = !bg    || d.blood === bg;
      const cityMatch  = !city  || d.city === city;
      const availMatch = !avail || (avail === 'available' ? d.available : !d.available);
      return bgMatch && cityMatch && availMatch;
    });
    renderDonors(results);
  }, 700);
}

function handleContact(name) {
  showToast(`✅ Contact request sent to ${name}!`);
}

// ── Render Emergency ──────────────────────────
function renderEmergency(requests) {
  const grid = document.getElementById('emergencyGrid');
  grid.innerHTML = '';

  requests.forEach((r, i) => {
    const card = document.createElement('div');
    card.className = `emergency-card ${r.priority} fade-up`;
    card.style.transitionDelay = `${i * 0.08}s`;

    card.innerHTML = `
      <div class="emerg-top">
        <div>
          <span class="priority-badge ${r.priority}">${r.priority.toUpperCase()}</span>
        </div>
        <div class="emerg-blood">${r.blood}</div>
      </div>
      <div class="emerg-patient">${r.patient}</div>
      <div class="emerg-meta">
        <span>🏥 ${r.hospital}</span>
        <span>📍 ${r.city}</span>
        <span>🕐 Posted ${r.time}</span>
      </div>
      <div class="emerg-footer">
        <span class="emerg-units">🩸 ${r.units} unit${r.units>1?'s':''} needed</span>
        <button class="respond-btn" onclick="respondToEmergency('${r.patient}')">Respond</button>
      </div>`;

    grid.appendChild(card);
    requestAnimationFrame(() => {
      setTimeout(() => card.classList.add('visible'), 50 + i * 80);
    });
  });
}

function respondToEmergency(patient) {
  showToast(`🆘 Response sent! Donor matched for ${patient}.`);
}

// ── Render Camps ──────────────────────────────
function renderCamps(camps) {
  const grid = document.getElementById('campsGrid');
  grid.innerHTML = '';

  camps.forEach((camp, i) => {
    const card = document.createElement('div');
    card.className = 'camp-card fade-up';
    card.style.transitionDelay = `${i * 0.08}s`;

    card.innerHTML = `
      <div class="camp-date-banner">
        <div class="camp-day">${camp.day}</div>
        <div class="camp-month-year">
          <span class="camp-month">${camp.month}</span>
          <span class="camp-year">${camp.year}</span>
        </div>
      </div>
      <div class="camp-body">
        <div class="camp-name">${camp.name}</div>
        <div class="camp-info">
          <div class="camp-info-item"><span class="camp-info-icon">⏰</span>${camp.time}</div>
          <div class="camp-info-item"><span class="camp-info-icon">📍</span>${camp.venue}</div>
          <div class="camp-info-item"><span class="camp-info-icon">🏢</span>${camp.organizer}</div>
        </div>
        <div class="camp-footer">
          <span class="camp-spots">✅ ${camp.spots} spots</span>
          <button class="register-btn" onclick="registerCamp('${camp.name}')">Register Free</button>
        </div>
      </div>`;

    grid.appendChild(card);
    requestAnimationFrame(() => {
      setTimeout(() => card.classList.add('visible'), 50 + i * 80);
    });
  });
}

function registerCamp(name) {
  showToast(`🎉 Registered for: ${name.substring(0, 30)}...`);
}

function handleAddCamp(event) {
  event.preventDefault();
  const name = document.getElementById('campName').value.trim();
  const organizer = document.getElementById('campOrganizer').value.trim();
  const spots = document.getElementById('campSpots').value.trim();
  const dateVal = document.getElementById('campDate').value;
  const time = document.getElementById('campTime').value.trim();
  const venue = document.getElementById('campVenue').value.trim();

  if (!name || !organizer || !spots || !dateVal || !time || !venue) {
    showToast("❌ Please fill in all fields.");
    return;
  }

  const dateObj = new Date(dateVal);
  if (isNaN(dateObj.getTime())) {
    showToast("❌ Invalid date.");
    return;
  }

  const day = String(dateObj.getDate()).padStart(2, '0');
  const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const month = months[dateObj.getMonth()];
  const year = dateObj.getFullYear();

  const currentCamps = getCampsList();
  const newCamp = {
    id: currentCamps.length > 0 ? Math.max(...currentCamps.map(c => c.id)) + 1 : 1,
    name,
    day,
    month,
    year,
    time,
    venue,
    organizer,
    spots: parseInt(spots, 10)
  };

  currentCamps.push(newCamp);
  localStorage.setItem('bloodconnect_camps', JSON.stringify(currentCamps));

  renderCamps(currentCamps);
  closeModal('addCampModal');
  
  // Reset form
  event.target.reset();
  showToast("🎉 Donation camp registered successfully!");
}

// ── Render Timeline ───────────────────────────
function renderTimeline(history) {
  const container = document.getElementById('donationTimeline');
  container.innerHTML = '';

  history.forEach((item, i) => {
    const el = document.createElement('div');
    el.className = 'timeline-item fade-up';
    el.style.transitionDelay = `${i * 0.1}s`;

    el.innerHTML = `
      <div class="tl-card">
        <div class="tl-date">${item.date}</div>
        <div class="tl-title">${item.title}</div>
        <div class="tl-meta">🏥 ${item.hospital} &nbsp;·&nbsp; ${item.type}</div>
        <span class="tl-status ${item.status}">${item.status.charAt(0).toUpperCase() + item.status.slice(1)}</span>
      </div>`;

    container.appendChild(el);
  });
}

// ── Render Achievements ───────────────────────
function renderAchievements(achList) {
  const grid = document.getElementById('achievementsGrid');
  grid.innerHTML = '';

  achList.forEach((ach, i) => {
    const card = document.createElement('div');
    card.className = `achievement-card ${ach.unlocked ? 'unlocked' : 'locked'} fade-up`;
    card.style.transitionDelay = `${i * 0.07}s`;

    card.innerHTML = `
      <div class="ach-badge">${ach.unlocked ? '🔓' : '🔒'}</div>
      <div class="ach-icon">${ach.icon}</div>
      <div class="ach-title">${ach.title}</div>
      <div class="ach-desc">${ach.desc}</div>`;

    grid.appendChild(card);
  });
}

// ── Render Hospital Table ─────────────────────
function renderHospitalTable(requests) {
  const tbody = document.getElementById('hospitalTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  requests.forEach(r => {
    const pr = r.priority;
    const st = r.status === 'active' ? 'ts-active' : r.status === 'critical' ? 'ts-critical' : 'ts-pending';
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>${r.patient}</strong></td>
      <td><span style="font-family:'Playfair Display',serif;font-weight:700;color:var(--red-deep)">${r.blood}</span></td>
      <td>${r.units}</td>
      <td><span class="priority-badge ${pr}">${pr.toUpperCase()}</span></td>
      <td><span class="table-status ${st}">${r.status}</span></td>
      <td><button class="btn btn-sm btn-primary" onclick="handleContact('${r.patient}')">Match</button></td>`;
    tbody.appendChild(row);
  });
}

// ── Render Admin Table ────────────────────────
let filteredUsers = [...ADMIN_USERS];

function renderAdminTable(users) {
  const tbody = document.getElementById('adminTableBody');
  if (!tbody) return;
  tbody.innerHTML = '';

  users.forEach(u => {
    const statusClass = u.status === 'verified' ? 'ts-active' : u.status === 'active' ? 'ts-active' : 'ts-pending';
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>${u.name}</strong></td>
      <td>${u.role}</td>
      <td><span style="font-family:'Playfair Display',serif;font-weight:700;color:var(--red-deep)">${u.blood}</span></td>
      <td>${u.city}</td>
      <td><span class="table-status ${statusClass}">${u.status}</span></td>
      <td>${u.joined}</td>
      <td>
        <button class="btn btn-sm" style="background:var(--rose-pale);color:var(--red-deep);border:none;cursor:pointer" onclick="showToast('✅ Action completed!')">Edit</button>
      </td>`;
    tbody.appendChild(row);
  });
}

function filterUsers(query) {
  const q = query.toLowerCase();
  filteredUsers = ADMIN_USERS.filter(u =>
    u.name.toLowerCase().includes(q) ||
    u.city.toLowerCase().includes(q) ||
    u.role.toLowerCase().includes(q)
  );
  renderAdminTable(filteredUsers);
}

// ── Render Notifications ──────────────────────
function renderNotifications(notifs) {
  const list = document.getElementById('notifList');
  if (!list) return;
  list.innerHTML = '';

  notifs.forEach(n => {
    const item = document.createElement('div');
    item.className = 'notif-item';
    item.innerHTML = `
      <div class="notif-item-icon">${n.icon}</div>
      <div class="notif-item-body">
        <div class="notif-item-title">${n.title}</div>
        <div class="notif-item-text">${n.text}</div>
        <div class="notif-item-time">${n.time}</div>
      </div>`;
    list.appendChild(item);
  });
}

function toggleNotifCenter() {
  const center = document.getElementById('notificationCenter');
  center.classList.toggle('open');
}

// ── Render FAQs ───────────────────────────────
function renderFAQs(faqs) {
  const container = document.getElementById('faqList');
  if (!container) return;
  container.innerHTML = '';

  faqs.forEach(faq => {
    const item = document.createElement('div');
    item.className = 'faq-item';

    item.innerHTML = `
      <button class="faq-q">
        ${faq.q}
        <span>+</span>
      </button>
      <div class="faq-a">${faq.a}</div>`;

    container.appendChild(item);
  });
}

function initFAQAccordion() {
  document.addEventListener('click', e => {
    const btn = e.target.closest('.faq-q');
    if (!btn) return;

    const isOpen   = btn.classList.contains('open');
    const allBtns  = document.querySelectorAll('.faq-q');
    const allPanels = document.querySelectorAll('.faq-a');

    allBtns.forEach(b => b.classList.remove('open'));
    allPanels.forEach(p => p.classList.remove('open'));

    if (!isOpen) {
      btn.classList.add('open');
      btn.nextElementSibling.classList.add('open');
    }
  });
}

// ── Tabs ──────────────────────────────────────
function initTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;

      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      tab.classList.add('active');
      const content = document.getElementById(`tab-${target}`);
      if (content) {
        content.classList.add('active');

        // Trigger fade-up in that tab
        content.querySelectorAll('.fade-up').forEach(el => {
          el.classList.remove('visible');
          requestAnimationFrame(() => {
            setTimeout(() => el.classList.add('visible'), 50);
          });
        });

        // Init charts when admin tab opens
        if (target === 'admin') {
          setTimeout(initCharts, 100);
        }
      }
    });
  });
}

// ── Charts ────────────────────────────────────
let chartsInited = false;

function initCharts() {
  if (chartsInited) return;
  chartsInited = true;

  const bloodGroupCtx = document.getElementById('bloodGroupChart');
  const monthlyCtx    = document.getElementById('monthlyChart');
  const fulfillCtx    = document.getElementById('fulfillmentChart');
  const trendsCtx     = document.getElementById('trendsChart');

  if (!bloodGroupCtx) return;

  const red   = '#C0152A';
  const rose  = '#FFE4E8';
  const slate = '#2D2D44';

  // Blood Group Distribution
  new Chart(bloodGroupCtx, {
    type: 'doughnut',
    data: {
      labels: ['A+','A-','B+','B-','O+','O-','AB+','AB-'],
      datasets: [{
        data: [28, 7, 24, 6, 22, 5, 5, 3],
        backgroundColor: ['#C0152A','#E8192C','#FF4B6E','#FF7090','#FFAABB','#FFD0D8','#FBE8EA','#F5F5F5'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { font: { family: 'Inter', size: 11 }, padding: 12 } }
      },
      cutout: '62%'
    }
  });

  // Monthly Donations
  new Chart(monthlyCtx, {
    type: 'bar',
    data: {
      labels: ['Jul','Aug','Sep','Oct','Nov','Dec','Jan'],
      datasets: [{
        label: 'Donations',
        data: [820, 950, 880, 1100, 1350, 1280, 1480],
        backgroundColor: red,
        borderRadius: 6,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11 } } },
        y: { grid: { color: '#f0f0f0' }, ticks: { font: { family: 'Inter', size: 11 } } }
      }
    }
  });

  // Fulfillment Rate
  new Chart(fulfillCtx, {
    type: 'line',
    data: {
      labels: ['Jul','Aug','Sep','Oct','Nov','Dec','Jan'],
      datasets: [{
        label: 'Fulfillment %',
        data: [91, 88, 93, 95, 94, 97, 98],
        borderColor: red,
        backgroundColor: 'rgba(192,21,42,.08)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: red,
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11 } } },
        y: { min: 80, max: 100, grid: { color: '#f0f0f0' }, ticks: { font: { family: 'Inter', size: 11 }, callback: v => v + '%' } }
      }
    }
  });

  // Active Donor Trends
  new Chart(trendsCtx, {
    type: 'line',
    data: {
      labels: ['Jul','Aug','Sep','Oct','Nov','Dec','Jan'],
      datasets: [
        {
          label: 'Active Donors',
          data: [30200, 31400, 33000, 34500, 36200, 37100, 38120],
          borderColor: red,
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          tension: 0.4,
          pointBackgroundColor: red,
          pointRadius: 4,
          pointBorderColor: '#fff',
          pointBorderWidth: 2
        },
        {
          label: 'New Registrations',
          data: [1200, 1400, 1600, 1500, 1700, 900, 1020],
          borderColor: '#FFB347',
          backgroundColor: 'transparent',
          borderWidth: 2,
          tension: 0.4,
          pointBackgroundColor: '#FFB347',
          pointRadius: 4,
          pointBorderColor: '#fff',
          pointBorderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom', labels: { font: { family: 'Inter', size: 11 }, padding: 12 } } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11 } } },
        y: { grid: { color: '#f0f0f0' }, ticks: { font: { family: 'Inter', size: 11 } } }
      }
    }
  });
}

// ── Modals ────────────────────────────────────
function initModals() {
  document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', e => {
      if (e.target === modal) closeModal(modal.id);
    });
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.open').forEach(m => closeModal(m.id));
    }
  });
}

function openModal(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.remove('open');
  document.body.style.overflow = '';
}

function switchModal(fromId, toId) {
  closeModal(fromId);
  setTimeout(() => openModal(toId), 200);
}

function togglePass(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.type = input.type === 'password' ? 'text' : 'password';
}

function selectRole(btn) {
  document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function selectPriority(btn) {
  document.querySelectorAll('.priority-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// ── Availability Toggle ───────────────────────
function initAvailToggle() {
  const toggle = document.getElementById('availToggle');
  if (!toggle) return;
  toggle.addEventListener('change', () => {
    const status = toggle.checked ? 'Active' : 'Inactive';
    showToast(`🔄 Availability set to: ${status}`);
  });
}

// ── Toast Notification ────────────────────────
function showToast(message, duration = 3500) {
  let toast = document.getElementById('globalToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'globalToast';
    toast.style.cssText = `
      position:fixed; bottom:100px; left:50%; transform:translateX(-50%) translateY(0);
      background:#1A1A2E; color:#fff; padding:12px 24px; border-radius:12px;
      font-family:Inter,sans-serif; font-size:.88rem; font-weight:500;
      box-shadow:0 8px 32px rgba(0,0,0,.3); z-index:9999;
      transition:all .3s cubic-bezier(.4,0,.2,1); white-space:nowrap;
      max-width:90vw; text-align:center;
    `;
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.style.opacity = '1';
  toast.style.transform = 'translateX(-50%) translateY(0)';

  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(16px)';
  }, duration);
}

// ── Active nav link on scroll ─────────────────
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const links    = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(s => {
      if (window.scrollY >= s.offsetTop - 120) current = s.id;
    });
    links.forEach(l => {
      l.classList.toggle('active', l.getAttribute('href') === `#${current}`);
    });
  }, { passive: true });
}

document.addEventListener('DOMContentLoaded', initScrollSpy);

// ── Ripple effect on buttons ──────────────────
document.addEventListener('click', e => {
  const btn = e.target.closest('.btn.ripple');
  if (!btn) return;
  const ripple = document.createElement('span');
  const rect   = btn.getBoundingClientRect();
  const size   = Math.max(btn.offsetWidth, btn.offsetHeight) * 2;
  ripple.style.cssText = `
    position:absolute; border-radius:50%; background:rgba(255,255,255,.35);
    width:${size}px; height:${size}px;
    left:${e.clientX - rect.left - size/2}px;
    top:${e.clientY - rect.top - size/2}px;
    transform:scale(0); animation:rippleAnim .5s linear;
    pointer-events:none;
  `;
  btn.appendChild(ripple);
  setTimeout(() => ripple.remove(), 600);
});

const style = document.createElement('style');
style.textContent = `@keyframes rippleAnim { to { transform: scale(1); opacity: 0; } }`;
document.head.appendChild(style);

// ── Backend API Integration ──────────────────
const API_BASE_URL = "http://127.0.0.1:5000/api";

function initBackendIntegration() {
  const regSubmitBtn = document.getElementById("regSubmitBtn");
  const loginSubmitBtn = document.getElementById("loginSubmitBtn");

  if (regSubmitBtn) {
    regSubmitBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      
      const firstName = document.getElementById("regFirstName").value.trim();
      const lastName = document.getElementById("regLastName").value.trim();
      const email = document.getElementById("regEmail").value.trim();
      const phone = document.getElementById("regPhone").value.trim();
      const bloodGroup = document.getElementById("regBloodGroup").value;
      const password = document.getElementById("regPass").value;

      if (!firstName || !lastName || !email || !phone || !bloodGroup || !password) {
        showToast("❌ Please fill in all registration fields.");
        return;
      }

      regSubmitBtn.innerText = "Creating Account...";
      regSubmitBtn.disabled = true;

      try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            full_name: `${firstName} ${lastName}`,
            email: email,
            phone_number: phone,
            password: password,
            blood_group: bloodGroup
          })
        });

        const result = await response.json();
        
        if (response.ok) {
          showToast("🎉 Registration successful! Verification email sent.");
          closeModal("registerModal");
          setTimeout(() => openModal("loginModal"), 1000);
        } else {
          showToast(`❌ Registration failed: ${result.message}`);
        }
      } catch (err) {
        console.error("Registration error:", err);
        showToast("❌ Network error. Make sure Flask is running on port 5000.");
      } finally {
        regSubmitBtn.innerText = "Create Account";
        regSubmitBtn.disabled = false;
      }
    });
  }

  if (loginSubmitBtn) {
    loginSubmitBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPass").value;

      if (!email || !password) {
        showToast("❌ Please enter your email and password.");
        return;
      }

      loginSubmitBtn.innerText = "Signing In...";
      loginSubmitBtn.disabled = true;

      try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: email,
            password: password
          })
        });

        const result = await response.json();

        if (response.ok) {
          showToast("🔓 Login successful!");
          localStorage.setItem("access_token", result.data.access_token);
          localStorage.setItem("user_email", result.data.user.email);
          localStorage.setItem("user_role", result.data.user.role);
          closeModal("loginModal");
          
          setTimeout(() => window.location.reload(), 1000);
        } else {
          showToast(`❌ Login failed: ${result.message}`);
        }
      } catch (err) {
        console.error("Login error:", err);
        showToast("❌ Network error. Make sure Flask is running on port 5000.");
      } finally {
        loginSubmitBtn.innerText = "Sign In";
        loginSubmitBtn.disabled = false;
      }
    });
  }

  // Update navbar Actions if logged in
  const token = localStorage.getItem("access_token");
  if (token) {
    const navActions = document.querySelector(".nav-actions");
    const userEmail = localStorage.getItem("user_email");
    const role = localStorage.getItem("user_role");
    
    if (navActions) {
      navActions.innerHTML = `
        <span style="font-size:0.85rem;color:var(--text);font-weight:600;margin-right:12px">👤 ${userEmail} (${role})</span>
        <button class="btn btn-ghost" id="logoutBtn">Logout</button>
      `;
      
      const logoutBtn = document.getElementById("logoutBtn");
      if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
          localStorage.clear();
          showToast("🚪 Logged out successfully!");
          setTimeout(() => window.location.reload(), 1000);
        });
      }
    }
  }
}