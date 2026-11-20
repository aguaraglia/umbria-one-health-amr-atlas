/* Rapporto ISTISAN 26/7: tabella per distretto, senza poligoni. */
(function () {
  "use strict";
  const path = "public/data/istisan_26_7_umbria_2024.json";
  const esc = (value) => String(value == null ? "" : value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));
  const num = (value, digits) => Number(value).toLocaleString("it-IT", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  });
  const delta = (value) => {
    const n = Number(value);
    const text = num(Math.abs(n), 1);
    if (n > 0) return "+" + text;
    if (n < 0) return "−" + text;
    return text;
  };
  const amount = (value) => num(value, Number.isInteger(Number(value)) ? 1 : (String(value).split(".")[1] || "").length > 1 ? 2 : 1);

  const districtRows = (rows) => rows.map((row) => {
    const total = row.district === "Totale";
    return `<tr class="${total ? "district-total" : ""}"><td>${esc(row.district)}</td><td>${esc(row.usl)}</td><td>${amount(row.ddd_1000_inh_day)}</td><td>${delta(row.ddd_delta_pct_24_23)}</td><td>${num(row.prevalence_of_use_pct, 1)}</td><td>${amount(row.spend_per_capita_eur)}</td><td>${delta(row.spend_delta_pct_24_23)}</td></tr>`;
  }).join("");

  const hospitalRows = (rows) => rows.map((row) => {
    const total = row.structure === "Umbria";
    return `<tr class="${total ? "district-total" : ""}"><td>${esc(row.structure)}</td><td>${amount(row.ddd_100_bed_days)}</td><td>${delta(row.ddd_delta_pct_24_23)}</td><td>${amount(row.spend_per_bed_day_eur)}</td><td>${delta(row.spend_delta_pct_24_23)}</td></tr>`;
  }).join("");

  const markup = (data) => {
    const source = data.source || {};
    const usl = data.usl_table8_total_ddd || {};
    const uslLine = Object.keys(usl).map((key) => `${esc(key)} ${amount(usl[key])}`).join("; ");
    return `<section class="istisan-panel literature-section" aria-labelledby="istisan-title"><div class="data-digest-heading"><div><p class="section-kicker">CONSUMO, NON RESISTENZA</p><h2 id="istisan-title">Uso degli antibiotici per distretto, 2024</h2><p class="istisan-lead">Rapporti ISTISAN 26/7. I 12 distretti non hanno un confine ISTAT: la tabella non ha poligoni e non è un layer della mappa.</p></div></div><h3>Territorio, per distretto (Tabella 3)</h3><div class="table-wrap"><table class="literature-table"><thead><tr><th>Distretto</th><th>USL</th><th>DDD/1000 ab die</th><th>Δ DDD %</th><th>Prevalenza d'uso %</th><th>Spesa pro capite €</th><th>Δ spesa %</th></tr></thead><tbody>${districtRows(data.districts_table3 || [])}</tbody></table></div><h3>Ospedale (Tabella 29)</h3><div class="table-wrap"><table class="literature-table"><thead><tr><th>Struttura</th><th>DDD/100 giornate</th><th>Δ DDD %</th><th>Spesa per giornata €</th><th>Δ spesa %</th></tr></thead><tbody>${hospitalRows(data.hospital_table29 || [])}</tbody></table></div><p class="governance-note">${esc(data.attribution || "")} Licenza ${esc(data.license || "CC BY 4.0")}. ${esc(data.limitations || "")} Tabella 8, DDD/1000 ab die: ${uslLine}. ${source.url ? `<a href="${esc(source.url)}" target="_blank" rel="noreferrer">Apri il rapporto ↗</a>` : ""}</p></section>`;
  };

  const mount = (html) => {
    if (document.getElementById("istisan-districts")) return;
    const host = document.querySelector(".data-digest") || document.querySelector(".evidence-shell");
    if (!host) return;
    const holder = document.createElement("div");
    holder.id = "istisan-districts";
    holder.innerHTML = html;
    host.appendChild(holder);
  };

  fetch(path, { cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error(String(response.status));
      return response.json();
    })
    .then((data) => mount(markup(data)))
    .catch((error) => {
      console.warn("[AMR Atlas] Tabella ISTISAN non disponibile", error);
    });
}());
