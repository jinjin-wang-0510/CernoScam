
import os
import re
import json
import html as _html
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
APP_NAME = "CernoScam"

st.set_page_config(
    page_title=f"{APP_NAME} — AI Scam Detector",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon=None,
)


# ----------------------------------------------------------------------------
# STYLE
# ----------------------------------------------------------------------------

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --page: #69868c;
            --text: #e1f5ed;
            --muted: #b9d2ca;
            --card: #2f4549;
            --card-2: #26393d;
            --card-3: #1f3033;
            --line: #46646a;
            --ink: #1c2e31;

            --green: #c5dfb5;
            --green-hover: #d8eacb;

            --good: #9fd8a6;
            --bad: #f4a29a;
            --warn: #f0c27a;
        }

        /* =========================================================
           GLOBAL STYLES
        ========================================================= */

        *,
        *::before,
        *::after {
            box-sizing: border-box;
        }

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100%;
    min-height: 100%;
    height: auto !important;
    overflow-x: hidden !important;
    overflow-y: auto !important;
    background: var(--page) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', sans-serif !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    height: auto !important;
    min-height: 100vh !important;
    max-height: none !important;
    overflow: visible !important;
    background: var(--page) !important;
    color: var(--text);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', sans-serif !important;
}

[data-testid="stMain"] > div {
    height: auto !important;
    min-height: 100vh !important;
    max-height: none !important;
    overflow: visible !important;
}

        /* Hide Streamlit chrome */
        header[data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        #MainMenu,
        footer {
            display: none !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Avoid clipping page content on narrow screens */
        [data-testid="stMain"] {
            overflow: visible !important;
        }

        img,
        video,
        iframe,
        svg {
            max-width: 100%;
        }

        /* =========================================================
           DESKTOP PHONE FRAME
        ========================================================= */

        div.block-container,
[data-testid="stMainBlockContainer"] {
    position: relative;
    display: block;

    max-width: 430px !important;
    width: 100% !important;

    height: auto !important;
    min-height: 100vh !important;
    max-height: none !important;

    margin: 20px auto !important;
    padding: 48px 16px 40px !important;

    overflow: visible !important;
    overscroll-behavior-y: auto;

    border: 13px solid transparent;
    border-radius: 52px;

    background:
        linear-gradient(var(--page), var(--page)) padding-box,
        linear-gradient(
            145deg,
            #7a969c 0%,
            #46646a 20%,
            #1c2e31 45%,
            #26393d 62%,
            #69868c 82%,
            #1f3033 100%
        ) border-box;

    box-shadow:
        inset 0 0 0 2px #091011,
        0 0 0 1.5px #92b0b5,
        0 0 0 3px #182427,
        0 28px 60px rgba(12, 23, 25, 0.4),
        0 6px 14px rgba(12, 23, 25, 0.25);
}
        /* =========================================================
           TYPOGRAPHY
        ========================================================= */

        .stApp,
        .stApp input,
        .stApp textarea,
        .stApp button,
        .stApp label {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                         'Segoe UI', sans-serif !important;
        }

        [data-testid="stMarkdownContainer"] {
            color: var(--text);
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {
            color: var(--text);
            font-size: 0.92rem;
            line-height: 1.65;
        }

        [data-testid="stMarkdownContainer"] h1 {
            color: var(--text) !important;
            font-size: 2rem;
            font-weight: 800 !important;
            line-height: 1.12;
            letter-spacing: -0.045em;
            margin: 0 0 0.65rem;
        }

        [data-testid="stMarkdownContainer"] h2 {
            color: var(--text) !important;
            font-size: 1.5rem;
            font-weight: 700 !important;
            line-height: 1.25;
            letter-spacing: -0.03em;
        }

        [data-testid="stMarkdownContainer"] h3 {
            color: var(--text) !important;
            font-size: 1.12rem;
            font-weight: 700 !important;
            line-height: 1.35;
        }

        [data-testid="stMarkdownContainer"] h4,
        [data-testid="stMarkdownContainer"] strong,
        [data-testid="stMarkdownContainer"] b {
            color: var(--text);
            font-weight: 700;
        }

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] * {
            color: var(--muted) !important;
            font-size: 0.8rem;
            line-height: 1.5;
        }

        code {
            color: var(--text) !important;
            background: var(--card-3) !important;
            padding: 2px 5px;
            border-radius: 5px;
            overflow-wrap: anywhere;
        }

        /* =========================================================
           NAVIGATION TABS
        ========================================================= */

        .stTabs [data-baseweb="tab-list"] {
            position: sticky;
            top: 26px;
            z-index: 60;

            display: flex;
            gap: 3px;
            padding: 4px;
            margin-bottom: 16px;

            background: var(--card-2) !important;
            border: 1px solid var(--line);
            border-radius: 13px;

            box-shadow: 0 0 0 8px var(--page);
        }

        .stTabs [data-baseweb="tab"] {
            flex: 1 1 0;
            min-width: 0;
            height: auto;
            justify-content: center;

            padding: 9px 4px;
            border-radius: 9px;

            background: transparent !important;
            color: var(--muted) !important;

            font-size: 0.76rem;
            font-weight: 600;
            white-space: normal;
        }

        .stTabs [data-baseweb="tab"] p {
            color: inherit !important;
            font-size: inherit;
            font-weight: inherit;
            line-height: 1.3;
        }

        .stTabs [aria-selected="true"] {
            background: #355055 !important;
            color: var(--text) !important;
            box-shadow: inset 0 -2px 0 var(--green);
        }

        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* =========================================================
           MAIN CONTAINERS
        ========================================================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--card) !important;
            border: 1px solid var(--line) !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 14px rgba(20, 35, 38, 0.13);
            min-width: 0;
        }

        /* Do not paint every nested wrapper with the card color */
        div[data-testid="stVerticalBlockBorderWrapper"] > div,
        div[data-testid="stVerticalBlockBorderWrapper"] > div > div,
        div[data-testid="stVerticalBlockBorderWrapper"]
            [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }

        /* =========================================================
           DASHBOARD BRANDING
        ========================================================= */

        .brand-name {
            color: var(--text) !important;
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.055em;
            line-height: 1.02;
            margin: 2px 0 10px;
            overflow-wrap: anywhere;
        }

        .brand-sub {
            color: var(--muted) !important;
            font-size: 0.92rem;
            font-weight: 400;
            line-height: 1.6;
        }

        .steps {
            color: var(--text);
            font-size: 0.9rem;
            line-height: 1.9;
            margin: 0;
            padding-left: 21px;
        }

        .steps li {
            padding-left: 2px;
        }

        .section-label {
            color: var(--muted) !important;
            font-size: 0.69rem;
            font-weight: 700;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        /* =========================================================
           METRICS
        ========================================================= */

        div[data-testid="stMetric"] {
            background: var(--card-2) !important;
            border: 1px solid var(--line) !important;
            border-radius: 11px !important;
            padding: 10px 12px;
            min-width: 0;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] * {
            color: var(--muted) !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            color: var(--text) !important;
            font-size: 1.45rem;
            font-weight: 700 !important;
            overflow-wrap: anywhere;
        }

        /* =========================================================
           INPUTS
        ========================================================= */

        .stTextArea textarea,
        .stTextInput input,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input {
            background: var(--card-2) !important;
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
            border: 1px solid var(--line) !important;
            border-radius: 9px !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stTextArea textarea:focus,
        .stTextInput input:focus {
            border-color: var(--green) !important;
            box-shadow: 0 0 0 1px var(--green) !important;
        }

        .stTextArea textarea::placeholder,
        .stTextInput input::placeholder {
            color: var(--muted) !important;
            -webkit-text-fill-color: var(--muted) !important;
            opacity: 0.85;
        }

        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] p,
        [data-testid="stRadio"] label,
        [data-testid="stRadio"] p,
        [data-testid="stCheckbox"] label {
            color: var(--text) !important;
        }

        [data-testid="stRadio"] [role="radiogroup"] {
            gap: 8px;
        }

        /* =========================================================
           FILE UPLOADER
        ========================================================= */

        [data-testid="stFileUploader"] {
            min-width: 0;
            padding: 9px;
            background: var(--card-2) !important;
            border: 1px solid var(--line) !important;
            border-radius: 11px !important;
        }

        [data-testid="stFileUploaderDropzone"],
        [data-testid="stFileUploader"] section {
            min-width: 0;
            background: var(--card-2) !important;
            border: 1px dashed var(--line) !important;
            border-radius: 8px !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            max-width: 100%;
        }

        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] span {
            color: var(--muted);
            overflow-wrap: anywhere;
        }

        /* =========================================================
           BUTTONS
        ========================================================= */

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] button {
            width: 100%;
            min-height: 2.6rem;
            padding: 0.62rem 0.9rem;

            background: var(--green) !important;
            color: var(--ink) !important;
            border: 1px solid var(--green) !important;
            border-radius: 10px !important;

            font-family: 'Inter', sans-serif !important;
            font-size: 0.88rem;
            font-weight: 700 !important;

            transition: background 0.15s ease, border-color 0.15s ease;
        }

        .stButton > button p,
        .stDownloadButton > button p,
        [data-testid="stFormSubmitButton"] button p {
            color: var(--ink) !important;
            font-weight: 700 !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            background: var(--green-hover) !important;
            border-color: var(--green-hover) !important;
            color: var(--ink) !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background: var(--card) !important;
            color: var(--text) !important;
            border: 1px solid var(--line) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }

        [data-testid="stFileUploaderDropzone"] button * {
            color: var(--text) !important;
        }

        /* =========================================================
           SCANNER RESULT TILES
        ========================================================= */

        .tile-row {
            display: grid;
            grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
            gap: 9px;
            margin-bottom: 14px;
        }

        .tile {
            min-width: 0;
            padding: 11px 12px;
            background: var(--card-2) !important;
            border: 1px solid var(--line) !important;
            border-radius: 11px !important;
            color: var(--text);
        }

        .tile-label {
            color: var(--muted) !important;
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.075em;
            text-transform: uppercase;
            line-height: 1.4;
            margin-bottom: 5px;
        }

        .tile-value {
            color: var(--text);
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1.25;
            overflow-wrap: anywhere;
        }

        .tile-value.small {
            padding-top: 5px;
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .tile-value .denom {
            color: var(--muted);
            font-size: 0.85rem;
            font-weight: 500;
        }

        .pill {
            display: inline-block;
            max-width: 100%;
            padding: 3px 9px;
            border: 1px solid;
            border-radius: 999px;
            font-size: 0.67rem;
            font-weight: 700;
            letter-spacing: 0.035em;
            line-height: 1.4;
            text-transform: uppercase;
            white-space: normal;
            overflow-wrap: anywhere;
        }

        .riskbar {
            height: 8px;
            background: var(--card-2);
            border: 1px solid var(--line);
            border-radius: 5px;
            overflow: hidden;
        }

        .riskbar > div {
            height: 100%;
            border-radius: 5px;
        }

        .riskscale {
            display: flex;
            justify-content: space-between;
            gap: 4px;
            margin-top: 5px;
            color: var(--muted);
            font-size: 0.63rem;
        }

        .engine-note {
            color: var(--muted);
            font-size: 0.75rem;
            line-height: 1.55;
            margin-top: 10px;
            padding-top: 9px;
            border-top: 1px solid var(--line);
            overflow-wrap: anywhere;
        }

        .engine-note b {
            color: var(--text);
        }

        /* =========================================================
           RED FLAGS
        ========================================================= */

        .flag {
            min-width: 0;
            margin-bottom: 10px;
            padding: 12px 13px;
            background: var(--card-2) !important;
            border: 1px solid var(--line) !important;
            border-left: 4px solid var(--c) !important;
            border-radius: 0 10px 10px 0 !important;
        }

        .flag-head {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 7px;
        }

        .flag-type {
            color: var(--text);
            font-size: 0.87rem;
            font-weight: 600;
        }

        .flag-quote {
            margin: 7px 0;
            padding: 7px 9px;
            background: var(--card-3) !important;
            border-radius: 7px;
            color: var(--text) !important;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-size: 0.8rem;
            line-height: 1.55;
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        .flag-reason {
            color: var(--muted);
            font-size: 0.84rem;
            line-height: 1.55;
            overflow-wrap: anywhere;
        }

        /* =========================================================
           RECOMMENDED ACTIONS
        ========================================================= */

        .action-row {
            display: flex;
            align-items: flex-start;
            gap: 9px;
            padding: 9px 0;
            border-bottom: 1px solid var(--line);
            min-width: 0;
        }

        .action-row:last-child {
            border-bottom: none;
        }

        .action-tag {
            flex: 0 0 49px;
            width: 49px;
            padding: 3px 0;
            border: 1px solid;
            border-radius: 6px;
            text-align: center;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .action-tag.avoid {
            color: var(--bad);
            border-color: var(--bad);
            background: #f4a29a22;
        }

        .action-tag.do {
            color: var(--good);
            border-color: var(--good);
            background: #9fd8a622;
        }

        .action-text {
            min-width: 0;
            flex: 1;
            color: var(--text);
            font-size: 0.88rem;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        /* =========================================================
           URL RESULTS
        ========================================================= */

        .url-row {
            padding: 9px 0;
            border-bottom: 1px solid var(--line);
            font-size: 0.84rem;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        .url-row:last-child {
            border-bottom: none;
        }

        .url-row code {
            display: inline-block;
            max-width: 100%;
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        .url-note {
            color: var(--muted);
            font-size: 0.78rem;
        }

        .url-note.bad {
            color: var(--bad);
            font-weight: 600;
        }

        /* =========================================================
           OUT-OF-BAND PLAYBOOK
        ========================================================= */

        .pb-intro {
            margin-bottom: 12px;
            color: var(--muted);
            font-size: 0.81rem;
            line-height: 1.6;
        }

        .pb-step {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 9px 0;
            border-bottom: 1px solid var(--line);
            color: var(--text);
            font-size: 0.88rem;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        .pb-step:last-child {
            border-bottom: none;
        }

        .pb-num {
            display: flex;
            flex: 0 0 24px;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: var(--green);
            color: var(--ink);
            font-size: 0.75rem;
            font-weight: 800;
        }

        .pb-head {
            margin: 12px 0 6px;
            color: var(--text);
            font-weight: 700;
            font-size: 0.9rem;
        }

        .pb-bullets {
            margin: 0;
            padding-left: 19px;
            color: var(--muted);
            font-size: 0.87rem;
            line-height: 1.75;
        }

        .pb-bullets li {
            padding-left: 2px;
            margin-bottom: 4px;
            overflow-wrap: anywhere;
        }

        /* =========================================================
           EMPTY STATE
        ========================================================= */

        .empty {
            padding: 27px 8px;
            text-align: center;
        }

        .empty-title {
            margin-bottom: 7px;
            color: var(--text);
            font-size: 1.05rem;
            font-weight: 700;
        }

        .empty-text {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.65;
        }

        /* =========================================================
           ALERTS AND MISCELLANEOUS WIDGETS
        ========================================================= */

        [data-testid="stAlert"] {
            background: var(--card-2) !important;
            border: 1px solid var(--line) !important;
            border-radius: 11px !important;
        }

        [data-testid="stAlert"] p {
            color: var(--text) !important;
            line-height: 1.55;
        }

        [data-testid="stSpinner"] p {
            color: var(--text) !important;
        }

        hr {
            border-color: var(--line) !important;
        }

        /* =========================================================
           REAL MOBILE SCREENS
        ========================================================= */

        @media (max-width: 500px) {
            [data-testid="stAppViewContainer"]::before,
            [data-testid="stAppViewContainer"]::after {
                display: none !important;
            }

            div.block-container,
            [data-testid="stMainBlockContainer"] {
                width: 100% !important;
                max-width: 100% !important;
                height: auto !important;
                min-height: 100dvh !important;

                margin: 0 !important;
                padding: 22px 14px 32px !important;

                overflow: visible !important;
                border: none !important;
                border-radius: 0 !important;
                box-shadow: none !important;

                background: var(--page) !important;
            }

            div.block-container::before,
            [data-testid="stMainBlockContainer"]::before {
                display: none !important;
            }

            /* Avoid excessively tight spacing in mobile containers */
            [data-testid="stVerticalBlock"] {
                min-width: 0;
                gap: 0.8rem;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 12px !important;
                box-shadow: 0 3px 10px rgba(20, 35, 38, 0.1);
            }

            /* Keep headings distinctive but appropriately sized */
            [data-testid="stMarkdownContainer"] h1 {
                font-size: 1.7rem !important;
                line-height: 1.2 !important;
                letter-spacing: -0.035em;
                overflow-wrap: anywhere;
            }

            [data-testid="stMarkdownContainer"] h2 {
                font-size: 1.35rem !important;
                line-height: 1.3 !important;
            }

            [data-testid="stMarkdownContainer"] h3 {
                font-size: 1.05rem !important;
            }

            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li {
                font-size: 0.9rem;
                line-height: 1.6;
            }

            .brand-name {
                font-size: 2.55rem;
                letter-spacing: -0.045em;
            }

            .brand-sub {
                font-size: 0.88rem;
            }

            /* Tabs stay inside the screen */
            .stTabs [data-baseweb="tab-list"] {
                position: sticky;
                top: 0;
                gap: 2px;
                padding: 3px;
                margin-bottom: 13px;
                border-radius: 11px;
                box-shadow: 0 0 0 5px var(--page);
            }

            .stTabs [data-baseweb="tab"] {
                padding: 9px 2px;
                font-size: 0.7rem;
                white-space: normal;
                overflow-wrap: anywhere;
            }

            .stTabs [data-baseweb="tab"] p {
                font-size: 0.7rem;
                line-height: 1.3;
            }

            /* Result tiles remain a compact two-column grid */
            .tile-row {
                grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
                gap: 7px;
            }

            .tile {
                padding: 9px;
                border-radius: 9px !important;
            }

            .tile-label {
                font-size: 0.61rem;
                letter-spacing: 0.055em;
            }

            .tile-value {
                font-size: 1.35rem;
            }

            .tile-value.small {
                font-size: 0.82rem;
            }

            .riskscale {
                font-size: 0.57rem;
            }

            /* Prevent upload controls and buttons from overflowing */
            [data-testid="stFileUploader"] {
                padding: 6px;
            }

            [data-testid="stFileUploaderDropzone"] {
                padding: 8px !important;
            }

            [data-testid="stFileUploaderDropzone"] button {
                max-width: 100%;
                white-space: normal !important;
            }

            .stButton > button,
            .stDownloadButton > button {
                min-height: 2.8rem;
                padding: 0.65rem 0.7rem;
                white-space: normal !important;
                overflow-wrap: anywhere;
            }

            /* Let long messages and URLs wrap instead of widening the page */
            .flag,
            .flag-quote,
            .flag-reason,
            .action-text,
            .pb-step,
            .pb-bullets,
            .url-row,
            .engine-note {
                min-width: 0;
                overflow-wrap: anywhere;
                word-break: break-word;
            }

            .action-row {
                gap: 7px;
            }

            .action-tag {
                flex-basis: 45px;
                width: 45px;
            }

            /* The screenshot preview must fit the screen */
            [data-testid="stImage"] img {
                width: 100%;
                height: auto;
                object-fit: contain;
            }

            pre,
            code {
                white-space: pre-wrap !important;
                overflow-wrap: anywhere !important;
                word-break: break-word;
            }
        }

        /* Small phones */
        @media (max-width: 360px) {
            div.block-container,
            [data-testid="stMainBlockContainer"] {
                padding-right: 10px !important;
                padding-left: 10px !important;
            }

            .brand-name {
                font-size: 2.2rem;
            }

            .stTabs [data-baseweb="tab"],
            .stTabs [data-baseweb="tab"] p {
                font-size: 0.64rem;
            }

            .tile {
                padding: 8px;
            }

            .tile-value {
                font-size: 1.2rem;
            }

            .tile-value.small {
                font-size: 0.75rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.5-flash-lite"

MODE_CLOUD = "Cloud AI (screenshot)"
MODE_LOCAL = "On-device (private text)"

_SCHEMA = """
Return ONLY valid JSON (no markdown fences, no commentary) matching exactly this schema:
{
  "risk_score": <integer 0-100>,
  "risk_level": "<LOW RISK | SUSPICIOUS | HIGH RISK>",
  "confidence": <integer 0-100>,
  "category": "<one of: Phishing, Payment Scam, Fake Job/Internship, Fake Offer, Banking Scam, Impersonation, Delivery Scam, OTP Scam, Investment Scam, 
  Account Verification Scam, Other>",
  "summary": "<1-3 sentence plain-English explanation>",
  "extracted_text": "<the raw text you read from the message/screenshot>",
  "red_flags": [
    {
      "text": "<exact suspicious snippet>",
      "type": "<short label e.g. Payment Request, Urgency, Suspicious URL, Impersonation>",
      "severity": "<HIGH|MEDIUM|LOW>",
      "reason": "<why this is suspicious>"
    }
  ],
  "actions": ["<short imperative safety action>", "..."]__PLAYBOOK__
}
Rules:
- risk_level must match risk_score using: 0-29 LOW RISK, 30-69 SUSPICIOUS, 70-100 HIGH RISK.
- Never claim certainty. This is an AI risk assessment, not a guarantee.
- If the content looks completely legitimate, still return the schema with a low risk_score and empty/short red_flags.__PLAYBOOK_RULE__
"""

_PLAYBOOK_FIELD = """,
  "playbook": {
    "verify_steps": ["<3-5 specific out-of-band steps for THIS message that name the real organisation and the real channel to use, e.g. open the official app or call the number on the card>"],
    "if_you_already_acted": ["<2-4 concrete damage-control steps for THIS scam type>"],
    "report_to": ["<1-3 places to report this kind of scam>"]
  }"""

_PLAYBOOK_RULE = """
- Playbook: out-of-band means using a channel the sender does not control. Never tell the user to use any link, phone number or contact from the suspicious message. Do not suggest replying to the sender."""

SCHEMA_HINT = _SCHEMA.replace("__PLAYBOOK__", _PLAYBOOK_FIELD).replace("__PLAYBOOK_RULE__", _PLAYBOOK_RULE)

PROMPT_INTRO = (
    f"You are {APP_NAME}, an AI assistant that analyzes screenshots of messages "
    "(SMS, WhatsApp, email, job offers, payment requests, banking alerts, delivery "
    "notifications, etc.) to detect scams. Carefully read all visible text in the image, "
    "then assess scam risk."
)

# Palette: page #69868c, text #e1f5ed, cards a darker shade of the page color.
SEVERITY_COLOR = {"HIGH": "#f4a29a", "MEDIUM": "#f0c27a", "LOW": "#e6d98a"}
RISK_COLOR = {"HIGH RISK": "#f4a29a", "SUSPICIOUS": "#f0c27a", "LOW RISK": "#9fd8a6"}


def esc(value) -> str:
    """HTML-escape any text that came from the user or the AI before putting it in markup."""
    return _html.escape(str(value), quote=True)

# GEMINI
def get_client():
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)


def analyze_image(image: Image.Image):
    from google.genai import types
    client = get_client()
    prompt = f"{PROMPT_INTRO}\n\nAnalyze the attached screenshot.\n{SCHEMA_HINT}"
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt, image],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return response.text



# OUT-OF-BAND PLAYBOOKS (built-in fallbacks, used when the AI omits or garbles its own)
CATEGORY_TO_PLAYBOOK = {
    "Phishing": "account", "Banking Scam": "account", "OTP Scam": "account",
    "Account Verification Scam": "account", "Delivery Scam": "delivery",
    "Fake Job/Internship": "job", "Impersonation": "impersonation",
    "Investment Scam": "investment", "Payment Scam": "payment", "Fake Offer": "payment",
    "Other": "other",
}

PLAYBOOKS = {
    "account": {
        "verify_steps": [
            "Do not tap any link, open any attachment or call any number in the message. Close it.",
            "Open the provider's official app, or type its website address yourself, and look for the same alert in your notifications or inbox there.",
            "If you want to speak to someone, call the number printed on the back of your card or on your latest statement.",
            "Ask the real support team whether they sent this message, and quote its exact wording.",
        ],
        "if_you_already_acted": [
            "Change the password for that account from the official app or site, and for any other account that reuses it.",
            "If you shared card details or a one-time code, call your bank on the number on your card and ask them to block the card and review recent transactions.",
            "Turn on multi-factor authentication and check recent sign-ins for anything you do not recognise.",
        ],
        "report_to": [
            "Forward phishing emails to the impersonated organisation's abuse address and to your country's cybercrime reporting service.",
            "Report scam texts to your mobile carrier (many accept forwarding to 7726).",
        ],
    },
    "delivery": {
        "verify_steps": [
            "Do not tap the link or pay the fee. Real couriers do not collect payment through text links.",
            "Find the tracking number from your order confirmation, then enter it on the courier's official website or app, typed or opened by you.",
            "Check the retailer's order page to confirm you actually have a parcel on its way.",
            "If the courier site shows no problem, delete the message.",
        ],
        "if_you_already_acted": [
            "If you paid, call your card issuer, report the payment as fraud and ask for a replacement card.",
            "Change passwords for any account whose login you typed on the page.",
            "Watch your statements for small test charges over the next weeks.",
        ],
        "report_to": [
            "Forward the text to your carrier's spam reporting number (many accept 7726).",
            "Report it to your national consumer-protection or cybercrime site.",
        ],
    },
    "job": {
        "verify_steps": [
            "Do not send ID, bank details or any fee. Real employers never charge you to start work.",
            "Find the company on its official website and use the careers page or main switchboard to ask whether this recruiter and role exist.",
            "Search the recruiter's name and the company on a professional network and check that the profile is established.",
            "Ask for a written offer on company letterhead and a video interview before sharing anything.",
        ],
        "if_you_already_acted": [
            "If you paid, contact your bank or payment app immediately to dispute the transfer.",
            "If you sent ID, place a fraud alert with your credit bureau and watch for new accounts opened in your name.",
            "Change passwords on any account you shared.",
        ],
        "report_to": [
            "Report the profile or number on the platform where it contacted you.",
            "Report the offer to your national fraud or consumer-protection authority.",
        ],
    },
    "impersonation": {
        "verify_steps": [
            "Stop and do not act on the request, however urgent it sounds.",
            "Contact the real person using a number or channel you already hold, never the one in the message.",
            "Ask a colleague or family member to confirm the request with that person independently.",
            "Check the sender's address or number carefully for lookalike characters.",
        ],
        "if_you_already_acted": [
            "Contact your bank immediately and ask to recall or freeze any payment.",
            "Tell your manager or IT security so others can be warned.",
            "Change passwords if you shared credentials.",
        ],
        "report_to": [
            "Report to your IT or security team if this involved work.",
            "Report to your national fraud reporting service.",
        ],
    },
    "investment": {
        "verify_steps": [
            "Do not transfer money or share wallet or account details.",
            "Check whether the firm is registered with your country's financial regulator, using the regulator's own website.",
            "Search the firm's name with the words scam and complaints.",
            "Be wary of guaranteed returns. Talk to an independent adviser before investing.",
        ],
        "if_you_already_acted": [
            "Stop sending any more money, even if told it is needed to release your funds.",
            "Contact your bank or exchange straight away to try to stop or recall transfers.",
            "Keep screenshots and receipts for the report.",
        ],
        "report_to": [
            "Report to your financial regulator's scam-reporting page.",
            "Report to your national fraud and cybercrime service.",
        ],
    },
    "payment": {
        "verify_steps": [
            "Do not send money, gift cards or crypto, and do not share codes.",
            "Contact the organisation or seller through its official website, not the message.",
            "Confirm any invoice or order in your own records or account.",
            "Ask a trusted person to look at it before you act.",
        ],
        "if_you_already_acted": [
            "Contact your bank or payment provider at once to ask for the payment to be stopped or recalled.",
            "If you paid by gift card, contact the card issuer with the card numbers and receipts.",
            "Change any passwords you shared.",
        ],
        "report_to": [
            "Report to your national fraud reporting service.",
            "Report to the platform or payment provider used.",
        ],
    },
    "other": {
        "verify_steps": [
            "Do not click links, open attachments or reply with personal information.",
            "Find the organisation's official contact details yourself and ask whether they sent this.",
            "Check the sender's address or number for small spelling differences.",
            "If still unsure, ask someone you trust before acting.",
        ],
        "if_you_already_acted": [
            "Change relevant passwords and enable multi-factor authentication.",
            "Contact your bank if any financial details were shared.",
            "Keep screenshots as evidence.",
        ],
        "report_to": ["Report to your national cybercrime or consumer-protection service."],
    },
}


def _str_list(value, limit: int, maxlen: int = 400):
    out = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                out.append(item.strip()[:maxlen])
    return out[:limit]


def sanitize_playbook(pb, category: str):
    """Use the AI's playbook when it is usable, falling back to a built-in one per category."""
    base = PLAYBOOKS[CATEGORY_TO_PLAYBOOK.get(category, "other")]
    if not isinstance(pb, dict):
        return base
    return {
        "verify_steps": _str_list(pb.get("verify_steps"), 6) or base["verify_steps"],
        "if_you_already_acted": _str_list(pb.get("if_you_already_acted"), 5) or base["if_you_already_acted"],
        "report_to": _str_list(pb.get("report_to"), 4) or base["report_to"],
    }


def safe_parse(raw_text: str):
    """Parse Gemini JSON output; fall back gracefully if malformed."""
    if not raw_text:
        return default_result("Empty AI response.")
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```json|^```|```$", "", cleaned, flags=re.MULTILINE).strip()
    try:
        data = json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*}", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except Exception:
                return default_result("Could not parse AI response as JSON.")
        else:
            return default_result("Could not parse AI response as JSON.")
    if not isinstance(data, dict):
        return default_result("Unexpected AI response format.")

    data.setdefault("risk_score", 50)
    data.setdefault("confidence", 50)
    data.setdefault("category", "Other")
    data.setdefault("summary", "No summary provided.")
    data.setdefault("extracted_text", "")
    data.setdefault("red_flags", [])
    data.setdefault("actions", [
        "Do not click suspicious links.",
        "Do not send money or share OTP/PIN.",
        "Verify through the official website or helpline.",
    ])

    try:
        score = int(data["risk_score"])
    except Exception:
        score = 50
    score = max(0, min(100, score))
    data["risk_score"] = score
    data["risk_level"] = (
        "HIGH RISK" if score >= 70 else "SUSPICIOUS" if score >= 30 else "LOW RISK"
    )
    if data["category"] not in CATEGORY_TO_PLAYBOOK:
        data["category"] = "Other"

    cleaned_flags = []
    for f in data.get("red_flags", []) or []:
        if not isinstance(f, dict):
            continue
        sev = str(f.get("severity", "MEDIUM")).upper()
        if sev not in ("HIGH", "MEDIUM", "LOW"):
            sev = "MEDIUM"
        cleaned_flags.append({
            "text": str(f.get("text", ""))[:300],
            "type": str(f.get("type", "Suspicious Content")),
            "severity": sev,
            "reason": str(f.get("reason", "")),
        })
    data["red_flags"] = cleaned_flags
    data["actions"] = _str_list(data.get("actions"), 8) or ["Verify independently before taking any action."]
    data["playbook"] = sanitize_playbook(data.get("playbook"), data["category"])
    return data


def default_result(reason: str):
    return {
        "risk_score": 0,
        "risk_level": "LOW RISK",
        "confidence": 0,
        "category": "Other",
        "failed": True,
        "summary": f"Analysis unavailable: {reason} Please try again or verify manually.",
        "extracted_text": "",
        "red_flags": [],
        "actions": [
            "Do not click suspicious links.",
            "Do not send money or share OTP/PIN.",
            "Verify independently before taking any action.",
        ],
        "playbook": PLAYBOOKS["other"],
    }


# ----------------------------------------------------------------------------
# URL HEURISTICS
# ----------------------------------------------------------------------------
SUSPICIOUS_TLDS = {".xyz", ".info", ".top", ".club", ".click", ".gq", ".tk", ".ml", ".cf", ".support", ".help", ".shop", ".online", ".site", ".link", ".live"}
BRAND_HINTS = ["bank", "paypal", "amazon", "google", "microsoft", "apple", "kyc", "verify", "secure", "delivery", "gov",
               "turnpike", "ezpass", "duquesne", "usps", "fedex", "irs"]


def find_urls(text: str):
    return re.findall(r"(?:https?://|www\.|bit\.ly/)[^\s\"']+", text, flags=re.IGNORECASE)


def score_url(url: str):
    reasons = []
    lower = url.lower()
    if any(lower.endswith(tld) or tld + "/" in lower for tld in SUSPICIOUS_TLDS):
        reasons.append("unusual top-level domain")
    if lower.count("-") >= 3:
        reasons.append("excessive hyphens")
    if lower.count(".") >= 4:
        reasons.append("excessive subdomains")
    if any(b in lower for b in BRAND_HINTS) and not any(
        official in lower for official in [".gov", ".com/", ".co."]
    ):
        reasons.append("uses a trusted brand name in a non-official domain")
    if "bit.ly" in lower or "tinyurl" in lower:
        reasons.append("shortened/obfuscated link")
    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", lower):
        reasons.append("raw IP address used instead of domain")
    return reasons


# ON-DEVICE ANALYSIS (nothing leaves this computer)
def _rx(pattern: str):
    return re.compile(pattern, re.IGNORECASE)


# (pattern, flag type, severity, reason, risk points)
OFFLINE_RULES = [
    (_rx(r"\b(within \d+ ?(?:minutes?|mins?|hours?|hrs?)|today at \d|immediately|right away|act now|final (?:notice|warning|reminder)|urgent|asap|expires? (?:today|tonight))\b"),
     "Urgency", "HIGH", "A manufactured deadline meant to stop you thinking or checking.", 18),
    (_rx(r"\b(disconnect\w*|shut ?off|suspend\w*|locked|blocked|frozen|terminated|deactivat\w+|arrest\w*|legal action|lawsuit|warrant|late fee|penalt\w+|collections?)\b"),
     "Threat", "HIGH", "Threatens a penalty or loss to force quick action.", 18),
    (_rx(r"\b(otp|one[- ]time (?:code|password|pin)|verification code|passcode|password|cvv|card number|security code|social security|ssn|routing number|account number)\b"),
     "Sensitive data request", "HIGH", "Asks for codes, credentials or financial identifiers that real organisations do not request this way.", 22),
    (_rx(r"\b(gift cards?|prepaid (?:card|cash)|bitcoin(?: atm)?|crypto(?:currency)?|zelle|cash ?app|venmo|wire transfer|western union|money order)\b"),
     "Unusual payment method", "HIGH", "Requests a payment method that is hard to trace or reverse.", 22),
    (_rx(r"\b(pay(?:ment)?|fee|balance|invoice|owe[sd]?|overdue|past due|unpaid)\b"),
     "Payment demand", "MEDIUM", "Pressures you to send money.", 10),
    (_rx(r"\b(do not tell|don't tell|keep this (?:between|private|confidential)|do not (?:hang up|call|contact)|don't (?:hang up|call))\b"),
     "Secrecy / isolation", "HIGH", "Tries to stop you from checking with anyone else.", 16),
    (_rx(r"\b(congratulations|you(?:'ve| have) (?:won|been selected)|free (?:gift|iphone|prize)|claim your|lottery|prize|guaranteed returns?|risk[- ]free|no experience (?:needed|required))\b"),
     "Too good to be true", "MEDIUM", "Promises a reward or return that is out of proportion to the effort.", 14),
    (_rx(r"\b(dear (?:customer|user|member|client|account holder)|valued customer)\b"),
     "Generic greeting", "LOW", "The sender does not know your name.", 8),
    (_rx(r"\b(telegram|whatsapp me|message me on|text me at)\b"),
     "Unofficial channel", "MEDIUM", "Moves the conversation to a private app.", 10),
    (_rx(r"\b(duquesne light|pa turnpike|pennsylvania turnpike|e-?zpass|toll|irs|social security administration|medicare|usps|ups|fedex|dhl|bank|credit union|paypal|amazon|apple|microsoft|netflix|electric|utility|customer (?:care|service)|fraud (?:department|team)|security team)\b"),
     "Brand or authority impersonation", "MEDIUM", "Names a trusted organisation. Scammers borrow these names, so check through that organisation's own channels.", 8),
]

OFFLINE_CATEGORIES = [
    (_rx(r"\b(otp|one[- ]time|verification code)\b"), "OTP Scam"),
    (_rx(r"\b(parcel|package|delivery|redeliver\w*|courier|tracking)\b"), "Delivery Scam"),
    (_rx(r"\b(job|salary|hiring|recruit\w*|position|internship|work from home)\b"), "Fake Job/Internship"),
    (_rx(r"\b(invest\w*|crypto\w*|trading|returns?|profit)\b"), "Investment Scam"),
    (_rx(r"\b(bank|credit union|kyc|account (?:is |has been )?(?:locked|blocked|suspended))\b"), "Banking Scam"),
    (_rx(r"\b(toll|e-?zpass|turnpike|duquesne light|utility|electric|bill|invoice|fee|balance)\b"), "Payment Scam"),
    (_rx(r"\b(prize|winner|lottery|congratulations|free)\b"), "Fake Offer"),
]


def analyze_offline(text: str):
    """Rule-based scam check. Runs entirely in Python on this device, with no model and no network."""
    flags, points = [], 0
    for rx, kind, severity, reason, pts in OFFLINE_RULES:
        m = rx.search(text)
        if m:
            flags.append({"text": m.group(0), "type": kind, "severity": severity, "reason": reason})
            points += pts
    for url in find_urls(text):
        problems = score_url(url)
        if problems:
            flags.append({"text": url, "type": "Suspicious link", "severity": "HIGH",
                          "reason": "This link has warning signs: " + ", ".join(problems) + "."})
            points += 25
        else:
            flags.append({"text": url, "type": "Link in an unexpected message", "severity": "MEDIUM",
                          "reason": "Do not open links in unsolicited messages. Go to the organisation's site yourself."})
            points += 8

    score = min(100, points)
    category = next((name for rx, name in OFFLINE_CATEGORIES if rx.search(text)), "Phishing" if find_urls(text) else "Other")
    kinds = ", ".join(dict.fromkeys(f["type"].lower() for f in flags[:3]))
    if score >= 70:
        summary = f"This message shows classic scam signals ({kinds}). Treat it as a scam unless you verify it through an official channel."
    elif score >= 30:
        summary = f"This message has some warning signs ({kinds}). Verify it through an official channel before acting."
    else:
        summary = "The built-in rules found no strong scam signals. Rules cannot catch everything, so verify anything unexpected."
    actions = [
        "Do not click links or open attachments in the message.",
        "Do not share codes, passwords or card details.",
        "Verify through the organisation's official app, website, or the number on your bill or card.",
    ]
    if any(f["type"] == "Unusual payment method" for f in flags):
        actions.append("Never pay by gift card, crypto, prepaid card or Zelle to someone who contacted you first.")
    return safe_parse(json.dumps({
        "risk_score": score, "confidence": min(85, 40 + 6 * len(flags)) if flags else 50, "category": category,
        "summary": summary, "extracted_text": text, "red_flags": flags, "actions": actions,
    }))


# PRIVATE PYTHON RULE-BASED ANALYSIS
def analyze_on_device(text: str):
        """Analyze text using built-in Python rules without a model or network."""
        result = analyze_offline(text)
        result["engine"] = "built-in Python rules"
        result["private"] = True
        return result
# ----------------------------------------------------------------------------
# UI COMPONENTS
# ----------------------------------------------------------------------------
def pill(label: str, color: str) -> str:
    return (
        f'<span class="pill" style="color:{color};background:{color}26;'
        f'border-color:{color};">{esc(label)}</span>'
    )


def label(text: str):
    st.markdown(f'<div class="section-label">{esc(text)}</div>', unsafe_allow_html=True)


def numbered(items) -> str:
    return "".join(
        f'<div class="pb-step"><span class="pb-num">{i}</span><span>{esc(t)}</span></div>'
        for i, t in enumerate(items, 1)
    )


def render_playbook(result: dict):
    pb = result.get("playbook") or PLAYBOOKS["other"]

    with st.container(border=True):
        label("Out-of-band playbook")
        st.markdown(
            '<div class="pb-intro">Out-of-band means checking through a channel the sender does not control. '
            "Do not reply, and do not use any link, phone number or contact that appears in the suspicious message.</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="pb-head" style="margin-top:0">Verify independently</div>', unsafe_allow_html=True)
        st.markdown(numbered(pb["verify_steps"]), unsafe_allow_html=True)

    with st.container(border=True):
        label("If you already responded")
        st.markdown(
            '<ul class="pb-bullets">' + "".join(f"<li>{esc(t)}</li>" for t in pb["if_you_already_acted"]) + "</ul>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="pb-head">Report it</div>', unsafe_allow_html=True)
        st.markdown(
            '<ul class="pb-bullets">' + "".join(f"<li>{esc(t)}</li>" for t in pb["report_to"]) + "</ul>",
            unsafe_allow_html=True,
        )


def render_results(result: dict, image: Image.Image = None):
    level = result["risk_level"]
    color = RISK_COLOR.get(level, "#e1f5ed")
    engine = esc(result.get("engine", "AI"))
    engine_note = (
        f"Analyzed on this device by <b>{engine}</b>. Your message was not sent to any cloud service."
        if result.get("private") else f"Analyzed in the cloud by <b>{engine}</b>."
    )

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="section-label">Risk assessment</div>
            <div class="tile-row">
              <div class="tile">
                <div class="tile-label">Risk score</div>
                <div class="tile-value" style="color:{color};">{result['risk_score']}<span class="denom"> / 100</span></div>
              </div>
              <div class="tile">
                <div class="tile-label">Risk level</div>
                <div class="tile-value small">{pill(level, color)}</div>
              </div>
              <div class="tile">
                <div class="tile-label">Confidence</div>
                <div class="tile-value">{esc(result['confidence'])}%</div>
              </div>
              <div class="tile">
                <div class="tile-label">Category</div>
                <div class="tile-value small">{esc(result['category'])}</div>
              </div>
            </div>
            <div class="riskbar"><div style="width:{result['risk_score']}%;background:{color};"></div></div>
            <div class="riskscale"><span>0</span><span>Suspicious 30</span><span>High 70</span><span>100</span></div>
            <div class="engine-note">{engine_note}</div>
            """,
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        label("Summary")
        st.write(result["summary"])

    with st.container(border=True):
        label(f"Red flags ({len(result['red_flags'])})")
        if result["red_flags"]:
            for f in result["red_flags"]:
                sev = f["severity"]
                st.markdown(
                    f"""<div class="flag" style="--c:{SEVERITY_COLOR[sev]};">
                    <div class="flag-head">{pill(sev, SEVERITY_COLOR[sev])}
                    <span class="flag-type">{esc(f['type'])}</span></div>
                    <div class="flag-quote">{esc(f['text'])}</div>
                    <div class="flag-reason">{esc(f['reason'])}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            st.write("No red flags detected.")

    if image is not None:
        with st.container(border=True):
            label("Analyzed screenshot")
            st.image(image)
            if result["red_flags"]:
                tags = " ".join(pill(f["type"], SEVERITY_COLOR[f["severity"]]) for f in result["red_flags"])
                st.markdown(tags, unsafe_allow_html=True)
                st.caption(
                    "Exact on-image coordinates are not always reliable, so flags are "
                    "summarized as tags and detailed above."
                )
            else:
                st.caption("No specific red-flag regions detected.")

    urls = find_urls(result.get("extracted_text", "") or "")
    if urls:
        with st.container(border=True):
            label("Detected URLs (not visited)")
            rows = ""
            for u in urls:
                reasons = score_url(u)
                if reasons:
                    note = f'<span class="url-note bad">Suspicious: {esc(", ".join(reasons))}</span>'
                else:
                    note = '<span class="url-note">No obvious red flags found</span>'
                rows += f'<div class="url-row"><code>{esc(u)}</code><br>{note}</div>'
            st.markdown(rows, unsafe_allow_html=True)

    with st.container(border=True):
        label("Recommended actions")
        rows = ""
        for a in result["actions"]:
            avoid = any(w in a.lower() for w in ["don't", "do not", "avoid", "never"])
            tag = '<span class="action-tag avoid">Avoid</span>' if avoid else '<span class="action-tag do">Do</span>'
            rows += f'<div class="action-row">{tag}<span class="action-text">{esc(a)}</span></div>'
        st.markdown(rows, unsafe_allow_html=True)

    render_playbook(result)


def render_empty_state():
    with st.container(border=True):
        st.markdown(
            """
            <div class="empty">
              <div class="empty-title">No analysis yet</div>
              <div class="empty-text">
                Upload a screenshot of a suspicious message
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# DASHBOARD TAB
def render_dashboard_tab():
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="brand-name">{APP_NAME}</div>
            <div class="brand-sub">AI-powered scam detection for messages, emails and screenshots.</div>
            """,
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        label("How it works")
        st.markdown(
            '<ol class="steps">'
            "<li>Upload a screenshot</li>"
            "<li>AI analyzes the content</li>"
            "<li>Risk is calculated</li>"
            "<li>Red flags are identified</li>"
            "<li>Safety actions are recommended</li>"
            "</ol>",
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        label("Session statistics")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Scans performed", st.session_state.stats["scans"])
        with c2:
            st.metric("High-risk detections", st.session_state.stats["high_risk"])


# SCANNER TAB
def render_scanner_tab():
    pending = None  # ("cloud", image) or ("local", text)

    with st.container(border=True):
        label("Input")
        mode = st.radio("Analysis mode", [MODE_CLOUD, MODE_LOCAL], horizontal=True,
                        label_visibility="collapsed", key="scan_mode")

        if mode == MODE_CLOUD:
            if not GEMINI_API_KEY:
                st.error("GEMINI_API_KEY is not set. Add it to a `.env` file before scanning.")
            st.caption("Drag and drop an SMS, WhatsApp, email or suspicious message screenshot.")
            uploaded = st.file_uploader(
                "Upload screenshot", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed"
            )
            image = None
            if uploaded is not None:
                try:
                    image = Image.open(uploaded).convert("RGB")
                    st.image(image, caption="Preview")
                except Exception:
                    st.error("Could not read this image. Please upload a valid PNG, JPG, JPEG or WEBP file.")

            if st.button("Scan for scams", key="scan_cloud"):
                if not GEMINI_API_KEY:
                    st.error("Cannot scan: GEMINI_API_KEY is missing.")
                elif image is None:
                    st.warning("Please upload a screenshot first.")
                else:
                    pending = ("cloud", image)
        else:
            st.caption(
                "Private mode. No AI model is used."
            )
            text = st.text_area(
                "Message text", key="local_text", height=170, label_visibility="collapsed",
                placeholder="Paste the text of the message here...",
            )
            if st.button("Analyze on this device", key="scan_local"):
                if text.strip():
                    pending = ("local", text.strip())
                else:
                    st.warning("Please paste the message text first.")

    if pending is not None:
        kind, payload = pending
        result, error = None, None
        with st.spinner("Analyzing with Gemini AI..." if kind == "cloud" else "Analyzing on this device..."):
            try:
                if kind == "cloud":
                    result = safe_parse(analyze_image(payload))
                    if result.get("failed"):
                        error, result = result["summary"], None
                    else:
                        result["engine"], result["private"] = MODEL_NAME, False
                else:
                    result = analyze_on_device(payload)
            except Exception as exc:
                error = f"Gemini API error: {type(exc).__name__}: {exc}"

        if error:
            st.error(error)
        else:
            st.session_state.stats["scans"] += 1
            if result["risk_level"] == "HIGH RISK":
                st.session_state.stats["high_risk"] += 1
            st.session_state.last = {"result": result, "image": payload if kind == "cloud" else None}
            st.rerun()  # refresh the Dashboard statistics along with the results

    last = st.session_state.get("last")
    if last:
        render_results(last["result"], image=last["image"])
    else:
        render_empty_state()


# ----------------------------------------------------------------------------
# GAME TAB
# ----------------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def _find_game_dir():
    """Find the folder that holds the game's index.html."""
    for folder in (os.path.join(APP_DIR, "game"), os.path.join(os.getcwd(), "game"), APP_DIR):
        if os.path.isfile(os.path.join(folder, "index.html")):
            return folder
    return os.path.join(APP_DIR, "game")  # default (may not exist)


GAME_DIR = _find_game_dir()

# Shows any JavaScript error as a banner inside the game frame instead of a silent blank page.
ERROR_BANNER = """
<script>
window.addEventListener('error', function (e) {
  var d = document.createElement('div');
  d.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;background:#f4a29a;'
    + 'color:#1c2e31;padding:10px 14px;font:14px/1.4 monospace;white-space:pre-wrap;';
  d.textContent = 'Game error: ' + e.message + ' (line ' + e.lineno + ')';
  document.documentElement.appendChild(d);
});
</script>
"""


def _read(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def load_game_html():
    """
    components.html() renders the HTML string inside an iframe with no file access,
    so <link href="style.css"> and <script src="script.js"> never load. Inline them.
    """
    html = _read(os.path.join(GAME_DIR, "index.html"))
    if html is None:
        return None, ["index.html"]

    missing = []

    css = _read(os.path.join(GAME_DIR, "style.css"))
    if css is None:
        missing.append("style.css")
    else:
        html = re.sub(
            r'<link[^>]*href=["\']style\.css["\'][^>]*>',
            lambda m: f"<style>\n{css}\n</style>",
            html,
            count=1,
        )

    js = _read(os.path.join(GAME_DIR, "script.js"))
    if js is None:
        missing.append("script.js")
    else:
        # The game's code contains the text "</script>" inside strings; escape it so the
        # browser does not end the inline script early.
        js = js.replace("</script>", "<\\/script>")
        html = re.sub(
            r'<script[^>]*src=["\']script\.js["\'][^>]*>\s*</script>',
            lambda m: f"<script>\n{js}\n</script>",
            html,
            count=1,
        )

    if "</head>" in html:
        html = html.replace("</head>", ERROR_BANNER + "</head>", 1)
    else:
        html = ERROR_BANNER + html

    return html, missing


def render_game_tab():
    try:
        game_html, missing = load_game_html()
    except Exception as exc:
        st.error(f"Could not load the game: {exc}")
        return

    if game_html is None:
        try:
            listing = ", ".join(sorted(os.listdir(APP_DIR))) or "(empty)"
        except Exception:
            listing = "(could not list)"
        st.error(
            f"Could not find the game's `index.html`. I looked in `{GAME_DIR}` and nearby folders. "
            "Create a folder named `game` next to `app.py` and put `index.html`, "
            "`style.css` and `script.js` inside it."
        )
        st.caption(f"Files currently next to app.py ({APP_DIR}): {listing}")
        return

    if missing:
        st.warning(
            "Missing game files: " + ", ".join(f"`{m}`" for m in missing)
            + ". The game may look unstyled or not respond to clicks."
        )
    components.html(game_html, height=600, scrolling=True)


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main():
    inject_css()

    if "stats" not in st.session_state:
        st.session_state.stats = {"scans": 0, "high_risk": 0}

    # Tabs are the very first element on the page (the top navigation of the "phone").
    dashboard_tab, scanner_tab, game_tab = st.tabs(["Dashboard", "Scanner", "Detective"])

    with dashboard_tab:
        render_dashboard_tab()

    with scanner_tab:
        render_scanner_tab()

    with game_tab:
        render_game_tab()



if __name__ == "__main__":
    main()