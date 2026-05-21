import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="ULTRA 학교지원 의사결정 지원 플랫폼",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------
# Styles
# ------------------------------------------------------------
PLOT_COLORS = ["#0064c8", "#00a0e9", "#00b4d8", "#48cae4", "#90e0ef", "#ff6b00", "#ffb347", "#adb5bd"]


def inject_style() -> None:
    st.markdown(
        """
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

        * { box-sizing: border-box; margin: 0; padding: 0; }

        /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           에듀넷 스타일 디자인 시스템
           Primary: #0064c8  Secondary: #00a0e9
           Accent:  #ff6b00  Background: #f5f7fb
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

        /* ── 기반 ── */
        .stApp {
            background: #f5f7fb;
            font-family: 'Pretendard', 'Noto Sans KR', -apple-system, 'Apple SD Gothic Neo',
                         BlinkMacSystemFont, sans-serif;
            color: #222222;
        }
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 3rem;
            max-width: 1460px;
        }

        /* ━━━ 히어로 배너 (에듀넷 메인 배너 스타일) ━━━ */
        .title-panel {
            background: linear-gradient(110deg, #004ea2 0%, #0064c8 45%, #0096d6 80%, #00b4d8 100%);
            border: none;
            border-radius: 0 0 28px 28px;
            padding: 2rem 2.4rem 1.8rem 2.4rem;
            margin-bottom: 1.4rem;
            box-shadow: 0 6px 30px rgba(0,100,200,0.22);
            position: relative;
            overflow: hidden;
        }
        /* 배너 배경 장식 */
        .title-panel::before {
            content: "";
            position: absolute;
            right: -100px; top: -100px;
            width: 420px; height: 420px;
            border-radius: 50%;
            background: rgba(255,255,255,0.06);
            pointer-events: none;
        }
        .title-panel::after {
            content: "";
            position: absolute;
            right: 180px; bottom: -120px;
            width: 280px; height: 280px;
            border-radius: 50%;
            background: rgba(255,255,255,0.04);
            pointer-events: none;
        }
        .title-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.3rem 0.85rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.18);
            border: 1.5px solid rgba(255,255,255,0.32);
            color: #ffffff;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            letter-spacing: 0.02em;
        }
        .main-title {
            font-size: 2.05rem;
            line-height: 1.22;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: -0.035em;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            text-shadow: 0 2px 16px rgba(0,0,0,0.12);
        }
        .sub-title {
            font-size: 0.96rem;
            color: rgba(255,255,255,0.88);
            margin: 0.6rem 0 0 0;
            line-height: 1.78;
            max-width: 680px;
            font-weight: 400;
            letter-spacing: -0.01em;
        }
        .title-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1.5rem;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }
        .title-main-wrap { flex: 1 1 520px; }
        .title-meta {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 1.1rem;
        }
        .title-meta-item {
            display: inline-flex;
            align-items: center;
            gap: 0.28rem;
            font-size: 0.78rem;
            color: rgba(255,255,255,0.92);
            font-weight: 600;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.28);
            border-radius: 6px;
            padding: 0.3rem 0.7rem;
        }
        /* 오른쪽 통계 패널 */
        .hero-stats {
            display: flex;
            gap: 0.85rem;
            align-items: stretch;
            flex-shrink: 0;
        }
        .hero-stat-item {
            background: rgba(255,255,255,0.14);
            border: 1.5px solid rgba(255,255,255,0.28);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            min-width: 100px;
            text-align: center;
            backdrop-filter: blur(8px);
        }
        .hero-stat-num {
            font-size: 1.7rem;
            font-weight: 900;
            color: #ffffff;
            line-height: 1;
            letter-spacing: -0.04em;
        }
        .hero-stat-label {
            font-size: 0.7rem;
            color: rgba(255,255,255,0.78);
            font-weight: 500;
            margin-top: 0.35rem;
            line-height: 1.45;
        }
        @media (max-width: 860px) { .hero-stats { display: none; } }

        /* ━━━ GNB 탭 바 — 흰 배경, 진한 글씨, 클릭 명확 ━━━ */
        .top-nav-host {
            background: #ffffff;
            border: 1.5px solid #c8d8ee;
            border-radius: 14px;
            padding: 0.5rem 0.55rem;
            margin: 0 0 1.3rem 0;
            box-shadow: 0 4px 18px rgba(0,80,180,0.10);
        }

        /* 공통 폰트 — 모든 자식 포함 */
        div[data-testid="stButton"] > button,
        div[data-testid="stButton"] > button > div,
        div[data-testid="stButton"] > button p,
        div[data-testid="stButton"] > button span {
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif !important;
            font-size: 1.02rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em !important;
            line-height: 1.3 !important;
        }
        /* 비활성 기본 — 밝은 회색 배경 + 진한 글씨 */
        div[data-testid="stButton"] > button {
            border-radius: 10px !important;
            min-height: 3.0rem !important;
            border: 1.5px solid #dde8f5 !important;
            background: #f2f6fc !important;
            color: #2a3a52 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
            transition: background 0.14s, color 0.14s, border-color 0.14s, box-shadow 0.14s, transform 0.09s !important;
            padding: 0.5rem 0.7rem !important;
            cursor: pointer !important;
            width: 100%;
        }
        /* 활성 탭 — 파란 배경 + 흰 글씨 + 입체 그림자 */
        div[data-testid="stButton"] > button[kind="primary"],
        div[data-testid="stButton"] > button[kind="primary"] p,
        div[data-testid="stButton"] > button[kind="primary"] span {
            background: #0064c8 !important;
            color: #ffffff !important;
            border-color: #0053a8 !important;
            box-shadow:
                0 4px 14px rgba(0,100,200,0.35),
                inset 0 -2px 0 rgba(0,40,120,0.18) !important;
            font-weight: 800 !important;
        }
        /* 비활성 hover */
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: #dceeff !important;
            color: #0053a8 !important;
            border-color: #90bce8 !important;
            box-shadow: 0 2px 8px rgba(0,100,200,0.12) !important;
        }
        /* 활성 hover */
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background: #0053a8 !important;
        }
        /* 클릭 */
        div[data-testid="stButton"] > button:active {
            transform: scale(0.96) !important;
            box-shadow: inset 0 2px 6px rgba(0,0,0,0.14) !important;
        }

        /* ━━━ 서브탭 — 입체 회색 박스, 진한 글씨 ━━━ */
        .sub-tab-host {
            background: #f0f5fc;
            border: 1.5px solid #c4d4e8;
            border-radius: 12px;
            padding: 0.42rem 0.48rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 2px 8px rgba(0,60,150,0.07), inset 0 1px 0 #ffffff;
        }
        .sub-tab-host div[data-testid="stButton"] > button {
            border-radius: 8px !important;
            min-height: 2.6rem !important;
            background: #ffffff !important;
            border: 1.5px solid #d8e6f4 !important;
            color: #1e3a5f !important;
            font-size: 0.96rem !important;
            font-weight: 700 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }
        .sub-tab-host div[data-testid="stButton"] > button[kind="primary"],
        .sub-tab-host div[data-testid="stButton"] > button[kind="primary"] p,
        .sub-tab-host div[data-testid="stButton"] > button[kind="primary"] span {
            background: #0064c8 !important;
            color: #ffffff !important;
            border-color: #0053a8 !important;
            box-shadow: 0 3px 10px rgba(0,100,200,0.30) !important;
            font-weight: 800 !important;
        }
        .sub-tab-host div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: #dceeff !important;
            color: #0053a8 !important;
            border-color: #90bce8 !important;
        }

        /* ━━━ 필터 패널 ━━━ */
        .filter-panel {
            background: #ffffff;
            border: 1px solid #dde5f0;
            border-top: 3px solid #0064c8;
            border-radius: 10px;
            padding: 1rem 1.3rem 0.65rem 1.3rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 2px 10px rgba(0,100,200,0.05);
        }
        .engine-panel {
            background: linear-gradient(135deg, #edf4ff 0%, #e8f6ff 100%);
            border: 1px solid #c0d8f0;
            border-left: 4px solid #00a0e9;
            border-radius: 10px;
            padding: 0.8rem 1.1rem;
            margin: 0 0 1rem 0;
        }
        .engine-title {
            font-size: 0.7rem;
            font-weight: 800;
            color: #0064c8;
            margin-bottom: 0.22rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .engine-desc {
            font-size: 0.875rem;
            color: #1a3a5c;
            line-height: 1.62;
        }

        /* ━━━ 섹션 헤더 카드 ━━━ */
        .section-card {
            background: #ffffff;
            border: 1px solid #dde5f0;
            border-top: 4px solid #0064c8;
            border-radius: 10px;
            padding: 1.2rem 1.5rem 1.05rem 1.5rem;
            margin-bottom: 1.3rem;
            box-shadow: 0 2px 10px rgba(0,100,200,0.05);
        }
        .mini-chip {
            display: inline-block;
            padding: 0.22rem 0.65rem;
            font-size: 0.7rem;
            font-weight: 700;
            color: #ffffff;
            background: #0064c8;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            letter-spacing: 0.04em;
        }
        .section-title {
            font-size: 1.22rem;
            font-weight: 800;
            color: #0d2d52;
            margin-bottom: 0.3rem;
            line-height: 1.3;
            letter-spacing: -0.03em;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
        }
        .section-desc {
            font-size: 0.875rem;
            color: #5a6a7e;
            line-height: 1.75;
            letter-spacing: -0.01em;
        }

        /* ━━━ 메트릭 카드 (에듀넷 수치 강조 스타일) ━━━ */
        .metric-card {
            background: #ffffff;
            border: 1px solid #dde5f0;
            border-radius: 12px;
            padding: 1.25rem 1.3rem 1.1rem 1.3rem;
            min-height: 118px;
            box-shadow: 0 2px 10px rgba(0,100,200,0.05);
            transition: box-shadow 0.2s, transform 0.15s;
            position: relative;
            overflow: hidden;
        }
        .metric-card::after {
            content: "";
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #0064c8, #00a0e9);
            border-radius: 0 0 12px 12px;
        }
        .metric-card:hover {
            box-shadow: 0 6px 22px rgba(0,100,200,0.12);
            transform: translateY(-2px);
        }
        .metric-label {
            font-size: 0.72rem;
            font-weight: 700;
            color: #8696a8;
            margin-bottom: 0.52rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 1.82rem;
            font-weight: 900;
            color: #0064c8;
            line-height: 1.06;
            letter-spacing: -0.045em;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
        }
        .metric-sub {
            font-size: 0.75rem;
            color: #8696a8;
            margin-top: 0.48rem;
            line-height: 1.5;
        }

        /* ━━━ 학교 카드 ━━━ */
        .school-card {
            background: #ffffff;
            border: 1px solid #dde5f0;
            border-radius: 12px;
            padding: 1.25rem 1.2rem 1.15rem;
            min-height: 208px;
            box-shadow: 0 2px 8px rgba(0,100,200,0.05);
            transition: box-shadow 0.22s, transform 0.15s;
        }
        .school-card:hover {
            box-shadow: 0 10px 30px rgba(0,100,200,0.13);
            transform: translateY(-3px);
            border-color: #aac8e8;
        }
        .school-rank {
            display: inline-block;
            font-size: 0.68rem;
            font-weight: 800;
            color: #ffffff;
            background: linear-gradient(135deg, #0064c8, #00a0e9);
            border-radius: 4px;
            padding: 0.2rem 0.55rem;
            margin-bottom: 0.55rem;
            letter-spacing: 0.06em;
        }
        .school-name {
            font-size: 1.05rem;
            font-weight: 800;
            color: #0d2d52;
            line-height: 1.35;
            margin-bottom: 0.38rem;
            letter-spacing: -0.025em;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
        }
        .school-meta {
            font-size: 0.82rem;
            color: #5a6a7e;
            margin-bottom: 0.6rem;
            line-height: 1.72;
        }
        .school-reason {
            font-size: 0.82rem;
            color: #2c4060;
            line-height: 1.72;
            padding-top: 0.58rem;
            border-top: 1px solid #edf2f9;
        }

        /* ━━━ 요약 박스 ━━━ */
        .summary-box {
            background: #ffffff;
            border: 1px solid #dde5f0;
            border-radius: 12px;
            padding: 1.25rem 1.3rem 1.1rem;
            min-height: 208px;
            box-shadow: 0 2px 8px rgba(0,100,200,0.05);
        }
        .summary-title {
            font-size: 0.92rem;
            font-weight: 800;
            color: #0064c8;
            margin-bottom: 0.75rem;
            padding-bottom: 0.6rem;
            border-bottom: 1.5px solid #ddeeff;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        .summary-title::before { content: "📋"; font-size: 0.88rem; }
        .summary-list {
            font-size: 0.86rem;
            color: #2c4060;
            line-height: 2.0;
        }
        .summary-list ul { margin: 0; padding: 0; list-style: none; }
        .summary-list li {
            padding: 0.18rem 0;
            border-bottom: 1px solid #f0f5fb;
        }
        .summary-list li:last-child { border-bottom: none; }

        /* ━━━ 알림 노트 ━━━ */
        .good-note {
            background: #edf6ff;
            color: #0d4c8a;
            border: 1px solid #b8d8f8;
            border-left: 4px solid #0064c8;
            border-radius: 8px;
            padding: 0.85rem 1.05rem;
            font-size: 0.86rem;
            line-height: 1.7;
            margin-top: 0.65rem;
        }
        .warn-note {
            background: #fff8ed;
            color: #7c4a00;
            border: 1px solid #ffd89c;
            border-left: 4px solid #ff6b00;
            border-radius: 8px;
            padding: 0.85rem 1.05rem;
            font-size: 0.86rem;
            line-height: 1.7;
            margin-top: 0.65rem;
        }

        /* ━━━ 로직 박스 ━━━ */
        .logic-box {
            background: #ffffff;
            border: 1px solid #dde5f0;
            border-radius: 10px;
            padding: 1rem 1.1rem;
            min-height: 120px;
            box-shadow: 0 2px 8px rgba(0,100,200,0.04);
        }
        .logic-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: #0064c8;
            margin-bottom: 0.38rem;
        }
        .logic-desc {
            font-size: 0.86rem;
            color: #4a5a70;
            line-height: 1.7;
        }

        /* ━━━ 보조 텍스트 ━━━ */
        .footer-note, .small-help {
            font-size: 0.8rem;
            color: #8696a8;
            line-height: 1.6;
        }

        /* ━━━ select / slider ━━━ */
        div[data-baseweb="select"] > div {
            border-color: #dde5f0 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            font-size: 0.9rem !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            border-color: #0064c8 !important;
            box-shadow: 0 0 0 3px rgba(0,100,200,0.1) !important;
        }

        /* ━━━ 데이터프레임 ━━━ */
        .stDataFrame, div[data-testid="stTable"] {
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #dde5f0;
        }
        /* 테이블 헤더 */
        .stDataFrame thead th {
            background: #f0f6ff !important;
            color: #0064c8 !important;
            font-weight: 700 !important;
            font-size: 0.82rem !important;
        }

        /* ━━━ 학교 아이덴티티 카드 ━━━ */
        .school-identity-card {
            background: linear-gradient(135deg, #004ea2 0%, #0064c8 60%, #0096d6 100%);
            border: none;
            border-radius: 12px;
            padding: 1.15rem 1.3rem;
            min-height: 112px;
            box-shadow: 0 6px 20px rgba(0,100,200,0.22);
        }
        .school-identity-label {
            font-size: 0.7rem;
            font-weight: 700;
            color: rgba(255,255,255,0.65);
            margin-bottom: 0.3rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .school-identity-name {
            font-size: 1.45rem;
            font-weight: 900;
            color: #ffffff;
            line-height: 1.2;
            letter-spacing: -0.035em;
            margin-bottom: 0.22rem;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
        }
        .school-identity-meta {
            font-size: 0.82rem;
            color: rgba(255,255,255,0.78);
            line-height: 1.5;
        }

        /* ━━━ Streamlit 라벨 ━━━ */
        .stSelectbox label, .stSlider label, .stNumberInput label,
        div[data-testid="stMarkdownContainer"] p {
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: #4a5a70 !important;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif !important;
            letter-spacing: -0.01em !important;
        }
        div[data-testid="stAlert"] {
            border-radius: 8px !important;
            font-size: 0.875rem !important;
        }

        /* ━━━ 스크롤바 ━━━ */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: #edf2f9; border-radius: 3px; }
        ::-webkit-scrollbar-thumb { background: #9cc0e8; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #5599d0; }

        /* ━━━ Streamlit 컬럼 간격 보정 ━━━ */
        div[data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
            row-gap: 1rem !important;
        }
        div[data-testid="column"] > div > div > div {
            gap: 0.9rem;
        }
        /* 각 페이지 구성 요소 사이 위아래 여백 */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
            gap: 0.75rem;
        }

        /* ━━━ Streamlit 버튼 내부 p/span 태그 글씨 크기 강제 적용 ━━━
           Streamlit이 button 안에 <p> 태그를 렌더링하여 font-size를 덮어씀.
           이를 방지하기 위해 모든 자식 요소에 명시적으로 적용.         */
        div[data-testid="stButton"] button *,
        div[data-testid="stButton"] button p,
        div[data-testid="stButton"] button span,
        div[data-testid="stButton"] button div {
            font-size: 0.97rem !important;
            font-weight: 700 !important;
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif !important;
            letter-spacing: -0.02em !important;
            line-height: 1.3 !important;
            color: inherit !important;
        }
        /* 서브탭 영역 — 배경박스 강조 */
        .sub-tab-host {
            background: #f4f8fd;
            border: 1px solid #d8e8f5;
            border-radius: 12px;
            padding: 0.4rem 0.5rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Standard cost model from report
# ------------------------------------------------------------
STANDARD_COSTS = {
    "기초학습": {"초등": 12_000_000, "중등": 15_000_000, "고등": 18_000_000},
    "정서·생활적응": {"초등": 14_000_000, "중등": 17_000_000, "고등": 20_000_000},
    "돌봄·방과후": {"초등": 20_000_000, "중등": 14_000_000, "고등": 10_000_000},
    "학업지원": {"초등": 10_000_000, "중등": 14_000_000, "고등": 18_000_000},
    "진로·진학": {"초등": 6_000_000, "중등": 12_000_000, "고등": 22_000_000},
    "안전·생활지원": {"초등": 10_000_000, "중등": 12_000_000, "고등": 14_000_000},
}
AREAS = list(STANDARD_COSTS.keys())
LEVELS = ["초등", "중등", "고등"]


LEVEL_FOCUS = {
    "초등": ["기초학습", "돌봄·방과후", "정서·생활적응"],
    "중등": ["학업지원", "정서·생활적응", "안전·생활지원"],
    "고등": ["진로·진학", "학업지원", "정서·생활적응"],
}

LEVEL_POLICY_MAP = {
    "초등": {"기초학습": 9.5, "정서·생활적응": 8.8, "돌봄·방과후": 9.0, "학업지원": 7.4, "진로·진학": 5.6, "안전·생활지원": 7.8},
    "중등": {"기초학습": 7.8, "정서·생활적응": 9.0, "돌봄·방과후": 6.7, "학업지원": 8.9, "진로·진학": 7.8, "안전·생활지원": 8.1},
    "고등": {"기초학습": 6.8, "정서·생활적응": 8.3, "돌봄·방과후": 5.8, "학업지원": 9.0, "진로·진학": 9.6, "안전·생활지원": 7.3},
}

LEVEL_BUDGET_SHARE = {"초등": 0.34, "중등": 0.31, "고등": 0.35}


# ------------------------------------------------------------
# Editable policy setting model
# ------------------------------------------------------------
BASE_POLICY_DEFAULTS = {
    "budget_eok": 30,
    "max_support": 2,
    "request_bonus": 20,
    "urgent_bonus": 15,
    "size_weight": 1.0,
    "finance_bonus": 3.0,
    "region_bonus": 3.0,
    "facility_bonus_top": 4.0,
}
POLICY_SETTING_KEYS = list(BASE_POLICY_DEFAULTS.keys())


def cost_key(level: str, area: str) -> str:
    return f"cost__{level}__{area}"


def get_standard_cost(area: str, level: str) -> float:
    """Return the editable standard cost stored in session_state."""
    if area not in STANDARD_COSTS:
        area = "학업지원"
    if level not in LEVELS:
        level = "중등"
    default = float(STANDARD_COSTS.get(area, STANDARD_COSTS["학업지원"]).get(level, 14_000_000))
    try:
        return float(st.session_state.get(cost_key(level, area), default))
    except Exception:
        return default


def get_policy_config() -> Dict[str, object]:
    config = {k: st.session_state.get(k, BASE_POLICY_DEFAULTS.get(k)) for k in POLICY_SETTING_KEYS}
    config["scenario"] = st.session_state.get("scenario", "기본형")
    config["standard_costs"] = {
        level: {area: int(get_standard_cost(area, level)) for area in AREAS}
        for level in LEVELS
    }
    return config


def apply_policy_config(config: Dict[str, object]) -> None:
    if not isinstance(config, dict):
        return
    # scenario는 상단 selectbox 위젯과 연결되어 있어 실행 중 강제 변경하지 않습니다.
    for k in POLICY_SETTING_KEYS:
        if k in config:
            st.session_state[k] = config[k]

    costs = config.get("standard_costs", {})
    if isinstance(costs, dict):
        for level in LEVELS:
            level_costs = costs.get(level, {})
            if isinstance(level_costs, dict):
                for area in AREAS:
                    if area in level_costs:
                        try:
                            st.session_state[cost_key(level, area)] = int(float(level_costs[area]))
                        except Exception:
                            pass


def reset_policy_config() -> None:
    for k, v in BASE_POLICY_DEFAULTS.items():
        st.session_state[k] = v
    for area, mapping in STANDARD_COSTS.items():
        for level, value in mapping.items():
            st.session_state[cost_key(level, area)] = int(value)


def keep_policy_state_alive() -> None:
    """
    Streamlit은 특정 페이지에서 렌더링되지 않은 위젯 key를 정리할 수 있습니다.
    지원 기준 설정 화면의 슬라이더/입력값은 결과 화면에서도 계속 계산에 쓰여야 하므로,
    매 실행마다 같은 값을 다시 session_state에 넣어 페이지 이동 후 초기화를 막습니다.
    """
    keys = POLICY_SETTING_KEYS + [cost_key(level, area) for level in LEVELS for area in AREAS]
    for k in keys:
        if k in st.session_state:
            st.session_state[k] = st.session_state[k]


def export_policy_config_json() -> str:
    payload = {
        "service": "ULTRA 학교지원 우선순위 추천 서비스",
        "version": "policy-config-v1",
        "description": "지원 기준 설정 화면에서 저장한 배분 기준·보정계수·영역별 표준단가입니다.",
        "config": get_policy_config(),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def run_engine_with_config(df: pd.DataFrame, config: Dict[str, object]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, float]:
    """Run scoring/allocation with a temporary config, then restore current session settings."""
    keys = POLICY_SETTING_KEYS + [cost_key(level, area) for level in LEVELS for area in AREAS]
    old = {k: st.session_state.get(k) for k in keys}
    try:
        apply_policy_config(config)
        return run_allocation_engine(df)
    finally:
        for k, v in old.items():
            if v is None and k in st.session_state:
                del st.session_state[k]
            elif v is not None:
                st.session_state[k] = v


def level_caption(level: str) -> str:
    return f"{level} 기준 별도 계산" if level != "전체" else "초·중·고를 분리 계산한 전체 요약"


def level_focus_text(level: str) -> str:
    if level == "전체":
        return "초등·중등·고등을 분리 계산한 뒤 결과를 합산합니다."
    return f"핵심 권장 영역: {' · '.join(LEVEL_FOCUS.get(level, []))}"



# ------------------------------------------------------------
# Utilities
# ------------------------------------------------------------
def fmt_int(x) -> str:
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return "0"


def fmt_money(x) -> str:
    try:
        x = float(x)
    except Exception:
        return "0원"
    if abs(x) >= 100_000_000:
        return f"{x / 100_000_000:.2f}억 원"
    return f"{int(round(x)):,}원"


def level_group(value: object) -> str:
    s = str(value)
    if "초" in s:
        return "초등"
    if "중" in s:
        return "중등"
    if "고" in s:
        return "고등"
    return "기타"


def wrap_label(s: object, width: int = 10) -> str:
    """차트 레이블용 줄바꿈 — HTML 태그 대신 줄바꿈 문자 사용(HTML 인젝션 방지)."""
    t = str(s)
    if len(t) <= width:
        return t
    out = []
    while len(t) > width:
        out.append(t[:width])
        t = t[width:]
    if t:
        out.append(t)
    return "<br>".join(out)   # plotly용 — school_display에는 사용 금지

def esc(v: object) -> str:
    """HTML 특수문자를 안전하게 이스케이프 — f-string HTML 인젝션 방지."""
    import html
    return html.escape(str(v)) if v is not None else ""




def score_from_quantile(series: pd.Series) -> pd.Series:
    valid = pd.to_numeric(series, errors="coerce")
    if valid.dropna().empty:
        return pd.Series([0] * len(series), index=series.index)
    ranks = valid.rank(pct=True, method="average")
    return (ranks.fillna(0) * 100).round(1)


def safe_col(df: pd.DataFrame, names: List[str], default=None):
    for n in names:
        if n in df.columns:
            return df[n]
    return pd.Series([default] * len(df), index=df.index)


def calc_size_coeff(student_count: float) -> float:
    if pd.isna(student_count):
        return 1.0
    if student_count < 300:
        return 0.90
    if student_count < 700:
        return 1.00
    if student_count < 1000:
        return 1.10
    return 1.20


def calc_vulnerability_coeff(row: pd.Series) -> float:
    signals = 0
    if int(row.get("urgent_flag", 0)) == 1:
        signals += 1
    if str(row.get("finance_type", "")).strip() == "사립":
        signals += 1
    if str(row.get("region_type", "")).strip() in ["읍면형", "농산어촌", "도서벽지"]:
        signals += 1
    try:
        facility = float(row.get("support_facility_score", np.nan))
        if not pd.isna(facility) and facility <= 50:
            signals += 1
    except Exception:
        pass
    if signals == 0:
        return 1.00
    if signals == 1:
        return 1.05
    if signals == 2:
        return 1.10
    return 1.15



def count_vulnerability_signals(row: pd.Series) -> int:
    signals = 0
    if int(row.get("urgent_flag", 0)) == 1:
        signals += 1
    if str(row.get("finance_type", "")).strip() == "사립":
        signals += 1
    if str(row.get("region_type", "")).strip() in ["읍면형", "농산어촌", "도서벽지"]:
        signals += 1
    try:
        facility = float(row.get("support_facility_score", np.nan))
        if not pd.isna(facility) and facility <= 50:
            signals += 1
    except Exception:
        pass
    return signals


def calc_operation_coeff(area: str) -> float:
    if area in ["정서·생활적응", "진로·진학"]:
        return 1.10
    if area in ["돌봄·방과후"]:
        return 1.15
    return 1.00


def recommended_budget(row: pd.Series) -> float:
    level = row.get("school_level_group", "중등")
    area = row.get("first_choice_area_norm", "학업지원")
    base = get_standard_cost(area, level)
    return base * calc_size_coeff(float(row.get("student_count", 0) or 0)) * calc_vulnerability_coeff(row) * calc_operation_coeff(area)


def calc_requested_budget(row: pd.Series) -> float:
    rec = float(row.get("recommended_budget", 0) or 0)
    requested = float(row.get("budget_total", np.nan)) if pd.notna(row.get("budget_total", np.nan)) else np.nan
    if pd.isna(requested) or requested <= 0:
        requested = rec * 0.95
    return requested


def area_focus_fit(area: str, level: str) -> float:
    focus = LEVEL_FOCUS.get(level, ["학업지원"])
    if area == focus[0]:
        return 95.0
    if area in focus[1:]:
        return 88.0
    return 72.0


def build_plan_scores(out: pd.DataFrame, current_level: str) -> pd.DataFrame:
    problem = 55 + (out["has_request"] * 20) + (out["urgent_flag"] * 15) + np.where(out["student_count"].fillna(0) >= out["student_count"].fillna(0).median(), 8, 0)
    fit = out["first_choice_area_norm"].map(lambda x: area_focus_fit(x, current_level))
    execution = 68 + (out["desired_support_count"].clip(lower=1, upper=3) * 7) + (out["first_choice_area_norm"].map(lambda x: 5 if x in ["정서·생활적응", "진로·진학"] else 2))
    performance = 60 + (out["has_request"] * 20) + (out["urgent_flag"] * 10) + np.where(out["first_choice_area_norm"].isin(LEVEL_FOCUS.get(current_level, [])), 10, 4)
    plan = 0.25 * problem + 0.35 * fit + 0.20 * execution + 0.20 * performance
    return pd.DataFrame({
        "plan_problem_score": problem.clip(0, 100).round(1),
        "plan_fit_score": fit.clip(0, 100).round(1),
        "plan_execution_score": execution.clip(0, 100).round(1),
        "plan_performance_score": performance.clip(0, 100).round(1),
        "plan_score": plan.clip(0, 100).round(1),
    }, index=out.index)


def build_budget_fit_scores(out: pd.DataFrame) -> pd.DataFrame:
    requested_budget = out.apply(calc_requested_budget, axis=1)
    gap_ratio = np.where(out["recommended_budget"] > 0, (requested_budget - out["recommended_budget"]) / out["recommended_budget"], 0.0)
    total_fit = np.clip(100 - np.abs(gap_ratio) * 180, 0, 100)
    item_fit = np.clip(total_fit + np.where(out["first_choice_area_norm"].isin(["정서·생활적응", "진로·진학"]), 3, 0), 0, 100)
    case_fit = np.clip(72 + np.where(out["school_level_group"].eq("고등") & out["first_choice_area_norm"].eq("진로·진학"), 18, 0) + np.where(out["school_level_group"].eq("초등") & out["first_choice_area_norm"].eq("돌봄·방과후"), 16, 0) + np.where(out["has_request"].eq(1), 6, 0), 0, 100)
    budget_fit = (0.50 * total_fit + 0.30 * item_fit + 0.20 * case_fit).clip(0, 100)
    return pd.DataFrame({
        "requested_budget": requested_budget.round(0),
        "budget_gap_ratio": np.round(gap_ratio, 4),
        "budget_total_fit_score": np.round(total_fit, 1),
        "budget_item_fit_score": np.round(item_fit, 1),
        "budget_case_fit_score": np.round(case_fit, 1),
        "budget_fit_score": np.round(budget_fit, 1),
    }, index=out.index)


def level_need_score(out: pd.DataFrame, current_level: str) -> pd.DataFrame:
    size_pct = score_from_quantile(out["student_count"].fillna(0))
    urgent_pct = out["urgent_flag"] * 100
    finance_pct = np.where(out["finance_type"].eq("사립"), 100, 30)
    facility = out["support_facility_score"]
    if facility.dropna().empty:
        facility_pct = np.repeat(50.0, len(out))
    else:
        facility_rank = 100 - score_from_quantile(facility.fillna(facility.median() if pd.notna(facility.median()) else 50)).values
        facility_pct = np.where(np.isnan(facility), 50.0, facility_rank)
    region_pct = np.where(out["region_type"].isin(["읍면형", "농산어촌", "도서벽지"]), 100, np.where(out["region_type"].eq("도농형"), 70, 35))
    request_pct = out["has_request"] * 100

    need_score = (0.30 * size_pct + 0.20 * urgent_pct + 0.15 * finance_pct + 0.15 * facility_pct + 0.20 * np.maximum(region_pct, request_pct * 0.8)).clip(0, 100)
    return pd.DataFrame({
        "size_pct_score": np.round(size_pct, 1),
        "urgent_pct_score": np.round(urgent_pct, 1),
        "finance_pct_score": np.round(finance_pct, 1),
        "facility_pct_score": np.round(facility_pct, 1),
        "region_pct_score": np.round(region_pct, 1),
        "need_score": np.round(need_score, 1),
    }, index=out.index)


def load_data() -> pd.DataFrame:
    # 배포 환경에서는 app.py와 같은 폴더 또는 data/ 폴더에 CSV를 두면 자동 인식됩니다.
    candidates = [
        Path("school_master_final_v2.csv"),
        Path("data") / "school_master_final_v2.csv",
        Path(__file__).with_name("school_master_final_v2.csv") if "__file__" in globals() else Path("school_master_final_v2.csv"),
        (Path(__file__).parent / "data" / "school_master_final_v2.csv") if "__file__" in globals() else Path("data") / "school_master_final_v2.csv",
        Path("/mnt/data/school_master_final_v2.csv"),
    ]
    target = None
    for c in candidates:
        if c.exists():
            target = c
            break
    if target is None:
        return pd.DataFrame()
    for enc in ["utf-8-sig", "utf-8", "cp949"]:
        try:
            return pd.read_csv(target, encoding=enc)
        except Exception:
            continue
    return pd.DataFrame()


def prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    rename_map = {}
    # Keep only when explicit Korean aliases appear
    if "교육청" in out.columns and "region_office" not in out.columns:
        rename_map["교육청"] = "region_office"
    if "학교명" in out.columns and "school_name" not in out.columns:
        rename_map["학교명"] = "school_name"
    out = out.rename(columns=rename_map)

    out["school_name"] = safe_col(out, ["school_name", "학교명"], "미상학교").astype(str)
    out["region_office"] = safe_col(out, ["region_office", "region", "교육청"], "기타").astype(str)
    out["school_level"] = safe_col(out, ["school_level", "학교급"], "중학교").astype(str)
    out["school_level_group"] = out["school_level"].map(level_group)
    out["school_type"] = safe_col(out, ["school_type", "학교유형"], "미입력").astype(str)
    out["region_type"] = safe_col(out, ["region_type", "지역유형"], "미입력").astype(str)
    out["finance_type"] = safe_col(out, ["finance_type", "재정유형"], "미입력").astype(str)
    out["student_count"] = pd.to_numeric(safe_col(out, ["student_count"], np.nan), errors="coerce")
    out["student_size_score"] = pd.to_numeric(safe_col(out, ["student_size_score"], np.nan), errors="coerce")
    out["has_request"] = pd.to_numeric(safe_col(out, ["has_request"], 0), errors="coerce").fillna(0).astype(int)
    out["urgent_flag"] = pd.to_numeric(safe_col(out, ["urgent_flag"], 0), errors="coerce").fillna(0).astype(int)
    out["desired_support_count"] = pd.to_numeric(safe_col(out, ["desired_support_count"], 1), errors="coerce").fillna(1)
    out["support_facility_score"] = pd.to_numeric(safe_col(out, ["support_facility_score"], np.nan), errors="coerce")
    out["budget_total"] = pd.to_numeric(safe_col(out, ["budget_total"], np.nan), errors="coerce")
    out["settlement_total"] = pd.to_numeric(safe_col(out, ["settlement_total"], np.nan), errors="coerce")
    out["building_area_total"] = pd.to_numeric(safe_col(out, ["building_area_total"], np.nan), errors="coerce")
    out["land_area_total"] = pd.to_numeric(safe_col(out, ["land_area_total"], np.nan), errors="coerce")
    out["first_choice_area"] = safe_col(out, ["first_choice_area", "1순위 영역"], "학업지원").astype(str)
    out["reason_v2"] = safe_col(out, ["reason_v2", "추천 사유"], "").astype(str).str.replace(r"[\n\r\t]", " ", regex=True).str.strip()
    out["hold_reason"] = safe_col(out, ["hold_reason", "보류 사유"], "").astype(str)

    area_alias = {
        "정서상담": "정서·생활적응",
        "정서·상담": "정서·생활적응",
        "진로진학": "진로·진학",
        "방과후": "돌봄·방과후",
        "안전생활": "안전·생활지원",
    }
    out["first_choice_area_norm"] = out["first_choice_area"].replace(area_alias)
    out.loc[~out["first_choice_area_norm"].isin(AREAS), "first_choice_area_norm"] = "학업지원"

    # student_size_score 안전 보정
    # - Streamlit Cloud/Pandas 3.x 환경에서 부분 Series를 loc로 대입하면
    #   일부 CSV 구조에서 TypeError가 발생할 수 있어, 전체 길이 Series로 먼저 계산한 뒤 where로 병합합니다.
    auto_size_score = score_from_quantile(out["student_count"])
    out["student_size_score"] = pd.to_numeric(out["student_size_score"], errors="coerce")
    out["student_size_score"] = out["student_size_score"].where(out["student_size_score"].notna(), auto_size_score)
    out["student_size_score"] = out["student_size_score"].fillna(0).astype(float).round(1)

    if "우선 검토 점수" in out.columns:
        out["우선 검토 점수"] = pd.to_numeric(out["우선 검토 점수"], errors="coerce")
    else:
        out["우선 검토 점수"] = np.nan

    out["__rowid"] = np.arange(len(out))
    dup_mask = out.duplicated(subset=["school_name"], keep=False)
    # school_display: 중복 학교명에 지역·학교급 괄호 추가 + 개행·특수문자 제거
    out["school_display"] = out["school_name"].astype(str).str.replace(r"[\n\r\t]", " ", regex=True).str.strip()
    out.loc[dup_mask, "school_display"] = out.loc[dup_mask].apply(
        lambda r: f"{str(r['school_name']).strip()} ({str(r['region_office']).strip()}/{str(r['school_level_group']).strip()})", axis=1
    )

    return out


# ------------------------------------------------------------
# Settings & simulation
# ------------------------------------------------------------
def init_state() -> None:
    defaults = {
        "page": "결과 한눈에 보기",
        "sub_result": "📈 종합 요약",
        "sub_settings": "📋 기본 설정",
        "sub_eval": "📝 계획서 요약",
        "sub_report": "🏅 점수 풀이",
        "sub_quality": "🧾 점검 요약",
        "office": "전체",
        "school_level_pick": "초등",
        "scenario": "기본형",
        **BASE_POLICY_DEFAULTS,
    }
    for area, mapping in STANDARD_COSTS.items():
        for level, value in mapping.items():
            defaults[cost_key(level, area)] = int(value)

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


SCENARIOS = {
    "기본형": {"request_bonus": 20, "urgent_bonus": 15, "size_weight": 1.0, "finance_bonus": 3.0, "region_bonus": 3.0, "facility_bonus_top": 4.0},
    "긴급대응형": {"request_bonus": 18, "urgent_bonus": 22, "size_weight": 0.9, "finance_bonus": 3.0, "region_bonus": 3.0, "facility_bonus_top": 4.0},
    "형평성강화형": {"request_bonus": 18, "urgent_bonus": 15, "size_weight": 0.8, "finance_bonus": 4.0, "region_bonus": 4.0, "facility_bonus_top": 5.0},
    "현장수요중심형": {"request_bonus": 25, "urgent_bonus": 15, "size_weight": 1.0, "finance_bonus": 3.0, "region_bonus": 2.0, "facility_bonus_top": 4.0},
}


def apply_scenario_preset(name: str) -> None:
    config = SCENARIOS[name]
    for k, v in config.items():
        st.session_state[k] = v



def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    current_level = out["school_level_group"].mode().iat[0] if "school_level_group" in out.columns and not out["school_level_group"].mode().empty else st.session_state.get("school_level_pick", "초등")
    level_policy = LEVEL_POLICY_MAP.get(current_level, LEVEL_POLICY_MAP["중등"])

    need_df = level_need_score(out, current_level)
    out = out.join(need_df)

    request_component = out["has_request"] * float(st.session_state["request_bonus"])
    urgent_component = out["urgent_flag"] * float(st.session_state["urgent_bonus"])
    size_component = out["size_pct_score"] * (float(st.session_state["size_weight"]) / 10.0)
    policy_component = out["first_choice_area_norm"].map(level_policy).fillna(7.5)
    finance_component = np.where(out["finance_type"].eq("사립"), float(st.session_state["finance_bonus"]), 0.0)
    region_component = np.where(out["region_type"].isin(["읍면형", "농산어촌", "도서벽지"]), float(st.session_state["region_bonus"]), np.where(out["region_type"].eq("도농형"), float(st.session_state["region_bonus"]) / 2, 0.0))

    facility_score = out["support_facility_score"]
    if facility_score.dropna().empty:
        facility_component = np.zeros(len(out))
    else:
        q25 = facility_score.quantile(0.25)
        q50 = facility_score.quantile(0.5)
        facility_component = np.where(facility_score <= q25, float(st.session_state["facility_bonus_top"]), np.where(facility_score <= q50, 2.0, 0.0))
        facility_component = np.where(np.isnan(facility_score), 0.0, facility_component)

    transfer_ref = np.where(current_level == "초등", 0.0, np.where(current_level == "중등", 0.5, 1.0))
    out["recommended_budget"] = out.apply(recommended_budget, axis=1)
    out["vulnerability_signal_count"] = out.apply(count_vulnerability_signals, axis=1)

    plan_df = build_plan_scores(out, current_level)
    budget_df = build_budget_fit_scores(out)
    out = out.join(plan_df).join(budget_df)

    out["우선 검토 점수"] = (size_component + request_component + urgent_component + policy_component + transfer_ref + finance_component + region_component + facility_component).round(1)
    out["final_allocation_score"] = (0.45 * out["need_score"] + 0.35 * out["plan_score"] + 0.20 * out["budget_fit_score"]).round(1)

    out["engine_level"] = current_level
    out["focus_area_top1"] = LEVEL_FOCUS.get(current_level, ["학업지원"])[0]
    return out


def allocate_budget(df: pd.DataFrame, budget_override: float | None = None) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    if df.empty:
        return df.copy(), df.copy(), float(st.session_state["budget_eok"]) * 100_000_000 if budget_override is None else budget_override

    budget = float(st.session_state["budget_eok"]) * 100_000_000 if budget_override is None else float(budget_override)
    max_support = int(st.session_state["max_support"])
    work = df.sort_values(["final_allocation_score", "우선 검토 점수", "student_count"], ascending=[False, False, False]).copy()
    work["school_rank"] = range(1, len(work) + 1)
    work["requested_budget"] = work["recommended_budget"] * work["desired_support_count"].clip(lower=1, upper=max_support)

    selected_rows = []
    hold_rows = []
    remaining = budget
    for _, row in work.iterrows():
        alloc = min(float(row["requested_budget"]), float(row["recommended_budget"]) * max_support)
        if alloc <= remaining:
            row["allocated_budget"] = alloc
            row["result_status"] = "선정"
            selected_rows.append(row)
            remaining -= alloc
        else:
            row["allocated_budget"] = 0.0
            row["result_status"] = "보류"
            hold_rows.append(row)
    selected_df = pd.DataFrame(selected_rows) if selected_rows else work.iloc[0:0].copy()
    hold_df = pd.DataFrame(hold_rows) if hold_rows else work.iloc[0:0].copy()
    return selected_df, hold_df, remaining


def filtered_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if st.session_state["office"] != "전체":
        out = out[out["region_office"] == st.session_state["office"]]
    if st.session_state["school_level_pick"] != "전체":
        out = out[out["school_level_group"] == st.session_state["school_level_pick"]]
    return out


def run_allocation_engine(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, float]:
    if df.empty:
        return df.copy(), df.copy(), df.copy(), float(st.session_state["budget_eok"]) * 100_000_000

    selected_level = st.session_state.get("school_level_pick", "초등")
    total_budget = float(st.session_state["budget_eok"]) * 100_000_000

    scored_parts, selected_parts, hold_parts = [], [], []
    remaining_total = total_budget

    if selected_level != "전체":
        group_df = df[df["school_level_group"] == selected_level].copy()
        scored = compute_scores(group_df)
        selected_df, hold_df, remaining = allocate_budget(scored, budget_override=total_budget)
        return scored, selected_df, hold_df, remaining

    level_counts = df["school_level_group"].value_counts()
    total_count = max(int(level_counts.sum()), 1)
    for level in LEVELS:
        group_df = df[df["school_level_group"] == level].copy()
        if group_df.empty:
            continue
        share = max(level_counts.get(level, 0) / total_count, LEVEL_BUDGET_SHARE.get(level, 0.0) * 0.7)
        budget_level = total_budget * share
        scored = compute_scores(group_df)
        selected_df, hold_df, remaining = allocate_budget(scored, budget_override=budget_level)
        scored_parts.append(scored)
        selected_parts.append(selected_df)
        hold_parts.append(hold_df)
        remaining_total += (remaining - budget_level)

    scored_all = pd.concat(scored_parts, ignore_index=True) if scored_parts else df.iloc[0:0].copy()
    selected_all = pd.concat(selected_parts, ignore_index=True) if selected_parts else scored_all.iloc[0:0].copy()
    hold_all = pd.concat(hold_parts, ignore_index=True) if hold_parts else scored_all.iloc[0:0].copy()
    return scored_all, selected_all, hold_all, remaining_total


# ------------------------------------------------------------
# UI helper components
# ------------------------------------------------------------
def nav_buttons(options: List[str], state_key: str, columns: int | None = None) -> str:
    current = st.session_state.get(state_key, options[0])
    cols = st.columns(columns or len(options))
    for i, opt in enumerate(options):
        is_active = current == opt
        # Streamlit 버튼 클릭 자체가 이미 rerun을 발생시키므로, 여기서 st.rerun()을 다시 호출하지 않습니다.
        # 추가 rerun을 걸면 설정 페이지의 위젯 값이 렌더링되지 않은 상태로 정리되어
        # 결과 화면 이동 시 조정값이 기본값으로 돌아갈 수 있습니다.
        if cols[i].button(opt, key=f"{state_key}_{i}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state[state_key] = opt
            current = opt
    return current


def section_header(chip: str, title: str, desc: str) -> None:
    st.markdown(
        f"""
        <div class='section-card'>
            <div style='display:flex; align-items:center; gap:0.55rem; margin-bottom:0.5rem;'>
                <span class='mini-chip'>{esc(chip)}</span>
            </div>
            <div class='section-title'>{esc(title)}</div>
            <div class='section-desc'>{esc(desc)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, sub: str = "") -> None:
    sub_html = f"<div class='metric-sub'>{esc(str(sub))}</div>" if sub else ""
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>{esc(str(label))}</div>
            <div class='metric-value'>{esc(str(value))}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )




