# 🌾 kilimo-bima — Parametric Crop Insurance Calculator

**First AI-powered parametric crop insurance calculator for Kenya smallholder farmers.**

## The Structural Problem

Conventional insurance fails in low-income agricultural markets because of claims
adjustment costs. Sending a field agent to verify a drought-damaged farm in rural
Turkana costs more than the claim itself. This makes small-farm insurance
economically impossible to provide through traditional channels.

**Parametric insurance eliminates this entirely:**

```
Trigger:  Satellite NDVI drops below threshold for N consecutive weeks
Action:   Automatic M-PESA transfer to enrolled farmer
Cost:     Zero claims adjustment. Zero fraud investigation.
```

## How It Works

1. Farmer selects their county, crop, and acreage
2. App queries NDMA drought history for that county
3. Risk score calculated from drought frequency + crop vulnerability
4. Premium estimated using area-yield index methodology
5. M-PESA payment flow demonstrated (DEMO only)

## Research Basis

- Area-Yield Index insurance methodology (ACRE Africa, 2023)
- World Bank Agricultural Finance WP2024
- NDMA County Drought Monitoring Reports

## Run It

```bash
pip install streamlit
streamlit run app.py
```

⚠️ DEMO tool — not a real insurance product. Verify products at ira.go.ke.

---
*© 2026 Gabriel Mahia / AI Kung Fu LLC · MIT License*
