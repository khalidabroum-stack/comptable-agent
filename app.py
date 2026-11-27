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

# ================= 5. BREAKEVENT =================
st.header("5. Breakevent - شحال أقصى CPL تقدر تخلصو")
if leads > 0:
    breakevent_cpl = (delivered * (prix_vente - cout_produit - 65) + profit_upsell_total - 300) / (leads * 1.1)
    st.metric("Breakevent CPL", f"{breakevent_cpl:.2f} DH", f"CPL ديالك دابا: {cpl:.2f} DH")
    st.write(f"**إلا وصل الـ CPL لـ {breakevent_cpl:.2f} DH، راك متعادل - لا ربح لا خسارة.**")
    if cpl < breakevent_cpl:
        st.success(f"✅ الـ CPL ديالك {cpl:.2f} DH أقل من Breakevent {breakevent_cpl:.2f} DH - راك رابح")
    elif cpl > breakevent_cpl:
        st.error(f"⛔ الـ CPL ديالك {cpl:.2f} DH فايت Breakevent {breakevent_cpl:.2f} DH - راك خاسر")
    else:
        st.info("⚖️ متعادل")
else:
    st.write("دخل عدد Leads باش نحسبو Breakevent")

# ================= 6. حاسبة الهدف الشهري - جديد =================
st.header("6. 🎯 حاسبة الهدف الشهري - بـ مصاريفك الحقيقية")
st.write("عطيني الهدف ديالك، و أنا نحسب ليك شحال خاصك من Lead و Confirm و Delivered في النهار")

c1, c2 = st.columns(2)
with c1:
    objectif_mois2 = st.number_input("🎯 شحال بغيتي تربح صافي في الشهر؟ (DH)", min_value=0.0, value=10000.0, key="obj_mois")
    nb_jours2 = st.number_input("📅 شحال من يوم غادي تخدم؟", min_value=1, value=30, key="obj_jours")
with c2:
    obj_conf3 = st.number_input("📞 CONF ديالك (%)", min_value=1.0, max_value=100.0, value=50.0, key="obj_conf")
    obj_deliv3 = st.number_input("🚚 DELIV ديالك (%)", min_value=1.0, max_value=100.0, value=50.0, key="obj_deliv")

c1, c2, c3 = st.columns(3)
with c1:
    obj_cpl_dollar2 = st.number_input("💰 CPL (بـ $ دولار)", min_value=0.0, value=3.0, key="obj_cpl_dollar")
with c2:
    taux2 = st.number_input("💱 الدولار شحال داير؟ (DH)", min_value=0.0, value=10.0, key="obj_taux")
with c3:
    obj_cpl_dh2 = obj_cpl_dollar2 * taux2
    st.metric("CPL بالدرهم", f"{obj_cpl_dh2:.0f} DH")

upsell_par_delivered = st.number_input("💰 متوسط ربح Upsell في كل Delivered (DH) - إلا ما دايرش حط 0", min_value=0.0, value=0.0, key="obj_upsell")

if st.button("🤖 حسب ليا شحال خاصني نجيب في النهار", type="primary", key="btn_obj"):
    conf3 = obj_conf3 / 100
    deliv3 = obj_deliv3 / 100
    marge_avant_pub = prix_vente - cout_produit - 65 + upsell_par_delivered
    cout_pub_par_deliv2 = (obj_cpl_dh2 * 1.1) / (conf3 * deliv3) if conf3 > 0 and deliv3 > 0 else 9999
    profit_par_deliv2 = marge_avant_pub - cout_pub_par_deliv2

    if profit_par_deliv2 <= 0:
        st.error(f"🚨 كتخسر {abs(profit_par_deliv2):.0f} DH في كل Delivered! المارج {marge_avant_pub:.0f} DH و الإعلان {cout_pub_par_deliv2:.0f} DH")
        st.stop()

    delivered_mois2 = (objectif_mois2 + 300) / profit_par_deliv2
    delivered_jour2 = delivered_mois2 / nb_jours2
    confirm_mois2 = delivered_mois2 / deliv3
    confirm_jour2 = confirm_mois2 / nb_jours2
    lead_mois2 = confirm_mois2 / conf3
    lead_jour2 = lead_mois2 / nb_jours2
    ads_spend_mois2 = lead_mois2 * obj_cpl_dh2
    ads_spend_jour2 = ads_spend_mois2 / nb_jours2

    st.subheader(f"🏆 باش تربح {objectif_mois2:.0f} DH في الشهر، خاصك في النهار:")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📩 LEAD في النهار", f"{lead_jour2:.0f}")
    m2.metric("📞 CONFIRM في النهار", f"{confirm_jour2:.0f}")
    m3.metric("📦 DELIVERED في النهار", f"{delivered_jour2:.1f}")
    m4.metric("💰 AD SPEND في النهار", f"{ads_spend_jour2:.0f} DH")

    st.write(f"**📩 LEAD في الشهر:** {lead_mois2:.0f} | **📞 CONFIRM:** {confirm_mois2:.0f} | **📦 DELIVERED:** {delivered_mois2:.0f}")
    st.write(f"**المارج قبل الإعلان:** {marge_avant_pub:.0f} DH - **الإعلان في البياسة:** {cout_pub_par_deliv2:.0f} DH = **الربح في البياسة: {profit_par_deliv2:.0f} DH**")
    st.write(f"**AD SPEND في الشهر:** {ads_spend_mois2:.0f} DH + ads.ma {300 + ads_spend_mois2*0.10:.0f} DH")
    st.success(f"✅ واقعي! غير {lead_jour2:.0f} Lead في النهار و توصل لـ {objectif_mois2:.0f} DH")