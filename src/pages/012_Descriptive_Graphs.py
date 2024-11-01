import plotly.express as px
import polars as pl
import streamlit as st

import scripts.script_functions as functs


def print_updated_time():
    from datetime import datetime

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"App last updated at {current_time}"


def set_page_configs() -> None:
    # can only set this once, first thing to set
    st.set_page_config(
        layout="wide",
        page_title="Basic Descriptive Graphs",
        initial_sidebar_state="expanded",
    )
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def get_posts_by_date(dta: pl.DataFrame) -> pl.DataFrame:
    return (
        # dta.group_by("year_month", "company_name").agg(pl.count().alias("count")).sort("year_month")
        # dta.group_by("year_month", "company_name").agg(pl.count().alias("count"))
        dta.group_by(pl.col("year_month_dt"))
        .agg(pl.count().alias("count"))
        .sort("year_month_dt")
    )


def graph_post_by_date(fig_dta: pl.DataFrame):
    fig_title = "Posts by Date"
    # fig = alt.Chart(fig_dta).mark_line().encode(x="year_month_dt", y="count", color="company_name")
    fig = px.line(fig_dta, x="year_month_dt", y="count", title="Posts by Date")
    return fig, fig_title, fig_dta


def get_posts_by_date_by_company(dta: pl.DataFrame) -> pl.DataFrame:
    return (
        # dta.group_by("year_month", "company_name").agg(pl.count().alias("count")).sort("year_month")
        # dta.group_by("year_month", "company_name").agg(pl.count().alias("count"))
        dta.group_by(pl.col("year_month_dt"), pl.col("company_name"))
        .agg(pl.count().alias("count"))
        .sort("year_month_dt")
        .sort("company_name")
    )


def graph_post_by_date_by_company(fig_dta: pl.DataFrame):
    fig_title = "Posts by Company by Date"
    # fig = alt.Chart(fig_dta).mark_line().encode(x="year_month_dt", y="count", color="company_name")
    fig = px.line(
        fig_dta, x="year_month_dt", y="count", color="company_name", title="Posts by Date"
    )
    return fig, fig_title, fig_dta


def display_graph(fig_title, fig, fig_dta):
    st.write(f"## {fig_title}")
    # st.altair_chart(fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    chart_display = st.checkbox(f"Display Dataframe for {fig_title}?")
    if chart_display:
        st.write(f"#### {fig_title} Dataframe")
        st.dataframe(fig_dta)
        st.write(f"Dataframe shape: {fig_dta.shape}")


def main() -> None:
    set_page_configs()
    dta = functs.load_dta()
    dta_by_date = get_posts_by_date(dta)
    fig, fig_title, fig_dta = graph_post_by_date(dta_by_date)
    st.plotly_chart(fig, use_container_width=True)
    dta_by_date = get_posts_by_date_by_company(dta)
    fig, fig_title, fig_dta = graph_post_by_date_by_company(dta_by_date)
    st.plotly_chart(fig, use_container_width=True)
    # st.altair_chart(fig, use_container_width=True)
    # fig = px.line(
    #     fig_dta, x="year_month_dt", y="count", color="company_name", title="Posts by Date"
    # )
    # functs.display_graph(fig, fig_title, fig_dta)
    # display_graph(fig, fig_title, fig_dta)

    dictionary_dicts = functs.create_dictionary_dicts()
    for dictionary_name, dictionary_dict in dictionary_dicts.items():
        st.write(
            f"### {dictionary_dict['label']} ({dictionary_name}) dictionary:\ndictionary terms: {', '.join(dictionary_dict['terms'])}"
        )
    st.sidebar.write(print_updated_time())  # PROGRESSTRACKING:
    print(print_updated_time())  # PROGRESSTRACKING:


main()
