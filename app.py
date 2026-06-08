# Copyright (c) 2026 Gabriel Mahia / AI Kung Fu LLC. MIT License.
# kilimo-bima-ai — Parametric Crop Insurance Calculator for Kenya
# Research: ACRE Africa Methodology 2023, World Bank AgFin WP2024, NDMA Kenya

import streamlit as st
import datetime

st.set_page_config(page_title="Kilimo Bima AI", page_icon="🌾", layout="centered")
st.markdown("""
<style>
.stApp{background:#071a0e;color:#e8f5e9}
.risk-high{background:#1a0000;border:1px solid #c62828;border-radius:8px;padding:12px}
.risk-med{background:#1a1000;border:1px solid #ef6c00;border-radius:8px;padding:12px}
.risk-low{background:#001a04;border:1px solid #2e7d32;border-radius:8px;padding:12px}
.mpesa-card{background:#001a0a;border:2px solid #00a651;border-radius:10px;padding:16px}
</style>""", unsafe_allow_html=True)

COUNTIES = {
    "Turkana":{"drought_pct":85,"phase":"Crisis","region":"ASAL"},
    "Marsabit":{"drought_pct":75,"phase":"Emergency","region":"ASAL"},
    "Mandera":{"drought_pct":80,"phase":"Crisis","region":"ASAL"},
    "Wajir":{"drought_pct":78,"phase":"Crisis","region":"ASAL"},
    "Garissa":{"drought_pct":72,"phase":"Alert","region":"ASAL"},
    "Kitui":{"drought_pct":55,"phase":"Alert","region":"Semi-Arid"},
    "Makueni":{"drought_pct":50,"phase":"Stressed","region":"Semi-Arid"},
    "Machakos":{"drought_pct":40,"phase":"Stressed","region":"Semi-Arid"},
    "Kajiado":{"drought_pct":45,"phase":"Stressed","region":"Semi-Arid"},
    "Nakuru":{"drought_pct":25,"phase":"Stressed","region":"Rift Valley"},
    "Narok":{"drought_pct":30,"phase":"Stressed","region":"Rift Valley"},
    "Uasin Gishu":{"drought_pct":20,"phase":"Minimal","region":"Rift Valley"},
    "Trans Nzoia":{"drought_pct":15,"phase":"Minimal","region":"Rift Valley"},
    "Kisumu":{"drought_pct":18,"phase":"Minimal","region":"Nyanza"},
    "Kakamega":{"drought_pct":12,"phase":"Minimal","region":"Western"},
    "Kiambu":{"drought_pct":15,"phase":"Minimal","region":"Central"},
    "Nyeri":{"drought_pct":18,"phase":"Minimal","region":"Central"},
    "Meru":{"drought_pct":22,"phase":"Minimal","region":"Eastern"},
    "Nairobi":{"drought_pct":10,"phase":"Minimal","region":"Nairobi"},
    "Mombasa":{"drought_pct":18,"phase":"Minimal","region":"Coast"},
}

CROPS = {
    "Mahindi (Maize)":{"key":"maize","risk":1.0,"input_per_acre":8000},
    "Maharagwe (Beans)":{"key":"beans","risk":0.9,"input_per_acre":5000},
    "Viazi (Potatoes)":{"key":"potatoes","risk":0.8,"input_per_acre":15000},
    "Ngano (Wheat)":{"key":"wheat","risk":0.85,"input_per_acre":10000},
    "Mtama (Sorghum)":{"key":"sorghum","risk":0.7,"input_per_acre":4000},
    "Muhogo (Cassava)":{"key":"cassava","risk":0.6,"input_per_acre":3000},
    "Chai (Tea)":{"key":"tea","risk":0.5,"input_per_acre":20000},
}

SEASONS = {
    "Masika (Long Rains: Mar-Jun)":{"multiplier":1.0},
    "Vuli (Short Rains: Oct-Dec)":{"multiplier":1.2},
}

st.markdown("## 🌾 Kilimo Bima AI")
st.markdown("**Bima ya Mazao kwa Wakulima Wadogo — Parametric Crop Insurance for Kenya Smallholders**")
st.caption("⚠️ DEMO — Educational tool. Not a real insurance product. Verify at ira.go.ke")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    county_name = st.selectbox("📍 Kaunti (County)", sorted(COUNTIES.keys()), index=9)
    crop_name = st.selectbox("🌱 Zao (Crop)", list(CROPS.keys()))
with col2:
    acreage = st.number_input("📐 Ekari (Acres)", min_value=0.1, max_value=50.0, value=1.0, step=0.5)
    season_name = st.selectbox("🗓️ Msimu (Season)", list(SEASONS.keys()))

phone = st.text_input("📱 Nambari ya M-PESA", placeholder="0712345678",
                       help="Demo payment flow illustration only")
calculate = st.button("🧮 Hesabu Bima (Calculate Insurance)", type="primary")

