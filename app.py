import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agent V11 - Expert Complet", page_icon="🤖", layout="wide")
st.title("🤖 Agent V11 - Expert Complet")
st.write("الحملة + الفيديو + الكوبي + السكيلينغ - كلشي فبلاصة وحدة")

tab1, tab2, tab3 = st.tabs(["📊 1. تحليل الحملة - SCALE or KILL", "🎬 2. تحليل الفيديو + Ad Copy", "🚀 3. بناء حملة بحال Expert"])

# ================= TAB 1 - تحليل الحملة =================
with tab1:
    st.subheader("📁 Upload Facebook Export")
    uploaded = st.file_uploader("Upload CSV / Excel من Meta Ads", type=["csv", "xlsx", "xls"], key="exp")
    
    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        
        def find_col(possibles):
            for c in df.columns:
                for p in possibles:
                    if p.lower() in c.lower():
                        return c
            return None
        col_campaign = find_col(["campaign name"])
        col_spend = find_col(["amount spent"])
        col_impr = find_col(["impressions"])
        col_click_link = find_col(["link clicks"])
        col_click_all = find_col(["clicks (all)"])
        col_landing = find_col(["landing page views"])
        col_leads = find_col(["leads", "results", "purchases"])

        def get(row, col, default=0):
            try:
                if col is None: return default
                v = row[col]
                return float(str(v).replace(",", "").replace(" ", "")) if pd.notna(v) else default
            except: return default

        if col_campaign:
            selected = st.selectbox("Campaign Name", df[col_campaign].unique().tolist())
            row = df[df[col_campaign] == selected].iloc[0]
        else:
            row = df.iloc[0]

        spend = get(row, col_spend)
        impressions = get(row, col_impr)
        clicks_link = get(row, col_click_link)
        clicks_all = get(row, col_click_all)
        landing = get(row, col_landing)
        leads = get(row, col_leads)
        cpl = (spend/leads) if leads>0 else 999
        lead_rate = (leads/landing*100) if landing>0 else 0
        landing_rate = (landing/clicks_link*100) if clicks_link>0 else 0
        ctr_link = (clicks_link/impressions*100) if impressions>0 else 0
        cpc = (spend/clicks_link) if clicks_link>0 else 0
        cpm = (spend/impressions*1000) if impressions>0 else 0

        st.write("**الفيديو - من Ad بوحدو (ما كاينش فالـ Export)**")
        c1, c2 = st.columns(2)
        with c1:
            views_3s = st.number_input("3-Second Video Views", min_value=0, value=int(impressions*0.25) if impressions>0 else 0, key="v3")
            views_15s = st.number_input("15-Second Video Views", min_value=0, value=0, key="v15")
            thruplay = st.number_input("ThruPlay", min_value=0, value=0, key="th")
        with c2:
            v25 = st.number_input("Video Plays at 25%", min_value=0, value=0, key="25")
            v50 = st.number_input("Video Plays at 50%", min_value=0, value=0, key="50")
            v75 = st.number_input("Video Plays at 75%", min_value=0, value=0, key="75")
            v95 = st.number_input("Video Plays at 95%", min_value=0, value=0, key="95")
        load_time = st.number_input("Page Speed (seconds)", min_value=0.0, value=2.5, key="sp")
        bounce = st.number_input("Bounce Rate %", min_value=0.0, value=60.0, key="bo")
        days = st.number_input("Days running?", min_value=1, value=3, key="days")
        current_budget = st.number_input("Current Daily Budget (MAD)", min_value=0.0, value=200.0, key="bud")
        target_cpl = st.number_input("Target CPL - شحال بغيتي تخلص على Lead؟ (MAD)", min_value=0.0, value=20.0, key="tcpl")

        if st.button("🤖 Analyze - فين المشكل و شحال نسكيلي؟", type="primary", key="ana1"):
            hook = (views_3s / impressions * 100) if impressions > 0 else 0
            hold = (views_15s / views_3s * 100) if views_3s > 0 else 0
            r50 = (v50 / impressions * 100) if impressions > 0 else 0
            r75 = (v75 / impressions * 100) if impressions > 0 else 0
            
            st.divider()
            st.subheader("🏆 DECISION + شحال نسكيلي؟")
            if spend < 150:
                st.info(f"⏳ WAIT - صرفتي غير {spend:.0f} MAD. خليها حتى 300-400 MAD عاد حكم. ما تحبس ما تسكيلي.")
            elif hook >= 25 and ctr_link >= 1 and cpl <= target_cpl and lead_rate >= 10:
                new_budget = current_budget * 1.2
                new_budget_2 = new_budget * 1.2
                st.success(f"🚀 SCALE! - سكيلي دابا!")
                st.write(f"**علاش؟** Hook {hook:.1f}% مزيان + CTR {ctr_link:.2f}% مزيان + CPL {cpl:.1f} MAD أقل من الهدف ديالك {target_cpl:.0f} + Lead Rate {lead_rate:.1f}% مزيان.")
                st.write(f"**شحال نزيد؟**")
                st.write(f"اليوم: {current_budget:.0f} MAD -> بعد 2 أيام: **{new_budget:.0f} MAD** (+20%)")
                st.write(f"من بعد 2 أيام أخرى: **{new_budget_2:.0f} MAD** (+20% عاود)")
                st.write(f"إلا CPL طلع فوق {target_cpl*1.5:.0f} MAD، حبس السكيلينغ و رجع لـ {current_budget:.0f} MAD.")
                st.write("**القاعدة الذهبية:** ما تزيدش كثر من 20% كل يومين، و ما تبدلش الفيديو ولا الجمهور ملي كتسكيلي.")
            elif hook < 20 and ctr_link < 0.8 and cpl > 40 and days >= 3:
                st.error(f"🛑 KILL IT! - حبسها! Hook {hook:.1f}% + CTR {ctr_link:.2f}% + CPL {cpl:.1f} MAD - كلشي طايح و دازو {days} أيام. كتخسر {spend:.0f} MAD بلا فايدة. حبسها و بدا وحدة جديدة.")
            else:
                st.warning("🔧 FIX IT! - صايب المشكل اللي لتحت، ما تحبس ما تسكيلي.")

            st.divider()
            st.subheader("🔍 المشكل فين بالضبط؟ + علاش؟ + شنو ندير؟")
            if hook < 25:
                st.error(f"🔴 المشكل هنا: HOOK - {hook:.1f}% (خاصو يكون فوق 25%)")
                st.write("**علاش كاين المشكل؟** أول 3 ثواني ما شدّوش الناس. الناس ففيسبوك كيسكروليو بسرعة، إلا ما وقفتيهمش ف 3s اللولة، غادي يدوزو.")
                st.write("**شنو خاصك تدير؟** بدل غير 3 ثواني اللولة: بدا بالمشكل: 'كتعاني من...؟' ولا بنتيجة: 'شوف النتيجة ف 7 أيام'. ما تبداش بلوغو ولا سلام. سير لـ Tab 2 و حط الفيديو ديالك، غادي نعطيك سكريبت جديد.")
            elif hold < 30:
                st.error(f"🔴 المشكل هنا: HOLD - {hold:.1f}% (خاصو يكون فوق 30%)")
                st.write("**علاش؟** Hook شدّهم ولكن الوسط ممل، هربو قبل 15s.")
                st.write("**شنو تدير؟** قصر الفيديو ل 25-30 ثانية، العرض يبان قبل 10s، كل 3 ثواني دير شي حاجة جديدة (تصويرة، زوم، كتابة).")
            elif r50 - r75 > 10:
                st.error(f"🔴 المشكل هنا: الفيديو طويل - هربو {r50-r75:.1f}% بين 50% و 75%")
                st.write("**علاش؟** الناس ملّو فالوسط. **شنو تدير؟** قصر الفيديو، دير CTA فالوسط.")
            if ctr_link < 1:
                st.error(f"🟠 المشكل هنا: CTA - CTR {ctr_link:.2f}% (خاصو فوق 1%)")
                st.write("**علاش؟** الناس كملو الفيديو ولكن ما عرفوش شنو يديرو. **شنو تدير؟** فاللخر قول: 'كليكي على اللين دابا، العرض كيسالي اليوم' + الثمن واضح + زر كيبان.")
            elif cpc > 3:
                st.error(f"🟠 المشكل هنا: CPC غالي - {cpc:.2f} MAD")
                st.write("**علاش؟** الجمهور غالط. **شنو تدير؟** جرب Broad بلا اهتمامات.")
            if landing_rate < 70:
                st.error(f"🟠 المشكل هنا: الصفحة ثقيلة - دخلو غير {landing_rate:.0f}%")
                st.write(f"**علاش؟** كليكاو {clicks_link:.0f} ولكن دخلو غير {landing:.0f}. الصفحة كتعطل {load_time:.1f}s. **شنو تدير؟** صغر التصاور، حيد الفيديو الكبير فالبداية، خاصها تحل فأقل من 2s.")
            elif bounce > 70:
                st.error(f"🟠 المشكل هنا: Bounce {bounce:.0f}%")
                st.write("**علاش؟** الميساج ديال الفيديو ماشي هو الميساج ديال الصفحة. **شنو تدير؟** نفس المنتج، نفس الثمن، نفس العرض فالفيديو و فالصفحة.")
            elif lead_rate < 10:
                st.error(f"🟠 المشكل هنا: الصفحة ما كتقنعش - غير {lead_rate:.1f}% عمرو الفورم")
                st.write("**علاش؟** الصفحة ما فيهاش ثقة. **شنو تدير؟** الثمن واضح الفوق؟ Reviews كيبانو؟ عرض: توصيل فابور؟ زر 'اطلب الان' كبير؟")

            st.divider()
            st.write(f"📉 Funnel: Impressions {impressions:.0f} -> 3s {views_3s} ({hook:.0f}%) -> Link Clicks {clicks_link:.0f} -> Landing {landing:.0f} ({landing_rate:.0f}%) -> Leads {leads:.0f} ({lead_rate:.1f}%) | CPL {cpl:.1f} | CPM {cpm:.1f} | CPC {cpc:.2f}")