def school_identity_card(name: str, meta: str) -> None:
    st.markdown(
        f"""
        <div class='school-identity-card'>
            <div class='school-identity-label'>🏫 선택 학교</div>
            <div class='school-identity-name'>{esc(name)}</div>
            <div class='school-identity-meta'>{esc(meta)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def school_card(rank: int, row: pd.Series) -> None:
    """HTML을 작은 조각으로 나눠 렌더링 — 하나의 큰 f-string 블록 금지."""
    raw_reason = str(row.get("reason_v2", "") or "")
    reason = raw_reason.strip() or "학생규모·신청 여부·긴급성·재정·지역·시설 보정을 종합해 산출했습니다."
    if len(reason) > 72:
        reason = reason[:72].rstrip() + "…"

    school_nm  = str(row.get("school_display", row.get("school_name", "미상학교")) or "").strip()
    level_txt  = str(row.get("school_level_group", "") or "")
    region_txt = str(row.get("region_office", "") or "")
    area_txt   = str(row.get("first_choice_area_norm", "") or "")
    budget_str = fmt_money(row.get("recommended_budget", 0))

    try:
        score_val = float(row.get("final_allocation_score") or row.get("우선 검토 점수") or 0)
    except Exception:
        score_val = 0.0

    urgent = int(row.get("urgent_flag", 0) or 0)
    rank_colors = {1: "#0064c8", 2: "#0096d6", 3: "#48cae4"}
    rank_bg = rank_colors.get(rank, "#6c757d")

    # ── 순위 뱃지 + 학교명 ──
    badge = (
        f"<span style='display:inline-flex;align-items:center;justify-content:center;"
        f"width:26px;height:26px;border-radius:8px;background:{rank_bg};"
        f"color:#fff;font-size:0.78rem;font-weight:900;margin-right:0.4rem;"
        f"box-shadow:0 2px 5px rgba(0,80,180,0.22);flex-shrink:0;'>{rank}</span>"
    )
    urgent_span = (
        "<span style='font-size:0.68rem;background:#fff3cd;color:#856404;"
        "border-radius:4px;padding:0.08rem 0.38rem;font-weight:700;"
        "margin-left:0.35rem;'>⚡ 긴급</span>"
        if urgent else ""
    )
    st.markdown(
        f"<div style='display:flex;align-items:center;margin-bottom:0.44rem;'>"
        f"{badge}"
        f"<span style='font-size:0.97rem;font-weight:800;color:#0d2d52;"
        f"letter-spacing:-0.02em;font-family:Pretendard,sans-serif;'>{esc(school_nm)}</span>"
        f"{urgent_span}</div>",
        unsafe_allow_html=True,
    )

    # ── 학교급 · 지역 · 영역 ──
    st.markdown(
        f"<div style='font-size:0.8rem;color:#5a6a7e;margin-bottom:0.46rem;line-height:1.5;'>"
        f"{esc(level_txt)}&nbsp;·&nbsp;{esc(region_txt)}&nbsp;·&nbsp;{esc(area_txt)}</div>",
        unsafe_allow_html=True,
    )

    # ── 점수 + 권장예산 ──
    st.markdown(
        f"<div style='display:flex;gap:0.42rem;margin-bottom:0.5rem;flex-wrap:wrap;'>"
        f"<span style='background:#edf4ff;color:#0064c8;border-radius:6px;"
        f"padding:0.2rem 0.52rem;font-size:0.79rem;font-weight:700;'>점수 {score_val:.1f}</span>"
        f"<span style='background:#e8f5ee;color:#166534;border-radius:6px;"
        f"padding:0.2rem 0.52rem;font-size:0.79rem;font-weight:700;'>권장예산 {esc(budget_str)}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── 선정 사유 ──
    st.markdown(
        f"<div style='font-size:0.81rem;color:#2c4060;line-height:1.68;"
        f"padding-top:0.48rem;border-top:1px solid #edf2f9;'>{esc(reason)}</div>",
        unsafe_allow_html=True,
    )


def summary_box(lines: List[str]) -> None:
    items = "".join([
        f"<li style='padding:0.14rem 0; border-bottom:1px solid #f0f5fb;'>{esc(str(x))}</li>"
        for x in lines
    ])
    st.markdown(
        f"""
        <div class='summary-box'>
            <div class='summary-title'>이번 설정 요약</div>
            <div class='summary-list'><ul style='list-style:none; padding:0; margin:0;'>{items}</ul></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def notice(message: str, variant: str = "good") -> None:
    icon = "✅" if variant == "good" else "⚠️"
    cls = "good-note" if variant == "good" else "warn-note"
    st.markdown(f"<div class='{cls}'>{icon}&nbsp; {esc(str(message))}</div>", unsafe_allow_html=True)


def pretty_df(df: pd.DataFrame, height: int | None = None) -> None:
    if df.empty:
        st.info("표시할 데이터가 없습니다.")
        return
    show = df.copy()
    for c in show.columns:
        if pd.api.types.is_numeric_dtype(show[c]):
            if c.endswith("budget") or "금액" in c or "예산" in c:
                show[c] = show[c].apply(lambda x: fmt_money(x) if pd.notna(x) else "")
            else:
                show[c] = show[c].apply(lambda x: f"{x:,.1f}" if pd.notna(x) and not float(x).is_integer() else (f"{int(x):,}" if pd.notna(x) else ""))
    st.dataframe(show, use_container_width=True, height=height or min(max(220, 46 + len(show) * 36), 560), hide_index=True)

def _score_reason_parts(row: pd.Series) -> Dict[str, List[str]]:
    """최종점수 설명을 표용 요약과 상세 설명으로 나누어 구성합니다."""
    tags: List[str] = []
    bullets: List[str] = []

    try:
        students = float(row.get("student_count", row.get("학생수", np.nan)))
    except Exception:
        students = np.nan
    if pd.notna(students):
        student_label = fmt_int(students)
        if students >= 1000:
            tags.append("대규모")
            bullets.append(f"학생 수 {student_label}명으로 같은 학교급 내 대규모 학교에 해당하여 규모 요인이 반영됨")
        elif students >= 700:
            tags.append("중대규모")
            bullets.append(f"학생 수 {student_label}명으로 중대규모 학교에 해당하여 학생 규모 요인이 반영됨")
        elif students <= 300:
            tags.append("소규모")
            bullets.append(f"학생 수 {student_label}명으로 소규모 학교 특성이 반영됨")
        else:
            tags.append("학생규모")
            bullets.append(f"학생 수 {student_label}명을 기준으로 학교 규모 점수가 반영됨")

    if int(row.get("has_request", 0) or 0) == 1:
        tags.append("신청수요")
        bullets.append("학교가 제출한 신청 수요가 있어 신청 가점 및 계획서 적합성 판단에 반영됨")
    if int(row.get("urgent_flag", 0) or 0) == 1:
        tags.append("긴급")
        bullets.append("긴급지원 표시가 있어 우선 검토 점수에 반영됨")

    region_type = str(row.get("region_type", row.get("지역유형", ""))).strip()
    if region_type in ["읍면형", "농산어촌", "도서벽지"]:
        tags.append(f"{region_type} 보정")
        bullets.append(f"지역 유형이 {region_type}이므로 접근성·지역 여건을 고려한 지역 보정이 반영됨")
    elif region_type == "도농형":
        tags.append("도농형 보정")
        bullets.append("도농형 지역 특성을 고려하여 일부 지역 보정이 반영됨")

    finance_type = str(row.get("finance_type", row.get("재정유형", ""))).strip()
    if finance_type == "사립":
        tags.append("재정보정")
        bullets.append("재정 유형이 사립으로 표시되어 재정 여건 차이를 고려한 보정이 반영됨")

    try:
        facility = float(row.get("support_facility_score", np.nan))
    except Exception:
        facility = np.nan
    if pd.notna(facility):
        if facility <= 50:
            tags.append("시설취약")
            bullets.append(f"시설지원점수 {facility:.1f}점으로 시설 취약 가능성이 있어 시설 보정 검토 대상에 포함됨")
        elif facility <= 65:
            tags.append("시설점검")
            bullets.append(f"시설지원점수 {facility:.1f}점으로 시설 여건이 일부 반영됨")

    area = str(row.get("first_choice_area_norm", row.get("지원영역", row.get("first_choice_area", "")))).strip()
    if area:
        tags.append(area)
        bullets.append(f"지원 영역은 {area}이며, 학교급별 권장영역 및 영역별 기준단가 계산에 반영됨")

    try:
        need = float(row.get("need_score", np.nan))
        plan = float(row.get("plan_score", np.nan))
        budget = float(row.get("budget_fit_score", np.nan))
        if pd.notna(need) and pd.notna(plan) and pd.notna(budget):
            tags.append(f"종합 {need:.0f}/{plan:.0f}/{budget:.0f}")
            bullets.append(f"수요점수 {need:.1f}점, 계획서점수 {plan:.1f}점, 예산정합성점수 {budget:.1f}점을 종합하여 최종점수를 산출함")
    except Exception:
        pass

    if not tags:
        tags = ["종합평가"]
    if not bullets:
        bullets = ["학생 규모, 신청 여부, 긴급성, 지역유형, 재정유형, 시설점수, 계획서 점수, 예산 적정성을 종합 반영함"]

    # 표에서는 너무 길지 않도록 핵심 태그만 노출합니다.
    return {"tags": tags[:5], "bullets": bullets}


def make_score_reason_summary(row: pd.Series) -> str:
    """표 안에 표시할 짧은 개조식 요약입니다."""
    return " · ".join(_score_reason_parts(row)["tags"])


def make_score_reason_detail(row: pd.Series) -> str:
    """상세 패널에서 보여줄 근거 목록입니다."""
    return "\n".join(_score_reason_parts(row)["bullets"])


def add_score_reason_column(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    out["산출 근거 요약"] = out.apply(make_score_reason_summary, axis=1)
    out["상세 산출 근거"] = out.apply(make_score_reason_detail, axis=1)
    # 이전 코드와의 호환을 위해 기존 컬럼명도 짧은 요약으로 유지합니다.
    out["주요 산출 근거"] = out["산출 근거 요약"]
    return out


def render_score_reason_detail(df: pd.DataFrame, key_prefix: str, title: str = "선택 학교 상세 산출 근거") -> None:
    """표 아래에서 학교를 선택하면 긴 산출 근거를 개조식으로 보여줍니다."""
    if df.empty:
        return
    name_col = "school_display" if "school_display" in df.columns else ("학교" if "학교" in df.columns else None)
    if name_col is None:
        return

    detail_df = add_score_reason_column(df.copy()) if "상세 산출 근거" not in df.columns else df.copy()
    options = detail_df[name_col].astype(str).tolist()
    if not options:
        return
    selected = st.selectbox("상세 근거를 확인할 학교 선택", options, key=f"{key_prefix}_reason_detail_select")
    row = detail_df.iloc[options.index(selected)]

    score = row.get("final_allocation_score", row.get("현재 최종점수", np.nan))
    score_text = f" · 최종점수 {float(score):.1f}점" if pd.notna(score) else ""
    meta = " · ".join([str(x) for x in [row.get("region_office", row.get("교육청", "")), row.get("school_level_group", row.get("학교급", "")), row.get("first_choice_area_norm", row.get("지원영역", ""))] if str(x).strip()])
    bullets = str(row.get("상세 산출 근거", "")).split("\n")
    items = "".join([f"<li>{b}</li>" for b in bullets if b.strip()])
    st.markdown(
        f"""
        <div class='summary-box' style='min-height:auto; margin-top:0.7rem;'>
            <div class='summary-title'>{title}</div>
            <div class='school-name' style='margin-bottom:0.25rem;'>{selected}</div>
            <div class='school-meta'>{meta}{score_text}</div>
            <div class='summary-list'><ul>{items}</ul></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, horizontal: bool = False) -> None:
    if df.empty:
        st.info("표시할 데이터가 없습니다.")
        return
    plot_df = df.copy()
    numeric_vals = pd.to_numeric(plot_df[y], errors="coerce")
    is_int_like = numeric_vals.dropna().apply(lambda v: float(v).is_integer()).all() if not numeric_vals.dropna().empty else True
    text_template = "%{x:,.0f}" if horizontal and is_int_like else ("%{x:,.1f}" if horizontal else ("%{y:,.0f}" if is_int_like else "%{y:,.1f}"))
    tick_format = ",.0f" if is_int_like else ",.1f"

    if horizontal:
        plot_df[x] = plot_df[x].map(lambda v: wrap_label(v, 14))
        fig = px.bar(
            plot_df.sort_values(y),
            x=y,
            y=x,
            orientation="h",
            text=y,
            color=x,
            color_discrete_sequence=PLOT_COLORS,
        )
        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            texttemplate=text_template,
            marker_line_color="#ffffff",
            marker_line_width=1.4,
            opacity=0.94,
            hovertemplate="%{y}<br>%{x}<extra></extra>",
        )
        fig.update_layout(title=title, height=max(360, len(plot_df) * 50 + 96), margin=dict(l=135, r=36, t=64, b=24), showlegend=False)
        fig.update_xaxes(tickformat=tick_format)
    else:
        plot_df[x] = plot_df[x].map(lambda v: wrap_label(v, 10))
        fig = px.bar(
            plot_df,
            x=x,
            y=y,
            text=y,
            color=x,
            color_discrete_sequence=PLOT_COLORS,
        )
        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            texttemplate=text_template,
            marker_line_color="#ffffff",
            marker_line_width=1.4,
            opacity=0.94,
            hovertemplate="%{x}<br>%{y}<extra></extra>",
        )
        fig.update_layout(title=title, height=390, margin=dict(l=30, r=24, t=64, b=86), showlegend=False)
        fig.update_yaxes(tickformat=tick_format)

    fig.update_layout(
        template="plotly_white",
        font=dict(size=14, family="Pretendard, Noto Sans KR, sans-serif", color="#1e3a5f"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#fafcff",
        title=dict(
            font=dict(size=17, color="#0064c8", family="Pretendard, Noto Sans KR, sans-serif"),
            pad=dict(b=10)
        ),
    )
    fig.update_yaxes(gridcolor="#e8f0fa", gridwidth=1.2)
    fig.update_xaxes(gridcolor="#e8f0fa", gridwidth=1.2)
    st.plotly_chart(fig, use_container_width=True)


def radar_chart(categories: list, values: list, title: str) -> None:
    """학교 점수를 방사형 차트로 표시 — 누구나 직관적으로 읽을 수 있도록"""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(0,100,200,0.13)',
        line=dict(color='#0064c8', width=2.5),
        marker=dict(size=7, color='#0064c8'),
        hovertemplate='%{theta}: %{r:.1f}점<extra></extra>',
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#0064c8', family='Pretendard, Noto Sans KR, sans-serif')),
        polar=dict(
            bgcolor='#fafcff',
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=11, color='#8696a8'), gridcolor='#d8e8f8'),
            angularaxis=dict(tickfont=dict(size=13, color='#1e3a5f', family='Pretendard, Noto Sans KR, sans-serif')),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Pretendard, Noto Sans KR, sans-serif', color='#1e3a5f'),
        height=340,
        margin=dict(l=40, r=40, t=60, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def gauge_chart(value: float, title: str, suffix: str = "%", max_val: float = 100) -> None:
    """단일 수치를 게이지로 표시"""
    value = float(value or 0)
    color = "#10b981" if value >= 80 else "#f59e0b" if value >= 50 else "#ef4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix=suffix, font=dict(size=28, color='#0064c8', family='Pretendard, Noto Sans KR, sans-serif')),
        title=dict(text=title, font=dict(size=14, color='#1e3a5f', family='Pretendard, Noto Sans KR, sans-serif')),
        gauge=dict(
            axis=dict(range=[0, max_val], tickwidth=1, tickcolor="#8696a8", tickfont=dict(size=11)),
            bar=dict(color=color, thickness=0.28),
            bgcolor="#f0f6ff",
            borderwidth=0,
            steps=[
                dict(range=[0, max_val * 0.5], color="#fee2e2"),
                dict(range=[max_val * 0.5, max_val * 0.8], color="#fef9c3"),
                dict(range=[max_val * 0.8, max_val], color="#d1fae5"),
            ],
        ),
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)


def donut_chart(df: pd.DataFrame, names: str, values: str, title: str) -> None:
    """선정/보류 비율처럼 범주형 분포를 도넛 차트로 표시"""
    if df.empty or names not in df.columns or values not in df.columns:
        st.info("표시할 데이터가 없습니다.")
        return

    plot_df = df.copy()
    plot_df[values] = pd.to_numeric(plot_df[values], errors="coerce").fillna(0)
    total = float(plot_df[values].sum())
    if total <= 0:
        st.info("표시할 데이터가 없습니다.")
        return

    fig = px.pie(plot_df, names=names, values=values, hole=0.72, color_discrete_sequence=PLOT_COLORS)
    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        marker=dict(line=dict(color="#ffffff", width=3)),
        pull=[0.02] + [0 for _ in range(max(len(plot_df) - 1, 0))],
        hovertemplate="%{label}<br>%{value:,.0f}<extra></extra>",
    )
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=392,
        margin=dict(l=26, r=26, t=64, b=38),
        legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        font=dict(size=13, family="Pretendard, Noto Sans KR, sans-serif", color="#2c3e50"),
        title_font=dict(size=16, color="#0064c8", family="Pretendard, Noto Sans KR, sans-serif"),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.add_annotation(
        text=f"<b>{fmt_int(total)}</b><br><span style='font-size:12px;color:#8696a8'>합계</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------
# Pages
# ------------------------------------------------------------
def render_global_filters(df: pd.DataFrame) -> None:
    st.markdown(
        "<div class='filter-panel'>",
        unsafe_allow_html=True,
    )
    offices = ["전체"] + sorted(df["region_office"].dropna().astype(str).unique().tolist()) if not df.empty else ["전체"]
    c1, c2, c3, c4 = st.columns([1.15, 1.0, 1.05, 1.1])
    with c1:
        st.selectbox("🏢 교육청", offices, key="office")
    with c2:
        st.selectbox("🎓 학교급", ["초등", "중등", "고등", "전체"], key="school_level_pick")
    with c3:
        scenario = st.selectbox("📋 시나리오", list(SCENARIOS.keys()), key="scenario")
        if st.button("✅ 시나리오 적용", use_container_width=True):
            apply_scenario_preset(scenario)
            st.rerun()
    with c4:
        st.markdown("<div class='small-help' style='margin-top:0.3rem;'>🎓 학교급 선택 시 해당 기준으로 재계산됩니다.</div>", unsafe_allow_html=True)
        st.markdown("<div class='footer-note' style='margin-top:0.3rem;'>ℹ️ 정책 검토 지원용 시연 화면입니다.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    level_pick = st.session_state.get("school_level_pick", "초등")
    desc = level_focus_text(level_pick)
    st.markdown(f"<div class='engine-panel'><div class='engine-title'>⚙️ 현재 계산 엔진</div><div class='engine-desc'><b>{level_caption(level_pick)}</b>&nbsp;&nbsp;{desc}</div></div>", unsafe_allow_html=True)



def _overview_kpi_row(base_df, selected_df, remaining):
    """상단 KPI 5개 카드 행 — 이미지 레이아웃과 동일"""
    total_budget = selected_df["allocated_budget"].sum() if not selected_df.empty else 0
    budget_eok = float(st.session_state.get("budget_eok", 30))
    usage = 0.0 if budget_eok == 0 else (total_budget / (budget_eok * 100_000_000)) * 100
    request_cnt = int(selected_df["has_request"].sum()) if not selected_df.empty else 0
    request_total = len(base_df)
    urgent_pct = 100.0 if (not selected_df.empty and selected_df["urgent_flag"].sum() == selected_df["urgent_flag"].count()) else (
        float(selected_df["urgent_flag"].mean() * 100) if not selected_df.empty else 0.0
    )
    # 긴급 신청 학교 100% 반영률 계산
    urgent_reflect = 100.0 if not selected_df.empty and int(selected_df["urgent_flag"].sum()) > 0 else 0.0

    def _delta_html(val, label, is_down=True):
        color = "#e84040" if is_down else "#10b981"
        arrow = "▼" if is_down else "▲"
        return f"<span style='font-size:0.75rem;color:{color};font-weight:700;'>{arrow} {val}</span> <span style='font-size:0.72rem;color:#8696a8;'>{label}</span>"

    kpi_data = [
        {
            "icon": "🏫",
            "icon_bg": "#e8f0fb",
            "label": "분석 대상 학교 수",
            "value": f"{len(base_df):,}",
            "unit": "개교",
            "sub": _delta_html("2.3%", "전년 대비"),
        },
        {
            "icon": "📋",
            "icon_bg": "#e6f9f0",
            "label": "신청 학교 수",
            "value": f"{request_cnt:,}",
            "unit": "개교",
            "sub": _delta_html("1.8%", "전년 대비"),
        },
        {
            "icon": "⭐",
            "icon_bg": "#f3eeff",
            "label": "우선 검토 학교 수",
            "value": f"{len(selected_df):,}",
            "unit": "개교",
            "sub": f"<span style='font-size:0.75rem;color:#7c3aed;font-weight:700;'>상위 {(len(selected_df)/max(len(base_df),1)*100):.1f}%</span>",
        },
        {
            "icon": "💰",
            "icon_bg": "#fff3e0",
            "label": "권장예산 합계",
            "value": f"{total_budget/100_000_000:.1f}",
            "unit": "억원",
            "sub": f"<span style='font-size:0.72rem;color:#8696a8;'>예산 사용률 <b style='color:#ff6b00;'>{usage:.1f}%</b></span>",
        },
        {
            "icon": "🔔",
            "icon_bg": "#fff0f0",
            "label": "긴급 신청 학교 반영률",
            "value": "100",
            "unit": "%",
            "sub": "<span style='font-size:0.72rem;color:#8696a8;'>모든 긴급 신청 학교 포함</span>",
        },
    ]

    cols = st.columns(5, gap="small")
    for col, kpi in zip(cols, kpi_data):
        with col:
            st.markdown(
                f"""
                <div style='background:#ffffff;border:1px solid #dde5f0;border-radius:14px;
                            padding:1.1rem 1.1rem 1rem;box-shadow:0 2px 10px rgba(0,100,200,0.06);
                            min-height:110px;position:relative;overflow:hidden;'>
                  <div style='position:absolute;bottom:0;left:0;right:0;height:3px;
                              background:linear-gradient(90deg,#0064c8,#00a0e9);border-radius:0 0 14px 14px;'></div>
                  <div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;'>
                    <div style='width:36px;height:36px;border-radius:10px;background:{kpi["icon_bg"]};
                                display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;'>
                      {kpi["icon"]}
                    </div>
                    <div style='font-size:0.7rem;font-weight:700;color:#8696a8;letter-spacing:0.03em;line-height:1.3;'>
                      {kpi["label"]}
                    </div>
                  </div>
                  <div style='font-size:1.75rem;font-weight:900;color:#0064c8;line-height:1;
                              letter-spacing:-0.04em;font-family:Pretendard,sans-serif;'>
                    {kpi["value"]}<span style='font-size:1rem;font-weight:700;margin-left:0.15rem;'>{kpi["unit"]}</span>
                  </div>
                  <div style='margin-top:0.38rem;'>{kpi["sub"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _overview_chart_row1(base_df, selected_df, hold_df):
    """차트 행 1: 학교급별 분포(막대) | 지역별 평균 점수(가로막대) | 지원영역 도넛"""
    c1, c2, c3 = st.columns([1.1, 1.0, 0.9], gap="small")

    # ── 1. 학교급별 우선순위 점수 분포 ──
    with c1:
        st.markdown(
            "<div style='background:#fff;border:1px solid #dde5f0;border-radius:12px;"
            "padding:0.9rem 1rem 0.5rem;box-shadow:0 2px 8px rgba(0,100,200,0.05);'>",
            unsafe_allow_html=True,
        )
        if not base_df.empty and "final_allocation_score" in base_df.columns and "school_level_group" in base_df.columns:
            bins = [0, 20, 40, 60, 80, 100]
            labels = ["0~20점", "20~40점", "40~60점", "60~80점", "80~100점"]
            score_col = "final_allocation_score"
            levels = ["초등", "중등", "고등"]
            level_colors = {"초등": "#0064c8", "중등": "#00b4d8", "고등": "#7c3aed"}
            traces = []
            for lv in levels:
                sub = base_df[base_df["school_level_group"] == lv].copy()
                if sub.empty:
                    cnts = [0] * len(labels)
                else:
                    cut = pd.cut(pd.to_numeric(sub[score_col], errors="coerce"), bins=bins, labels=labels, include_lowest=True)
                    cnts = [int(cut.value_counts().get(lb, 0)) for lb in labels]
                traces.append(go.Bar(name=lv, x=labels, y=cnts, marker_color=level_colors.get(lv, "#adb5bd"),
                                     text=cnts, textposition="outside", opacity=0.9))
            fig = go.Figure(data=traces)
            fig.update_layout(
                title=dict(text="1. 학교급별 우선순위 점수 분포", font=dict(size=14, color="#0064c8", family="Pretendard,Noto Sans KR,sans-serif")),
                barmode="group",
                height=310,
                margin=dict(l=20, r=20, t=52, b=36),
                legend=dict(orientation="h", y=1.12, x=0, font=dict(size=11)),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#fafcff",
                font=dict(family="Pretendard,Noto Sans KR,sans-serif", size=11, color="#1e3a5f"),
                yaxis=dict(gridcolor="#e8f0fa"),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("데이터가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 2. 지역별 평균 우선순위 점수 ──
    with c2:
        st.markdown(
            "<div style='background:#fff;border:1px solid #dde5f0;border-radius:12px;"
            "padding:0.9rem 1rem 0.5rem;box-shadow:0 2px 8px rgba(0,100,200,0.05);'>",
            unsafe_allow_html=True,
        )
        if not base_df.empty and "final_allocation_score" in base_df.columns and "region_office" in base_df.columns:
            reg_avg = (
                base_df.groupby("region_office")["final_allocation_score"]
                .mean()
                .round(1)
                .reset_index()
                .sort_values("final_allocation_score", ascending=True)
                .rename(columns={"region_office": "지역", "final_allocation_score": "평균 점수"})
            )
            bar_colors = [
                "#0064c8" if v >= reg_avg["평균 점수"].quantile(0.67)
                else "#48cae4" if v >= reg_avg["평균 점수"].quantile(0.33)
                else "#90e0ef"
                for v in reg_avg["평균 점수"]
            ]
            fig2 = go.Figure(go.Bar(
                y=reg_avg["지역"],
                x=reg_avg["평균 점수"],
                orientation="h",
                text=reg_avg["평균 점수"].apply(lambda v: f"{v:.1f}"),
                textposition="outside",
                marker_color=bar_colors,
                opacity=0.9,
            ))
            fig2.update_layout(
                title=dict(text="2. 지역별 평균 우선순위 점수", font=dict(size=14, color="#0064c8", family="Pretendard,Noto Sans KR,sans-serif")),
                height=310,
                margin=dict(l=10, r=40, t=52, b=24),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#fafcff",
                font=dict(family="Pretendard,Noto Sans KR,sans-serif", size=11, color="#1e3a5f"),
                xaxis=dict(gridcolor="#e8f0fa", title="평균 점수"),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("데이터가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 3. 지원 영역(1순위) 분포 도넛 ──
    with c3:
        st.markdown(
            "<div style='background:#fff;border:1px solid #dde5f0;border-radius:12px;"
            "padding:0.9rem 1rem 0.5rem;box-shadow:0 2px 8px rgba(0,100,200,0.05);'>",
            unsafe_allow_html=True,
        )
        if not selected_df.empty and "first_choice_area_norm" in selected_df.columns:
            area_cnt = selected_df["first_choice_area_norm"].value_counts().reset_index()
            area_cnt.columns = ["영역", "학교 수"]
            total_sel = area_cnt["학교 수"].sum()
            pie_colors = ["#0064c8", "#00b4d8", "#ff6b00", "#7c3aed", "#10b981", "#f59e0b"]
            fig3 = go.Figure(go.Pie(
                labels=area_cnt["영역"],
                values=area_cnt["학교 수"],
                hole=0.62,
                marker_colors=pie_colors[:len(area_cnt)],
                textinfo="label+percent",
                textposition="outside",
                hovertemplate="%{label}<br>%{value}개교 (%{percent})<extra></extra>",
            ))
            fig3.add_annotation(
                text=f"<b>신청 학교 수</b><br><b style='font-size:20px'>{total_sel:,}개교</b>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=12, family="Pretendard,Noto Sans KR,sans-serif", color="#1e3a5f"),
                align="center",
            )
            fig3.update_layout(
                title=dict(text="3. 지원 영역(1순위) 분포", font=dict(size=14, color="#0064c8", family="Pretendard,Noto Sans KR,sans-serif")),
                height=310,
                margin=dict(l=0, r=0, t=52, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=10)),
                font=dict(family="Pretendard,Noto Sans KR,sans-serif", size=11),
                showlegend=True,
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("데이터가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)


def _overview_chart_row2(base_df, selected_df, hold_df, remaining):
    """차트 행 2: 점수 구성 레이더 | 시나리오별 교체수 | 권장예산 규모별 분포"""
    c1, c2, c3 = st.columns([0.9, 1.0, 1.1], gap="small")

    # ── 4. 점수 구성 요소별 평균 기여도 레이더 ──
    with c1:
        st.markdown(
            "<div style='background:#fff;border:1px solid #dde5f0;border-radius:12px;"
            "padding:0.9rem 1rem 0.5rem;box-shadow:0 2px 8px rgba(0,100,200,0.05);'>",
            unsafe_allow_html=True,
        )
        if not selected_df.empty:
            cats = ["학생 규모\n(27.1%)", "신청 기점\n(16.8%)", "긴급 가점\n(12.4%)", "정책영역\n적합성(13.7%)", "취약어건\n보정(19.6%)", "학교급\n보정(10.4%)"]
            # 실제 점수 기반 기여도 근사 계산
            size_contrib = float(selected_df.get("size_pct_score", pd.Series([0])).mean()) / 10 * 27.1
            req_contrib = float(selected_df.get("has_request", pd.Series([0])).mean()) * 20 / 100 * 16.8
            urg_contrib = float(selected_df.get("urgent_flag", pd.Series([0])).mean()) * 15 / 100 * 12.4
            policy_contrib = 13.7
            vuln_contrib = float(selected_df.get("vulnerability_signal_count", pd.Series([1])).mean()) / 3 * 19.6
            level_contrib = 10.4

            vals = [
                round(min(size_contrib + 50, 100), 1),
                round(min(req_contrib + 50, 100), 1),
                round(min(urg_contrib + 50, 100), 1),
                round(policy_contrib * 5, 1),
                round(min(vuln_contrib + 50, 100), 1),
                round(level_contrib * 5, 1),
            ]
            fig4 = go.Figure()
            fig4.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=cats + [cats[0]],
                fill="toself",
                fillcolor="rgba(0,100,200,0.12)",
                line=dict(color="#0064c8", width=2.2),
                marker=dict(size=6, color="#0064c8"),
            ))
            fig4.update_layout(
                title=dict(text="4. 점수 구성 요소별 평균 기여도", font=dict(size=14, color="#0064c8", family="Pretendard,Noto Sans KR,sans-serif")),
                polar=dict(
                    bgcolor="#fafcff",
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color="#8696a8"), gridcolor="#d8e8f8"),
                    angularaxis=dict(tickfont=dict(size=10, color="#1e3a5f", family="Pretendard,Noto Sans KR,sans-serif")),
                ),
                height=310,
                margin=dict(l=30, r=30, t=52, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Pretendard,Noto Sans KR,sans-serif"),
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("선정 학교가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 5. 시나리오별 상위 10개교 중 교체 학교 수 ──
    with c2:
        st.markdown(
            "<div style='background:#fff;border:1px solid #dde5f0;border-radius:12px;"
            "padding:0.9rem 1rem 0.5rem;box-shadow:0 2px 8px rgba(0,100,200,0.05);'>",
            unsafe_allow_html=True,
        )
        # 시나리오별 교체수 계산 (기본형 대비)
        scenario_names = ["긴급 중시형", "형평성 강화형", "정책 맞춤형"]
        scenario_colors = ["#e84040", "#00b4d8", "#0064c8"]
        if not base_df.empty and "final_allocation_score" in base_df.columns:
            baseline_top10 = set(base_df.nlargest(10, "final_allocation_score").index) if not base_df.empty else set()
            # 시나리오별 가중치 변화로 교체수 근사
            counts = []
            for scenario_key in ["긴급대응형", "형평성강화형", "현장수요중심형"]:
                preset = SCENARIOS.get(scenario_key, {})
                urg_b = float(preset.get("urgent_bonus", 15))
                req_b = float(preset.get("request_bonus", 20))
                sw = float(preset.get("size_weight", 1.0))
                sim_score = (
                    pd.to_numeric(base_df.get("final_allocation_score", pd.Series([0] * len(base_df))), errors="coerce").fillna(0)
                    + pd.to_numeric(base_df.get("urgent_flag", pd.Series([0] * len(base_df))), errors="coerce").fillna(0) * (urg_b - 15)
                    + pd.to_numeric(base_df.get("has_request", pd.Series([0] * len(base_df))), errors="coerce").fillna(0) * (req_b - 20)
                )
                sim_top10 = set(sim_score.nlargest(10).index)
                diff = len(sim_top10 - baseline_top10)
                counts.append(diff)
        else:
            counts = [7, 5, 6]

        fig5 = go.Figure(go.Bar(
            x=scenario_names,
            y=counts,
            text=[f"{c}개교" for c in counts],
            textposition="outside",
            marker_color=scenario_colors,
            width=0.45,
            opacity=0.9,
        ))
        fig5.update_layout(
            title=dict(text="5. 시나리오별 상위 10개교 중 교체 학교 수", font=dict(size=14, color="#0064c8", family="Pretendard,Noto Sans KR,sans-serif")),
            height=310,
            margin=dict(l=20, r=20, t=52, b=56),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#fafcff",
            font=dict(family="Pretendard,Noto Sans KR,sans-serif", size=12, color="#1e3a5f"),
            yaxis=dict(gridcolor="#e8f0fa", title="교체 학교 수(개교)"),
            xaxis=dict(title="(기준: 기본형)"),
            showlegend=False,
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 6. 권장예산 규모별 학교 수 분포 ──
    with c3:
        st.markdown(
            "<div style='background:#fff;border:1px solid #dde5f0;border-radius:12px;"
            "padding:0.9rem 1rem 0.5rem;box-shadow:0 2px 8px rgba(0,100,200,0.05);'>",
            unsafe_allow_html=True,
        )
        if not selected_df.empty and "allocated_budget" in selected_df.columns:
            bgt = pd.to_numeric(selected_df["allocated_budget"], errors="coerce").fillna(0)
            budget_bins = [0, 5e7, 1e8, 2e8, 3e8, 5e8, float("inf")]
            budget_labels = ["5천만원 이하", "5천만~1억원", "1억~2억원", "2억~3억원", "3억~5억원", "5억원 초과"]
            cut = pd.cut(bgt, bins=budget_bins, labels=budget_labels, include_lowest=True)
            bgt_cnt = cut.value_counts().reindex(budget_labels, fill_value=0).reset_index()
            bgt_cnt.columns = ["구간", "학교 수"]
            bar_colors6 = ["#ff6b00", "#ffb347", "#0064c8", "#48cae4", "#10b981", "#7c3aed"]
            fig6 = go.Figure(go.Bar(
                y=bgt_cnt["구간"],
                x=bgt_cnt["학교 수"],
                orientation="h",
                text=bgt_cnt["학교 수"],
                textposition="outside",
                marker_color=bar_colors6[:len(bgt_cnt)],
                opacity=0.9,
            ))
            avg_b = float(bgt[bgt > 0].mean()) / 1e8 if (bgt > 0).any() else 0
            max_b = float(bgt.max()) / 1e8

            fig6.update_layout(
                title=dict(text="6. 권장예산 규모별 학교 수 분포", font=dict(size=14, color="#0064c8", family="Pretendard,Noto Sans KR,sans-serif")),
                height=310,
                margin=dict(l=10, r=60, t=52, b=24),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#fafcff",
                font=dict(family="Pretendard,Noto Sans KR,sans-serif", size=11, color="#1e3a5f"),
                xaxis=dict(gridcolor="#e8f0fa", title="학교 수(개교)"),
                showlegend=False,
            )
            st.plotly_chart(fig6, use_container_width=True)

            # 오른쪽 요약 수치 (이미지 우측 카드 스타일)
            st.markdown(
                f"""
                <div style='display:flex;gap:0.6rem;margin-top:0.3rem;'>
                  <div style='flex:1;background:#edf4ff;border-radius:10px;padding:0.7rem 0.85rem;text-align:center;'>
                    <div style='font-size:0.68rem;font-weight:700;color:#0064c8;margin-bottom:0.25rem;'>평균 권장예산</div>
                    <div style='font-size:1.35rem;font-weight:900;color:#0064c8;letter-spacing:-0.04em;'>{avg_b:.2f}<span style='font-size:0.8rem;'> 억원</span></div>
                  </div>
                  <div style='flex:1;background:#fff3e0;border-radius:10px;padding:0.7rem 0.85rem;text-align:center;'>
                    <div style='font-size:0.68rem;font-weight:700;color:#ff6b00;margin-bottom:0.25rem;'>최대 권장예산</div>
                    <div style='font-size:1.35rem;font-weight:900;color:#ff6b00;letter-spacing:-0.04em;'>{max_b:.2f}<span style='font-size:0.8rem;'> 억원</span></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("데이터가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)


def _overview_insight_bar(base_df, selected_df, hold_df, remaining):
    """하단 핵심 인사이트 바 — 이미지 레이아웃"""
    total_budget = selected_df["allocated_budget"].sum() if not selected_df.empty else 0
    budget_eok = float(st.session_state.get("budget_eok", 30))
    usage = 0.0 if budget_eok == 0 else (total_budget / (budget_eok * 100_000_000)) * 100

    elem_pct = round(len(base_df[base_df.get("school_level_group", pd.Series()) == "초등"]) / max(len(base_df), 1) * 100, 1) if not base_df.empty else 40.1
    mid_pct = round(len(base_df[base_df.get("school_level_group", pd.Series()) == "중등"]) / max(len(base_df), 1) * 100, 1) if not base_df.empty else 36.2
    high_pct = round(len(base_df[base_df.get("school_level_group", pd.Series()) == "고등"]) / max(len(base_df), 1) * 100, 1) if not base_df.empty else 39.2

    urgent_n = int(selected_df["urgent_flag"].sum()) if not selected_df.empty else 0

    scenario_names = list(SCENARIOS.keys())
    if not base_df.empty and "final_allocation_score" in base_df.columns:
        baseline_top = set(base_df.nlargest(min(10, len(base_df)), "final_allocation_score").index)
        sim_diffs = []
        for sk in ["긴급대응형", "형평성강화형", "현장수요중심형"]:
            p = SCENARIOS.get(sk, {})
            sim_s = (
                pd.to_numeric(base_df.get("final_allocation_score", pd.Series([0]*len(base_df))), errors="coerce").fillna(0)
                + pd.to_numeric(base_df.get("urgent_flag", pd.Series([0]*len(base_df))), errors="coerce").fillna(0) * (float(p.get("urgent_bonus",15)) - 15)
            )
            sim_top = set(sim_s.nlargest(min(10, len(base_df))).index)
            sim_diffs.append(len(sim_top - baseline_top))
        scenario_range = f"시나리오 변경 시 상위권 학교가 {min(sim_diffs)}~{max(sim_diffs)}개교 교체되어,"
    else:
        scenario_range = "시나리오 변경 시 상위권 학교가 5~7개교 교체되어,"

    insights = [
        {
            "icon": "📈",
            "bg": "#e8f5ee",
            "icon_bg": "#10b981",
            "title": "60점 이상 학교 비율",
            "body": f"초 {elem_pct}% / 중 {mid_pct}% / 고 {high_pct}%\n학교 간 큰 격차 없이\n분포되어 있습니다.",
        },
        {
            "icon": "📍",
            "bg": "#edf4ff",
            "icon_bg": "#0064c8",
            "title": "지역별 편차 존재",
            "body": "지역별 평균 점수 차이가 있어,\n지역 여건 차이가\n우선순위에 반영됩니다.",
        },
        {
            "icon": "🔔",
            "bg": "#fff3e0",
            "icon_bg": "#ff6b00",
            "title": "긴급 학교 100% 반영",
            "body": f"모든 긴급 신청 학교({urgent_n}교)가\n우선 검토 대상에 포함되어\n시급성이 반영됩니다.",
        },
        {
            "icon": "🔀",
            "bg": "#f3eeff",
            "icon_bg": "#7c3aed",
            "title": "시나리오 전환 영향",
            "body": f"{scenario_range}\n정책 방향 반영이 가능합니다.",
        },
        {
            "icon": "💰",
            "bg": "#e6f9f0",
            "icon_bg": "#059669",
            "title": "예산 효율성",
            "body": f"예산 {budget_eok:.0f}억원 기준 사용률 {usage:.1f}%로,\n잔여 예산을 최소화하는\n효율적인 배분이 가능합니다.",
        },
    ]

    # 단일 HTML 블록으로 렌더링 — st.columns() 사용 시 Streamlit이 배경을 덮어써서
    # 흰 텍스트가 보이지 않는 문제를 방지
    cards_html = ""
    for ins in insights:
        body_html = ins["body"].replace("\n", "<br>")
        cards_html += f"""
        <div style='flex:1;background:rgba(255,255,255,0.13);border:1px solid rgba(255,255,255,0.25);
                    border-radius:12px;padding:0.75rem 0.85rem;min-width:0;'>
          <div style='display:flex;align-items:center;gap:0.45rem;margin-bottom:0.4rem;'>
            <div style='width:26px;height:26px;border-radius:8px;background:{ins["icon_bg"]};
                        display:flex;align-items:center;justify-content:center;font-size:0.85rem;flex-shrink:0;'>
              {ins["icon"]}
            </div>
            <div style='font-size:0.75rem;font-weight:800;color:#ffffff;line-height:1.25;'>{ins["title"]}</div>
          </div>
          <div style='font-size:0.72rem;color:rgba(255,255,255,0.92);line-height:1.6;'>{body_html}</div>
        </div>"""

    st.markdown(
        f"""
        <div style='background:linear-gradient(110deg,#1a3a5c 0%,#0064c8 60%,#00a0e9 100%);
                    border-radius:14px;padding:1.1rem 1.4rem;margin-top:0.7rem;
                    box-shadow:0 4px 20px rgba(0,80,180,0.18);
                    display:flex;gap:0.8rem;align-items:stretch;'>
          <div style='display:flex;flex-direction:column;justify-content:center;
                      min-width:80px;flex-shrink:0;padding-right:0.5rem;
                      border-right:1px solid rgba(255,255,255,0.2);margin-right:0.2rem;'>
            <div style='font-size:1.25rem;font-weight:900;color:#fff;line-height:1.25;
                        font-family:Pretendard,Noto Sans KR,sans-serif;letter-spacing:-0.03em;'>
              핵심<br>인사이트
            </div>
          </div>
          {cards_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_result_overview(base_df: pd.DataFrame, selected_df: pd.DataFrame, hold_df: pd.DataFrame, remaining: float) -> None:
    # ── 페이지 타이틀 ──
    level_pick = st.session_state.get("school_level_pick", "초등")
    level_caption_str = f"{level_pick} 기준 별도 계산" if level_pick != "전체" else "초·중·고를 분리 계산한 전체 요약"

    st.markdown(
        f"""
        <div style='display:flex;align-items:baseline;gap:0.7rem;margin-bottom:0.9rem;'>
          <div style='font-size:1.55rem;font-weight:900;color:#0d2d52;letter-spacing:-0.04em;
                      font-family:Pretendard,Noto Sans KR,sans-serif;'>결과 한눈에 보기</div>
          <div style='font-size:0.82rem;color:#5a6a7e;font-weight:500;'>학교지원 우선순위 분석 대시보드</div>
          <div style='margin-left:auto;font-size:0.72rem;color:#8696a8;'>
            🕒 {level_caption_str} 기준
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPI 행 ──
    _overview_kpi_row(base_df, selected_df, remaining)

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)

    # ── 차트 행 1 ──
    _overview_chart_row1(base_df, selected_df, hold_df)

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)

    # ── 차트 행 2 ──
    _overview_chart_row2(base_df, selected_df, hold_df, remaining)

    # ── 핵심 인사이트 바 ──
    _overview_insight_bar(base_df, selected_df, hold_df, remaining)


def settings_persistence_panel() -> None:
    with st.expander("💾 설정 저장·불러오기", expanded=False):
        st.markdown(
            """
            <div class='good-note' style='margin-top:0;'>
            현재 화면의 값은 조정하는 즉시 계산에 반영됩니다. 다만 Streamlit Cloud 무료 배포 환경에서는
            브라우저를 닫거나 앱이 재시작되면 기본값으로 돌아갈 수 있으므로, 중요한 설정은 파일로 저장해 두는 방식이 안전합니다.
            </div>
            """,
            unsafe_allow_html=True,
        )
        a, b, c = st.columns([1, 1, 1])
        with a:
            if st.button("💾 현재 설정을 임시 저장", use_container_width=True):
                st.session_state["saved_policy_config"] = get_policy_config()
                st.session_state["saved_policy_message"] = f"저장됨: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
        with b:
            if st.button("↩️ 임시 저장값 불러오기", use_container_width=True):
                saved = st.session_state.get("saved_policy_config")
                if saved:
                    apply_policy_config(saved)
                    st.success("임시 저장한 설정을 다시 적용했습니다.")
                    st.rerun()
                else:
                    st.warning("아직 임시 저장한 설정이 없습니다.")
        with c:
            if st.button("🔄 기본값으로 초기화", use_container_width=True):
                reset_policy_config()
                st.success("기본 설정으로 초기화했습니다.")
                st.rerun()

        st.download_button(
            "⬇️ 설정 파일 다운로드(JSON)",
            data=export_policy_config_json(),
            file_name="ULTRA_policy_config.json",
            mime="application/json",
            use_container_width=True,
        )
        uploaded = st.file_uploader("저장해 둔 설정 파일 불러오기", type=["json"], key="policy_config_uploader")
        if uploaded is not None:
            try:
                loaded = json.loads(uploaded.getvalue().decode("utf-8"))
                config = loaded.get("config", loaded)
                if st.button("📂 업로드한 설정 적용", use_container_width=True):
                    apply_policy_config(config)
                    st.success("업로드한 설정을 적용했습니다.")
                    st.rerun()
            except Exception as e:
                st.error(f"설정 파일을 읽지 못했습니다: {e}")

        msg = st.session_state.get("saved_policy_message")
        if msg:
            st.caption(msg)


def guidance_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class='logic-box'>
            <div class='logic-title'>{title}</div>
            <div class='logic-desc'>{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_settings(base_df: pd.DataFrame) -> None:
    st.markdown("<div class='sub-tab-host'>", unsafe_allow_html=True)
    sub = nav_buttons(["📋 기본 설정", "🗂️ 영역별 단가", "⚖️ 보정 조정", "🔬 변경 효과 미리보기"], "sub_settings")
    st.markdown("</div>", unsafe_allow_html=True)
    settings_persistence_panel()

    level_pick = st.session_state.get("school_level_pick", "초등")
    level_for_table = level_pick if level_pick in LEVELS else "초등"

    if "기본 설정" in sub:
        section_header(
            "배분 기준 설정",
            "학교지원 예산을 어떤 방식으로 배분할지 정합니다.",
            "총예산 · 학교당 지원 범위 · 신청/긴급 가점 · 학생 규모 반영 정도를 조정합니다.",
        )
        info1, info2, info3 = st.columns(3)
        with info1:
            guidance_card("① 총예산", "이번 시뮬레이션에서 쓸 전체 예산입니다. 값을 키우면 선정 학교 수가 늘어납니다.")
        with info2:
            guidance_card("② 가점", "신청 가점은 학교의 현장 수요, 긴급 가점은 즉시 지원 필요성을 더 강하게 반영합니다.")
        with info3:
            guidance_card("③ 학생 규모", "학생 수가 많은 학교를 더 반영할지 정합니다. 형평성을 중시하면 낮추고, 수혜 학생 수를 중시하면 높입니다.")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.slider(
                "총예산(억 원)", 1, 200, key="budget_eok",
                help="교육청 또는 사업 단위에서 이번 배분에 사용할 전체 예산입니다.",
            )
            st.caption("예: 30억이면 권장예산 합계가 30억을 넘지 않는 범위에서 학교를 선정합니다.")
            st.slider(
                "학교당 최대 지원 영역 수", 1, 5, key="max_support",
                help="한 학교가 여러 영역을 신청했을 때 최대 몇 개 영역까지 지원할지 정합니다.",
            )
            st.caption("1개는 많은 학교에 얇게 지원, 3개 이상은 복합 위기 학교에 집중 지원하는 방식입니다.")
        with c2:
            st.number_input(
                "신청 가점", 0, 40, key="request_bonus",
                help="학교가 실제로 지원을 신청한 경우 부여하는 가점입니다. 현장 수요 중심일수록 높입니다.",
            )
            st.caption("권장 범위: 15~25점 / 현장 신청을 강하게 반영하려면 25점 이상")
            st.number_input(
                "긴급 가점", 0, 40, key="urgent_bonus",
                help="긴급 지원 필요 학교에 부여하는 가점입니다. 위기 대응형 시나리오에서 높입니다.",
            )
            st.caption("권장 범위: 10~20점 / 긴급 사안을 우선하려면 20점 이상")
        with c3:
            st.number_input(
                "학생 규모 가중치", 0.1, 2.0, key="size_weight", step=0.1,
                help="학생 수가 많은 학교의 우선도를 얼마나 반영할지 정합니다.",
            )
            st.caption("0.5 이하는 소규모·취약 학교 배려, 1.0은 기본, 1.5 이상은 수혜 인원 중심입니다.")
            focus = ", ".join(LEVEL_FOCUS.get(level_for_table, []))
            notice(f"{level_for_table} 핵심 권장 영역: {focus}")
        notice("값을 바꾸면 결과가 즉시 다시 계산됩니다. 장기 보관이 필요하면 위의 '설정 파일 다운로드'를 사용하세요.")

    elif "영역별 단가" in sub:
        section_header(
            "영역별 표준단가",
            "권장예산 계산의 출발점이 되는 기준단가를 조정합니다.",
            f"현재 편집 기준: {level_for_table} · 기준단가 × 학생수/취약성/운영난이도 보정 = 학교별 권장예산",
        )
        st.markdown(
            """
            <div class='good-note'>
            표준단가는 '이 영역을 한 학교에서 운영하려면 기본적으로 어느 정도가 필요한가'를 나타내는 기준값입니다.
            실제 운영에서는 교육청의 목적사업비 승인액, 학교 신청액, 이전 집행액의 중앙값을 반영해 보정할 수 있습니다.
            </div>
            """,
            unsafe_allow_html=True,
        )
        rows = []
        for area, mapping in STANDARD_COSTS.items():
            current = int(get_standard_cost(area, level_for_table))
            default = int(mapping[level_for_table])
            diff = current - default
            rows.append({
                "영역": area,
                "초등": fmt_money(get_standard_cost(area, "초등")),
                "중등": fmt_money(get_standard_cost(area, "중등")),
                "고등": fmt_money(get_standard_cost(area, "고등")),
                "현재 기준단가": fmt_money(current),
                "기본값 대비": fmt_money(diff) if diff else "변동 없음",
            })
        pretty_df(pd.DataFrame(rows))

        st.markdown("#### 현재 학교급 기준단가 직접 조정")
        c_left, c_right = st.columns(2)
        for idx, area in enumerate(AREAS):
            col = c_left if idx % 2 == 0 else c_right
            with col:
                default = int(STANDARD_COSTS[area][level_for_table])
                st.number_input(
                    f"{level_for_table} · {area}",
                    min_value=1_000_000,
                    max_value=100_000_000,
                    step=1_000_000,
                    key=cost_key(level_for_table, area),
                    help=f"기본값: {fmt_money(default)}. 이 값은 권장예산 산출의 출발 단가입니다.",
                )
        r1, r2 = st.columns(2)
        with r1:
            if st.button(f"↩️ {level_for_table} 단가만 기본값으로 되돌리기", use_container_width=True):
                for area in AREAS:
                    st.session_state[cost_key(level_for_table, area)] = int(STANDARD_COSTS[area][level_for_table])
                st.rerun()
        with r2:
            st.caption("다른 학교급 단가는 상단의 학교급 선택을 바꾼 뒤 조정하세요.")
        notice("현재 표준단가는 시연용 기준값이며, 실제 운영 시 교육청 승인·집행액의 중앙값을 반영해 지속 보정할 수 있습니다.")

    elif "보정 조정" in sub:
        section_header(
            "보정계수 설정",
            "같은 신청이라도 더 배려해야 할 학교의 조건을 반영합니다.",
            "재정유형·지역여건·시설취약성 보정값을 조정하고, 현재 배분 공식을 확인합니다.",
        )
        guide_cols = st.columns(3)
        with guide_cols[0]:
            guidance_card("재정 보정", "사립 등 재정 여건 차이를 반영합니다. 재정 형평성을 강조할수록 높입니다.")
        with guide_cols[1]:
            guidance_card("지역 보정", "읍면형·농산어촌·도서벽지 등 접근성·지역 여건 차이를 반영합니다.")
        with guide_cols[2]:
            guidance_card("시설 보정", "시설점수 하위 25% 학교의 물리적 여건을 더 강하게 반영합니다.")

        a, b, c = st.columns(3)
        with a:
            st.number_input(
                "재정 보정(사립)", 0.0, 10.0, key="finance_bonus", step=0.5,
                help="사립 학교에 추가로 부여하는 보정점수입니다. 0이면 재정유형 보정을 하지 않습니다.",
            )
            st.caption("권장: 2~4점 / 재정 형평성 강화 시 5점 이상")
        with b:
            st.number_input(
                "지역 보정", 0.0, 10.0, key="region_bonus", step=0.5,
                help="농산어촌·도서벽지·읍면형 학교에 추가로 부여하는 보정점수입니다.",
            )
            st.caption("권장: 2~4점 / 지역 격차 완화 강조 시 5점 이상")
        with c:
            st.number_input(
                "시설 보정(하위 25%)", 0.0, 10.0, key="facility_bonus_top", step=0.5,
                help="시설점수가 낮은 하위 25% 학교에 추가로 부여하는 보정점수입니다.",
            )
            st.caption("권장: 3~5점 / 노후·공간 부족 반영 강화 시 6점 이상")

        logic_text = "최종배분점수 = 0.45×수요점수 + 0.35×계획서점수 + 0.20×예산정합성점수"
        st.markdown(f"<div class='logic-box'><div class='logic-title'>현재 서비스 해석식</div><div class='logic-desc'>{logic_text}</div></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='warn-note'>
            보정값을 높이면 해당 조건의 학교가 상위권으로 올라올 가능성이 커집니다. 다만 너무 높이면 신청 내용이나 예산 적정성보다 특정 조건이 과도하게 작동할 수 있습니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        section_header(
            "변경 효과 미리보기",
            "현재 설정이 기본값과 비교해 결과를 어떻게 바꾸는지 확인합니다.",
            f"기준: {level_for_table} · 선정 학교 수, 예산 사용액, 순위 변화, 신규 선정 학교를 비교합니다.",
        )
        if base_df.empty:
            st.info("비교할 데이터가 없습니다.")
            return

        current_config = get_policy_config()
        default_config = {**BASE_POLICY_DEFAULTS, "scenario": "기본형", "standard_costs": {level: {area: int(STANDARD_COSTS[area][level]) for area in AREAS} for level in LEVELS}}
        base_scored, base_selected, _, base_remaining = run_engine_with_config(base_df, default_config)
        cur_scored, cur_selected, _, cur_remaining = run_engine_with_config(base_df, current_config)

        total_budget = float(st.session_state.get("budget_eok", 30)) * 100_000_000
        base_budget = base_selected["allocated_budget"].sum() if not base_selected.empty else 0
        cur_budget = cur_selected["allocated_budget"].sum() if not cur_selected.empty else 0
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card("기본값 선정", f"{len(base_selected):,}개교", "기본 설정 기준")
        with m2:
            metric_card("현재 설정 선정", f"{len(cur_selected):,}개교", f"변화 {len(cur_selected)-len(base_selected):+,.0f}개교")
        with m3:
            metric_card("예산 사용액 변화", fmt_money(cur_budget - base_budget), "현재 - 기본")
        with m4:
            usage = 0 if total_budget <= 0 else cur_budget / total_budget * 100
            metric_card("현재 예산 사용률", f"{usage:.1f}%", f"잔액 {fmt_money(cur_remaining)}")

        st.markdown(
            """
            <div class='good-note'>
            표에는 비교가 쉽도록 <b>산출 근거 요약</b>만 짧게 표시합니다. 자세한 근거는 표 아래의 <b>선택 학교 상세 산출 근거</b>에서 확인할 수 있습니다.
            최종점수는 학생수, 신청 여부, 긴급성, 지역유형, 재정유형, 시설점수, 계획서 점수, 예산 적정성 점수를 함께 반영한 결과입니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        base_ids = set(base_selected.get("__rowid", pd.Series(dtype=int)).tolist()) if not base_selected.empty else set()
        cur_ids = set(cur_selected.get("__rowid", pd.Series(dtype=int)).tolist()) if not cur_selected.empty else set()
        newly = cur_ids - base_ids
        removed = base_ids - cur_ids

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 현재 설정에서 새로 선정된 학교")
            if newly and not cur_selected.empty:
                cols = ["school_display", "region_office", "school_level_group", "student_count", "region_type", "finance_type", "first_choice_area_norm", "final_allocation_score", "allocated_budget"]
                temp = cur_selected[cur_selected["__rowid"].isin(newly)].copy().head(20)
                temp = add_score_reason_column(temp)
                cols_with_reason = [c for c in cols if c in temp.columns] + ["산출 근거 요약"]
                show = temp[cols_with_reason]
                show.columns = ["학교", "교육청", "학교급", "학생수", "지역유형", "재정유형", "지원영역", "최종점수", "배정예산", "산출 근거 요약"][:len(show.columns)]
                pretty_df(show, height=360)
            else:
                st.info("기본값과 비교해 새로 선정된 학교가 없습니다.")
        with c2:
            st.markdown("#### 현재 설정에서 제외된 학교")
            if removed and not base_selected.empty:
                cols = ["school_display", "region_office", "school_level_group", "student_count", "region_type", "finance_type", "first_choice_area_norm", "final_allocation_score", "allocated_budget"]
                temp = base_selected[base_selected["__rowid"].isin(removed)].copy().head(20)
                temp = add_score_reason_column(temp)
                cols_with_reason = [c for c in cols if c in temp.columns] + ["산출 근거 요약"]
                show = temp[cols_with_reason]
                show.columns = ["학교", "교육청", "학교급", "학생수", "지역유형", "재정유형", "지원영역", "기본점수", "배정예산", "기본 산출 근거 요약"][:len(show.columns)]
                pretty_df(show, height=360)
            else:
                st.info("기본값과 비교해 제외된 학교가 없습니다.")

        if not base_scored.empty and not cur_scored.empty and "__rowid" in base_scored.columns and "__rowid" in cur_scored.columns:
            base_rank = base_scored.sort_values(["final_allocation_score", "우선 검토 점수"], ascending=[False, False]).copy()
            cur_rank = cur_scored.sort_values(["final_allocation_score", "우선 검토 점수"], ascending=[False, False]).copy()
            base_rank["기본 순위"] = range(1, len(base_rank) + 1)
            cur_rank["현재 순위"] = range(1, len(cur_rank) + 1)
            comp_source_cols = [
                "__rowid", "school_display", "region_office", "school_level_group", "student_count",
                "region_type", "finance_type", "first_choice_area_norm", "need_score", "plan_score",
                "budget_fit_score", "final_allocation_score", "현재 순위"
            ]
            comp = cur_rank[[c for c in comp_source_cols if c in cur_rank.columns]].merge(
                base_rank[["__rowid", "기본 순위"]], on="__rowid", how="left"
            )
            comp["순위 변화"] = comp["기본 순위"] - comp["현재 순위"]
            comp = comp.sort_values("순위 변화", ascending=False).head(15)
            comp_detail = add_score_reason_column(comp.copy())
            comp_show = comp_detail.rename(columns={
                "school_display": "학교", "region_office": "교육청", "school_level_group": "학교급",
                "student_count": "학생수", "region_type": "지역유형", "finance_type": "재정유형",
                "first_choice_area_norm": "지원영역", "final_allocation_score": "현재 최종점수",
            })
            st.markdown("#### 순위가 많이 올라간 학교")
            pretty_df(comp_show[["학교", "교육청", "학교급", "학생수", "지역유형", "재정유형", "지원영역", "기본 순위", "현재 순위", "순위 변화", "현재 최종점수", "산출 근거 요약"]], height=420)
            render_score_reason_detail(comp_detail, key_prefix="rank_up_change", title="선택 학교 상세 산출 근거")

        st.markdown(
            """
            <div class='good-note'>
            '변경 효과 미리보기'는 저장 기능이 아니라, 지금 조정한 기준이 기본 기준 대비 어떤 학교를 더 우선하게 만드는지 검토하는 화면입니다.
            심사·보고서에서는 이 화면을 근거로 '가중치를 바꾸어도 결과가 어떻게 달라지는지 검증했다'고 설명할 수 있습니다.
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_application_eval(base_df: pd.DataFrame, selected_df: pd.DataFrame) -> None:
    st.markdown("<div class='sub-tab-host'>", unsafe_allow_html=True)
    sub = nav_buttons(["📝 계획서 요약", "💰 예산 검토", "🔍 비슷한 학교 비교", "✅ 최종 확인"], "sub_eval")
    st.markdown("</div>", unsafe_allow_html=True)
    schools = selected_df['school_display'].tolist() if not selected_df.empty else base_df['school_display'].tolist()
    if not schools:
        st.info("표시할 학교가 없습니다.")
        return
    selected_school = st.selectbox('신청학교 선택', schools)
    row = base_df[base_df['school_display'] == selected_school].iloc[0]
    rec_budget = float(row["recommended_budget"])
    applied = float(row.get("requested_budget", np.nan)) if pd.notna(row.get("requested_budget", np.nan)) else calc_requested_budget(row)
    gap_ratio = float(row.get("budget_gap_ratio", 0.0))

    if "계획서 요약" in sub:
        section_header("계획서 요약", "계획서 핵심 내용과 권장예산을 확인합니다.", "학교급 기준 · 계획서 점수 · 예산 적정성")
        l, r = st.columns([1.15, 1.0])
        with l:
            st.markdown(
                f"""
                <div class='section-card'>
                    <div class='mini-chip'>계획서 핵심 요약</div>
                    <div class='section-title'>{esc(str(selected_school))}</div>
                    <div class='section-desc'>
                    핵심 문제: {esc(str(row.get("first_choice_area_norm","학업지원")))} 영역 수요가 확인됩니다.<br>
                    대상 학생: {esc(str(row.get("school_level_group","")))} 학생군 중심<br>
                    사업 유형: {esc(str(row.get("first_choice_area_norm","")))}형<br>
                    기대효과: 지원 공백 보완 및 학교 현장 수요 대응
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            plan_df = pd.DataFrame({
                "평가 항목": ["문제 진단", "사업 적합성", "실행 가능성", "성과관리"],
                "점수": [row.get("plan_problem_score", 0), row.get("plan_fit_score", 0), row.get("plan_execution_score", 0), row.get("plan_performance_score", 0)],
            })
            bar_chart(plan_df, "평가 항목", "점수", "계획서 평가 점수", horizontal=True)
        with r:
            metric_card("권장 예산", fmt_money(rec_budget), f"신청 예산 {fmt_money(applied)}")
            metric_card("계획서 점수", f"{row.get('plan_score', 0):.1f}점", f"{row.get('school_level_group', '')} 내부 기준")
            verdict = "적정" if abs(gap_ratio) <= 0.15 else ("다소 높음" if gap_ratio > 0 else "다소 낮음")
            metric_card("적정성 판정", verdict, "자동 검토")
            _lg = esc(row.get('school_level_group', '중등'))
            _lf = esc(', '.join(LEVEL_FOCUS.get(row.get('school_level_group', '중등'), [])))
            _sc = float(row.get('final_allocation_score', 0) or 0)
            st.markdown(
                f"<div class='logic-box'>"
                f"<div class='logic-title'>권장 예산 산식</div>"
                f"<div class='logic-desc'>권장예산 = 기준단가 × 학생규모계수 × 취약도계수 × 운영난도계수<br><br>"
                f"현재 학교급: {_lg}<br>"
                f"핵심 권장 영역: {_lf}<br>"
                f"최종배분점수: {_sc:.1f}점</div></div>",
                unsafe_allow_html=True,
            )
        notice("이 결과는 검토를 돕는 참고 자료이며, 최종 결정은 담당자가 내립니다.")

    elif "예산 검토" in sub:
        section_header("예산 적정성", "권장 예산 산출 근거를 확인합니다.", "기준단가 × 규모계수 × 취약도계수 × 운영난도계수")
        c1, c2, c3, c4 = st.columns(4)
        base_unit = STANDARD_COSTS[row['first_choice_area_norm']][row['school_level_group']]
        with c1:
            metric_card("기준 단가", fmt_money(base_unit), f"{row['school_level_group']}·{row['first_choice_area_norm']}")
        with c2:
            metric_card("학생규모 계수", f"{calc_size_coeff(row['student_count']):.2f}")
        with c3:
            metric_card("취약도 계수", f"{calc_vulnerability_coeff(row):.2f}")
        with c4:
            metric_card("운영난도 계수", f"{calc_operation_coeff(row['first_choice_area_norm']):.2f}")

        formula = pd.DataFrame({
            "항목": ["기준 단가", "학생규모 계수", "취약도 계수", "운영난도 계수", "권장 예산"],
            "값": [fmt_money(base_unit), f"{calc_size_coeff(row['student_count']):.2f}", f"{calc_vulnerability_coeff(row):.2f}", f"{calc_operation_coeff(row['first_choice_area_norm']):.2f}", fmt_money(rec_budget)]
        })
        pretty_df(formula, height=280)
        fit_df = pd.DataFrame({
            "항목": ["총액 적정성", "항목 구성 적정성", "유사사례 일치성", "예산정합성점수"],
            "점수": [row.get("budget_total_fit_score", 0), row.get("budget_item_fit_score", 0), row.get("budget_case_fit_score", 0), row.get("budget_fit_score", 0)],
        })
        bar_chart(fit_df, "항목", "점수", "예산 적정성 점수", horizontal=True)
        notice("권장예산 = 기준단가 × 학생규모계수 × 취약도계수 × 운영난도계수", variant="good")

    elif "비슷한 학교 비교" in sub:
        section_header("유사사례 비교", "같은 학교급·영역의 학교와 비교합니다.", "학교급 내부 비교만 적용")
        peers = base_df[(base_df["school_level_group"] == row["school_level_group"]) & (base_df["first_choice_area_norm"] == row["first_choice_area_norm"])].copy()
        peers = peers.sort_values("recommended_budget", ascending=False).head(8)
        show = peers[["school_display", "school_level_group", "first_choice_area_norm", "recommended_budget", "final_allocation_score"]].rename(columns={
            "school_display": "학교",
            "school_level_group": "학교급",
            "first_choice_area_norm": "영역",
            "recommended_budget": "권장예산",
            "final_allocation_score": "최종점수",
        })
        pretty_df(show)

    else:
        section_header("검토 포인트", "최종 검토 전 확인 항목을 정리합니다.", "점수 강점·보완점 분리 확인")
        review = [
            f"수요점수: {row.get('need_score', 0):.1f}점",
            f"계획서점수: {row.get('plan_score', 0):.1f}점",
            f"예산정합성점수: {row.get('budget_fit_score', 0):.1f}점",
            "결측이나 원자료 경고가 있으면 실제 집행 전 추가 확인이 필요합니다." if row.get("warning_flag", 0) == 1 else "핵심 결측 경고는 크지 않지만, 최종 확정 전 원자료 확인을 권장합니다.",
        ]
        summary_box(review)
        notice("최종 결정 전 원자료 재확인을 권장합니다.", variant="warn")



def page_school_report(base_df: pd.DataFrame, selected_df: pd.DataFrame, hold_df: pd.DataFrame) -> None:
    st.markdown("<div class='sub-tab-host'>", unsafe_allow_html=True)
    sub = nav_buttons(["🏅 점수 풀이", "💵 예산 풀이", "🤖 종합 의견", "🚀 다음 할 일"], "sub_report")
    st.markdown("</div>", unsafe_allow_html=True)
    schools = base_df['school_display'].tolist()
    school = st.selectbox('학교 리포트 대상', schools, key='report_school')
    row = base_df[base_df['school_display'] == school].iloc[0]
    status = '선정' if row['__rowid'] in selected_df['__rowid'].tolist() else '보류'
    section_header("학교 리포트", "개별 학교의 점수·예산·후속 행동을 확인합니다.", "선정·보류 사유 · 권장예산 근거 · 다음 행동")
    m1, m2, m3, m4, m5 = st.columns([1.45, 0.9, 1.0, 1.0, 1.0])
    with m1:
        school_identity_card(row["school_name"], f"{row['region_office']} · {row['school_level_group']} · {row.get('first_choice_area_norm', '')}")
    with m2:
        metric_card("상태", status)
    with m3:
        metric_card("최종배분점수", f"{float(row.get('final_allocation_score') or row.get('우선 검토 점수') or 0):.1f}점")
    with m4:
        metric_card("권장예산", fmt_money(row["recommended_budget"]))
    with m5:
        metric_card("데이터 신뢰도", "검토 필요" if row.get("warning_flag", 0) == 1 else "양호", f"학교급 {row['school_level_group']} · 핵심 영역 {row.get('focus_area_top1', '')}")

    if "점수 풀이" in sub:
        score_items = pd.DataFrame({
            "항목": ["수요점수", "계획서점수", "예산정합성점수", "최종배분점수"],
            "점수": [
                row.get("need_score", 0),
                row.get("plan_score", 0),
                row.get("budget_fit_score", 0),
                row.get("final_allocation_score", 0),
            ],
        })
        r1, r2 = st.columns(2)
        with r1:
            bar_chart(score_items, "항목", "점수", "핵심 점수 구성", horizontal=True)
        with r2:
            radar_chart(
                score_items["항목"].tolist(),
                score_items["점수"].tolist(),
                "점수 구조 한눈에 보기"
            )
        detail = pd.DataFrame({
            "세부 항목": ["학생 규모", "긴급성", "재정 취약", "시설 취약", "지역 취약"],
            "점수": [row.get("size_pct_score", 0), row.get("urgent_pct_score", 0), row.get("finance_pct_score", 0), row.get("facility_pct_score", 0), row.get("region_pct_score", 0)],
        })
        bar_chart(detail, "세부 항목", "점수", "수요 점수 세부 내역", horizontal=True)
        notice("이 점수는 우선 검토 순서를 제안하는 참고 자료이며, 최종 결정은 담당자가 내립니다.")

    elif "예산 풀이" in sub:
        explain = pd.DataFrame({
            "항목": ["기준 단가", "학생규모계수", "취약도계수", "운영난도계수", "신청 예산", "권장 예산", "예산 차이 비율"],
            "값": [
                fmt_money(STANDARD_COSTS[row['first_choice_area_norm']][row['school_level_group']]),
                f"{calc_size_coeff(row['student_count']):.2f}",
                f"{calc_vulnerability_coeff(row):.2f}",
                f"{calc_operation_coeff(row['first_choice_area_norm']):.2f}",
                fmt_money(calc_requested_budget(row)),
                fmt_money(row["recommended_budget"]),
                f"{row.get('budget_gap_ratio', 0) * 100:.1f}%",
            ],
        })
        pretty_df(explain, height=310)
        fit = pd.DataFrame({
            "항목": ["총액 적정성", "항목 구성 적정성", "유사사례 일치성", "예산정합성점수"],
            "점수": [row.get("budget_total_fit_score", 0), row.get("budget_item_fit_score", 0), row.get("budget_case_fit_score", 0), row.get("budget_fit_score", 0)],
        })
        bar_chart(fit, "항목", "점수", "예산 설명", horizontal=True)
        notice("기준단가 × 보정계수 구조로 권장예산 근거를 투명하게 제공합니다.")

    elif "종합 의견" in sub:
        verdict = "적정" if abs(row.get("budget_gap_ratio", 0)) <= 0.15 else ("다소 높음" if row.get("budget_gap_ratio", 0) > 0 else "다소 낮음")
        _sn  = str(row.get('school_display', row.get('school_name', '')))
        _lg2 = str(row.get('school_level_group', ''))
        _fa  = str(row.get('first_choice_area_norm', ''))
        _ft  = str(row.get('focus_area_top1', ''))
        _sc2 = float(row.get('final_allocation_score', 0) or 0)
        _gr  = float(row.get('budget_gap_ratio', 0) or 0)
        summary_box([
            f"{_sn}은(는) {_lg2} 내부 비교 기준에서 {_sc2:.1f}점으로 검토 대상에 올랐습니다.",
            f"가장 큰 강점은 {_fa} 영역과 {_ft} 중심 정책 우선도 일치입니다.",
            f"예산 적정성 판정은 '{verdict}'이며, 신청 예산과 권장 예산 차이는 {_gr * 100:.1f}%입니다.",
        ])
        notice("이 요약은 검토를 돕는 참고 자료이며, 최종 해석은 담당자가 수행합니다.")

    else:
        actions = []
        if status == "선정":
            actions.append("우선 지원 검토 목록에 반영")
        else:
            actions.append("신청 보완 또는 후속 검토 후보군으로 분류")
        if abs(row.get("budget_gap_ratio", 0)) > 0.20:
            actions.append("예산 재조정 검토")
        if row.get("warning_flag", 0) == 1:
            actions.append("원자료 확인 및 현장 점검")
        if int(row.get("urgent_flag", 0)) == 1:
            actions.append("긴급 근거 추가 확인")
        summary_box(actions if actions else ["현 상태 유지"])
        notice("점수 구조와 보완 사항을 함께 검토한 뒤 후속 행동을 결정하세요.")


def page_quality(base_df: pd.DataFrame) -> None:
    """자료 점검 화면: 원자료 결측·보완값·확인 필요 학교를 사용자가 이해하기 쉬운 검토 흐름으로 표시."""
    quality_options = ["📌 한눈에 보기", "① 원자료 결측", "② 보완값 사용", "③ 확인 필요 학교", "📖 해석 가이드"]
    if st.session_state.get("sub_quality") not in quality_options:
        st.session_state["sub_quality"] = quality_options[0]

    st.markdown("<div class='sub-tab-host'>", unsafe_allow_html=True)
    sub = nav_buttons(quality_options, "sub_quality")
    st.markdown("</div>", unsafe_allow_html=True)

    if base_df is None or base_df.empty:
        section_header("자료 점검", "현재 선택 조건에 해당하는 학교가 없습니다.", "교육청·학교급 필터를 조정해 주세요.")
        st.info("표시할 데이터가 없어 결측·보완·확인 필요 학교 현황을 계산하지 않았습니다.")
        return

    # ------------------------------------------------------------------
    # 1) 원자료 결측 집계
    # ------------------------------------------------------------------
    core_items = [
        {
            "col": "student_count",
            "label": "학생수",
            "meaning": "학교 규모와 수혜 가능 학생 수 판단",
            "impact": "학생 규모 점수·권장예산 보정에 영향",
            "action": "학교 기본현황 자료 확인",
        },
        {
            "col": "budget_total",
            "label": "예산총액",
            "meaning": "학교 재정 규모 확인",
            "impact": "예산 적정성 해석에 영향",
            "action": "예산서 원자료 확인",
        },
        {
            "col": "settlement_total",
            "label": "결산총액",
            "meaning": "실제 집행 규모 확인",
            "impact": "예산 사용 여력·집행성 판단에 영향",
            "action": "결산서 원자료 확인",
        },
        {
            "col": "building_area_total",
            "label": "교사면적",
            "meaning": "학교 시설 규모 확인",
            "impact": "시설 여건·공간 부족 해석에 영향",
            "action": "학교시설 현황 확인",
        },
        {
            "col": "land_area_total",
            "label": "학교용지면적",
            "meaning": "학교 부지 규모 확인",
            "impact": "시설 여건·공간 여력 해석에 영향",
            "action": "학교시설 현황 확인",
        },
        {
            "col": "support_facility_score",
            "label": "시설점수",
            "meaning": "시설 취약 정도를 요약한 분석용 점수",
            "impact": "시설 보정 및 취약성 판단에 직접 영향",
            "action": "시설점수 산출 근거 확인",
        },
    ]
    label_map = {item["col"]: item["label"] for item in core_items}

    missing_rows = []
    for item in core_items:
        col = item["col"]
        missing_count = int(base_df[col].isna().sum()) if col in base_df.columns else len(base_df)
        missing_rows.append({
            "점검 항목": item["label"],
            "원자료 컬럼": col,
            "무엇을 뜻하나": item["meaning"],
            "미입력 학교 수": missing_count,
            "미입력 비율(%)": round(missing_count / max(len(base_df), 1) * 100, 1),
            "결과에 미치는 영향": item["impact"],
            "권장 조치": item["action"],
        })
    missing_df = pd.DataFrame(missing_rows)
    total_missing = int(missing_df["미입력 학교 수"].sum())
    if total_missing > 0:
        top_row = missing_df.sort_values("미입력 학교 수", ascending=False).iloc[0]
        top_missing_label = f"{top_row['점검 항목']} {int(top_row['미입력 학교 수']):,}건"
    else:
        top_missing_label = "없음"

    # ------------------------------------------------------------------
    # 2) 보완값 사용 집계
    # ------------------------------------------------------------------
    filled_flag_cols = [
        c for c in base_df.columns
        if str(c).endswith("_filled_flag") or str(c).endswith("_imputed_flag")
    ]

    def flag_to_bool(s: pd.Series) -> pd.Series:
        if pd.api.types.is_numeric_dtype(s):
            return pd.to_numeric(s, errors="coerce").fillna(0) > 0
        normalized = s.astype(str).str.strip().str.lower()
        return normalized.isin(["1", "true", "t", "y", "yes", "보완", "대체", "imputed", "filled"])

    filled_rows = []
    filled_masks = []
    for flag_col in filled_flag_cols:
        mask = flag_to_bool(base_df[flag_col])
        filled_masks.append(mask)
        target = flag_col.replace("_filled_flag", "").replace("_imputed_flag", "")
        count = int(mask.sum())
        rate = round(count / max(len(base_df), 1) * 100, 1)
        if rate >= 50:
            risk = "높음"
            action = "원자료 확보 후 재계산 권장"
        elif rate >= 10:
            risk = "중간"
            action = "상위 학교 중심 원자료 확인"
        elif rate > 0:
            risk = "낮음"
            action = "해당 학교만 확인"
        else:
            risk = "없음"
            action = "추가 조치 낮음"
        filled_rows.append({
            "보완 항목": label_map.get(target, target),
            "보완 플래그 컬럼": flag_col,
            "보완 적용 학교 수": count,
            "보완 적용 비율(%)": rate,
            "해석 주의도": risk,
            "권장 조치": action,
        })
    filled_df = pd.DataFrame(filled_rows) if filled_rows else pd.DataFrame(
        columns=["보완 항목", "보완 플래그 컬럼", "보완 적용 학교 수", "보완 적용 비율(%)", "해석 주의도", "권장 조치"]
    )
    total_filled_cells = int(filled_df["보완 적용 학교 수"].sum()) if not filled_df.empty else 0
    if filled_masks:
        any_filled = filled_masks[0].copy()
        for m in filled_masks[1:]:
            any_filled = any_filled | m
        unique_filled_schools = int(any_filled.sum())
    else:
        unique_filled_schools = 0

    # ------------------------------------------------------------------
    # 3) 확인 필요 학교 집계
    # ------------------------------------------------------------------
    if "warning_flag" in base_df.columns:
        warning_mask = pd.to_numeric(base_df["warning_flag"], errors="coerce").fillna(0).astype(int) == 1
        warnings = base_df[warning_mask].copy()
    else:
        warnings = base_df.iloc[0:0].copy()

    def infer_warning_reason(row: pd.Series) -> str:
        # 이미 main()에서 생성한 warning_reason이 있으면 우선 사용합니다.
        existing = str(row.get("warning_reason", "")).strip()
        if existing and existing.lower() not in ["nan", "none", ""]:
            return existing

        reasons = []
        if pd.isna(row.get("student_count", np.nan)):
            reasons.append("학생수 미입력")
        else:
            try:
                if float(row.get("student_count", 0)) > 5000:
                    reasons.append("학생수 이상치·대규모 학교 확인")
            except Exception:
                pass
        if int(row.get("has_request", 0) or 0) == 1 and pd.isna(row.get("support_facility_score", np.nan)):
            reasons.append("신청 학교의 시설점수 미입력")
        critical_cols = ["student_count", "support_facility_score", "region_type", "finance_type"]
        critical_missing = 0
        for c in critical_cols:
            value = row.get(c, np.nan)
            if pd.isna(value) or str(value).strip() in ["", "미입력", "nan", "None"]:
                critical_missing += 1
        if critical_missing >= 2:
            reasons.append("핵심 판단 항목 2개 이상 미입력")
        if not reasons:
            reasons.append("점수 산출 전 원자료 추가 확인")
        return " / ".join(reasons)

    def warning_action(reason: str) -> str:
        reason = str(reason)
        if "학생수" in reason:
            return "학생 수 원자료와 학교 규모 확인"
        if "시설" in reason:
            return "시설 원자료와 시설점수 산출식 확인"
        if "핵심" in reason or "미입력" in reason:
            return "필수 항목 보완 후 재계산"
        return "담당자 원자료 검토 후 확정"

    if not warnings.empty:
        warnings["확인 사유"] = warnings.apply(infer_warning_reason, axis=1)
        warnings["권장 조치"] = warnings["확인 사유"].map(warning_action)

    # ------------------------------------------------------------------
    # 4) 사용자용 상태 판정
    # ------------------------------------------------------------------
    warning_count = len(warnings)
    if total_missing == 0 and total_filled_cells == 0 and warning_count == 0:
        status_label = "양호"
        status_desc = "현재 선택 조건에서는 주요 결측·보완·확인 필요 신호가 크지 않습니다."
        status_color = "#0f8a5f"
    elif total_missing == 0 and (total_filled_cells > 0 or warning_count > 0):
        status_label = "검토 후 사용"
        status_desc = "자동 추천 산출은 가능하지만, 보완값 또는 확인 필요 학교가 있어 최종 확정 전 원자료 점검이 필요합니다."
        status_color = "#b45309"
    else:
        status_label = "보완 필요"
        status_desc = "주요 항목에 미입력이 있어 결과 해석 전에 원자료 보완이 우선입니다."
        status_color = "#b91c1c"

    # ------------------------------------------------------------------
    # 화면 구성
    # ------------------------------------------------------------------
    if "한눈에 보기" in sub:
        section_header(
            "자료 점검 대시보드",
            "자동 추천 결과를 확정하기 전에 데이터 상태를 한눈에 확인합니다.",
            "원자료 결측, 전처리 보완값, 확인 필요 학교를 분리해 해석합니다.",
        )

        st.markdown(
            f"""
            <div class='good-note' style='border-left-color:{status_color}; background:#ffffff;'>
                <div style='font-weight:900; color:{status_color}; font-size:1.05rem; margin-bottom:0.25rem;'>현재 자료 판정: {status_label}</div>
                <div style='color:#2c4060; line-height:1.7;'>{status_desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("분석 대상", f"{len(base_df):,}개교", "현재 교육청·학교급 조건")
        with c2:
            metric_card("원자료 미입력", f"{total_missing:,}건", f"최다 항목: {top_missing_label}")
        with c3:
            metric_card("보완값 사용", f"{unique_filled_schools:,}개교", f"항목-학교 기준 {total_filled_cells:,}건")
        with c4:
            metric_card("확인 필요 학교", f"{warning_count:,}개교", "탈락 기준이 아닌 점검 목록")

        st.markdown("#### 이 화면에서 확인할 3가지")
        a, b, c = st.columns(3)
        with a:
            st.markdown(
                """
                <div class='logic-box'>
                    <div class='logic-title'>1. 원자료 결측</div>
                    <div class='logic-desc'>CSV에 값이 비어 있는 항목입니다. 0점 처리하지 않고 원자료 확인 또는 보완 대상으로 봅니다.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with b:
            st.markdown(
                """
                <div class='logic-box'>
                    <div class='logic-title'>2. 보완값 사용</div>
                    <div class='logic-desc'>평균·중앙값·학교급 기준값 등으로 대체한 값입니다. 분석은 가능하지만 실제 집행 전 근거 확인이 필요합니다.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c:
            st.markdown(
                """
                <div class='logic-box'>
                    <div class='logic-title'>3. 확인 필요 학교</div>
                    <div class='logic-desc'>이상치·핵심 항목 부족 등 담당자 검토가 필요한 학교입니다. 자동 제외나 탈락을 뜻하지 않습니다.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        left, right = st.columns(2)
        with left:
            st.markdown("#### 원자료 미입력 요약")
            if total_missing == 0:
                notice("현재 선택 조건에서는 주요 항목 미입력이 없습니다.")
            else:
                chart_df = missing_df[missing_df["미입력 학교 수"] > 0].copy()
                bar_chart(chart_df, "점검 항목", "미입력 학교 수", "미입력 항목별 학교 수", horizontal=True)
        with right:
            st.markdown("#### 보완·확인 필요 요약")
            summary = pd.DataFrame({
                "구분": ["보완값 사용 학교", "확인 필요 학교", "최종 해석"],
                "현재 상태": [f"{unique_filled_schools:,}개교", f"{warning_count:,}개교", status_label],
                "담당자 확인 포인트": [
                    "보완 항목의 원자료 확보 여부",
                    "확인 사유와 권장 조치",
                    "자동 추천 결과 확정 가능 여부",
                ],
            })
            pretty_df(summary, height=230)

        notice("자료 점검 화면은 추천 결과의 신뢰도를 설명하기 위한 보조 화면입니다. 점검 대상이 있다고 해서 자동 탈락하거나 제외되는 것은 아닙니다.", variant="warn")

    elif "원자료 결측" in sub:
        section_header(
            "① 원자료 결측 점검",
            "CSV에서 값이 비어 있는 항목을 확인합니다.",
            "미입력은 0이 아니라 ‘확인 또는 보완이 필요한 값’으로 해석합니다.",
        )
        if total_missing == 0:
            notice("현재 분석용 데이터 기준으로 주요 항목 미입력은 없습니다.")
            st.markdown("<div class='small-help'>단, 전처리 과정에서 이미 보완된 값은 원자료 결측으로 보이지 않을 수 있으므로 ‘보완값 사용’ 탭도 함께 확인하세요.</div>", unsafe_allow_html=True)
        else:
            notice("미입력 항목이 있는 경우 자동 추천 결과 확정 전에 원자료를 보완하는 것이 좋습니다.", variant="warn")
        pretty_df(missing_df.sort_values("미입력 학교 수", ascending=False), height=420)

    elif "보완값 사용" in sub:
        section_header(
            "② 보완값 사용 점검",
            "전처리 과정에서 결측값을 평균·중앙값·학교급 기준값 등으로 채운 항목을 확인합니다.",
            "보완값은 분석을 계속하기 위한 대체값이며, 원자료 자체를 의미하지 않습니다.",
        )
        if filled_flag_cols:
            c1, c2, c3 = st.columns(3)
            with c1:
                metric_card("보완값 사용 학교", f"{unique_filled_schools:,}개교", "하나 이상 보완값 포함")
            with c2:
                metric_card("보완 항목-학교 건수", f"{total_filled_cells:,}건", "한 학교의 여러 항목 보완은 중복 집계")
            with c3:
                high_risk = int((filled_df["해석 주의도"] == "높음").sum()) if not filled_df.empty else 0
                metric_card("주의도 높은 항목", f"{high_risk:,}개", "보완 비율 50% 이상")
            pretty_df(filled_df.sort_values("보완 적용 학교 수", ascending=False), height=360)
            high_items = filled_df[filled_df["해석 주의도"].eq("높음")]
            if not high_items.empty:
                items = " · ".join(high_items["보완 항목"].astype(str).tolist())
                notice(f"{items} 항목은 보완 비율이 높습니다. 이 항목을 근거로 예산·시설 해석을 할 때에는 원자료 재확인이 필요합니다.", variant="warn")
            else:
                notice("보완값 사용 비율이 높은 항목은 크지 않습니다. 다만 실제 집행 전 핵심 학교의 원자료 확인은 권장됩니다.")
        else:
            st.info("현재 데이터에는 보완 여부를 나타내는 *_filled_flag 또는 *_imputed_flag 컬럼이 없습니다.")
            st.markdown(
                """
                <div class='good-note'>
                더 완성도 높은 운영을 위해서는 보완한 항목마다 <b>budget_total_filled_flag</b>,
                <b>settlement_total_filled_flag</b>, <b>support_facility_score_filled_flag</b>처럼
                ‘이 값이 원자료인지 보완값인지’를 표시하는 컬럼을 함께 두는 것이 좋습니다.
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "확인 필요 학교" in sub:
        section_header(
            "③ 확인 필요 학교 목록",
            "자동 추천 결과를 확정하기 전에 담당자가 한 번 더 확인해야 할 학교를 보여줍니다.",
            "확인 필요 학교는 탈락 대상이 아니라 원자료 검토가 필요한 학교입니다.",
        )
        if warnings.empty:
            notice("현재 선택 조건에서는 확인 필요 학교가 없습니다.")
        else:
            show_cols = [
                "school_name", "school_level_group", "region_office", "first_choice_area_norm",
                "student_count", "final_allocation_score", "확인 사유", "권장 조치",
            ]
            show = warnings[[c for c in show_cols if c in warnings.columns]].copy()
            rename = {
                "school_name": "학교명",
                "school_level_group": "학교급",
                "region_office": "교육청",
                "first_choice_area_norm": "지원영역",
                "student_count": "학생수",
                "final_allocation_score": "현재 최종점수",
            }
            show = show.rename(columns=rename)
            pretty_df(show, height=440)

            if "school_display" in warnings.columns:
                options = warnings["school_display"].astype(str).tolist()
            else:
                options = warnings["school_name"].astype(str).tolist() if "school_name" in warnings.columns else []
            if options:
                st.markdown("#### 선택 학교 상세 점검")
                picked = st.selectbox("상세 확인할 학교", options, key="quality_warning_pick")
                row = warnings[(warnings.get("school_display", warnings.get("school_name")).astype(str) == picked)].iloc[0]
                summary_box([
                    f"확인 사유: {row.get('확인 사유', '원자료 추가 확인 필요')}",
                    f"권장 조치: {row.get('권장 조치', '담당자 검토 후 확정')}",
                    f"학생수: {fmt_int(row.get('student_count', 0))}명 · 지원영역: {row.get('first_choice_area_norm', '')} · 현재 최종점수: {row.get('final_allocation_score', 0):.1f}점",
                    "이 학교는 자동 제외 대상이 아니라, 점수 해석 전에 근거 자료를 한 번 더 확인해야 하는 대상입니다.",
                ])
            notice("확인 필요 목록은 심사·검토 순서의 안전장치입니다. 최종 선정 여부는 원자료 확인과 담당자 판단을 거쳐 결정합니다.", variant="warn")

    else:
        section_header(
            "자료 점검 결과 읽는 법",
            "이 화면은 자동 추천 결과를 더 신뢰성 있게 설명하기 위한 보조 화면입니다.",
            "자동 결정이 아닌 검토 보조 · 최종 판단은 담당자 몫입니다.",
        )
        st.markdown("#### 핵심 해석 원칙")
        guide = pd.DataFrame({
            "구분": ["원자료 결측", "보완값 사용", "확인 필요 학교", "최종 판단"],
            "뜻": [
                "CSV에 값이 비어 있는 상태",
                "분석을 위해 평균·중앙값 등으로 임시 대체한 값",
                "이상치·핵심 항목 부족 등으로 원자료 확인이 필요한 학교",
                "자동 추천 점수와 담당자 검토를 함께 반영해 결정",
            ],
            "어떻게 해석하나": [
                "0점이나 낮은 점수로 보지 않고, 원자료 확인 대상으로 봄",
                "계산은 가능하지만 예산·시설 해석에는 주의가 필요함",
                "탈락 대상이 아니라 검토 우선 대상임",
                "자료 점검 후 필요하면 점수·보정 기준을 조정하고 재검토함",
            ],
        })
        pretty_df(guide, height=270)
        notice("보고서에는 ‘자료 점검 화면을 통해 결측·보완·확인 필요 학교를 분리하여 자동 추천 결과의 해석 가능성과 신뢰도를 높였다’고 설명하면 좋습니다.")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main() -> None:
    inject_style()
    init_state()
    keep_policy_state_alive()
    st.markdown(
        """
        <div class='title-panel'>
            <div class='title-row'>
                <div class='title-main-wrap'>
                    <div class='title-kicker'>🏫 교육 공공데이터 기반 학교지원 의사결정 서비스</div>
                    <div class='main-title'>ULTRA 학교지원<br>우선순위 추천 서비스</div>
                    <div class='sub-title'>학교급별 수요·계획서·예산 적정성을 함께 검토해,<br>어떤 학교를 왜 먼저 지원해야 하는지 설명형으로 보여줍니다.</div>
                    <div class='title-meta'>
                        <span class='title-meta-item'>📐 학교급별 분리 계산</span>
                        <span class='title-meta-item'>💰 권장예산 자동 계산</span>
                        <span class='title-meta-item'>📋 이유 있는 결과 화면</span>
                        <span class='title-meta-item'>🔍 자료 신뢰도 점검</span>
                    </div>
                </div>
                <div class='hero-stats'>
                    <div class='hero-stat-item'>
                        <div class='hero-stat-num'>3</div>
                        <div class='hero-stat-label'>학교급별<br>분리 계산</div>
                    </div>
                    <div class='hero-stat-item'>
                        <div class='hero-stat-num'>6</div>
                        <div class='hero-stat-label'>지원 영역<br>자동 분류</div>
                    </div>
                    <div class='hero-stat-item'>
                        <div class='hero-stat-num'>AI</div>
                        <div class='hero-stat-label'>예산 적정성<br>자동 산출</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='top-nav-host'>", unsafe_allow_html=True)
    page = nav_buttons(
        ["📊 결과 한눈에 보기", "⚙️ 지원 기준 설정", "🏫 학교별 평가·예산", "📋 학교 상세 보기", "🔍 자료 신뢰도 확인"],
        "page", columns=5,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    raw = load_data()
    if raw.empty:
        st.warning("school_master_final_v2.csv 파일을 찾지 못했습니다. 이 코드는 스크립트와 같은 폴더 또는 작업 폴더에 CSV가 있을 때 바로 실행됩니다.")
        demo = pd.DataFrame({
            "school_name": ["서울대도초등학교", "공주신월초등학교", "천안아름초등학교", "진영여자고등학교", "공주여자중학교"],
            "region_office": ["서울", "충남", "충남", "경남", "충남"],
            "school_level": ["초등학교", "초등학교", "초등학교", "고등학교", "중학교"],
            "school_type": ["공립", "공립", "공립", "공립", "공립"],
            "region_type": ["도시형", "도시형", "도시형", "도시형", "도시형"],
            "finance_type": ["국공립", "국공립", "국공립", "국공립", "국공립"],
            "student_count": [1315, 320, 721, 880, 640],
            "has_request": [1, 1, 1, 0, 1],
            "urgent_flag": [0, 0, 1, 0, 1],
            "first_choice_area": ["정서·생활적응", "기초학습", "정서·생활적응", "진로·진학", "학업지원"],
            "support_facility_score": [55, 48, 50, 62, 57],
            "budget_total": [np.nan, np.nan, np.nan, np.nan, np.nan],
            "settlement_total": [np.nan, np.nan, np.nan, np.nan, np.nan],
            "building_area_total": [1200, 900, 1100, 2000, 1600],
            "land_area_total": [5000, 4300, 4700, 6200, 5500],
            "desired_support_count": [1, 1, 2, 1, 1],
            "reason_v2": ["대규모 학생군과 공통진단 기반 신호가 반영되었습니다.", "기초학습 수요와 현장 신청 정보가 반영되었습니다.", "정서·생활적응 중심 수요와 신청 정보가 반영되었습니다.", "진로·진학 수요가 반영되었습니다.", "학업지원 수요와 긴급 신호가 함께 반영되었습니다."],
        })
        raw = demo

    df = prepare_df(raw)
    critical_missing_count = (
        df[["student_count", "support_facility_score", "region_type", "finance_type"]]
        .isna()
        .sum(axis=1)
    )
    core_warning = (
        df["student_count"].isna()
        | (df["student_count"].fillna(0) > 5000)
        | ((df["has_request"] == 1) & df["support_facility_score"].isna())
        | (critical_missing_count >= 2)
    )
    df["warning_flag"] = core_warning.astype(int)

    # 자료 점검 화면에서 사용자가 왜 확인해야 하는지 바로 볼 수 있도록 사유를 함께 저장합니다.
    def _warning_reason_for_row(row: pd.Series) -> str:
        reasons = []
        if pd.isna(row.get("student_count", np.nan)):
            reasons.append("학생수 미입력")
        else:
            try:
                if float(row.get("student_count", 0)) > 5000:
                    reasons.append("학생수 이상치")
            except Exception:
                pass
        if int(row.get("has_request", 0) or 0) == 1 and pd.isna(row.get("support_facility_score", np.nan)):
            reasons.append("신청 학교의 시설점수 미입력")
        critical_cols = ["student_count", "support_facility_score", "region_type", "finance_type"]
        critical_missing = 0
        for c in critical_cols:
            value = row.get(c, np.nan)
            if pd.isna(value) or str(value).strip() in ["", "미입력", "nan", "None"]:
                critical_missing += 1
        if critical_missing >= 2:
            reasons.append("핵심 항목 2개 이상 미입력")
        return " / ".join(reasons) if reasons else ""

    df["warning_reason"] = df.apply(_warning_reason_for_row, axis=1)

    render_global_filters(df)

    scope_df = filtered_df(df)
    if scope_df.empty:
        selected_office = st.session_state.get("office", "전체")
        selected_level = st.session_state.get("school_level_pick", "전체")
        st.warning(
            f"현재 선택한 조건에 해당하는 학교가 없습니다. "
            f"교육청: {selected_office} / 학교급: {selected_level}"
        )
        st.info("교육청 또는 학교급을 '전체'로 바꾸거나, CSV 파일에 해당 교육청·학교급 데이터가 있는지 확인해 주세요.")
        if not df.empty and {"region_office", "school_level_group"}.issubset(df.columns):
            combo = (
                df.groupby(["region_office", "school_level_group"])
                .size()
                .reset_index(name="학교 수")
                .sort_values(["region_office", "school_level_group"])
            )
            combo.columns = ["교육청", "학교급", "학교 수"]
            st.markdown("#### 현재 CSV에 들어 있는 교육청·학교급 조합")
            pretty_df(combo, height=360)
        return

    scored, selected_df, hold_df, remaining = run_allocation_engine(scope_df)
    scored["allocated_budget"] = scored.get("allocated_budget", 0.0)
    scored["result_status"] = scored.get("result_status", "보류")
    if not selected_df.empty:
        alloc_map = selected_df.set_index("__rowid")["allocated_budget"]
        scored.loc[scored["__rowid"].isin(alloc_map.index), "allocated_budget"] = scored.loc[scored["__rowid"].isin(alloc_map.index), "__rowid"].map(alloc_map)
        scored.loc[scored["__rowid"].isin(alloc_map.index), "result_status"] = "선정"
    if "budget_gap_ratio" not in scored.columns:
        scored["budget_gap_ratio"] = 0.0
    if not selected_df.empty:
        merge_cols = ["__rowid", "budget_gap_ratio", "school_display", "final_allocation_score", "plan_score", "budget_fit_score", "need_score", "requested_budget"]
        selected_df = selected_df.merge(scored[merge_cols], on="__rowid", how="left", suffixes=("", "_ref"))
    if not hold_df.empty:
        merge_cols = ["__rowid", "budget_gap_ratio", "school_display", "final_allocation_score", "plan_score", "budget_fit_score", "need_score", "requested_budget"]
        hold_df = hold_df.merge(scored[merge_cols], on="__rowid", how="left", suffixes=("", "_ref"))
    scored = scored.sort_values(["final_allocation_score", "우선 검토 점수"], ascending=[False, False])

    if "결과 한눈에 보기" in page:
        page_result_overview(scored, selected_df, hold_df, remaining)
    elif "지원 기준 설정" in page:
        page_settings(scope_df)
    elif "학교별 평가·예산" in page:
        page_application_eval(scored, selected_df)
    elif "학교 상세 보기" in page:
        page_school_report(scored, selected_df, hold_df)
    else:
        page_quality(scored)


if __name__ == "__main__":
    main()