if calculate:
    county = COUNTIES[county_name]
    crop = CROPS[crop_name]
    season = SEASONS[season_name]
    drought_pct = county["drought_pct"]
    risk_score = min(100, int(drought_pct * crop["risk"] * season["multiplier"]))
    input_cost = acreage * crop["input_per_acre"]
    premium = int(input_cost * 0.08 * (drought_pct / 100) * season["multiplier"])
    expected_payout = int(input_cost * 0.9)
    premium_pct = round(premium / input_cost * 100, 1)

    risk_label = ("HATARI KUBWA (VERY HIGH)" if risk_score > 65 else
                  "HATARI (HIGH)" if risk_score > 45 else
                  "WASTANI (MEDIUM)" if risk_score > 25 else "SALAMA (LOW)")
    risk_css = "risk-high" if risk_score > 65 else "risk-med" if risk_score > 45 else "risk-low"

    st.markdown("---")
    st.markdown("### 📊 Matokeo ya Tathmini (Risk Assessment)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Hatari ya Ukame", str(drought_pct) + "%", delta=county["phase"])
    m2.metric("Alama ya Hatari", str(risk_score) + "/100")
    m3.metric("Eneo la NDMA", county["region"])
    st.markdown(
        '<div class="' + risk_css + '"><strong>Kiwango cha Hatari:</strong> ' + risk_label + '<br/>'
        + 'Hali ya NDMA: <strong>' + county["phase"] + '</strong> — ' + county_name + '</div>',
        unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💰 Bei ya Bima (Insurance Economics)")
    e1, e2, e3 = st.columns(3)
    e1.metric("Gharama za Kilimo", "KES " + "{:,.0f}".format(input_cost))
    e2.metric("Malipo ya Bima", "KES " + "{:,.0f}".format(premium), delta=str(premium_pct) + "% ya gharama")
    e3.metric("Malipo ya Dharura", "KES " + "{:,.0f}".format(expected_payout))

    how_it_works = (
        "Bima hii inategemea satellite (NDVI) na data ya NDMA. "
        "Ukame ukiathiri " + county_name + " (" + county["phase"] + " phase), "
        "M-PESA yako itapokea KES " + "{:,}".format(expected_payout) + " ndani ya siku 14. "
        "Hakuna fomu. Hakuna haja ya uthibitisho wa mkono.\n\n"
        "(If drought triggers, you receive KES " + "{:,}".format(expected_payout) +
        " automatically via M-PESA within 14 days — no claim forms needed.)"
    )
    st.info(how_it_works)

    st.markdown("---")
    st.markdown("### 📱 Mtiririko wa Malipo ya M-PESA (Payment Flow)")

    normalized_phone = phone.strip().replace(" ", "")
    if normalized_phone.startswith("07") or normalized_phone.startswith("01"):
        normalized_phone = "254" + normalized_phone[1:]
    elif normalized_phone and not normalized_phone.startswith("254"):
        normalized_phone = "254" + normalized_phone
    if not normalized_phone:
        normalized_phone = "2547XXXXXXXX"

    account_ref = county_name[:4].upper() + "-" + crop["key"].upper() + "-" + str(datetime.date.today().year)
    st.markdown('<div class="mpesa-card">', unsafe_allow_html=True)
    mpesa_steps = (
        "**HATUA ZA UANDIKISHAJI (Enrollment Steps):**\n\n"
        "1. 📲 Nenda M-PESA → Lipa na M-PESA → Paybill\n"
        "2. ✏️ Nambari ya Biashara: **400200** (ACRE Africa Demo)\n"
        "3. ✏️ Akaunti: **" + account_ref + "**\n"
        "4. 💵 Kiasi: **KES " + "{:,.0f}".format(premium) + "** (premium ya msimu mmoja)\n"
        "5. 📞 Nambari yako: **" + normalized_phone + "**\n\n"
        "⚠️ DEMO ONLY — Do not send real money. For real enrollment: acreafrica.com or pula-advisors.com"
    )
    st.markdown(mpesa_steps)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ✅ Orodha ya Uhakikisho (Verification Checklist)")
    for item in [
        "Thibitisha hali ya NDMA kwa " + county_name + ": ndma.go.ke",
        "Angalia leseni ya kampuni ya bima: ira.go.ke",
        "Soma masharti yote kabla ya kulipa (Read all terms before paying)",
        "Hakikisha M-PESA paybill ni halisi — wasiliana na ACRE Africa au Pula",
        "Hifadhi risiti yako ya M-PESA kwa ushahidi wa malipo",
    ]:
        st.markdown("- [ ] " + item)

    with st.expander("📚 Msingi wa Utafiti (Research Basis)"):
        st.markdown("""
**Parametric Insurance Methodology:**
- ACRE Africa Satellite Crop Insurance (2023) — NDVI-based trigger
- World Bank Agricultural Finance WP2024 — input cost benchmarks
- NDMA County Monitoring Reports — drought frequency data

**Western Parallel:** Climate Corporation (US), Skywatch EasyCrop (Canada), WRMS India
**East Africa Gap:** Only ~3% of African smallholder farmers have any crop insurance (World Bank 2023).
        """)

st.markdown("---")
st.caption("🌾 kilimo-bima-ai · DEMO tool · Not affiliated with ACRE Africa, Pula, or Kenya IRA · MIT License")
