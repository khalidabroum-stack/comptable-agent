# ================= 🎯 حاسبة الهدف - مربوطة مع Contable ديالك =================
st.header("🎯 حاسبة الهدف الشهري - بـ مصاريفك الحقيقية")

st.write("عطيني الهدف ديالك، و أنا نحسب ليك شحال خاصك من Lead و Confirm و Delivered في النهار - بـ نفس الحساب ديال Contable ديالك.")

# --- 1. الهدف ---
st.subheader("1️⃣ الهدف ديالك")
c1, c2 = st.columns(2)
with c1:
    objectif_mois2 = st.number_input("🎯 شحال بغيتي تربح صافي في الشهر؟ (DH)", min_value=0.0, value=10000.0, key="obj2_mois")
    nb_jours2 = st.number_input("📅 شحال من يوم غادي تخدم؟", min_value=1, value=30, key="obj2_jours")
with c2:
    obj_conf3 = st.number_input("📞 CONF ديالك (%)", min_value=1.0, max_value=100.0, value=50.0, key="obj3_conf")
    obj_deliv3 = st.number_input("🚚 DELIV ديالك (%)", min_value=1.0, max_value=100.0, value=50.0, key="obj3_deliv")

# --- 2. CPL بالدولار ---
st.subheader("2️⃣ CPL ديالك")
c1, c2, c3 = st.columns(3)
with c1:
    obj_cpl_dollar2 = st.number_input("💰 CPL (بـ $ دولار)", min_value=0.0, value=3.0, key="obj3_cpl_dollar")
with c2:
    taux2 = st.number_input("💱 الدولار شحال داير؟ (DH)", min_value=0.0, value=10.0, key="obj3_taux")
with c3:
    obj_cpl_dh2 = obj_cpl_dollar2 * taux2
    st.metric("CPL بالدرهم", f"{obj_cpl_dh2:.0f} DH")

# --- 3. المنتج + المصاريف ديالك من Contable ---
st.subheader("3️⃣ المنتج و المصاريف - نفس Contable ديالك")
c1, c2, c3, c4 = st.columns(4)
with c1:
    cout_prod2 = st.number_input("📦 ثمن المنتج بالجملة (DH)", min_value=0.0, value=49.0, key="obj3_cout")
with c2:
    prix_vente3 = st.number_input("🏷️ بشحال كتبيع (DH)", min_value=0.0, value=269.0, key="obj3_vente")
with c3:
    frais_spec = st.number_input("👨‍💼 Specseller في Delivered (DH)", min_value=0.0, value=65.0, key="obj3_spec")
with c4:
    frais_ads_fixe = st.number_input("🧾 ads.ma ثابت (DH)", min_value=0.0, value=300.0, key="obj3_adsfixe")
    frais_ads_pct = 0.10
    st.write("ads.ma: 300 + 10%")

# --- 4. Upsell ---
st.subheader("4️⃣ Upsell - شحال كتربح في كل Delivered من Upsell؟")
c1, c2 = st.columns(2)
with c1:
    upsell_par_delivered = st.number_input("💰 متوسط ربح Upsell في كل Delivered (DH) - إلا ما دايرش حط 0", min_value=0.0, value=0.0, key="obj3_upsell")
with c2:
    st.write("مثال: إلا كل 10 Delivered كتبيع 2 Upsell و كتربح فيهم 50 DH، حط 10 DH هنا")
    st.write(f"المارج قبل الإعلان: {prix_vente3 - cout_prod2 - frais_spec + upsell_par_delivered:.0f} DH")

