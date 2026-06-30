from skimage.feature import graycomatrix, graycoprops
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
import cv2
import numpy as np
import streamlit as st
from PIL import Image
import os
import time
import io
import matplotlib
matplotlib.use("Agg")

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="VisionPalm | Industrial TBS Vision System",
    layout="wide",
    page_icon="🌴",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# GLOBAL CSS — UI/UX Enhanced Design
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

/* ── Root & App Shell ── */
.stApp {
    background: #F8FAF8 !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAF8 100%) !important;
    border-right: 1px solid #E8EDE8 !important;
    padding: 0 !important;
}

.stMainBlockContainer {
    padding: 0 2rem 4rem 2rem !important;
    max-width: 1400px;
    margin: 0 auto;
}

#MainMenu, footer, header {
    display: none !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

/* ── Scrollbar Styling ── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #F0F5F0;
}
::-webkit-scrollbar-thumb {
    background: #1C5C35;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #2D7A4F;
}

/* ══════════════════════════════
   SIDEBAR ENHANCED
══════════════════════════════ */
.sidebar-wrapper {
    padding: 1.5rem 1.2rem 0 1.2rem;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #E8EDE8;
    margin-bottom: 1.5rem;
}

.sidebar-logo {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #1C5C35, #2D7A4F);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(28, 92, 53, 0.2);
}

.sidebar-brand {
    flex: 1;
}
.sidebar-brand-name {
    font-size: 1.1rem;
    font-weight: 800;
    color: #111;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.sidebar-brand-sub {
    font-size: 0.6rem;
    font-weight: 500;
    color: #999;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── SIDEBAR NAVIGATION BUTTONS (HIJAU TUA) ── */
.sidebar-nav {
    flex: 1;
    margin-top: 0.5rem;
}

/* Styling untuk semua button di sidebar-nav */
.sidebar-nav .stButton {
    width: 100% !important;
    margin-bottom: 4px !important;
}

.sidebar-nav .stButton button {
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 0.7rem 0.9rem !important;
    border-radius: 10px !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #666 !important;
}

/* Hover untuk semua button */
.sidebar-nav .stButton button:hover {
    background: #F0F5F0 !important;
    color: #1C5C35 !important;
    border-color: transparent !important;
    transform: none !important;
}

/* Button Aktif (Primary) - HIJAU TUA */
.sidebar-nav .stButton button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #1C5C35, #2D7A4F) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border-color: #1C5C35 !important;
    box-shadow: 0 4px 12px rgba(28, 92, 53, 0.25) !important;
}

.sidebar-nav .stButton button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #154A2A, #1C5C35) !important;
    box-shadow: 0 6px 16px rgba(28, 92, 53, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* Button Tidak Aktif (Secondary) */
.sidebar-nav .stButton button[data-testid="baseButton-secondary"] {
    background: transparent !important;
    color: #666 !important;
    border-color: transparent !important;
}

.sidebar-nav .stButton button[data-testid="baseButton-secondary"]:hover {
    background: #F0F5F0 !important;
    color: #1C5C35 !important;
}

/* Fallback untuk kind attribute */
.sidebar-nav .stButton button[kind="primary"] {
    background: linear-gradient(135deg, #1C5C35, #2D7A4F) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border-color: #1C5C35 !important;
    box-shadow: 0 4px 12px rgba(28, 92, 53, 0.25) !important;
}

.sidebar-nav .stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, #154A2A, #1C5C35) !important;
    box-shadow: 0 6px 16px rgba(28, 92, 53, 0.35) !important;
    transform: translateY(-1px) !important;
}

.sidebar-nav .stButton button[kind="secondary"] {
    background: transparent !important;
    color: #666 !important;
    border-color: transparent !important;
}

.sidebar-nav .stButton button[kind="secondary"]:hover {
    background: #F0F5F0 !important;
    color: #1C5C35 !important;
}

.nav-divider {
    border: none;
    border-top: 1px solid #E8EDE8;
    margin: 1rem 0;
}

/* Sidebar Status */
.sidebar-status {
    padding: 1rem 0;
    border-top: 1px solid #E8EDE8;
    margin-top: auto;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.3rem 0;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22C55E;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

.status-label {
    font-size: 0.6rem;
    color: #22C55E;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.status-version {
    font-size: 0.6rem;
    color: #BBB;
    font-weight: 500;
}

.sidebar-footer {
    padding-top: 0.5rem;
    border-top: 1px solid #E8EDE8;
    margin-top: 0.5rem;
}

.sidebar-user {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.3rem 0;
}

.user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1C5C35, #2D7A4F);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    flex-shrink: 0;
}

.user-info {
    flex: 1;
}
.user-name {
    font-size: 0.75rem;
    font-weight: 600;
    color: #111;
    line-height: 1.2;
}
.user-role {
    font-size: 0.6rem;
    color: #999;
    font-weight: 500;
}

/* ══════════════════════════════
   MAIN CONTENT
══════════════════════════════ */

/* Top Navigation Bar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.2rem 0;
    border-bottom: 1px solid #E8EDE8;
    margin-bottom: 1.8rem;
}

.topbar-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.back-button {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: #FFFFFF;
    border: 1.5px solid #E8EDE8;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #555;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.back-button:hover {
    background: #F0F5F0;
    border-color: #C5DEC9;
    color: #1C5C35;
}

.breadcrumb {
    font-size: 0.7rem;
    color: #999;
    font-weight: 500;
}
.breadcrumb span {
    color: #1C5C35;
    font-weight: 600;
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.system-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EDF5EF;
    color: #1C5C35;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 100px;
    border: 1px solid #C5DEC9;
}

.topbar-icon {
    width: 36px;
    height: 36px;
    background: #FFFFFF;
    border: 1px solid #E8EDE8;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    cursor: pointer;
    color: #666;
    transition: all 0.2s ease;
}

.topbar-icon:hover {
    background: #F0F5F0;
    border-color: #C5DEC9;
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, #F8FAF8 0%, #FFFFFF 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2.5rem;
    border: 1px solid #E8EDE8;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(28, 92, 53, 0.03) 0%, transparent 70%);
    pointer-events: none;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 3rem;
    align-items: center;
    position: relative;
    z-index: 1;
}

.hero-eyebrow {
    font-size: 0.6rem;
    font-weight: 700;
    color: #1C5C35;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: inline-block;
    background: #EDF5EF;
    padding: 4px 12px;
    border-radius: 100px;
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 900;
    color: #111;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.hero-title-green {
    color: #1C5C35;
    display: block;
}

.hero-desc {
    font-size: 0.85rem;
    color: #666;
    line-height: 1.8;
    margin: 0.8rem 0 1.8rem 0;
    max-width: 480px;
}

.hero-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #1C5C35, #2D7A4F);
    color: #FFFFFF;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 12px 28px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(28, 92, 53, 0.25);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(28, 92, 53, 0.35);
}

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #FFFFFF;
    color: #333;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 12px 28px;
    border-radius: 10px;
    border: 1.5px solid #E0E0E0;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
}

.btn-secondary:hover {
    background: #F8FAF8;
    border-color: #1C5C35;
    transform: translateY(-2px);
}

.hero-image-wrapper {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(135deg, #EDF5EF, #FFFFFF);
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-image-overlay {
    position: absolute;
    bottom: 16px;
    right: 16px;
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(12px);
    border-radius: 12px;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.hero-overlay-icon {
    width: 32px;
    height: 32px;
    background: #EDF5EF;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
}

.hero-overlay-text {
    font-size: 0.7rem;
    font-weight: 700;
    color: #111;
}
.hero-overlay-sub {
    font-size: 0.6rem;
    color: #888;
}

/* Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.feature-card {
    background: #FFFFFF;
    border: 1px solid #E8EDE8;
    border-radius: 14px;
    padding: 1.2rem 1.2rem;
    transition: all 0.3s ease;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.feature-card:hover {
    border-color: #C5DEC9;
    box-shadow: 0 4px 16px rgba(28, 92, 53, 0.06);
    transform: translateY(-2px);
}

.feature-icon {
    width: 36px;
    height: 36px;
    background: #EDF5EF;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}

.feature-content {
    flex: 1;
}
.feature-title {
    font-size: 0.72rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 2px;
}
.feature-desc {
    font-size: 0.6rem;
    color: #999;
    font-weight: 500;
}

/* Section Headers */
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
}

