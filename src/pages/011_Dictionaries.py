from pathlib import Path

import polars as pl
import streamlit as st

import scripts.create_dictionaries as create_dictionaries


def print_updated_time():
    from datetime import datetime

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"App last updated at {current_time}"


def set_page_configs() -> None:
    # can only set this once, first thing to set
    st.set_page_config(
        layout="wide",
        page_title="Dictionary Terms",
        initial_sidebar_state="expanded",
    )
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def get_dirs() -> Path:
    parent_dir = Path(__file__).parent.parent
    dataframe_dir = parent_dir / "Dataframes"
    return dataframe_dir


def load_dta(dataframe_dir) -> pl.DataFrame:
    return pl.read_parquet((dataframe_dir / "combined_oil_company_dta.parquet"))


def main() -> None:
    set_page_configs()

    # dictionary_dicts = create_vars.create_dictionary_dicts()
    dictionary_dicts = create_dictionaries.create_dictionary_dicts()
    for dictionary_name, dictionary_dict in dictionary_dicts.items():
        st.write(
            f"### {dictionary_dict['label']} ({dictionary_name}) dictionary:\ndictionary terms: {', '.join(dictionary_dict['terms'])}"
        )
    st.sidebar.write(print_updated_time())  # PROGRESSTRACKING:
    print(print_updated_time())  # PROGRESSTRACKING:


main()
