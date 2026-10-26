const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let D,cur=1;
const badge=s=>({verified:'✅ Verified',check:'⚠️ Needs check',conflict:'⛔ Conflict'})[s]||s;
function renderDay(n){cur=n;const d=D.days.find(x=>x.day===n);
 document.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',+c.dataset.d===n));
 document.getElementById('day').innerHTML=`<span class="time">Day ${d.day} · ${esc(d.label)} · ${esc(d.city)}</span><h2>${esc(d.title)}</h2><p class="meta">🏨 Base: <b>${esc(d.base)}</b></p><p class="transit">🚇 <b>Transit:</b> ${esc(d.transit)}</p>`+
 d.items.map(i=>`<div class="item"><span class="time">${esc(i.time)}</span> <span class="badge ${i.status}">${badge(i.status)}</span><h3>${esc(i.name)}</h3><p>${esc(i.detail)}</p>${i.verified?`<p class="ver"><b>Verified:</b> ${esc(i.verified)}</p>`:''}<a class="src" href="${esc(i.source.url)}" target="_blank" rel="noopener">Source: ${esc(i.source.label)} ↗</a></div>`).join('');}
fetch('data.json').then(r=>r.json()).then(d=>{D=d;
 const chips=document.getElementById('chips');
 chips.innerHTML=d.days.map(x=>`<button class="chip ${x.items.some(i=>i.status==='conflict')?'conf':''}" data-d="${x.day}">Day ${x.day}<br><small>${esc(x.label)}</small></button>`).join('');
 chips.addEventListener('click',e=>{const b=e.target.closest('.chip');if(b)renderDay(+b.dataset.d)});
 // auto-select today if during trip (2026), else Day 1
 const now=new Date(),iso=now.toISOString().slice(0,10),hit=d.days.find(x=>x.date===iso);renderDay(hit?hit.day:1);
 document.getElementById('hotels').innerHTML=d.hotels.map(h=>`<article><h3>${esc(h.name)}</h3><p>${esc(h.nights)}</p><p>${esc(h.detail)}</p><span class="badge ${h.status}">${badge(h.status)}</span> <a class="src" href="${esc(h.source.url)}" target="_blank" rel="noopener">${esc(h.source.label)} ↗</a></article>`).join('');
 document.getElementById('flags').innerHTML=d.flags.map(f=>`<div class="flag ${f.sev}"><b>${esc(f.id)} · ${esc(f.title)}</b><p>${esc(f.detail)}</p><a class="src" href="${esc(f.source.url)}" target="_blank" rel="noopener">${esc(f.source.label)} ↗</a></div>`).join('');
 document.getElementById('fcount').textContent=`(${d.flags.length})`;
 document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');['days','hotels','flagged'].forEach(t=>document.getElementById('tab-'+t).hidden=t!==b.dataset.tab);});
 document.getElementById('q').addEventListener('input',e=>{const q=e.target.value.toLowerCase().trim();if(!q)return;const hit=d.days.find(x=>JSON.stringify(x).toLowerCase().includes(q));if(hit&&hit.day!==cur)renderDay(hit.day);});
}).catch(e=>{document.getElementById('day').textContent='Could not load data.json: '+e.message});
