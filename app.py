import streamlit as st

st.set_page_config(page_title="Agent V11 - Expert Complet", layout="wide")
st.title("📦 Agent V11 - Expert Complet")

# ================= 1. Leads =================
st.header("1. Leads & الطلبيات")

col1, col2 = st.columns(2)
with col1:
    leads = st.number_input("عدد Leads", min_value=0, value=100, step=1)
    delivered = st.number_input("عدد Delivered", min_value=0, value=28, step=1)
with col2:
    confirmes = st.number_input("عدد Confirmés", min_value=0, value=55, step=1)
    cpl = st.number_input("Cost Per Lead - CPL (DH)", min_value=0.0, value=4.0, step=0.5)

confirmation_rate = (confirmes / leads * 100) if leads > 0 else 0
delivered_rate = (delivered / confirmes * 100) if confirmes > 0 else 0
delivered_sur_leads = (delivered / leads * 100) if leads > 0 else 0

st.markdown("### 📊 النسب المئوية")
c1, c2, c3 = st.columns(3)
c1.metric("Confirmation Rate", f"{confirmation_rate:.1f}%", f"{confirmes} / {leads}")
c2.metric("Delivered Rate", f"{delivered_rate:.1f}%", f"{delivered} / {confirmes}")
c3.metric("Delivered / Leads", f"{delivered_sur_leads:.1f}%", f"{delivered} / {leads}")

# ================= 2. المنتج الأساسي =================
st.header("2. المنتج الأساسي")
cout_produit = st.number_input("ثمن المنتج بالجملة (DH)", min_value=0.0, value=49.0, step=1.0)
prix_vente = st.number_input("بشحال كتبيع (DH)", min_value=0.0, value=269.0, step=1.0)

# ================= 3. UPSELL 1 + UPSELL 2 =================
st.header("3. Upsell - 2 منتجات")

# --- Upsell 1 ---
st.subheader("Upsell 1 - المنتج اللول")
col1, col2, col3 = st.columns(3)
with col1:
    nb_upsell1 = st.number_input("عدد Upsell 1", min_value=0, value=0, step=1, key="nb1")
with col2:
    prix_upsell1 = st.number_input("بشحال بعتو Upsell 1 (DH)", min_value=0.0, value=0.0, step=1.0, key="prix1")
with col3:
    cout_upsell1 = st.number_input("بشحال شريتو Upsell 1 (DH)", min_value=0.0, value=0.0, step=1.0, key="cout1")

chiffre_upsell1 = nb_upsell1 * prix_upsell1
cout_total_upsell1 = nb_upsell1 * cout_upsell1
profit_upsell1 = chiffre_upsell1 - cout_total_upsell1

if nb_upsell1 > 0:
    st.success(f"ربح Upsell 1: {profit_upsell1:.0f} DH - ({prix_upsell1-cout_upsell1:.0f} DH فـ كل وحدة)")

st.markdown("---")

# --- Upsell 2 ---
st.subheader("Upsell 2 - المنتج الثاني - ثمن بوحدو")
col1, col2, col3 = st.columns(3)
with col1:
    nb_upsell2 = st.number_input("عدد Upsell 2", min_value=0, value=0, step=1, key="nb2")
with col2:
    prix_upsell2 = st.number_input("بشحال بعتو Upsell 2 (DH)", min_value=0.0, value=0.0, step=1.0, key="prix2")
with col3:
    cout_upsell2 = st.number_input("بشحال شريتو Upsell 2 (DH)", min_value=0.0, value=0.0, step=1.0, key="cout2")

chiffre_upsell2 = nb_upsell2 * prix_upsell2
cout_total_upsell2 = nb_upsell2 * cout_upsell2
profit_upsell2 = chiffre_upsell2 - cout_total_upsell2

if nb_upsell2 > 0:
    st.success(f"ربح Upsell 2: {profit_upsell2:.0f} DH - ({prix_upsell2-cout_upsell2:.0f} DH فـ كل وحدة)")

# المجموع ديال Upsell
chiffre_upsell_total = chiffre_upsell1 + chiffre_upsell2
cout_upsell_total = cout_total_upsell1 + cout_total_upsell2
profit_upsell_total = profit_upsell1 + profit_upsell2

if (nb_upsell1 + nb_upsell2) > 0:
    st.info(f"💰 مجموع Upsell: {nb_upsell1+nb_upsell2} وحدة - ربح كامل: {profit_upsell_total:.0f} DH")

# ================= 4. النتائج =================
st.header("4. النتائج - الحساب الحقيقي")

ads_spend = cpl * leads
frais_ads_ma = 300 + (ads_spend * 0.10)
frais_specsellers = delivered * 65

chiffre_principal = delivered * prix_vente
cout_produits = delivered * cout_produit

chiffre_affaires = chiffre_principal + chiffre_upsell_total
cout_total = cout_produits + cout_upsell_total + ads_spend + frais_ads_ma + frais_specsellers
profit = chiffre_affaires - cout_total

st.markdown("### 🧾 تفصيل المصاريف")
st.write(f"**مصاريف الإعلانات:** {cpl:.2f} DH × {leads} = **{ads_spend:.0f} DH**")
st.write(f"**ads.ma:** 300 DH + 10% ({ads_spend*0.10:.0f} DH) = **{frais_ads_ma:.0f} DH**")
st.write(f"**Service Specseller:** 65 DH × {delivered} = **{frais_specsellers:.0f} DH**")
st.write(f"**ثمن المنتجات:** {cout_produit:.0f} DH × {delivered} = **{cout_produits:.0f} DH**")
if nb_upsell1 > 0:
    st.write(f"**ثمن Upsell 1:** {cout_upsell1:.0f} DH × {nb_upsell1} = **{cout_total_upsell1:.0f} DH**")
if nb_upsell2 > 0:
    st.write(f"**ثمن Upsell 2:** {cout_upsell2:.0f} DH × {nb_upsell2} = **{cout_total_upsell2:.0f} DH**")

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Chiffre d'Affaires", f"{chiffre_affaires:.0f} DH", f"Principal {chiffre_principal:.0f} + Upsell {chiffre_upsell_total:.0f}")
c2.metric("Total Coûts", f"{cout_total:.0f} DH")
c3.metric("Profit Net", f"{profit:.0f} DH", f"منهم Upsell: {profit_upsell_total:.0f} DH")

cout_par_delivered = (cout_total / delivered) if delivered > 0 else 0
profit_par_delivered = (profit / delivered) if delivered > 0 else 0
marge_par_commande = prix_vente - cout_produit - 65

col1, col2 = st.columns(2)
col1.write(f"**التكلفة الكاملة ديال طلبية وحدة:** {cout_par_delivered:.2f} DH")
col1.write(f"**الربح فـ كل Delivered:** {profit_par_delivered:.2f} DH")
col2.write(f"**المارج قبل الإعلانات:** {marge_par_commande:.0f} DH")

if profit > 0:
    st.success(f"🎉 رابح بـ {profit:.0f} DH - كمل SCALE")
elif profit < 0:
    st.error(f"📉 خاسر بـ {profit:.0f} DH")
else:
    st.info("⚖️ متعادل - 0 DH")