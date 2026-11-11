"""Do countries that train AI researchers retain them, or does talent concentrate in a few destinations?

Streamlit data narrative for a government policy analyst.
Source: Ma & Yang (2026), Carnegie Endowment for International Peace, NeurIPS 2025 cohort,
workplaces observed in 2026. See the "Data and limits" tab and data/README.md.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parent / "data"
CARNEGIE_URL = "https://carnegieendowment.org/features/whos-ahead-in-the-global-ai-talent-race"

# Categorical slots 1-2 of the validated reference palette, plus a neutral for "small sample".
BLUE = "#2a78d6"
ORANGE = "#eb6834"
NEUTRAL = "#8d9096"
SMALL_N = 100  # below this many undergraduates, a retention % is shown as "interpret with care"

st.set_page_config(page_title="AI talent: train, retain, attract", page_icon="🎓", layout="wide")


# ---------------------------------------------------------------- data
@st.cache_data
def load():
    summary = pd.read_csv(DATA / "ai_talent_country_summary.csv")
    retention = pd.read_csv(DATA / "published_retention.csv")
    mobility = pd.read_csv(DATA / "published_mobility.csv")
    paths = pd.read_csv(DATA / "selected_career_paths.csv")
    return summary, retention, mobility, paths


summary, retention_src, mobility_src, paths = load()

# Derived columns (all arithmetic on the published counts; nothing is estimated).
COHORT = int(summary["undergraduate_educated_count"].sum())
df = summary.rename(
    columns={
        "country_or_region": "geo",
        "undergraduate_educated_count": "trained",
        "working_outside_origin_group_count": "left",
        "same_origin_work_group_count": "retained",
        "educated_elsewhere_working_here_count": "arrived",
        "work_destination_count": "working",
        "net_difference_count": "net",
        "published_retention_percent": "ret_pub",
        "recalculated_retention_percent": "ret",
    }
).copy()
df["label"] = df.apply(lambda r: f"{r.geo} (grouped)" if r.geography_type == "grouped_region" else r.geo, axis=1)
df["trained_share"] = df["trained"] / COHORT * 100
df["working_share"] = df["working"] / COHORT * 100
df["imported_share"] = df["arrived"] / df["working"] * 100  # share of those working here educated elsewhere
countries = df[df.geography_type == "country"].copy()
regions = df[df.geography_type == "grouped_region"].copy()


def pct(x, d=1):
    return f"{x:.{d}f}%"


def style(fig, height=420, **kw):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=20, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        **kw,
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.18)", zeroline=False)
    fig.update_yaxes(showgrid=False)
    return fig


# ---------------------------------------------------------------- header
st.title("Do countries that train AI researchers keep them?")
st.markdown(
    "**Question:** do countries that train AI researchers retain them, or does talent concentrate in a few "
    "destination countries?  \n"
    "**For:** a government policy analyst weighing how to develop, retain and attract AI research talent."
)

top_train = countries.nlargest(2, "trained")
top_work = countries.nlargest(2, "working")
top_train_share = top_train.trained_share.sum()
top_work_share = top_work.working_share.sum()
usa = df[df.geo == "USA"].iloc[0]
best_ret = countries.nlargest(1, "ret").iloc[0]
worst_ret = countries.nsmallest(1, "ret").iloc[0]
overall_ret = df["retained"].sum() / COHORT * 100

st.info(
    f"**Short answer: both, and the answer depends on which end you look at.** Retention ranges from "
    f"{pct(best_ret.ret, 0)} ({best_ret.geo}) to {pct(worst_ret.ret, 0)} ({worst_ret.geo}). Workplaces "
    f"are a little more concentrated than undergraduate training: {' and '.join(top_work.geo)} hold "
    f"{pct(top_work_share)} of the {COHORT:,} researchers' workplaces versus {pct(top_train_share)} of their "
    f"undergraduate degrees, a gap of {top_work_share - top_train_share:.1f} points. The USA stands out as an importer: "
    f"{pct(usa.imported_share)} of researchers working there studied elsewhere. *In this sample only, see \"Data and limits\".*"
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Researchers in sample", f"{COHORT:,}")
m2.metric(f"{' + '.join(top_train.geo)}: trained here", pct(top_train_share))
m3.metric(f"{' + '.join(top_work.geo)}: working here", pct(top_work_share))
m4.metric("USA workforce trained elsewhere", pct(usa.imported_share))
st.caption(
    "Sample = NeurIPS 2025 authors with complete career histories (about 40% of the conference's unique authors). "
    "\"Trained\" = country of undergraduate institution. \"Working\" = employer country in 2026."
)

tab_over, tab_ret, tab_net, tab_dest, tab_path, tab_ver, tab_about = st.tabs(
    ["1 · Train vs work", "2 · Retention", "3 · Attract & net flow", "4 · Where they work", "5 · Career paths", "6 · Verify a number", "Data and limits"]
)

# ---------------------------------------------------------------- 1 train vs work
with tab_over:
    st.subheader("Where researchers trained vs where they work")
    st.markdown(
        "Each geography's share of the whole sample, at undergraduate level (blue) and at the 2026 workplace "
        "(orange). A longer orange bar means the place hosts more researchers than it trained."
    )
    o = df.sort_values("working_share")
    fig = go.Figure()
    fig.add_bar(
        y=o.label, x=o.trained_share, orientation="h", name="Trained (undergraduate)", marker_color=BLUE,
        customdata=o[["trained"]], hovertemplate="%{y}<br>Trained: %{customdata[0]:,} (%{x:.1f}% of sample)<extra></extra>",
    )
    fig.add_bar(
        y=o.label, x=o.working_share, orientation="h", name="Working (2026)", marker_color=ORANGE,
        customdata=o[["working"]], hovertemplate="%{y}<br>Working: %{customdata[0]:,} (%{x:.1f}% of sample)<extra></extra>",
    )
    fig.update_layout(barmode="group", bargap=0.35, bargroupgap=0.08, xaxis_title="Share of the 10,280 researchers (%)")
    st.plotly_chart(style(fig, 520), width="stretch")
    st.caption(
        f"Reading it: China trained {pct(df[df.geo=='China'].trained_share.iloc[0])} of the sample and hosts "
        f"{pct(df[df.geo=='China'].working_share.iloc[0])}; the USA trained "
        f"{pct(usa.trained_share)} and hosts {pct(usa.working_share)}. Europe and Other are grouped regions, not countries."
    )
    with st.expander("Table view"):
        st.dataframe(
            o.sort_values("working", ascending=False)[["label", "trained", "working", "trained_share", "working_share"]]
            .rename(columns={"label": "Geography", "trained": "Trained (n)", "working": "Working (n)",
                             "trained_share": "Trained %", "working_share": "Working %"}),
            hide_index=True, width="stretch",
            column_config={"Trained %": st.column_config.NumberColumn(format="%.1f"),
                           "Working %": st.column_config.NumberColumn(format="%.1f")},
        )

# ---------------------------------------------------------------- 2 retention
with tab_ret:
    st.subheader("Retention: of those trained here, how many work here?")
    st.markdown(
        "Retention = researchers whose undergraduate and 2026 employer geography match, divided by everyone "
        "who did their undergraduate degree there. The number of researchers behind each bar is printed beside it."
    )
    r = countries.sort_values("ret")
    big, small = r[r.trained >= SMALL_N], r[r.trained < SMALL_N]
    fig = go.Figure()
    for sub, name, colour in [(big, f"n ≥ {SMALL_N} undergraduates", BLUE), (small, f"n < {SMALL_N} (interpret with care)", NEUTRAL)]:
        fig.add_bar(
            y=sub.geo, x=sub.ret, orientation="h", name=name, marker_color=colour,
            text=[f"{v:.1f}%  (n={n:,})" for v, n in zip(sub.ret, sub.trained)], textposition="outside",
            customdata=sub[["trained", "retained", "left"]],
            hovertemplate="%{y}<br>Retention %{x:.1f}%<br>Trained %{customdata[0]:,}; stayed %{customdata[1]:,}; "
                          "work elsewhere %{customdata[2]:,}<extra></extra>",
        )
    fig.add_vline(x=overall_ret, line_dash="dot", line_color="rgba(128,128,128,0.8)",
                  annotation_text=f"Whole sample {overall_ret:.0f}%", annotation_position="top")
    fig.update_layout(bargap=0.35, xaxis_title="Retention (%)", xaxis_range=[0, 105])
    fig.update_yaxes(categoryorder="array", categoryarray=r.geo.tolist())  # keep one sort across both colour groups
    st.plotly_chart(style(fig, 440), width="stretch")

    gr = regions.set_index("geo")
    c1, c2 = st.columns(2)
    c1.metric(f"Europe (grouped region), n={int(gr.loc['Europe','trained']):,}", pct(gr.loc["Europe", "ret"]))
    c2.metric(f"Other (grouped region), n={int(gr.loc['Other','trained']):,}", pct(gr.loc["Other", "ret"]))
    st.caption(
        "Europe and Other are groups of many countries, so a match within the group does not mean the researcher stayed in "
        "the same country. They are kept out of the country ranking. The UK is separate from Europe; Hong Kong is counted with China."
    )
    st.warning(
        f"**Scale matters.** China's retention ({pct(df[df.geo=='China'].ret.iloc[0],0)}) is lower than the USA's, "
        f"but China trained {int(df[df.geo=='China'].trained.iloc[0]):,} researchers, the most by far, so it also has the "
        f"largest absolute number working abroad ({int(df[df.geo=='China'].left.iloc[0]):,}). "
        f"A high rate on a small base ({int(usa.trained):,} for the USA) is a different policy fact."
    )

# ---------------------------------------------------------------- 3 attract & net
with tab_net:
    st.subheader("Attraction: who gains and who loses researchers?")
    view = st.radio("View", ["Net gain or loss", "Left vs arrived"], horizontal=True)
    n = df.sort_values("net")
    if view == "Net gain or loss":
        fig = go.Figure()
        fig.add_bar(
            y=n.label, x=n.net, orientation="h", showlegend=False,
            marker_color=[BLUE if v >= 0 else ORANGE for v in n.net],
            text=[f"{v:+,}" for v in n.net], textposition="outside",
            customdata=n[["arrived", "left"]],
            hovertemplate="%{y}<br>Net %{x:+,}<br>Arrived %{customdata[0]:,} − left %{customdata[1]:,}<extra></extra>",
        )
        fig.update_layout(bargap=0.35, xaxis_title="Net difference (arrived − left), researchers")
        fig.add_vline(x=0, line_color="rgba(128,128,128,0.8)")
        st.caption("Blue = hosts more researchers than it trained; orange = trained more than it hosts.")
        st.plotly_chart(style(fig, 480), width="stretch")
    else:
        fig = go.Figure()
        fig.add_bar(y=n.label, x=n.left, orientation="h", name="Left (trained here, work elsewhere)", marker_color=ORANGE,
                    hovertemplate="%{y}<br>Left: %{x:,}<extra></extra>")
        fig.add_bar(y=n.label, x=n.arrived, orientation="h", name="Arrived (trained elsewhere, work here)", marker_color=BLUE,
                    hovertemplate="%{y}<br>Arrived: %{x:,}<extra></extra>")
        fig.update_layout(barmode="group", bargap=0.35, bargroupgap=0.08, xaxis_title="Researchers")
        st.plotly_chart(style(fig, 520), width="stretch")

    st.markdown("#### Retain vs attract")
    st.markdown(
        "Horizontal: how many of its own graduates a country keeps. Vertical: how much of its research workforce "
        "was trained elsewhere. Countries only; grouped regions excluded."
    )
    pos = {"Australia": "top center", "UK": "bottom center", "Canada": "middle left", "Singapore": "top center"}
    fig = go.Figure()
    for sub, name, colour in [(countries[countries.trained >= SMALL_N], f"n ≥ {SMALL_N} undergraduates", BLUE),
                              (countries[countries.trained < SMALL_N], f"n < {SMALL_N} (interpret with care)", NEUTRAL)]:
        fig.add_scatter(
            x=sub.ret, y=sub.imported_share, mode="markers+text", name=name, text=sub.geo,
            textposition=[pos.get(g, "middle right") for g in sub.geo],
            marker=dict(size=12, color=colour, line=dict(width=2, color="rgba(255,255,255,0.9)")),
            customdata=sub[["trained", "working", "arrived"]],
            hovertemplate="%{text}<br>Retention %{x:.1f}%<br>Workforce trained elsewhere %{y:.1f}%<br>"
                          "Trained %{customdata[0]:,}; working %{customdata[1]:,}; arrived %{customdata[2]:,}<extra></extra>",
        )
    fig.update_layout(xaxis_title="Retention of own graduates (%)", yaxis_title="Workforce trained elsewhere (%)",
                      xaxis_range=[0, 100], yaxis_range=[-5, 105])
    fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.18)", zeroline=False)
    st.plotly_chart(style(fig, 460), width="stretch")
    st.caption(
        "Only the USA is high on both axes. Singapore, Australia, the UK and Canada draw most of their researchers from "
        "abroad but keep fewer than half of their own graduates, and each has a small base (≤ 216 undergraduates in this sample)."
    )

# ---------------------------------------------------------------- 4 where do they work (donut)
p = paths.rename(columns={"undergraduate_country_or_region": "u", "graduate_country_or_region": "g",
                          "work_country_or_region": "w", "researcher_count": "n"})
# Colour follows the geography everywhere it appears (fixed, never re-assigned by rank).
GEO_COLOUR = {"USA": "#eb6834", "China": "#6250d6", "Singapore": "#1baf7a", "Europe": "#eda100",
              "India": "#e87ba4", "Other": "#008300", "South Korea": "#e34948"}
NOT_PUBLISHED = "rgba(160,163,170,0.55)"


def donut(parts, centre):
    parts = [x for x in parts if x[1] > 0]
    fig = go.Figure(go.Pie(
        labels=[x[0] for x in parts], values=[x[1] for x in parts], marker=dict(colors=[x[2] for x in parts],
        line=dict(color="rgba(255,255,255,0.9)", width=2)), hole=0.5, sort=False, direction="clockwise",
        texttemplate="%{percent:.1%}", textposition="auto", insidetextorientation="horizontal",
        hovertemplate="%{label}<br>%{value:,} researchers (%{percent})<extra></extra>",
    ))
    fig.add_annotation(text=centre, x=0.5, y=0.5, showarrow=False, font=dict(size=15))
    fig.update_layout(height=430, margin=dict(l=10, r=10, t=10, b=10), legend=dict(font=dict(size=13)))
    return fig


with tab_dest:
    st.subheader("Where do researchers from (or in) a country end up?")
    mode = st.radio("Question", ["Trained in … → where do they work?", "Working in … → where did they train?"], horizontal=True)
    f1, f2 = st.columns([2, 1])
    geos = df.geo.tolist()
    if mode.startswith("Trained"):
        geo_sel = f1.selectbox("Undergraduate degree in", geos, index=geos.index("China"))
        row = df[df.geo == geo_sel].iloc[0]
        leavers = p[(p.u == geo_sel) & (p.w != geo_sel)].groupby("w").n.sum().sort_values(ascending=False)
        unlisted = int(row.left) - int(leavers.sum())
        only_move = f2.checkbox("Only those who left", value=False, help="Hide the people who stayed, to compare destinations.")
        parts = ([] if only_move else [(f"Stayed: works in {geo_sel}", int(row.retained), BLUE)])
        parts += [(f"Left → {w}", int(v), GEO_COLOUR.get(w, "#5b6b7f")) for w, v in leavers.items()]
        parts += [("Left → destination not published", unlisted, NOT_PUBLISHED)]
        total = sum(x[1] for x in parts)
        st.plotly_chart(donut(parts, f"{total:,}<br>trained in<br>{geo_sel}"), width="stretch")
        st.markdown(
            f"**How this adds up.** {int(row.trained):,} researchers did their undergraduate degree in {geo_sel}: "
            f"{int(row.retained):,} stayed and {int(row.left):,} work elsewhere (exact counts from the two source tables). "
            f"The published career paths name destinations for {int(leavers.sum()):,} of those who left; the other "
            f"{unlisted:,} left but their destination is not published, so they are one grey slice, not spread across countries."
        )
        if row.geography_type == "grouped_region":
            st.caption(f"{geo_sel} is a grouped region: working anywhere inside the group counts as “stayed”.")
    else:
        geo_sel = f1.selectbox("Currently working in", geos, index=geos.index("USA"))
        row = df[df.geo == geo_sel].iloc[0]
        incomers = p[(p.w == geo_sel) & (p.u != geo_sel)].groupby("u").n.sum().sort_values(ascending=False)
        unlisted = int(row.arrived) - int(incomers.sum())
        only_move = f2.checkbox("Only those trained elsewhere", value=False, help="Hide the people who trained here too.")
        parts = ([] if only_move else [(f"Trained in {geo_sel} too", int(row.retained), BLUE)])
        parts += [(f"Trained in {u}", int(v), GEO_COLOUR.get(u, "#5b6b7f")) for u, v in incomers.items()]
        parts += [("Trained elsewhere, origin not published", unlisted, NOT_PUBLISHED)]
        total = sum(x[1] for x in parts)
        st.plotly_chart(donut(parts, f"{total:,}<br>working in<br>{geo_sel}"), width="stretch")
        st.markdown(
            f"**How this adds up.** {int(row.working):,} researchers work in {geo_sel}: {int(row.retained):,} also did their "
            f"undergraduate degree there and {int(row.arrived):,} did it elsewhere (exact counts). The published career paths "
            f"name the origin for {int(incomers.sum()):,} of those who arrived; the other {unlisted:,} are one grey slice."
        )
        if row.geography_type == "grouped_region":
            st.caption(f"{geo_sel} is a grouped region: training anywhere inside the group counts as “trained here too”.")
    st.caption(
        "Donut rather than a full pie so the total sits in the middle. Blue = same geography. Grey = counted, but the "
        "source does not say where. Slice sizes are shares of the people shown."
    )
    with st.expander("Table view"):
        st.dataframe(pd.DataFrame(parts, columns=["Group", "Researchers", "colour"]).drop(columns="colour"),
                     hide_index=True, width="stretch")

# ---------------------------------------------------------------- 5 career paths (lollipop)
with tab_path:
    st.subheader("Selected career paths: undergraduate → graduate → work")
    covered = int(p.n.sum())
    st.warning(
        f"These are the **{len(p)} paths the publisher charted**, covering {covered:,} of {COHORT:,} researchers "
        f"({covered / COHORT * 100:.1f}%). The other {COHORT - covered:,} are not shown. This is not the full flow, and "
        "gaps are not zeros."
    )
    c1, c2, c3 = st.columns([2, 2, 1.4])
    u_sel = c1.multiselect("Undergraduate in", sorted(p.u.unique()), placeholder="All")
    w_sel = c2.multiselect("Working in (2026)", sorted(p.w.unique()), placeholder="All")
    moved_only = c3.checkbox("Only those who moved", help="Work geography differs from undergraduate geography.")
    q = p.copy()
    if u_sel: q = q[q.u.isin(u_sel)]
    if w_sel: q = q[q.w.isin(w_sel)]
    if moved_only: q = q[q.u != q.w]
    q = q.assign(moved=q.u != q.w, label=q.u + " → " + q.g + " → " + q.w).sort_values("n")
    if q.empty:
        st.info("No published path matches those filters.")
    else:
        fig = go.Figure()
        for moved, name, colour in [(False, "Works where they did their undergraduate degree", BLUE),
                                    (True, "Works in a different geography", ORANGE)]:
            sub = q[q.moved == moved]
            if sub.empty:
                continue
            xs, ys = [], []
            for lab, n in zip(sub.label, sub.n):          # stems: a line from 0 to the count
                xs += [0, n, None]; ys += [lab, lab, None]
            fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color=colour, width=3), hoverinfo="skip", showlegend=False)
            fig.add_scatter(
                x=sub.n, y=sub.label, mode="markers+text", name=name, text=[f"{v:,}" for v in sub.n], textposition="middle right",
                marker=dict(size=13, color=colour, line=dict(width=2, color="rgba(255,255,255,0.9)")),
                hovertemplate="%{y}<br>%{x:,} researchers<extra></extra>",
            )
        fig.update_layout(xaxis_title="Researchers", xaxis_range=[0, q.n.max() * 1.12])
        fig.update_yaxes(categoryorder="array", categoryarray=q.label.tolist())
        st.plotly_chart(style(fig, max(260, 34 * len(q) + 110)), width="stretch")
        st.caption("Read each row left to right as: undergraduate country → graduate-school country → 2026 workplace.")
    cu = p[(p.u == "China") & (p.g == "USA")]
    if len(cu):
        tot = int(cu.n.sum()); to_us = int(cu[cu.w == "USA"].n.sum()); to_cn = int(cu[cu.w == "China"].n.sum())
        st.caption(
            f"Of {tot:,} China-undergraduate, US-graduate researchers in these paths, {to_us:,} ({to_us / tot * 100:.1f}%) "
            f"work in the USA and {to_cn:,} ({to_cn / tot * 100:.1f}%) in China. Other China → USA → elsewhere paths, if any, "
            "were not published."
        )
    with st.expander("Table view"):
        st.dataframe(p[["u", "g", "w", "n"]].rename(columns={"u": "Undergraduate", "g": "Graduate", "w": "Work 2026", "n": "Researchers"}),
                     hide_index=True, width="stretch")

# ---------------------------------------------------------------- 5 verify
with tab_ver:
    st.subheader("Trace a number back to the source")
    geo = st.selectbox("Geography", df.geo.tolist(), index=df.geo.tolist().index("USA"))
    a = retention_src[retention_src.country_or_region == geo].iloc[0]
    b = mobility_src[mobility_src.country_or_region == geo].iloc[0]
    trained, left = int(a.undergraduate_educated_count), int(b.left_count)
    arrived = int(b.arrived_count)
    retained = trained - left
    calc = retained / trained * 100
    pub = float(a.published_retention_percent)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**① Source table A** · `published_retention.csv`")
        st.dataframe(a.drop("source_url").astype(str).to_frame("value"), width="stretch")
        st.markdown(f"[Flourish chart]({a.source_url})")
    with c2:
        st.markdown("**② Source table B** · `published_mobility.csv`")
        st.dataframe(b.drop("source_url").astype(str).to_frame("value"), width="stretch")
        st.markdown(f"[Flourish chart]({b.source_url})")
    with c3:
        st.markdown("**③ Calculation**")
        st.markdown(
            f"- Trained (A): **{trained:,}**\n"
            f"- Work elsewhere, “Left” (B): **{left:,}**\n"
            f"- Stayed = {trained:,} − {left:,} = **{retained:,}**\n"
            f"- Retention = {retained:,} / {trained:,} × 100 = **{calc:.6f}%**\n"
            f"- Published (rounded to 1 dp): **{pub}%**  →  matches: **{round(calc, 1) == pub}**\n"
            f"- Working here = {retained:,} + arrived {arrived:,} = **{retained + arrived:,}**"
        )
    row = df[df.geo == geo].iloc[0]
    ok = abs(row.ret - calc) < 1e-4 and int(row.working) == retained + arrived
    (st.success if ok else st.error)(
        f"The dashboard shows {row.ret:.1f}% for {geo}. "
        + ("It matches" if ok else "It does NOT match")
        + " the recomputation from the two source tables."
    )

    st.markdown("#### Integrity checks on the whole dataset")
    checks = pd.DataFrame([
        ("Undergraduate counts sum to 10,280", int(df.trained.sum()) == 10280),
        ("Work-destination counts sum to 10,280", int(df.working.sum()) == 10280),
        ("Net differences sum to 0", int(df.net.sum()) == 0),
        ("Every recalculated retention rounds to the published rate",
         bool((df.ret.round(1) == df.ret_pub).all())),
        ("Selected career paths: 18 rows, total 8,214", len(paths) == 18 and int(paths.researcher_count.sum()) == 8214),
    ], columns=["Check", "Passed"])
    st.dataframe(checks, hide_index=True, width="stretch")
    st.download_button("Download the main dataset (CSV)", (DATA / "ai_talent_country_summary.csv").read_bytes(),
                       "ai_talent_country_summary.csv", "text/csv")

# ---------------------------------------------------------------- about
with tab_about:
    st.subheader("Data and limits")
    st.markdown(
        f"""
