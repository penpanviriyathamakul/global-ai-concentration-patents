from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

FIVE_COUNTRIES = ["United States", "China", "Japan", "Korea", "Germany"]
START_YEAR, END_YEAR = 2010, 2024


def render_patent_view(data: pd.DataFrame) -> None:
    st.header("AI patents by country")
    st.caption("Unit: patents")
    st.caption("Source: OECD AI patent indicators, published by OECD. Shares use the world total (ALL).")
    st.caption(f"Latest observation: {data['date'].max().date().isoformat()}")

    selected = st.multiselect(
        "Countries",
        FIVE_COUNTRIES,
        default=FIVE_COUNTRIES,
        key="country_filter",
    )
    frame = data.loc[data["country"].isin(selected)].copy()
    frame["year"] = frame["date"].dt.year

    if frame.empty:
        st.info("No observations match the selected filters.")
    else:
        st.write(f"Selected: {', '.join(selected)}")

        # Metrics: latest year and change since the start of the period.
        end_values = frame[frame["year"] == END_YEAR].set_index("country")["ai_patents"]
        start_values = frame[frame["year"] == START_YEAR].set_index("country")["ai_patents"]
        columns = st.columns(len(selected))
        for column, country in zip(columns, [c for c in FIVE_COUNTRIES if c in selected]):
            end, start = int(end_values[country]), int(start_values[country])
            column.metric(
                f"{country}, {END_YEAR}",
                f"{end:,} patents",
                delta=f"{end - start:+,} since {START_YEAR}",
            )

        # Line chart: counts per year for the selected countries.
        fig_line = px.line(
            frame,
            x="year",
            y="ai_patents",
            color="country",
            markers=True,
            title="AI patents per year (counts)",
            labels={"year": "Year", "ai_patents": "AI patents", "country": "Country"},
        )
        fig_line.update_xaxes(dtick=1)
        st.plotly_chart(fig_line, width="stretch")

    # Shares and ranking use all five countries and the world total, so they do not depend on the country filter.
    # Keep them under the same condition so the empty state hides every output.
    if not frame.empty:
        wide = data.assign(year=data["date"].dt.year).pivot_table(
            index="year", columns="country", values="ai_patents", aggfunc="sum"
        )[FIVE_COUNTRIES]
        totals = data.assign(year=data["date"].dt.year).groupby("year")["world_total"].first()

        shares = wide.div(totals, axis=0) * 100
        shares["Others"] = 100 - shares[FIVE_COUNTRIES].sum(axis=1)

        long = shares.reset_index().melt(id_vars="year", var_name="Group", value_name="Share (%)")
        fig_area = px.area(
            long,
            x="year",
            y="Share (%)",
            color="Group",
            category_orders={"Group": FIVE_COUNTRIES + ["Others"]},
            title="Share of world AI patents by year (%)",
            labels={"year": "Year"},
        )
        fig_area.update_xaxes(dtick=1)
        st.plotly_chart(fig_area, width="stretch")
        st.caption(
            "Others = world total minus the five countries shown. "
            "Each year sums to 100%."
        )

        st.subheader("Rank by year (1 = most AI patents among the five)")
        year = st.slider(
            "Year for ranking",
            START_YEAR,
            END_YEAR,
            END_YEAR,
            key="year_select",
        )
        st.caption(
            "Ranks compare only the five countries shown; they are not a world ranking."
        )

        leader = wide.loc[year].idxmax()
        st.metric(f"Leader in {year}", leader, f"{int(wide.loc[year].max()):,} patents")

        ranks = wide.rank(axis=1, ascending=False, method="first").astype(int)
        highlighted = ranks.T.style.apply(
            lambda col: ["background-color: #ffe08a" if col.name == year else "" for _ in col],
            axis=0,
        )
        st.dataframe(highlighted)

        st.subheader("Share of world AI patents by year (%)")
        st.dataframe(shares.round(1).T)

    st.download_button(
        "Download filtered data",
        data=frame.drop(columns=["year"], errors="ignore").to_csv(index=False).encode("utf-8"),
        file_name="filtered_ai_patents.csv",
        mime="text/csv",
        key="patent_download",
    )