if st.button("🤖 حسب ليا شحال خاصني نجيب في النهار", type="primary", key="btn_obj3"):
    st.divider()
    conf3 = obj_conf3 / 100
    deliv3 = obj_deliv3 / 100

    # المارج قبل الاعلان - نفس Contable ديالك
    marge_avant_pub = prix_vente3 - cout_prod2 - frais_spec + upsell_par_delivered

    # ثمن الاعلان باش تجيب Delivered وحدة - مع 10% ديال ads.ma
    # ads_spend = Leads * CPL
    # Total ads = ads_spend * 1.1 + 300
    # Cout pub par Delivered = CPL * 1.1 / (CONF * DELIV)
    cout_pub_par_deliv2 = (obj_cpl_dh2 * 1.1) / (conf3 * deliv3) if conf3 > 0 and deliv3 > 0 else 9999

    # الربح الصافي في Delivered وحدة - من غير 300 الثابت
    profit_par_deliv2 = marge_avant_pub - cout_pub_par_deliv2

    if profit_par_deliv2 <= 0:
        st.error(f"🚨 كتخسر {abs(profit_par_deliv2):.0f} DH في كل Delivered! مستحيل توصل لـ {objectif_mois2:.0f} DH")
        st.write(f"**التفصيل:** كتبيع بـ {prix_vente3:.0f} - المنتج {cout_prod2:.0f} - Specseller {frais_spec:.0f} + Upsell {upsell_par_delivered:.0f} = **{marge_avant_pub:.0f} DH** مارج")
        st.write(f"**الإعلان باش تجيب Delivered وحدة:** {cout_pub_par_deliv2:.0f} DH - (CPL {obj_cpl_dh2:.0f} × 1.1 / {obj_conf3:.0f}% × {obj_deliv3:.0f}%)")
        st.write(f"**الحل:** نقص CPL لـ {obj_cpl_dh2*0.6:.0f} DH، ولا طلع CONF / DELIV، ولا زيد Upsell")
        st.stop()

    # شحال خاصك من Delivered في الشهر: (الهدف + 300) / الربح في البياسة
    delivered_mois2 = (objectif_mois2 + frais_ads_fixe) / profit_par_deliv2
    delivered_jour2 = delivered_mois2 / nb_jours2
    confirm_mois2 = delivered_mois2 / deliv3
    confirm_jour2 = confirm_mois2 / nb_jours2
    lead_mois2 = confirm_mois2 / conf3
    lead_jour2 = lead_mois2 / nb_jours2

    ads_spend_mois2 = lead_mois2 * obj_cpl_dh2
    ads_spend_jour2 = ads_spend_mois2 / nb_jours2
    frais_ads_ma_mois2 = frais_ads_fixe + (ads_spend_mois2 * frais_ads_pct)
    frais_spec_mois2 = delivered_mois2 * frais_spec
    chiffre_mois2 = delivered_mois2 * prix_vente3
    cout_produit_mois2 = delivered_mois2 * cout_prod2
    profit_upsell_mois2 = delivered_mois2 * upsell_par_delivered
    cout_total_mois2 = cout_produit_mois2 + ads_spend_mois2 + frais_ads_ma_mois2 + frais_spec_mois2
    profit_verif = chiffre_mois2 + profit_upsell_mois2 - cout_total_mois2

    st.subheader(f"🏆 باش تربح {objectif_mois2:.0f} DH صافي في الشهر، خاصك هادشي في النهار:")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📩 LEAD في النهار", f"{lead_jour2:.0f}")
    m2.metric("📞 CONFIRM في النهار", f"{confirm_jour2:.0f}")
    m3.metric("📦 DELIVERED في النهار", f"{delivered_jour2:.1f}")
    m4.metric("💰 AD SPEND في النهار", f"{ads_spend_jour2:.0f} DH")

    st.divider()
    st.subheader("📊 التفاصيل - في النهار")
    st.write(f"**📩 LEAD:** خاصك **{lead_jour2:.0f} Lead** في النهار")
    st.write(f"**📞 CONFIRM:** خاصك **{confirm_jour2:.0f} Confirm** - ({lead_jour2:.0f} × {obj_conf3:.0f}%)")
    st.write(f"**📦 DELIVERED:** غادي توصّل **{delivered_jour2:.1f} بياسة** - ({confirm_jour2:.0f} × {obj_deliv3:.0f}%)")
    st.write(f"**💰 AD SPEND:** غادي تصرف **{ads_spend_jour2:.0f} DH** في النهار + ads.ma")
    st.write(f"**⏰ في الساعة (12h):** **{lead_jour2/12:.1f} Lead** في الساعة")

    st.divider()
    st.subheader("📅 التفاصيل - في الشهر")
    st.write(f"**📩 LEAD:** **{lead_mois2:.0f} Lead** | **📞 CONFIRM:** **{confirm_mois2:.0f}** | **📦 DELIVERED:** **{delivered_mois2:.0f} بياسة**")
    st.write(f"**💰 AD SPEND:** **{ads_spend_mois2:.0f} DH** + **ads.ma: {frais_ads_ma_mois2:.0f} DH** (300 + 10%) = **{ads_spend_mois2 + frais_ads_ma_mois2:.0f} DH** كامل الإعلان")

    st.divider()
    st.subheader("💸 الحساب - في بياسة وحدة موصلة (نفس Contable)")
    st.write(f"**كتبيع بـ:** {prix_vente3:.0f} DH")
    st.write(f"**- المنتج:** {cout_prod2:.0f} DH")
    st.write(f"**- Specseller:** {frais_spec:.0f} DH")
    st.write(f"**+ Upsell:** {upsell_par_delivered:.0f} DH")
    st.write(f"**= المارج قبل الإعلان:** **{marge_avant_pub:.0f} DH**")
    st.write(f"**- الإعلان (مع 10% ads.ma):** {cout_pub_par_deliv2:.0f} DH")
    st.write(f"**= الربح الصافي في البياسة:** **{profit_par_deliv2:.0f} DH**")

    st.divider()
    st.subheader("🏁 الخلاصة ديال الشهر - التأكيد بـ Contable")
    st.write(f"**Chiffre d'Affaires:** {chiffre_mois2:.0f} DH + Upsell {profit_upsell_mois2:.0f} DH = **{chiffre_mois2 + profit_upsell_mois2:.0f} DH**")
    st.write(f"**- المنتجات:** {cout_produit_mois2:.0f} DH")
    st.write(f"**- Specseller:** {frais_spec_mois2:.0f} DH ({frais_spec:.0f} × {delivered_mois2:.0f})")
    st.write(f"**- الإعلان + ads.ma:** {ads_spend_mois2 + frais_ads_ma_mois2:.0f} DH")
    st.write(f"**= Profit Net:** **{profit_verif:.0f} DH** ✅ - قريب من الهدف ديالك {objectif_mois2:.0f} DH")

    # Breakevent - نفس Contable ديالك
    if lead_mois2 > 0:
        breakevent2 = (delivered_mois2 * (prix_vente3 - cout_prod2 - frais_spec) + profit_upsell_mois2 - frais_ads_fixe) / (lead_mois2 * 1.1)
        st.write(f"**Breakevent CPL ديالك:** **{breakevent2:.2f} DH** - CPL ديالك دابا {obj_cpl_dh2:.0f} DH")
        if obj_cpl_dh2 < breakevent2:
            st.success(f"✅ CPL ديالك أقل من Breakevent - راك رابح")
        else:
            st.error(f"⛔ CPL ديالك فايت Breakevent - راك خاسر")

    st.divider()
    st.subheader("⚠️ واش الهدف واقعي؟")
    if lead_jour2 > 100:
        st.warning(f"⚠️ خاصك {lead_jour2:.0f} Lead في النهار - بزاف! حسن CONF و DELIV ولا نقص CPL باش تنقص Leads")
    elif lead_jour2 > 50:
        st.warning(f"⚠️ خاصك {lead_jour2:.0f} Lead في النهار - ممكن ولكن خاصك Budget و Call Center واجدين")
    else:
        st.success(f"✅ واقعي! غير {lead_jour2:.0f} Lead في النهار و توصل لـ {objectif_mois2:.0f} DH")