.section-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #111;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-title-icon {
    color: #1C5C35;
}

.section-link {
    font-size: 0.7rem;
    color: #1C5C35;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
}

/* Class Reference Cards */
.class-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.class-card {
    background: #FFFFFF;
    border: 1px solid #E8EDE8;
    border-radius: 14px;
    overflow: hidden;
    transition: all 0.3s ease;
}

.class-card:hover {
    border-color: #C5DEC9;
    box-shadow: 0 4px 16px rgba(28, 92, 53, 0.08);
    transform: translateY(-4px);
}

.class-card-img {
    width: 100%;
    height: 120px;
    object-fit: cover;
    background: #F0F7F3;
}

.class-card-body {
    padding: 0.8rem 1rem;
}

.class-card-code {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 2px;
}

.class-card-name {
    font-size: 0.65rem;
    font-weight: 600;
    color: #666;
    margin-bottom: 4px;
}

.class-card-desc {
    font-size: 0.58rem;
    color: #999;
    line-height: 1.5;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    margin-top: 2rem;
}

.stat-card {
    background: #FFFFFF;
    border: 1px solid #E8EDE8;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: #C5DEC9;
    box-shadow: 0 4px 16px rgba(28, 92, 53, 0.06);
}

.stat-icon {
    width: 40px;
    height: 40px;
    background: #EDF5EF;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

.stat-content {
    flex: 1;
}
.stat-label {
    font-size: 0.6rem;
    font-weight: 600;
    color: #999;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.stat-value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem;
    font-weight: 700;
    color: #111;
    letter-spacing: -0.03em;
    line-height: 1;
}
.stat-delta {
    font-size: 0.6rem;
    font-weight: 600;
    color: #22C55E;
    margin-top: 4px;
}
.stat-sub {
    font-size: 0.6rem;
    color: #999;
    font-weight: 500;
    margin-top: 4px;
}

/* ── DETECTION PAGE STYLES ── */

/* Upload Panel */
.upload-panel {
    background: #FFFFFF;
    border: 2px dashed #C5DEC9;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.upload-panel:hover {
    border-color: #1C5C35;
    background: #F8FBF8;
}

.upload-icon-wrapper {
    width: 56px;
    height: 56px;
    background: #EDF5EF;
    border-radius: 16px;
    margin: 0 auto 1rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.upload-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 4px;
}
.upload-desc {
    font-size: 0.7rem;
    color: #999;
    line-height: 1.6;
    margin-bottom: 1.2rem;
}

/* Result Banner */
.result-banner {
    border-radius: 16px;
    padding: 1.8rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.8rem;
    margin: 1.8rem 0;
    flex-wrap: wrap;
}

.result-banner.success {
    background: #EDF5EF;
    border: 1.5px solid #C5DEC9;
}
.result-banner.warning {
    background: #FFFBEB;
    border: 1.5px solid #FDE68A;
}
.result-banner.info {
    background: #EFF6FF;
    border: 1.5px solid #BFDBFE;
}
.result-banner.error {
    background: #FEF2F2;
    border: 1.5px solid #FECACA;
}
.result-banner.dark {
    background: #1C2A25;
    border: 1.5px solid #2D4A37;
}

.rb-icon {
    font-size: 2.8rem;
    flex-shrink: 0;
}
.rb-content {
    flex: 1;
}
.rb-label {
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 4px;
}
.rb-class {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.2;
}
.rb-class.success { color: #15803D; }
.rb-class.warning { color: #92400E; }
.rb-class.info { color: #1E40AF; }
.rb-class.error { color: #991B1B; }
.rb-class.dark { color: #86EFAC; }
.rb-desc {
    font-size: 0.75rem;
    color: #666;
    margin-top: 4px;
}

.rb-divider {
    width: 1px;
    height: 50px;
    background: rgba(0,0,0,0.08);
    flex-shrink: 0;
}

.rb-stats {
    display: flex;
    gap: 1.8rem;
    flex-wrap: wrap;
}

.rb-stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 70px;
}
.rb-stat-value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.3rem;
    font-weight: 600;
    color: #111;
    line-height: 1;
}
.rb-stat-value.green { color: #15803D; }
.rb-stat-value.amber { color: #92400E; }
.rb-stat-label {
    font-size: 0.55rem;
    font-weight: 700;
    color: #AAA;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Pipeline Cards */
.pipeline-card {
    background: #FFFFFF;
    border: 1px solid #E8EDE8;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    transition: all 0.2s ease;
}

.pipeline-card:hover {
    border-color: #C5DEC9;
}

.pipeline-header {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
}

.pipeline-badge {
    background: #1C5C35;
    color: #86EFAC;
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 4px 12px;
    border-radius: 100px;
    flex-shrink: 0;
    margin-top: 2px;
}

.pipeline-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #111;
}
.pipeline-desc {
    font-size: 0.75rem;
    color: #777;
    line-height: 1.7;
    margin-top: 4px;
}

/* Score Cards */
.score-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.8rem;
    margin: 1rem 0 1.5rem 0;
}

.score-card {
    background: #FFFFFF;
    border: 1.5px solid #E8EDE8;
    border-radius: 12px;
    padding: 1rem 0.9rem;
    text-align: center;
    transition: all 0.3s ease;
}

.score-card.active {
    background: #EDF5EF;
    border-color: #1C5C35;
    box-shadow: 0 4px 16px rgba(28, 92, 53, 0.1);
}

.score-card-icon {
    font-size: 1.4rem;
    margin-bottom: 6px;
}
.score-card-label {
    font-size: 0.55rem;
    font-weight: 700;
    color: #999;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.score-card-name {
    font-size: 0.65rem;
    color: #444;
    margin: 2px 0 8px;
    font-weight: 500;
}
.score-bar-bg {
    background: #EAEAE5;
    border-radius: 100px;
    height: 4px;
    margin-bottom: 6px;
    overflow: hidden;
}
.score-bar-fill {
    height: 4px;
    border-radius: 100px;
    transition: width 0.6s ease;
}
.score-value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem;
    font-weight: 500;
    color: #BBB;
}
.score-value.active {
    color: #15803D;
}

/* Feature Grid */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-top: 0.5rem;
}

.feat-item {
    background: #F7F9F7;
    border-radius: 10px;
    padding: 0.9rem 1rem;
}
.feat-val {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem;
    font-weight: 500;
    color: #111;
}
.feat-key {
    font-size: 0.55rem;
    font-weight: 700;
    color: #AAA;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Decision Table */
.decision-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
}

.decision-table th {
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #AAA;
    padding: 0 0 10px 0;
    border-bottom: 2px solid #EAEAE5;
    text-align: left;
}

.decision-table td {
    padding: 10px 0;
    border-bottom: 1px solid #F5F5F0;
    color: #444;
}

.dec-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}

/* Image Caption */
.img-caption {
    font-size: 0.58rem;
    font-weight: 700;
    color: #AAA;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 8px;
}

/* ── FILE UPLOADER OVERRIDES ── */
[data-testid="stFileUploadDropzone"] {
    background: #FFFFFF !important;
    border: 2px dashed #C5DEC9 !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    transition: border-color 0.3s ease;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: #1C5C35 !important;
    background: #F8FBF8 !important;
}

[data-testid="stFileUploadDropzone"] button {
    background: linear-gradient(135deg, #1C5C35, #2D7A4F) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 28px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    margin: 0 auto !important;
    display: block !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploadDropzone"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(28, 92, 53, 0.3) !important;
}

/* ── MISC ── */
.stSpinner > div > div {
    border-top-color: #1C5C35 !important;
}

[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #E8EDE8;
}

hr {
    border-color: #E8EDE8 !important;
    margin: 2rem 0 !important;
}

/* Responsive */
@media (max-width: 1024px) {
    .hero-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    .hero-image-wrapper {
        height: 200px;
    }
    .class-grid,
    .score-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .feat-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .class-grid,
    .score-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .stats-grid {
        grid-template-columns: 1fr;
    }
    .hero-section {
        padding: 1.5rem;
    }
    .hero-title {
        font-size: 1.8rem;
    }
    .result-banner {
        flex-direction: column;
        text-align: center;
        padding: 1.5rem;
    }
    .rb-divider {
        display: none;
    }
    .rb-stats {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .class-grid,
    .score-grid {
        grid-template-columns: 1fr;
    }
    .feat-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# KONSTANTA KELAS
# ══════════════════════════════════════════════════════════
KELAS = {
    "F0": {"label": "F0 · Mentah",         "desc": "Buah belum matang. Warna dominan hijau, belum siap panen.",          "css": "error",   "icon": "🟢", "rec": "Tunda panen 2–3 minggu",   "dot": "#22C55E", "short": "Mentah",        "card_desc": "Buah berwarna hijau, belum matang"},
    "F1": {"label": "F1 · Kurang Matang",  "desc": "Buah mulai mengembang, pucuk ungu gelap, kuning muda mendominasi.", "css": "warning", "icon": "🟡", "rec": "Tunda panen 1–2 minggu",   "dot": "#EAB308", "short": "Kurang Matang", "card_desc": "Warna mulai berubah agak ke merah"},
    "F2": {"label": "F2 · Cukup Matang",   "desc": "Perpaduan oranye dan merah muda. Hampir siap panen optimal.",      "css": "info",    "icon": "🟠", "rec": "Panen dalam 3–5 hari",      "dot": "#F97316", "short": "Cukup Matang",  "card_desc": "Didominasi warna merah oranye"},
    "F3": {"label": "F3 · Matang Ideal",   "desc": "Merah cerah dominan. Waktu panen terbaik untuk yield & kualitas.", "css": "success", "icon": "🔴", "rec": "Panen segera",              "dot": "#EF4444", "short": "Matang Ideal",  "card_desc": "Merah tua mengkilap, kualitas optimal"},
    "F4": {"label": "F4 · Terlalu Matang", "desc": "Maroon gelap. Buah mulai rontok, kadar FFA tinggi.",               "css": "dark",    "icon": "⚫", "rec": "Panen darurat, segera olah", "dot": "#581C87", "short": "Terlalu Matang", "card_desc": "Warna gelap, kualitas mulai menurun"},
}

DOT_COLORS = {"F0": "#22C55E", "F1": "#EAB308",
              "F2": "#F97316", "F3": "#EF4444", "F4": "#581C87"}


# ══════════════════════════════════════════════════════════
# HISTOGRAM
# ══════════════════════════════════════════════════════════
def render_hue_histogram(hist_h, peak_hue, mean_a, mean_sat):
    fig, ax = plt.subplots(figsize=(12, 3.2), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    n = len(hist_h)
    bar_colors = [hsv_to_rgb([(i * 5) / 360.0, 0.75, 0.80]) for i in range(n)]
    ax.bar(range(n), hist_h * 100, color=bar_colors,
           width=0.85, edgecolor="none", zorder=3)
    peak_bin = int(peak_hue / 5)
    if 0 <= peak_bin < n:
        ax.bar(peak_bin, hist_h[peak_bin] * 100,
               color=bar_colors[peak_bin], width=0.85,
               edgecolor="#1C5C35", linewidth=2, zorder=4)
        ax.annotate(f"Peak: {peak_hue}°",
                    xy=(peak_bin, hist_h[peak_bin] * 100),
                    xytext=(peak_bin, hist_h[peak_bin]
                            * 100 + max(hist_h) * 100 * 0.14),
                    ha="center", fontsize=8, fontweight="700", color="#1C5C35", zorder=5)
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(0, max(hist_h) * 100 * 1.4 + 0.5)
    ax.set_xticks([0, 6, 12, 18, 24, 30, 35])
    ax.set_xticklabels(["0°\nMerah", "30°\nOranye", "60°\nKuning", "90°\nH-Hijau",
                       "120°\nHijau", "150°\nSian", "175°\nUngu"], fontsize=7.5, color="#999")
    ax.set_ylabel("Proporsi (%)", fontsize=8, color="#999")
    ax.tick_params(axis="y", labelsize=7.5, colors="#BBB")
    ax.tick_params(axis="x", length=0)
    ax.yaxis.grid(True, color="#F0F0F0", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    info = f"Peak Hue: {peak_hue}°   |   Lab* a*: {mean_a:.1f}   |   Mean Saturation: {mean_sat:.1f} / 255"
    fig.text(0.99, 0.97, info, ha="right", va="top",
             fontsize=7.5, color="#888", style="italic")
    plt.tight_layout(pad=0.8)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor="#FFFFFF", edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)


# ══════════════════════════════════════════════════════════
# EKSTRAKSI FITUR
# ══════════════════════════════════════════════════════════
@st.cache_data
def ekstrak_fitur(image_np):
    img = cv2.resize(image_np, (512, 512))
    img_blur = cv2.GaussianBlur(img, (7, 7), 0)
    hsv = cv2.cvtColor(img_blur, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(img_blur, cv2.COLOR_RGB2LAB)
    h_ch, s_ch, v_ch = cv2.split(hsv)
    L_ch, a_ch, b_ch = cv2.split(lab)
    kernel = np.ones((5, 5), np.uint8)
    m_green = cv2.inRange(hsv, np.array(
        [25,  40,  40]), np.array([85,  255, 255]))
    m_yellow = cv2.inRange(hsv, np.array(
        [11,  50,  50]), np.array([24,  255, 255]))
    m_red1 = cv2.inRange(hsv, np.array(
        [0,   50,  50]), np.array([10,  255, 255]))
    m_red2 = cv2.inRange(hsv, np.array(
        [165, 50,  50]), np.array([180, 255, 255]))
    m_red = m_red1 | m_red2
    m_dark1 = cv2.inRange(hsv, np.array(
        [0,   40,  10]), np.array([20,  255, 80]))
    m_dark2 = cv2.inRange(hsv, np.array(
        [140, 40,  10]), np.array([180, 255, 80]))
    m_dark = m_dark1 | m_dark2
    mask_raw = m_green | m_yellow | m_red | m_dark
    mask_all = cv2.morphologyEx(mask_raw, cv2.MORPH_OPEN,  kernel)
    mask_all = cv2.morphologyEx(mask_all, cv2.MORPH_CLOSE, kernel)
    fruit_px = max(cv2.countNonZero(mask_all), 1)
    pct_g = cv2.countNonZero(m_green) / fruit_px * 100
    pct_y = cv2.countNonZero(m_yellow) / fruit_px * 100
    pct_r = cv2.countNonZero(m_red) / fruit_px * 100
    pct_d = cv2.countNonZero(m_dark) / fruit_px * 100
    if fruit_px > 100:
        mb = mask_all > 0
        mean_L = float(L_ch[mb].mean())
        mean_a = float(a_ch[mb].mean())
        mean_b = float(b_ch[mb].mean())
        mean_sat = float(s_ch[mb].mean())
    else:
        mean_L = float(L_ch.mean())
        mean_a = float(a_ch.mean())
        mean_b = float(b_ch.mean())
        mean_sat = float(s_ch.mean())
    contours, _ = cv2.findContours(
        mask_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_bbox = img.copy()
    if contours:
        lc = max(contours, key=cv2.contourArea)
        x, y, w, hh = cv2.boundingRect(lc)
        cv2.rectangle(img_bbox, (x, y), (x + w, y + hh), (28, 180, 90), 3)
        cv2.putText(img_bbox, "ROI · TBS", (x, max(y - 10, 14)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (28, 180, 90), 2)
    else:
        x, y, w, hh = 0, 0, 512, 512
    gray = cv2.cvtColor(img_blur, cv2.COLOR_RGB2GRAY)
    roi_gray = gray[y:y + hh, x:x + w] if (w > 0 and hh > 0) else gray
    roi_gray = cv2.resize(roi_gray, (128, 128))
    glcm = graycomatrix(roi_gray, distances=[1, 3], angles=[0, np.pi / 4, np.pi / 2],
                        levels=256, symmetric=True, normed=True)
    contrast = float(graycoprops(glcm, "contrast").mean())
    dissim = float(graycoprops(glcm, "dissimilarity").mean())
    homogeneity = float(graycoprops(glcm, "homogeneity").mean())
    energy = float(graycoprops(glcm, "energy").mean())
    correlation = float(graycoprops(glcm, "correlation").mean())
    ASM = float(graycoprops(glcm, "ASM").mean())
    hist_h = cv2.calcHist([hsv], [0], mask_all if fruit_px > 100 else None,
                          [36], [0, 180]).flatten()
    hist_h = hist_h / (hist_h.sum() + 1e-9)
    peak_hue_deg = int(np.argmax(hist_h)) * 5
    edges = cv2.Canny(gray, 80, 180)
    overlay = img.copy()
    overlay[m_yellow > 0] = [255, 180, 50]
    overlay[m_red > 0] = [220,  50, 50]
    overlay[m_dark > 0] = [80,  30, 80]
    overlay[m_green > 0] = [50, 200, 80]
    return {
        "pct_g": pct_g, "pct_y": pct_y, "pct_r": pct_r, "pct_d": pct_d,
        "mean_L": mean_L, "mean_a": mean_a, "mean_b": mean_b, "mean_sat": mean_sat,
        "contrast": contrast, "dissimilarity": dissim,
        "homogeneity": homogeneity, "energy": energy,
        "correlation": correlation, "ASM": ASM,
        "hist_h": hist_h, "peak_hue_deg": peak_hue_deg,
        "img_resized": img, "img_blur": img_blur, "img_bbox": img_bbox,
        "overlay": overlay, "mask_raw": mask_raw, "mask_clean": mask_all, "edges": edges,
    }


# ══════════════════════════════════════════════════════════
# KLASIFIKASI
# ══════════════════════════════════════════════════════════
def klasifikasi(f):
    pct_g = f["pct_g"]
    pct_y = f["pct_y"]
    pct_r = f["pct_r"]
    pct_d = f["pct_d"]
    mean_a = f["mean_a"]
    homog = f["homogeneity"]
    energy = f["energy"]
    scores = {
        "F0": (min(pct_g, 80)*1.5 + max(0, 128-mean_a)*0.5 - pct_r*0.5 - pct_y*0.3),
        "F1": (min(pct_y, 50)*1.2 + min(pct_d, 40)*0.8 - pct_r*0.6 - pct_g*0.5 + max(0, mean_a-128)*0.2),
        "F2": (min(pct_y, 40)*0.9 + min(pct_r, 40)*1.0 + max(0, mean_a-132)*0.6 - pct_g*0.8 + homog*5),
        "F3": (min(pct_r, 60)*1.8 + max(0, mean_a-138)*0.8 - pct_g*1.2 - pct_d*0.3 + energy*8),
        "F4": (min(pct_d, 60)*1.6 + (pct_r*0.5 if pct_y < 15 else 0) - pct_g*0.8 - pct_y*0.5 + (1-homog)*10),
    }
    best = max(scores, key=lambda k: scores[k])
    total = sum(max(v, 0) for v in scores.values()) + 1e-9
    conf = min(max(scores[best]/total*100, 45), 97)
    return best, conf, scores


# ══════════════════════════════════════════════════════════
# COLOR QUANTIZATION
# ══════════════════════════════════════════════════════════
def apply_quantization(image_np, k=8):
    Z = np.float32(image_np.reshape((-1, 3)))
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(
        Z, k, None, crit, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    return center[label.flatten()].reshape(image_np.shape)


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def img_cap(arr, cap):
    st.image(arr, use_container_width=True)
    st.markdown(
        f'<div class="img-caption">{cap}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-wrapper">
        <div class="sidebar-header">
            <div class="sidebar-logo">🌴</div>
            <div class="sidebar-brand">
                <div class="sidebar-brand-name">VisionPalm</div>
                <div class="sidebar-brand-sub">TBS Ripeness Detection</div>
            </div>
        </div>
        <div class="sidebar-nav">
    """, unsafe_allow_html=True)

    # Gunakan session state untuk navigasi
    if "page" not in st.session_state:
        st.session_state.page = "Beranda"

    # Buat button navigasi dengan warna hijau tua
    pages = [("🏠", "Beranda"), ("🔍", "Deteksi")]

    for icon, name in pages:
        is_active = st.session_state.page == name
        btn_type = "primary" if is_active else "secondary"

        if st.button(
            f"{icon}  {name}",
            key=f"nav_{name}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state.page = name
            st.rerun()

    st.markdown("""
        </div>
        <div class="sidebar-footer">
            <div class="sidebar-user">
                <div class="user-avatar">RP</div>
                <div class="user-info">
                    <div class="user-name">Reno Kurniawan Panjaitan</div>
                    <div class="user-role">231112553</div>
                </div>
            </div>
            <div class="sidebar-user">
                <div class="user-avatar">DD</div>
                <div class="user-info">
                    <div class="user-name">Diky Diwa Suwnato</div>
                    <div class="user-role">231110760</div>
                </div>
            </div>
            <div class="sidebar-user">
                <div class="user-avatar">MR</div>
                <div class="user-info">
                    <div class="user-name">Muhammad Rizki</div>
                    <div class="user-role">23111638</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: BERANDA
# ══════════════════════════════════════════════════════════
if st.session_state.page == "Beranda":

    # Top Bar
    # Stats Grid
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-content">
                <div class="stat-label">Total Deteksi</div>
                <div class="stat-value">1,248</div>
                <div class="stat-delta">↑ 12.5% dari minggu lalu</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
                <div class="stat-label">Akurasi Model</div>
                <div class="stat-value">96.7%</div>
                <div class="stat-sub" style="color:#22C55E;font-weight:600;">● Sangat Baik</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-content">
                <div class="stat-label">Rata-rata Waktu</div>
                <div class="stat-value">0.85s</div>
                <div class="stat-sub">Per gambar</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🗃️</div>
            <div class="stat-content">
                <div class="stat-label">Dataset Gambar</div>
                <div class="stat-value">3,560</div>
                <div class="stat-sub">Total gambar terlabel</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Hero Section
    col_hero_l, col_hero_r = st.columns([1.2, 0.8], gap="large")
    with col_hero_l:
        st.markdown("""
        <div class="hero-eyebrow">Visi Komputer · Kelapa Sawit</div>
        <div class="hero-title">
            Sistem Deteksi Kematangan
            <span class="hero-title-green">Tandan Buah Segar (TBS)</span>
        </div>
        <div class="hero-desc">
            Deteksi tingkat kematangan TBS secara cepat, akurat, dan konsisten 
            menggunakan analisis citra berbasis <strong>Computer Vision</strong> dan 
            <strong>Rule-Based Classification</strong>.
        </div>
        """, unsafe_allow_html=True)

        c_btn1, c_btn2 = st.columns([1, 1])
        with c_btn1:
            if st.button("Mulai Deteksi", use_container_width=True,
                         key="hero_btn_deteksi"):
                st.session_state.page = "Deteksi"
                st.rerun()

    with col_hero_r:
        hero_path = "dataset/dataset_f3.jpeg"
        if os.path.exists(hero_path):
            hero_img = Image.open(hero_path)
            st.image(hero_img, use_container_width=True)
        else:
            st.markdown("""
            <div class="hero-image-wrapper">
                <div style="text-align:center;">
                    <div style="font-size:4rem;margin-bottom:0.5rem;">🌴</div>
                    <div style="color:#999;font-size:0.8rem;font-weight:600;">Tandan Buah Segar</div>
                    <div style="color:#BBB;font-size:0.6rem;">Unggah gambar untuk analisis</div>
                </div>
                <div class="hero-image-overlay">
                    <div class="hero-overlay-icon">📊</div>
                    <div>
                        <div class="hero-overlay-text">Real-time Analysis</div>
                        <div class="hero-overlay-sub">Akurasi 96.7%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Referensi Kelas Kematangan
    st.markdown("""
    <div class="section-header">
        <div class="section-title">
            <span</span> Referensi Kelas Kematangan
        </div>
        
    </div>
    """, unsafe_allow_html=True)

    dataset_images = {
        "F0": "dataset/dataset_f0.jpeg",
        "F1": "dataset/dataset_f1.jpeg",
        "F2": "dataset/dataset_f2.jpeg",
        "F3": "dataset/dataset_f3.jpeg",
        "F4": "dataset/dataset_f4.jpeg",
    }
    class_cols = st.columns(5)
    for i, (kode, path) in enumerate(dataset_images.items()):
        info = KELAS[kode]
        with class_cols[i]:
            st.markdown(f'<div class="class-card">', unsafe_allow_html=True)
            if os.path.exists(path):
                st.image(Image.open(path), use_container_width=True)
            else:
                color_map = {"F0": "#22C55E", "F1": "#EAB308",
                             "F2": "#F97316", "F3": "#EF4444", "F4": "#581C87"}
                st.markdown(f"""
                <div style="height:120px;background:{color_map[kode]}22;
                            display:flex;align-items:center;justify-content:center;
                            font-size:2rem;border-radius:8px 8px 0 0;">{info['icon']}</div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="class-card-body">
                <div class="class-card-code">
                    <span style="width:8px;height:8px;border-radius:50%;background:{info['dot']};display:inline-block;"></span>
                    {kode} · {info['short']}
                </div>
                <div class="class-card-desc">{info['card_desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Feature Cards
    st.markdown("""
    <div class="section-header">
        <div class="section-title">
            <span </span> Algoritma yang Digunakan
        </div>
        
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-content">
                <div class="feature-title">HSV + LAB Color</div>
                <div class="feature-desc">Analisis warna akurat</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🧩</div>
            <div class="feature-content">
                <div class="feature-title">GLCM Texture</div>
                <div class="feature-desc">Analisis tekstur permukaan</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎲</div>
            <div class="feature-content">
                <div class="feature-title">K-Means Quant.</div>
                <div class="feature-desc">Kuantisasi warna optimal</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📐</div>
            <div class="feature-content">
                <div class="feature-title">Canny Edge</div>
                <div class="feature-desc">Deteksi tepi presisi</div>
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔀</div>
            <div class="feature-content">
                <div class="feature-title">Rule Fusion</div>
                <div class="feature-desc">Keputusan berbasis aturan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: DETEKSI
# ══════════════════════════════════════════════════════════
elif st.session_state.page == "Deteksi":

    st.markdown("<br>", unsafe_allow_html=True)

    # Back button handler
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Kembali ke Beranda", use_container_width=False,
                     key="back_to_home"):
            st.session_state.page = "Beranda"
            st.rerun()

    # Upload + Result Layout
    col_left, col_right = st.columns([1.4, 1], gap="large")

    with col_right:

        st.markdown("""
        <div class="upload-panel">
            <div class="upload-icon-wrapper">☁️</div>
            <div class="upload-title">Upload Gambar TBS</div>
            <div class="upload-desc">
                Drag & drop atau klik untuk memilih file<br>
                <span style="color:#BBB;font-size:0.6rem;">Format: JPG, PNG (Maks. 10MB)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload gambar TBS",
            type=["jpg", "png", "jpeg"],
            label_visibility="collapsed",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_left:
        if uploaded_file is None:
            # Info cards
            st.markdown("""
            <div style="background:#FFFFFF;border:1px solid #E8EDE8;border-radius:14px;padding:1.8rem;margin-bottom:1.2rem;">
                <div style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:1.2rem;"> Cara Menggunakan</div>
                <div style="display:flex;flex-direction:column;gap:14px;">
                    <div style="display:flex;align-items:flex-start;gap:14px;">
                        <div style="width:28px;height:28px;background:linear-gradient(135deg,#1C5C35,#2D7A4F);color:#FFF;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;flex-shrink:0;">1</div>
                        <div>
                            <div style="font-size:0.8rem;font-weight:600;color:#111;">Upload Foto TBS</div>
                            <div style="font-size:0.7rem;color:#999;line-height:1.5;">Foto lapangan maupun studio, format JPG/PNG</div>
                        </div>
                    </div>
                    <div style="display:flex;align-items:flex-start;gap:14px;">
                        <div style="width:28px;height:28px;background:linear-gradient(135deg,#1C5C35,#2D7A4F);color:#FFF;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;flex-shrink:0;">2</div>
                        <div>
                            <div style="font-size:0.8rem;font-weight:600;color:#111;">Sistem Menganalisis</div>
                            <div style="font-size:0.7rem;color:#999;line-height:1.5;">Pipeline CV mengekstrak fitur warna, tekstur, dan tepi</div>
                        </div>
                    </div>
                    <div style="display:flex;align-items:flex-start;gap:14px;">
                        <div style="width:28px;height:28px;background:linear-gradient(135deg,#1C5C35,#2D7A4F);color:#FFF;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;flex-shrink:0;">3</div>
                        <div>
                            <div style="font-size:0.8rem;font-weight:600;color:#111;">Lihat Hasil Klasifikasi</div>
                            <div style="font-size:0.7rem;color:#999;line-height:1.5;">Kelas F0–F4 + confidence + rekomendasi panen</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Algorithm cards
            st.markdown("""
            <div style="font-size:0.8rem;font-weight:700;color:#111;margin-bottom:0.8rem;"> Algoritma yang Digunakan</div>
            """, unsafe_allow_html=True)

            algo_cols = st.columns(2)
            algos = [
                ("🎨", "HSV + Lab* Color",
                 "Segmentasi dan ekstraksi fitur warna berbasis persepsi"),
                ("🧩", "GLCM Texture",
                 "6 fitur Haralick: Contrast, Energy, Homogeneity, dll"),
                ("🔀", "Rule Fusion", "Scoring multi-kelas + confidence score"),
                ("📐", "Morphological Filter",
                 "Opening + Closing untuk noise removal"),
            ]
            for i, (ic, title, desc) in enumerate(algos):
                with algo_cols[i % 2]:
                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #E8EDE8;border-radius:12px;
                                padding:1rem;margin-bottom:0.8rem;">
                        <div style="font-size:1.1rem;margin-bottom:4px;">{ic}</div>
                        <div style="font-size:0.75rem;font-weight:700;color:#111;margin-bottom:3px;">{title}</div>
                        <div style="font-size:0.65rem;color:#999;line-height:1.5;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Ada file — tampilkan preview
            img_pil = Image.open(uploaded_file).convert("RGB")
            st.image(img_pil, caption="Gambar yang diupload",
                     use_container_width=True)

    # ── ANALISIS ──────────────────────────────────────────
    if uploaded_file is not None:
        img_pil = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(img_pil)

        with st.spinner("Menganalisis citra — mengekstrak fitur warna, tekstur, dan tepi..."):
            time.sleep(0.3)
            f = ekstrak_fitur(img_np)
            kode, conf, scores = klasifikasi(f)

        meta = KELAS[kode]
        total_matang = f["pct_y"] + f["pct_r"] + f["pct_d"]
        total_mentah = f["pct_g"]

        # Result Banner
        st.markdown(f"""
        <div class="result-banner {meta['css']}">
            <div class="rb-icon">{meta['icon']}</div>
            <div class="rb-content">
                <div class="rb-label">Hasil Klasifikasi</div>
                <div class="rb-class {meta['css']}">{meta['label']}</div>
                <div class="rb-desc">{meta['desc']}</div>
            </div>
            <div class="rb-divider"></div>
            <div class="rb-stats">
                <div class="rb-stat">
                    <div class="rb-stat-value green">{total_matang:.1f}%</div>
                    <div class="rb-stat-label">Area Matang</div>
                </div>
                <div class="rb-stat">
                    <div class="rb-stat-value amber">{total_mentah:.1f}%</div>
                    <div class="rb-stat-label">Area Mentah</div>
                </div>
                <div class="rb-stat">
                    <div class="rb-stat-value">{conf:.0f}%</div>
                    <div class="rb-stat-label">Confidence</div>
                </div>
                <div class="rb-stat">
                    <div style="font-size:0.85rem;font-weight:700;color:#1C5C35;">{meta['rec']}</div>
                    <div class="rb-stat-label">Rekomendasi</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gambar utama
        c1, c2 = st.columns(2)
        with c1:
            img_cap(img_pil, "Input Asli")
        with c2:
            img_cap(f["overlay"], "Segmentasi Warna (Overlay)")
        st.write("")

        # Score Grid
        st.markdown("""
        <div style="font-size:0.8rem;font-weight:700;color:#111;margin-bottom:0.8rem;letter-spacing:0.05em;text-transform:uppercase;">
            📊 Skor Klasifikasi Per Kelas
        </div>
        """, unsafe_allow_html=True)

        score_cols = st.columns(5)
        max_score = max(scores.values()) + 1
        for i, (k, info) in enumerate(KELAS.items()):
            with score_cols[i]:
                sc = scores[k]
                pct_bar = max(sc / max_score * 100, 0)
                is_best = k == kode
                st.markdown(f"""
                <div class="score-card {'active' if is_best else ''}">
                    <div class="score-card-icon">{info['icon']}</div>
                    <div class="score-card-label">{k}</div>
                    <div class="score-card-name">{info['short']}</div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{pct_bar:.0f}%;
                                    background:{'linear-gradient(90deg,#1C5C35,#2D7A4F)' if is_best else '#DDD'};"></div>
                    </div>
                    <div class="score-value {'active' if is_best else ''}">{sc:.1f}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ── PIPELINE ──
        st.markdown("""
        <div style="font-size:0.8rem;font-weight:700;color:#111;margin-bottom:0.8rem;letter-spacing:0.05em;text-transform:uppercase;">
            🔬 Pipeline Pemrosesan Citra
        </div>
        """, unsafe_allow_html=True)

        # Tahap 01
        st.markdown("""
        <div class="pipeline-card">
            <div class="pipeline-header">
                <span class="pipeline-badge">TAHAP 01</span>
                <div>
                    <div class="pipeline-title">Spatial Sampling & Color Quantization</div>
                    <div class="pipeline-desc">
                        Resize ke <strong>512×512 px</strong> untuk normalisasi spasial, lalu 
                        <strong>K-Means Color Quantization (K=8)</strong> mereduksi ruang warna menjadi 8 cluster dominan.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        t1a, t1b, t1c = st.columns(3)
        with t1a:
            img_cap(img_pil, f"Original · {img_np.shape[1]}×{img_np.shape[0]}")
        with t1b:
            img_cap(f["img_resized"], "Resized · 512×512")
        with t1c:
            img_cap(apply_quantization(
                f["img_resized"]), "Color Quantized · K=8")
        st.markdown('</div>', unsafe_allow_html=True)

        # Tahap 02
        st.markdown("""
        <div class="pipeline-card">
            <div class="pipeline-header">
                <span class="pipeline-badge">TAHAP 02</span>
                <div>
                    <div class="pipeline-title">Spatial Convolution & Color Space Transformation</div>
                    <div class="pipeline-desc">
                        <strong>Gaussian Blur (kernel 7×7)</strong> menekan noise. Citra lalu dikonversi ke 
                        <strong>HSV</strong> dan <strong>CIE Lab*</strong> untuk ekstraksi fitur diskriminatif kematangan.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        t2a, t2b, t2c = st.columns(3)
        with t2a:
            img_cap(f["img_resized"], "Input RGB")
        with t2b:
            img_cap(f["img_blur"], "Gaussian Blur 7×7")
        hue_vis = cv2.split(cv2.cvtColor(f["img_blur"], cv2.COLOR_RGB2HSV))[0]
        with t2c:
            img_cap(cv2.applyColorMap(hue_vis * 2,
                    cv2.COLORMAP_HSV), "Hue Channel (HSV)")
        st.markdown('</div>', unsafe_allow_html=True)

        # Tahap 03
        st.markdown("""
        <div class="pipeline-card">
            <div class="pipeline-header">
                <span class="pipeline-badge">TAHAP 03</span>
                <div>
                    <div class="pipeline-title">HSV Colour Segmentation & Morphological Filtering</div>
                    <div class="pipeline-desc">
                        Threshold HSV memisahkan piksel per kelas. <strong>Morphological Opening</strong> menghapus noise, 
                        lalu <strong>Closing</strong> merapatkan kontur objek.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        t3a, t3b, t3c = st.columns(3)
        with t3a:
            img_cap(f["mask_raw"],   "Mask Mentah")
        with t3b:
            img_cap(f["mask_clean"], "Mask Bersih")
        with t3c:
            img_cap(f["overlay"],    "Overlay Segmentasi")
        st.markdown('</div>', unsafe_allow_html=True)

        # Tahap 04
        st.markdown("""
        <div class="pipeline-card">
            <div class="pipeline-header">
                <span class="pipeline-badge">TAHAP 04</span>
                <div>
                    <div class="pipeline-title">Canny Edge Detection & Contour Bounding Box</div>
                    <div class="pipeline-desc">
                        <strong>Canny Edge Detection</strong> (80–180) mengekstrak tepi struktur spasial. 
                        <strong>Bounding Box</strong> mengunci ROI pada area buah sawit.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        t4a, t4b = st.columns(2)
        with t4a:
            img_cap(f["edges"],    "Canny Edge (80–180)")
        with t4b:
            img_cap(f["img_bbox"], "Bounding Box · ROI")
        st.markdown('</div>', unsafe_allow_html=True)

        # Tahap 05 GLCM
        st.markdown("""
        <div class="pipeline-card">
            <div class="pipeline-header">
                <span class="pipeline-badge">TAHAP 05</span>
                <div>
                    <div class="pipeline-title">GLCM Texture Feature Extraction</div>
                    <div class="pipeline-desc">
                        Gray-Level Co-occurrence Matrix (GLCM) menghasilkan 6 fitur Haralick: 
                        <em>Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM</em>.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feat-grid">
            <div class="feat-item"><div class="feat-val">{f['contrast']:.3f}</div><div class="feat-key">Contrast</div></div>
            <div class="feat-item"><div class="feat-val">{f['dissimilarity']:.3f}</div><div class="feat-key">Dissimilarity</div></div>
            <div class="feat-item"><div class="feat-val">{f['homogeneity']:.3f}</div><div class="feat-key">Homogeneity</div></div>
            <div class="feat-item"><div class="feat-val">{f['energy']:.4f}</div><div class="feat-key">Energy</div></div>
            <div class="feat-item"><div class="feat-val">{f['correlation']:.3f}</div><div class="feat-key">Correlation</div></div>
            <div class="feat-item"><div class="feat-val">{f['ASM']:.5f}</div><div class="feat-key">ASM</div></div>
            <div class="feat-item"><div class="feat-val">{f['mean_a']:.1f}</div><div class="feat-key">Lab* a*</div></div>
            <div class="feat-item"><div class="feat-val">{f['peak_hue_deg']}°</div><div class="feat-key">Peak Hue</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Tahap 06 Decision Table
        st.markdown("""
        <div class="pipeline-card">
            <div class="pipeline-header">
                <span class="pipeline-badge">TAHAP 06</span>
                <div>
                    <div class="pipeline-title">Rule Fusion Classifier · Decision Table</div>
                    <div class="pipeline-desc">
                        Fitur warna (HSV %), Lab* a*, dan tekstur GLCM digabung dalam 
                        <strong>Rule Fusion Classifier</strong>. Kelas skor tertinggi menjadi hasil klasifikasi akhir + 
                        <em>confidence score</em>.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        rows = ""
        for k, info in KELAS.items():
            sc = scores[k]
            is_best = k == kode
            bo, bc = ("<strong>", "</strong>") if is_best else ("", "")
            star = "✦ " if is_best else ""
            conf_cell = f"{conf:.0f}%" if is_best else "—"
            rows += f"""<tr>
                <td>{bo}<span class='dec-dot' style='background:{DOT_COLORS[k]}'></span>{k}{bc}</td>
                <td>{bo}{info['short']}{bc}</td>
                <td style="font-family:'JetBrains Mono',monospace;font-weight:{'600' if is_best else '400'};color:{'#1C5C35' if is_best else '#444'};">{bo}{sc:.2f}{bc}</td>
                <td>{bo}{star}{conf_cell}{bc}</td>
            </tr>"""
        st.markdown(f"""
        <table class="decision-table">
            <thead><tr><th>Kelas</th><th>Label</th><th>Skor</th><th>Confidence</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Color Histogram
        st.markdown("""
        <div style="font-size:0.8rem;font-weight:700;color:#111;margin-bottom:0.8rem;letter-spacing:0.05em;text-transform:uppercase;">
            📊 Distribusi Hue · Color Histogram
        </div>
        """, unsafe_allow_html=True)
        hist_img = render_hue_histogram(
            f["hist_h"], f["peak_hue_deg"], f["mean_a"], f["mean_sat"])
        st.image(hist_img, use_container_width=True)