**Source.** Ma, D., & Yang, B. (2026, 23 September). *Who's ahead in the global AI talent race?* Carnegie Endowment for
International Peace. [{CARNEGIE_URL}]({CARNEGIE_URL})

**How the numbers got here.** The three public Flourish tables embedded in the study were read from the page's chart data
(accessed 24 October 2026), saved as CSVs, and joined by country. Stayed = trained − left; working here = stayed + arrived;
net = arrived − left; retention = stayed / trained. These are the publisher's published counts, not Carnegie's individual-level
database, and not an official Carnegie CSV release. The extraction script is `data/build_data.mjs`.

**Read these before drawing conclusions**
- **One conference, elite sample.** Authors of accepted NeurIPS 2025 papers with complete three-stage career histories:
  10,280 researchers, about 40% of the conference's unique authors. Not all AI researchers, and not a random subset.
- **“Trained” means undergraduate institution country.** Not nationality, birthplace, or where an AI-specific degree was earned.
- **Timing.** Conference cohort 2025; workplaces observed in 2026. Undergraduate years differ across researchers. There is
  one snapshot, so no trends and no cause (for example, no claim about which policy changed anything).
- **“Retained” is a match, not a journey.** It can include people who left and came back, and it does not show immigration events.
- **Employer country** follows the study's institution/employer assignment; for multinationals this may be the home country.
- **Grouped regions.** Europe and Other are groups of countries. The UK is separate from Europe; Hong Kong is with China.
- **Small bases.** Rates for Australia, Singapore and Russia rest on fewer than 100 people each.
- **Career paths** cover 8,214 of the 10,280 researchers (79.9%).
- **Self-reported profiles.** Carnegie notes the profiles are self-maintained and cannot be independently verified per person; it also
  reports that Europe's direction is sensitive to the sample used.
"""
    )