# ================= TAB 2 - تحليل الفيديو + الكوبي =================
with tab2:
    st.subheader("🎬 حط ليا الفيديو و Ad Copy ديالك - نقول ليك فين الخلل")
    st.write("هادي بلاصة بوحدها ديال الفيديو. هنا كنحلو الفيديو بالتفصيل.")

    product = st.text_input("شنو المنتج؟", placeholder="مثال: كريم تبييض، ساعة، مكينة قهوة...")
    problem_product = st.text_input("شنو المشكل اللي كيحل المنتج؟", placeholder="مثال: البشرة كحلة، النعاس قليل...")
    audience = st.selectbox("شكون الجمهور؟", ["نساء 18-35", "نساء 35-55", "رجال 18-35", "رجال 35-55", "الأمهات", "الشباب"])
    video_type = st.selectbox("شنو نوع الفيديو اللي درتي؟", ["UGC - واحد كيهضر", "Voice Over + تصاور المنتج", "تصاور بلا هدرة", "إنفلونسر", "Before / After", "ما عرفتش"])
    video_length = st.number_input("شحال طول الفيديو؟ (ثواني)", min_value=5, value=30)
    hook_text = st.text_area("شنو قلتي فأول 3 ثواني؟ كتبو هنا بالضبط", placeholder="مثال: سلام عليكم، اليوم جبت ليكم...")
    cta_text = st.text_area("شنو قلتي فاللخر؟ (CTA)", placeholder="مثال: اطلبو دابا...")
    ad_copy = st.text_area("Ad Copy - شنو كتبتي فالنص ديال الإعلان ففيسبوك؟", placeholder="كتب النص كامل هنا...")
    has_price = st.selectbox("واش الثمن كاين فالفيديو؟", ["لا", "إيه فاللخر", "إيه فاللول"])
    has_offer = st.selectbox("واش كاين عرض؟ (توصيل فابور، تخفيض...)", ["لا، ما كاينش عرض", "إيه، توصيل فابور", "إيه، تخفيض", "إيه، 1+1 فابور"])

    video_file = st.file_uploader("📹 Upload الفيديو ديالك هنا (إلا بغيتي)", type=["mp4", "mov"], key="vid")
    if video_file:
        st.video(video_file)

    if st.button("🤖 حلل ليا الفيديو + الكوبي - فين الخلل؟", type="primary", key="ana2"):
        st.divider()
        st.subheader("🔍 تحليل الفيديو - فين الخلل؟")
        
        # Hook Analysis
        if "سلام" in hook_text or "اليوم جبت" in hook_text or len(hook_text) < 10:
            st.error("🔴 الخلل فالـ HOOK - أول 3 ثواني ميتين!")
            st.write(f"**قلتي:** '{hook_text}' - هادا Hook ديال يوتيوب، ماشي ديال فيسبوك. الناس غادي يدوزو.")
            st.write("**الحل:** بدل Hook. جرب واحد من هادو:")
        else:
            st.success("✅ Hook مزيان، ما فيهش مشكل كبير.")

        st.write("**🎬 السكريبت الجديد اللي خاصك تدير (30 ثانية):**")
        st.write(f"**0-3s HOOK:** 'كتعاني من {problem_product}؟ شوف هادي...' + وري المشكل فالكاميرا")
        st.write(f"**3-10s المشكل:** 'جربتي بزاف و والو؟ حيت المشكل هو...' + وري قبل / بعد")
        st.write(f"**10-20s الحل:** 'هاد {product} كيحلها ف 7 أيام، حيت...' + وري المنتج كيخدم، وري النتيجة")
        st.write(f"**20-25s الثقة:** 'أكثر من 500 واحد جربوه، شوفو شنو قالو...' + وري Reviews")
        st.write(f"**25-30s CTA:** 'كليكي على اللين دابا، العرض كيسالي اليوم، التوصيل فابور' + الثمن واضح")

        st.divider()
        st.subheader("🎥 نوع الفيديو + Avatar + الصوت - شنو اللي خدام فالمغرب؟")
        st.write(f"**نوع الفيديو اللي خاصك:**")
        if audience in ["نساء 18-35", "الأمهات"]:
            st.write("✅ **UGC - بنت كتهضر بالدارجة** - هي اللي خدامة مزيان فالمغرب دابا. ماشي Voice Over روبو، بنت حقيقية كتهضر بحال كتهضر مع صاحبتها.")
            st.write("**Avatar:** بنت مغربية 25-30 سنة، لابسة عادي، كتهضر فالدار، إضاءة طبيعية، تيليفون فاليد.")
            st.write("**الصوت:** صوت بنت بالدارجة، هادي و طبيعي، ماشي صوت إشهار. سرعة متوسطة، ما تجريش.")
        elif "رجال" in audience:
            st.write("✅ **UGC - راجل كيجرب المنتج** - راجل كيهضر بالدارجة، كيوري المنتج فاليد.")
            st.write("**Avatar:** راجل 28-35 سنة، كيهضر بثقة، لابس عادي.")
            st.write("**الصوت:** صوت راجل بالدارجة، قوي شوية، ما يكونش ممل.")
        else:
            st.write("✅ **UGC + Before / After** - وري قبل و بعد، هادي هي اللي كتبيع.")
        
        st.write("**الموسيقى:** موسيقى خفيفة فالخلف، ما تغطيش على الصوت. بلا موسيقى إلا كان UGC.")
        st.write("**الكتابة فالفيديو:** كل كلمة مهمة كتبها فالفيديو، حيت 80% كيتفرجو بلا صوت. دير Subtitles بالدارجة.")
        st.write(f"**طول الفيديو:** {video_length} ثانية - ", end="")
        if video_length > 40:
            st.write("طويل بزاف! قصرو لـ 25-30 ثانية.")
        else:
            st.write("مزيان، خليه 25-30 ثانية.")

        st.divider()
        st.subheader("✍️ تحليل Ad Copy - النص ديال الإعلان")
        if len(ad_copy) < 50:
            st.error("🔴 Ad Copy قصير بزاف ولا ما كاينش!")
            st.write("**علاش؟** فيسبوك كيعطي النص أهمية كبيرة. إلا كان قصير، الناس ما غاديش يثيقو.")
        if has_price == "لا":
            st.error("🔴 الخلل: الثمن ما كاينش فالفيديو!")
            st.write("**علاش؟** الناس كيكليكيو و كيتفاجئو بالثمن فالصفحة و كيهربو. **الحل:** قول الثمن فالفيديو ف 20s.")
        if has_offer == "لا، ما كاينش عرض":
            st.warning("🟠 ما كاينش عرض! زيد عرض باش الناس يكليكيو دابا.")
            st.write("**أحسن العروض فالمغرب:** توصيل فابور / 1+1 فابور / تخفيض 20% اليوم فقط.")

        st.write("**✍️ Ad Copy الجديد اللي خاصك تكتب (كوبيه نيشان):**")
        st.code(f"""كتعاني من {problem_product}؟ 😩

جربتي بزاف و والو؟ حيت المشكل ماشي فيك، المشكل فالمنتج اللي كنتي كتستعملي.

{product} كيحلها ليك ف 7 أيام، و أكثر من 500 بنت جربوه فالمغرب و عجبهم.

✅ النتيجة كتبان ف 7 أيام
✅ التوصيل فابور اليوم فقط
✅ الدفع عند التوصيل - ما تخلصي حتى يوصلك

👉 كليكي على اللين دابا و طلبي، العرض كيسالي اليوم!

# {product}""", language="text")
        st.write("**علاش هاد الكوبي خدام؟** 1) بدا بالمشكل 2) عطا الحل 3) عطا الثقة (500 بنت) 4) عطا عرض (توصيل فابور) 5) CTA واضح (كليكي دابا)")

