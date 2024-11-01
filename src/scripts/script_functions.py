from pathlib import Path

import plotly.express as px
import polars as pl
import streamlit as st


def create_dictionary_dicts():
    # TODO: adapt all the pages to use the dictionary first format
    # TODO: this is to make it easier to add new dictionaries and terms
    dictionary_dicts = {
        "climate_change": {
            "label": "Climate Change Dictionary",
            "terms": {
                "climate change": "#006d09",
                "global warming": "#bc1055",
                "greenhouse gas": "#0b913e",
                "methane": "#c66509",
                "emission": "#990099",
            },
        },
        "sustainability|exploitation": {
            "label": "Sustainability|Exploitation Dictionary",
            "terms": {
                # sustainability cool
                "sustain|sustainability": "#00FF00",
                "vegan": "#0000FF",
                "climate change": "#006d09",
                "environment": "#808000",
                "land use": "#008000",
                "water use": "#800080",
                "growing population": "#008080",
                "supply chain": "#000080",
                # exploitation warm
                "exploit|exploitation": "#FF0000",
                "process|processed": "#aa0000",
                "product|production|produce": "#999900",
                "kill": "#800000",
                "slaughter": "#4d0000",
                "butcher": "#aa0000",
            },
        },
        "prosocial": {
            "label": "Prosocial Dictionary",
            "terms": {
                "donate|donation": "#00FF00",
                "share|sharing": "#0000FF",
                "volunteer|volunteering": "#00FFFF",
                "honor": "#808000",
                "award": "#008000",
                "support": "#800080",
                "pledge": "#008080",
                "generosity|generos": "#000080",
                "compassion": "#FF0000",
                "community|communities": "#FFFF00",
                "contribut": "#FF00FF",
            },
        },
        "health_general": {
            "label": "General Health Dictionary",
            "terms": {
                "health": "#00FF00",
                "public health": "#0000FF",
                "antibiotic|prebiotic": "#00FFFF",
                "nutrition|nutritious|nutrient": "#808000",
                "hygiene": "#008000",
                "safe|safety": "#800080",
                "wellness": "#008080",
                "health safety": "#000080",
                "health expert|health research": "#FF0000",
                "health outcome|health benefits|health care|health clinic|health support|health service": "#FFFF00",
                "health department|health official|health inspection": "#FF00FF",
                "diet": "#800000",
                "heath product": "#FF8C00",
                "animal health|herd health|healthy cattle": "#aa0000",
            },
        },
        "ealth_human": {
            "label": "Human Health Dictionary",
            "terms": {
                "human health": "#00FF00",
                "public health": "#0000FF",
                "antibiotic|prebiotic": "#00FFFF",
                "nutrition|nutritious|nutrient": "#808000",
                "hygiene": "#008000",
                "safe|safety": "#800080",
                "wellness": "#008080",
                "health safety": "#000080",
                "health expert|health research": "#FF0000",
                "health outcome|health benefits|health care|health clinic|health support|health service": "#FFFF00",
                "health department|health official|health inspection": "#FF00FF",
                "diet": "#800000",
                "heath product": "#FF8C00",
            },
        },
    }
    return dictionary_dicts


def load_dta():
    def get_dirs() -> Path:
        parent_dir = Path(__file__).parent.parent
        dataframe_dir = parent_dir / "Dataframes"
        return dataframe_dir

    def load_dta_path(dataframe_dir) -> pl.DataFrame:
        return pl.read_parquet((dataframe_dir / "combined_oil_company_dta.parquet"))

    def remove_missing_values(dta: pl.DataFrame) -> pl.DataFrame:
        return dta.drop_nulls()

    def get_year_month_column(dta: pl.DataFrame) -> pl.DataFrame:
        dta = dta.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("year_month"))
        dta = dta.with_columns(
            pl.col("date").dt.strftime("%Y-%m").str.to_date(format="%Y-%m").alias("year_month_dt")
        )
        dta = dta.with_columns(pl.col("date").dt.year().cast(pl.Utf8).alias("year"))
        dta = dta.with_columns(pl.col("date").dt.month().cast(pl.Utf8).alias("month"))
        return dta
        # return dta.with_columns(pl.col("date").dt.strftime("%Y-%m").alias("year_month").sort())

    dataframe_dir = get_dirs()
    dta = load_dta_path(dataframe_dir)
    dta = remove_missing_values(dta)
    dta = get_year_month_column(dta)
    return dta


def display_graph(fig_title, fig, fig_dta):
    st.write(f"## {fig_title}")
    # st.altair_chart(fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    chart_display = st.checkbox(f"Display Dataframe for {fig_title}?")
    if chart_display:
        st.write(f"#### {fig_title} Dataframe")
        st.dataframe(fig_dta)
        st.write(f"Dataframe shape: {fig_dta.shape}")


def line_graph(fig_dta: pl.DataFrame, x_col: str, y_col: str, color_col: str, title: str):
    fig = px.line(fig_dta, x=x_col, y=y_col, color=color_col, title=title)
    return fig
