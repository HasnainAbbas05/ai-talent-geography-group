import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

// Rebuild the CSVs from a preserved snapshot of the publisher's chart data.
const dir = path.dirname(new URL(import.meta.url).pathname);
const source = JSON.parse(fs.readFileSync(path.join(dir, 'published_chart_data.json'), 'utf8'));
const quote = x => /[",\n\r]/.test(String(x ?? '')) ? '"' + String(x ?? '').replaceAll('"','""') + '"' : String(x ?? '');
function csv(name, headers, rows) {
  fs.writeFileSync(path.join(dir, name), [headers, ...rows].map(r => r.map(quote).join(',')).join('\n')+'\n');
}
const mobility = source.charts['30265299'];
const retention = source.charts['30285922'];
const careers = source.charts['30286797'];
const flows = new Map(mobility.rows.map(r => [r[0], r]));
const summary = retention.rows.map(r => {
  const [country, ownText, , publishedPct] = r;
  const own = Number(String(ownText).replaceAll(',', ''));
  const [, left, arrived] = flows.get(country);
  const retained = own - left;
  const employed = retained + arrived;
  const pct = retained / own * 100;
  assert.equal(Math.round(pct * 10) / 10, publishedPct);
  assert(own > 0 && retained >= 0 && employed >= 0);
  return [2025, 2026, country, ['Europe','Other'].includes(country) ? 'grouped_region' : 'country', own, left, retained, arrived, employed, arrived-left, publishedPct, Number(pct.toFixed(6)), retention.url, mobility.url];
});
assert.equal(summary.length, 11);
assert.equal(new Set(summary.map(r=>r[2])).size, 11);
assert.equal(summary.reduce((s,r)=>s+r[4],0), 10280);
assert.equal(summary.reduce((s,r)=>s+r[8],0), 10280);
assert.equal(summary.reduce((s,r)=>s+r[9],0), 0);
assert.equal(careers.rows.length, 18);
assert.equal(careers.rows.reduce((s,r)=>s+r[3],0), 8214);
csv('ai_talent_country_summary.csv', ['conference_cohort_year','workplace_observation_year','country_or_region','geography_type','undergraduate_educated_count','working_outside_origin_group_count','same_origin_work_group_count','educated_elsewhere_working_here_count','work_destination_count','net_difference_count','published_retention_percent','recalculated_retention_percent','retention_source_url','mobility_source_url'], summary);
csv('published_retention.csv', ['country_or_region','undergraduate_educated_count','published_retention_percent','source_url'], retention.rows.map(r=>[r[0],Number(String(r[1]).replaceAll(',','')),r[3],retention.url]));
csv('published_mobility.csv', ['country_or_region','left_count','arrived_count','net_difference_count','source_url'], mobility.rows.map(r=>[r[0],r[1],r[2],r[2]-r[1],mobility.url]));
csv('selected_career_paths.csv', ['conference_cohort_year','workplace_observation_year','undergraduate_country_or_region','graduate_country_or_region','work_country_or_region','researcher_count','coverage','source_url'], careers.rows.map(r=>[2025,2026,r[0],r[1],r[2],r[3],'18 published paths only; not the complete flow matrix',careers.url]));
console.log(JSON.stringify({checks:'passed',country_groups:11,cohort_total:10280,work_total:10280,net_total:0,selected_paths:18,selected_path_total:8214,selected_path_share_percent:8214/10280*100},null,2));