# ================= TAB 3 - بناء حملة Expert =================
with tab3:
    st.subheader("🚀 كيفاش تبني حملة بحال Expert - من الزيرو")
    st.write("هادي هي الطريقة اللي كيخدمو بيها الـ Experts فالمغرب، خطوة بخطوة:")

    st.write("**المرحلة 1: قبل ما تطلق (1 نهار)**")
    st.write("1. **المنتج:** واش كيحل مشكل حقيقي؟ واش الثمن ديالو بين 150-350 درهم؟ إلا كان أقل من 100، ما غاديش تربح مع التوصيل. إلا كان كثر من 400، الناس غادي يترددو.")
    st.write("2. **الفيديو:** 3 فيديوهات مختلفين: 1) UGC بنت كتهضر 2) Before / After 3) Voice Over + تصاور. ما تطلقش بفيديو واحد.")
    st.write("3. **الصفحة:** الثمن واضح الفوق، Reviews، زر 'اطلب الان' كبير، سرعة أقل من 2s. جربها فتيليفونك نتا اللول.")
    
    st.write("**المرحلة 2: الإطلاق (نهار 1-3)**")
    st.write("1. **Campaign Objective:** Sales ولا Leads - ماشي Traffic ولا Engagement!")
    st.write("2. **Budget:** 200 درهم فالنهار، CBO - خلي فيسبوك يوزع البودجيت.")
    st.write("3. **Audience:** Broad - المغرب كامل، 18-55، بلا اهتمامات. فيسبوك دابا كيعرف حسن منك شكون غادي يشري.")
    st.write("4. **Ad Sets:** 1 Ad Set فيه 3 فيديوهات. ما تديرش 5 Ad Sets فالبداية.")
    st.write("5. **ما تقيسش والو فأول 3 أيام!** خلي فيسبوك يتعلم. ما تبدلش البودجيت ولا الفيديو.")

    st.write("**المرحلة 3: التحليل (نهار 3)**")
    st.write("1. سير لـ Tab 1، Upload الـ Export، شوف القرار: SCALE ولا FIX ولا KILL")
    st.write("2. شوف الفيديو اللي جاب أقل CPL، حيد لاخرين، و زيد فيديو جديد بحالو.")
    st.write("3. إلا CPL مزيان، سكيلي +20% كل يومين.")

    st.write("**المرحلة 4: السكيلينغ (نهار 5+) - شحال نزيد؟**")
    st.write("**الطريقة الآمنة (Vertical Scaling):** زيد البودجيت 20% كل يومين. من 200 -> 240 -> 288 -> 345...")
    st.write("**الطريقة السريعة (Horizontal Scaling):** إلا كان CPL مزيان بزاف، دوبلي الحملة كاملة: دير Duplicate للحملة و زيد بودجيت جديد. ما تزيدش البودجيت فالحملة القديمة بزاف.")
    st.write("**إمتى نحبس؟** إلا CPL طلع 50% فوق الهدف ديالك لمدة 2 أيام، حبس السكيلينغ و رجع للبودجيت القديم.")
    st.write("**إمتى نقتل الحملة؟** إلا صرفتي 3x CPL ديالك و ما جابتيش حتى Lead، حبسها. مثال: إلا CPL ديالك 20 درهم و صرفتي 60 درهم و 0 Leads، حبسها.")

    st.write("**❌ الأخطاء اللي كيقتلو الحملة:**")
    st.write("- كتبدل البودجيت كل ساعة - فيسبوك كيتلف")
    st.write("- كتطلق بفيديو واحد - خاصك 3 على الأقل")
    st.write("- كتحكم على الحملة فأول نهار - خاصك 3 أيام على الأقل")
    st.write("- كتزيد البودجيت 100% دقة وحدة - فيسبوك كيخربق")
    st.write("- كتدير Audience ضيق بزاف - خليها Broad")
    