#!/usr/bin/env python3
"""
Build the Korea Trip itinerary static site.
Reads no external data — all content is defined below and was verified
line by line against official sources (see data/verification-log.md).

Output (repo root, served by GitHub Pages from main /):
  index.html, pages/*.html, assets/style.css, assets/app.js
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- sources
# Short name -> (label, url). Only official sources (venue / operator / govt).
SRC = {
    "SMG_AIRPORT": ("Seoul Metropolitan Government — Getting to Seoul from Incheon Airport",
                    "https://english.seoul.go.kr/service/entry/getting-to-seoul-from-incheon-airport/"),
    "AREX": ("Airport Railroad (AREX) — official site", "https://www.arex.or.kr/"),
    "LIMOBUS": ("Airport Limousine Co. — Bus 6015 route & fares",
                "https://airportlimousine.co.kr/en/sub/sub01.php?cat_no=21"),
    "Stanford": ("Stanford Hotel Myeongdong — official room page",
                 "https://www.stanford-hotel.com/myeongdong/en/room/view/16"),
    "STANFORD_FAQ": ("Stanford Hotel Myeongdong — official FAQ",
                     "https://stanford.webhelper.co.kr/myeongdong/en/contents/list/faq"),
    "TOWER_HOURS": ("N Seoul Tower — official hours", "https://www.nseoultower.co.kr/eng/visit/use.asp"),
    "TOWER_ADM": ("N Seoul Tower — official admission", "https://www.nseoultower.co.kr/eng/visit/use2.asp"),
    "TOWER_BUS": ("N Seoul Tower — getting here by bus", "https://www.nseoultower.co.kr/eng/visit/traffic.asp"),
    "TOWER_CABLE": ("N Seoul Tower — getting here by cable car", "https://www.nseoultower.co.kr/eng/visit/traffic2.asp"),
    "CABLECAR": ("Namsan Cable Car — official hours", "http://www.cablecar.co.kr/m/eng/guide/open.html"),
    "Lotte": ("Lotte Department Store — Myeongdong Main (official)",
              "https://global.lotteshopping.com/eng/store/main?cstrCd=0001"),
    "Shinsegae_VK": ("Korea Tourism Organization — Shinsegae Dept Store Main Store",
                     "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=106990"),
    "OLIVEYOUNG": ("Olive Young Myeongdong Town — official store page", "https://myeongdongtown.oliveyoung.com/"),
    "GWANGJANG_VK": ("Korea Tourism Organization — Gwangjang Market",
                     "https://english.visitkorea.or.kr/svc/whereToGo/locIntrdn/rgnContentsView.do?vcontsId=106345"),
    "Mangwon_VS": ("Visit Seoul (Seoul Tourism) — Mangwon Market",
                    "https://english.visitseoul.net/shopping/Mangwon-Market/ENP037950"),
    "KYOJA": ("Myeongdong Kyoja — official site, main restaurant", "http://www.mdkj.co.kr/en/restaurant/head.php"),
    "MICHELIN_KYOJA": ("MICHELIN Guide — Myeongdong Kyoja",
                       "https://guide.michelin.com/us/en/seoul-capital-area/kr-seoul/restaurant/myeongdong-kyoja"),
    "CRYSTALJADE": ("Crystal Jade Korea — Shinsegae Main Store (official)",
                    "https://www.crystaljade.co.kr/menu/menuInfo.do?shSq=49&shGb=H"),
    "PALACE": ("Gyeongbokgung Palace — official hours & admissions",
               "https://www.royalpalacekr.org/html/eng_gbg/guide/guide01_tab01.html"),
    "PALACE_VK": ("Korea Tourism Organization — Gyeongbokgung Palace",
                  "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=87740"),
    "GUARD": ("Korea Heritage Agency — Royal Palace Guard Ceremony", "https://www.kh.or.kr/cms/content/view/824"),
    "HOLIDAYS_VK": ("Korea Tourism Organization — 2026 public holidays",
                    "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140038"),
    "BUKCHON_SMG": ("Seoul Metropolitan Government — Bukchon visiting-hour restrictions",
                    "https://english.seoul.go.kr/notice-on-restrictions-for-tourist-visits-to-bukchon-special-management-area-effective-from-november-2024/"),
    "BUKCHON_VS": ("Visit Seoul (Seoul Tourism) — Bukchon Hanok Village",
                   "https://english.visitseoul.net/attractions/Bukchon-Hanok-Village/ENP000261"),
    "ONION": ("Cafe Onion — official store info (Anguk)", "https://m.onionkr.com/artfinger/offline.html?cate_no=26"),
    "DDP": ("DDP — official operating information", "https://ddp.or.kr/?menuno=340"),
    "DDP_VK": ("Korea Tourism Organization — Dongdaemun Design Plaza",
               "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=67162"),
    "COEX": ("Starfield COEX Mall — official site", "https://m.starfield.co.kr/coexmall?lang=en"),
    "COEX_VK": ("Korea Tourism Organization — Starfield COEX Mall",
                "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=73375"),
    "KORAIL": ("Korail — official booking (English)", "https://www.korail.com/global/en/main/en_main.html"),
    "L7": ("Lotte Hotels — L7 Haeundae (official)", "https://www.lottehotel.com/haeundae-l7/en"),
    "Haeundae_MKT": ("Busan Tourism (Visit Busan) — Haeundae Market",
                     "https://visitbusan.net/en/index.do?menuCd=DOM_000000301003001000&uc_seq=294&lang_cd=en"),
    "HAEUNDAE_BEACH": ("Busan Tourism (Visit Busan) — Haeundae Beach",
                       "https://www.visitbusan.net/index.do?menuCd=DOM_000000301001001000&uc_seq=373&lang_cd=en"),
    "Haeundae_MKT_VK": ("Korea Tourism Organization — Busan Haeundae Market",
                        "https://english.visitkorea.or.kr/svc/whereToGo/locIntrdn/rgnContentsView.do?vcontsId=84963"),
}

V = "Verified"
P = "Partial"
C = "Conflict"
U = "Unverified"


def row(name, location="", hours="", days="", cost="", claim="", status=U, src=None, note=""):
    return dict(name=name, location=location, hours=hours, days=days, cost=cost,
                claim=claim, status=status, src=src, note=note)


def nv(name, claim="", note="No official source confirmed in verification pass (Oct 2026). Hours/cost left blank per verification rules."):
    """Unverified row helper."""
    return row(name, claim=claim, status=U, note=note)


# ---------------------------------------------------------------- days
DAYS = [
    dict(
        n=1, slug="day-1", dow="Sunday", date="Nov 1, 2026",
        title="Arrive Seoul — SFO → Incheon → Myeongdong",
        area="Incheon Airport → Myeongdong, Seoul",
        plan=[
            "Fly SFO → ICN (Incheon International Airport). Depart Oct 31, arrive Nov 1 (as written in itinerary; exact flight/times not in the plan — see Flags).",
            "Transfer ICN → Seoul: AREX airport train or airport limousine bus.",
            "Check in at Stanford Hotel Myeongdong; light neighborhood walk, settle in, rest from jet lag.",
        ],
        getting=[
            ("Fastest to Seoul Station", "AREX Express (non-stop) from ICN T1/T2 → Seoul Station, then Subway Line 4 one stop to Hoehyeon/Myeongdong area or a short taxi to the hotel. AREX does <b>not</b> go to Myeongdong directly."),
            ("Easiest with luggage", "Airport Limousine Bus <b>6015</b> (or 6001) from ICN → Myeongdong stops near the hotel. Buy the ticket at the airport counter/kiosk before boarding."),
            ("Cheapest", "AREX All-stop train to Seoul Station, then Line 4. Slower, commuter-style seating."),
        ],
        rows=[
            row("AREX Express Train (non-stop)", "ICN T1/T2 → Seoul Station",
                hours="Service hours vary — see operator timetable", cost="₩13,000 adult (one-way)",
                claim="“Arex 45 min, $7”", status=P, src="SMG_AIRPORT",
                note="43 min from T1 / 51 min from T2 to Seoul Station (Seoul Metropolitan Government). The itinerary's “$7” matches neither the Express (₩13,000) nor All-stop fare exactly → USD treated as unverified estimate. Ends at Seoul Station — add Line 4 or taxi to Myeongdong."),
            row("AREX All-stop Train", "ICN T1/T2 → Seoul Station (14 stops)",
                hours="Service hours vary — see operator timetable", cost="₩4,150–4,750 adult (one-way)",
                claim="—", status=V, src="SMG_AIRPORT",
                note="59 min from T1 / 66 min from T2 to Seoul Station. Budget option; pay with transport card."),
            row("Airport Limousine Bus 6015", "ICN → Myeongdong (Mapo · Chungjeongno · Hoehyeon · Myeongdong)",
                hours="See operator timetable for first/last bus", cost="₩17,000 adult / ₩12,000 child (6–12)",
                claim="“Airport Limousine bus $13”", status=V, src="LIMOBUS",
                note="Fare confirmed on the operator's official page. “$13” in the itinerary is an unverified USD estimate of the same fare. Drops you near Myeongdong hotels — best door-to-door option with bags."),
            row("Stanford Hotel Myeongdong (Nights 1–8)", "84, Namdaemun-ro, Jung-gu, Seoul (opposite Lotte Department Store)",
                hours="Check-in from 15:00 · Check-out until 12:00",
                claim="“Check into Stanford Hotel in Myeongdong”", status=V, src="Stanford",
                note="Official site also lists early check-in / late check-out at ₩20,000 per hour, subject to occupancy (hotel FAQ). Nearest subway: Euljiro 1-ga (Line 2) — the hotel FAQ references Exit 7·8."),
        ],
        flags=["F13", "F17", "F20"],
    ),
    dict(
        n=2, slug="day-2", dow="Monday", date="Nov 2, 2026",
        title="N Seoul Tower & Myeongdong",
        area="Namsan · Myeongdong · Gwangjang Market (evening)",
        plan=[
            "Bus up to N Seoul Tower (Namsan); observatory visit.",
            "Myeongdong shopping district — fashion, K-beauty, food stalls (Lotte / Shinsegae department stores, Olive Young).",
            "Evening: Myeongdong night food market + Gwangjang Market (Netflix-famous hand-cut noodles), or Mangwon Market (less touristy alternative).",
            "Dinner options in itinerary: Pig Restaurant 2 (Itaewon) · Myeongdong Kyoja · Crystal Jade (Shinsegae B1) · Hongojib. Bar: Myeongdong Sookhee.",
        ],
        getting=[
            ("Hotel → N Seoul Tower (bus)", "Subway Line 4 Myeongdong → Chungmuro (1 stop), Exit 2, then Namsan Sunhwan Shuttle Bus <b>01A / 01B</b> to N Seoul Tower (₩1,500, transport card only). Bus 01A also stops at “Myeongdong Cathedral · Namdaemun Tax Office,” walkable from the hotel."),
            ("Hotel → N Seoul Tower (cable car)", "Walk or short taxi to the Namsan Cable Car lower station near Myeongdong, ride up (₩15,000 round trip), short walk to the tower."),
            ("Myeongdong → Gwangjang Market", "Subway Line 2 Euljiro 1-ga → Euljiro 4-ga, or Line 1 to Jongno 5-ga. Market is at 88 Changgyeonggung-ro, Jongno-gu."),
            ("Myeongdong → Mangwon Market", "Line 2 to Hapjeong, transfer Line 6 to Mangwon Station, Exit 2 (≈350 m walk)."),
        ],
        rows=[
            row("Namsan Sunhwan Shuttle Bus 01A / 01B", "Chungmuro Stn Exit 2 · Myeongdong Cathedral (01A) → N Seoul Tower",
                hours="06:30–23:00 · every 9 min (01A) / 14 min (01B)", cost="₩1,500 (transport card only)",
                claim="“Take bus to Namsun Tower. 31 min bus ride”", status=P, src="TOWER_BUS",
                note="Route, interval, hours and fare verified on the tower's official page. The “31 min” ride time is an itinerary estimate (depends on boarding stop). Private cars are restricted on Namsan — bus or cable car are the practical ways up."),
            row("N Seoul Tower — Observatory", "105 Namsangongwon-gil, Yongsan-gu (Namsan summit)",
                hours="Mon–Fri 10:00–22:30 · Sat–Sun & holidays 10:00–23:00 · last entry 30 min before close",
                days="Open year-round", cost="Adult (13+) ₩29,000 · Child 3–12 / Senior 65+ ₩23,000",
                claim="“Observatory 10:00–10:30 (entry until 10:00); cable car + observatory $31 each”",
                status=P, src="TOWER_HOURS",
                note="Itinerary omits PM: on Monday Nov 2 the observatory closes 22:30, last entry 22:00 — matches “entry until 10:00.” Admission price: official admission page (2nd source below). “$31” is an unverified USD estimate of cable car (₩15,000) + observatory (₩29,000) bought separately."),
            row("Namsan Cable Car", "83 Sopa-ro, Jung-gu (lower station near Myeongdong)",
                hours="10:00–23:00 daily (last round-trip ticket 22:30)", days="Open year-round, weather permitting",
                cost="Round trip: adult ₩15,000 / child ₩11,500 · One way: adult ₩12,000 / child ₩9,000",
                claim="“Cable Car Hours: 10:00–10:30”", status=C, src="CABLECAR",
                note="Itinerary's cable-car hours are wrong — they match the observatory's weekday closing instead. If you ride the shuttle bus up (plan step 1), you don't need a cable-car ticket at all. Fares per N Seoul Tower's official cable-car page; hours per the cable car operator."),
            row("Lotte Department Store — Myeongdong Main Store", "81, Namdaemun-ro, Jung-gu (directly across from the hotel)",
                hours="10:30–20:00 · extended days (Fri–Sun/holidays) 10:30–20:30",
                claim="“Lotte/Shinsegae 10:30–8:00pm weekdays, 10:30–8:30pm weekends”", status=V, src="Lotte",
                note="Matches official listing. Note: department stores close one day most months — check the official page for the November closure day before planning a big shop."),
            row("Shinsegae Department Store — Main Store", "63, Sogong-ro, Jung-gu (Hoehyeon Stn, Line 4)",
                hours="Mon–Thu 10:30–20:00 · Fri–Sun 10:30–20:30 · restaurants 11:00–21:30",
                claim="“Lotte/Shinsegae 10:30–8:00pm weekdays, 10:30–8:30pm weekends”", status=V, src="SHINSEGAE_VK",
                note="Matches Korea Tourism Organization listing. Monthly closure day varies — confirm on shinsegae.com for November."),
            row("Olive Young — Myeongdong Town (flagship)", "53, Myeongdong-gil, Jung-gu",
                hours="10:00–22:30 daily (incl. weekends & holidays)",
                claim="“Olive Young 8:00–12:00am”", status=C, src="OLIVEYOUNG",
                note="Itinerary hours do NOT match the official store page. Plan K-beauty shopping between 10:00 and 22:30. Other Myeongdong branches keep similar hours but verify per store."),
            row("Cosmetics / brand stores (general)", "Myeongdong shopping streets",
                claim="“Major brands 10:00–10:00pm”", status=U,
                note="No single official source covers all brand stores; hours vary by shop. Left unverified rather than guessed."),
            row("Myeongdong street-food stalls", "Myeongdong main streets (evenings)",
                claim="“Most stalls 11:00–10:00pm, some until 11:00pm”", status=U,
                note="Informal stalls have no official posted hours. Left unverified."),
            row("Gwangjang Market — food street", "88, Changgyeonggung-ro, Jongno-gu (Jongno 5-ga Stn, Line 1)",
                hours="Food street 09:00–23:00 · General market 09:00–18:00",
                days="Food street open year-round · General market closed Sundays",
                claim="“Hours: 9:00–11:00pm (some stalls until 2:00am)”", status=P, src="GWANGJANG_VK",
                note="Official Korea Tourism Organization hours: food street 09:00–23:00 daily. “Open until 2 AM” is unverified — plan to finish by 23:00. Individual stalls set their own days off."),
            row("Mangwon Market (alternative)", "27, Poeun-ro 6-gil, Mapo-gu (Mangwon Stn, Line 6, Exit 2)",
                hours="Daily 10:00–21:00 (varies by store)",
                claim="“Or go to Mangwon Market — less touristy”", status=V, src="MANGWON_VS",
                note="Per Visit Seoul (Seoul Tourism). Note it closes earlier than Gwangjang's food street — go for lunch/early evening, not late night."),
            row("Myeongdong Kyoja — main restaurant", "129, Toegye-ro, Jung-gu (relocated 2026; near Myeongdong Station)",
                hours="10:30–21:00", days="Closed only on Seollal & Chuseok day",
                claim="“Myeongdong Kyoja — Michelin hand-made dumplings, may be a line”", status=V, src="KYOJA",
                note="⚠️ RELOCATED in 2026. Many guides (incl. the MICHELIN Guide page) still show the old 29 Myeongdong 10-gil address — use the official site's 129 Toegye-ro. MICHELIN Guide listing confirms the restaurant; famous for kalguksu + mandu."),
            row("Crystal Jade — Shinsegae Main Store B1", "B1, Shinsegae Dept Store Main Branch, 63 Sogong-ro, Jung-gu",
                hours="Weekdays 10:30–20:00 · Weekends 10:30–20:30 (follows department store)",
                claim="“Crystal Jade — 2 locations in Myeongdong; go to Shinsegae Dept Store, basement”",
                status=P, src="CRYSTALJADE",
                note="⚠️ Closes 20:00 on Mondays (department-store hours; last order earlier) — workable only as an early dinner, not after night-market exploring. “2 locations in Myeongdong” not confirmed on the official page checked."),
            nv("Pig Restaurant 2 (Itaewon)", claim="“Eat at Pig Restaurant 2 — Premium Quality — Itaewon”"),
            nv("Hongojib (solo BBQ)", claim="“full BBQ for 1 for only $10”",
               note="No official source confirmed; “$10” price also unverified."),
            nv("Myeongdong Sookhee (bar)", claim="“Bars: Myeongdong Sookhee”"),
        ],
        flags=["F3", "F5", "F6", "F7", "F8", "F9", "F13", "F16"],
    ),
    dict(
        n=3, slug="day-3", dow="Tuesday", date="Nov 3, 2026",
        title="Gyeongbokgung Palace + Bukchon Hanok Village",
        area="Jongno · Anguk · Bukchon",
        alert="🚨 <b>This day does not work as written:</b> Gyeongbokgung Palace is <b>closed every Tuesday</b>, and the Royal Guard Changing Ceremony does not run on Tuesdays. Tue Nov 3, 2026 is not a Korean public holiday, so the holiday exception does not apply. <b>Suggested fix:</b> swap Day 3 with Day 4 (Wed) or Day 6 (Fri). Bukchon + Cafe Onion still work on Tuesday — see the Flagged for Review page.",
        plan=[
            "Gyeongbokgung Palace — main Joseon palace; Royal Guard Changing Ceremony (10:00 / 14:00); allow 3–4 hours (itinerary estimate).",
            "Lunch at a traditional restaurant near the palace (no venue named).",
            "Bukchon Hanok Village — traditional houses, photo spots, craft shops. Cafe Onion Anguk (arrive before opening — expect a line).",
            "Traditional tea house / tea ceremony experience (no venue named).",
        ],
        getting=[
            ("Hotel → Gyeongbokgung", "Line 2 Euljiro 1-ga → Euljiro 3-ga, transfer Line 3 → Gyeongbokgung Station. Gwanghwamun Station (Line 5) also serves the palace's main gate."),
            ("Palace → Bukchon / Cafe Onion", "Walk east toward Anguk Station (Line 3). Cafe Onion Anguk is ~3 min from Anguk Exit 3 (official store page)."),
            ("Bukchon timing rule", "Tourist sightseeing in the Red Zone (Bukchon-ro 11-gil) is allowed <b>10:00–17:00 only</b> — be out of the residential alleys by 17:00."),
        ],
        rows=[
            row("Gyeongbokgung Palace", "161, Sajik-ro, Jongno-gu (Gyeongbokgung Stn, Line 3 / Gwanghwamun Stn, Line 5)",
                hours="Nov–Dec 09:00–17:00 · final admission 16:00",
                days="🛑 CLOSED TUESDAYS (if Tue is a public holiday, closed the next business day instead)",
                cost="Adults 19–64: ₩3,000 · Free: under 19 & 65+ (per Korea Tourism Organization)",
                claim="“Nov–Feb 9:00–5:00pm, last admission 4:00; Closed Tuesdays; Admission 3,000 KRW (~$2.30), free under 19 / over 65”",
                status=C, src="PALACE",
                note="Every factual claim in the itinerary checks out against the palace's official page — except the plan schedules the visit on a Tuesday, when the palace is closed. Nov 3, 2026 is not a Korean public holiday (Korea Tourism Organization 2026 holiday list — no November holidays), so the exception does not apply. Free-entry ages per Korea Tourism Organization; official palace page lists ₩3,000 for ages 19–64."),
            row("Royal Guard Changing Ceremony", "Gwanghwamun / Heungnyemun Gate plaza, Gyeongbokgung",
                hours="10:00 & 14:00 (20 min) — ❌ not held on Tuesdays",
                claim="“Changing of the guard (10:00 AM, 2:00 PM, closed on Tuesdays)”", status=C, src="GUARD",
                note="Times verified via the Korea Heritage Agency, which also states the ceremony is excepted on Tuesdays (palace closure). On a swapped day, the 10:00 ceremony pairs well with a 09:00 palace entry."),
            row("Korea 2026 public holidays (check)", "—",
                days="No public holidays in November 2026",
                claim="—", status=V, src="HOLIDAYS_VK",
                note="Confirms Nov 3, 2026 is a regular Tuesday for all closure rules on this trip."),
            row("Bukchon Hanok Village (Red Zone rules)", "Bukchon-ro 11-gil area, Jongno-gu (Anguk Stn, Line 3)",
                hours="Tourist visiting allowed 10:00–17:00 · Restricted 17:00–10:00 next day (₩100,000 fine)",
                claim="“Bukchon Hanok Village — photo opportunities, craft shops” (no hours noted)", status=P, src="BUKCHON_SMG",
                note="Seoul Metropolitan Government rule, enforced since Mar 1, 2025 — missing from the itinerary. It's a lived-in residential area: keep voices down, don't photograph into homes. Shops/cafés you are a customer of are exempt from the restriction."),
            row("Cafe Onion — Anguk (Onion Anguk)", "5, Gyedong-gil, Jongno-gu (Anguk Stn, Line 3, Exit 3, ~3 min)",
                hours="Mon–Fri 07:00–22:00 · Weekends & holidays 09:00–22:00 · last order 21:30",
                days="Open year-round", claim="“Cafe Onion Anguk, in Hanok (arrive before it opens, there will be a line)”",
                status=V, src="ONION",
                note="Tuesday Nov 3 is a weekday → opens 07:00. If Day 3 is swapped because of the palace closure, recheck which day's opening time applies (weekend = 09:00)."),
            nv("Lunch — “traditional restaurant near palace”", claim="“Lunch at traditional restaurant near palace”",
               note="No venue named in the itinerary, so nothing to verify."),
            nv("Traditional tea house / tea ceremony", claim="“Operating Hours: Typically 12:00–9:00, some open until 10:00”",
               note="No venue named; “typical hours” cannot be verified against an official source."),
        ],
        flags=["F1", "F2", "F10"],
    ),
    dict(
        n=4, slug="day-4", dow="Wednesday", date="Nov 4, 2026",
        title="Seongsu — “the Brooklyn of Seoul” (+ DDP)",
        area="Seongsu-dong · Dongdaemun (DDP)",
        alert="⚠️ <b>Geography check:</b> the Dongdaemun Design Plaza (DDP) is in <b>Dongdaemun</b>, not Seongsu — and the itinerary's description (“industrial warehouses converted into flagship fashion pop-ups & artisan bakeries”) actually describes <b>Seongsu-dong's</b> café street. Both are on Subway Line 2, so combining them is easy, but budget the extra hop. Also: most Day 4 indie shops/cafés could not be confirmed from official sources — their hours are left blank and flagged rather than guessed.",
        plan=[
            "Solsot (Seongdong-gu) — stone-pot rice with sides; “come before opening time.”",
            "Dongdaemun Design Plaza (DDP).",
            "Hanjungsun — fruit mochi · Caricature portrait · Eternalog photo booth.",
            "Shopping/cafés: Blue Elephant (eyewear) · Cafe Far Ben (pistachio latte) · Cafe Onion · Rain Report Cafe · Jayeondo Sogeumppang (salt bread) · Musina Standard · Marge Sherwood · Ader Error · Brandy Melville.",
            "Break Silence — R&B & cocktails.",
            "Dinner: Chuncheongol Dakgalbi, or Uri Wang Galbitang.",
        ],
        getting=[
            ("Hotel → Seongsu", "Line 2 direct: Euljiro 1-ga → Seongsu Station (same line as the hotel — no transfer). Seongsu café street clusters around Yeonmujang-gil, a short walk from the station."),
            ("Seongsu ↔ DDP", "Line 2: Seongsu → Wangsimni → Dongdaemun History & Culture Park Station; DDP connects directly to that station (official DDP page)."),
        ],
        rows=[
            row("Dongdaemun Design Plaza (DDP)", "281, Eulji-ro, Jung-gu (Dongdaemun History & Culture Park Stn, Lines 2·4·5)",
                hours="10:00–20:00 (some spaces vary by program)", days="Closed Jan 1, Seollal & Chuseok day",
                cost="Free entry to public spaces; exhibitions/events ticketed separately",
                claim="“DDP — industrial warehouses converted into flagship fashion pop-ups & artisan bakeries”",
                status=P, src="DDP",
                note="Hours/closures verified on DDP's official site. The warehouse-conversion description belongs to Seongsu-dong, not DDP (a Zaha Hadid cultural complex). Address per Korea Tourism Organization."),
            nv("Solsot — Seongdong-gu", claim="“Stone pot rice dish w/ sides, $7–$14, come before opening time”",
               note="No official source confirmed; opening time and price range unverified."),
            nv("Hanjungsun (fruit mochi)"),
            nv("Caricature (animated portrait)", note="No venue named in the itinerary, so nothing to verify."),
            nv("Eternalog (photo booth)"),
            nv("Blue Elephant (eyewear, Seongsu)",
               note="Brand exists, but the Seongsu store's hours were not confirmed from an official source in this pass."),
            nv("Cafe Far Ben (pistachio latte)"),
            nv("Cafe Onion — Seongsu branch",
               note="The Anguk branch's hours are verified (Day 3). Seongsu branch hours were not pulled from the official store list in this pass — left blank rather than copied across."),
            nv("Rain Report Cafe (listed again on Day 6 — same or different branch?)"),
            nv("Jayeondo Sogeumppang — Seongsu (salt bread)", claim="“Jayeondo Sogeumppang — salt bread”",
               note="No official website found. Third-party listings conflict (09:00–22:00 vs 11:00–20:00) — left blank per rules; check on the day. Sells out early per multiple unofficial reports (not verified)."),
            nv("“Musina Standard” (likely MUSINSA STANDARD)", claim="“Musina Standard — basics store”",
               note="Name in itinerary appears misspelled; Seongsu store hours not confirmed from MUSINSA's official channels in this pass."),
            nv("Marge Sherwood (handbags, Seongsu)",
               note="Store-specific hours not confirmed from an official source in this pass."),
            nv("Ader Error (streetwear)",
               note="Which location isn't stated; store hours not confirmed from an official source in this pass."),
            nv("Brandy Melville",
               note="Which location isn't stated; store hours not confirmed from an official source in this pass."),
            nv("Break Silence (R&B & cocktails)"),
            nv("Chuncheongol Dakgalbi (dinner)", claim="“unlimited lettuce and perilla wraps”"),
            nv("Uri Wang Galbitang", claim="“located in Gangdong. Favorite of Ikseon-dong”",
               note="⚠️ The itinerary is self-contradictory: Gangdong-gu is far east Seoul, Ikseon-dong is central Jongno. One of the two is wrong — flagged for the owner to clarify which restaurant/area is meant."),
        ],
        flags=["F11", "F13", "F16", "F18", "F19"],
    ),
    dict(
        n=5, slug="day-5", dow="Thursday", date="Nov 5, 2026",
        title="Starfield COEX Mall — Gangnam",
        area="Samseong-dong, Gangnam",
        plan=[
            "Subway to Starfield COEX Mall.",
            "“Soul Market” for pastries & coffee (see flag — venue not identified).",
            "Photo with the Gangnam Style statue (COEX East Gate plaza).",
        ],
        getting=[
            ("Hotel → COEX", "Line 2 direct: Euljiro 1-ga → Samseong Station, connected to the mall underground. The itinerary's “47 min” is a door-to-door estimate — no official source states it (see table)."),
        ],
        rows=[
            row("Starfield COEX Mall", "513, Yeongdong-daero, Gangnam-gu (Samseong Stn, Line 2 · Bongeunsa Stn, Line 9)",
                hours="10:30–22:00 daily", days="Open year-round (varies by shop)",
                claim="“Take subway to Starfield COEX Mall (47 min)”", status=P, src="COEX",
                note="Mall hours/address verified on the official Starfield page (and Korea Tourism Organization). The direct Line 2 route from the hotel's station is factual; the 47-minute figure is unverified (depends on walking/waiting). Don't miss the Starfield Library inside (same hours, free — per Visit Seoul)."),
            nv("“Soul Market” (pastries & coffee, COEX)", claim="“Check out Soul Market for pastries & coffee”",
               note="No COEX tenant by this name could be identified from official sources in this pass. The name may be misremembered — flagged for the owner to confirm the intended shop."),
            row("Gangnam Style statue (“Gangnam Hands”)", "Outdoor plaza at COEX East Gate (near Samseong Stn Exit 6)",
                claim="“Take picture with gangnam style statue”", status=P, src="COEX_VK",
                note="Open-air public sculpture on the COEX plaza — no ticket or posted hours. Location relative to COEX confirmed via the mall's official/Korea Tourism Organization listing context; no separate official hours page exists for the statue."),
        ],
        flags=["F12"],
    ),
    dict(
        n=6, slug="day-6", dow="Friday", date="Nov 6, 2026",
        title="Ikseon-dong & Insadong",
        area="Ikseon-dong Hanok alleys · Insadong, Jongno",
        plan=[
            "Chwihyang — pork belly rose pasta.",
            "Rain Report Cafe (Insadong).",
            "Jayeondo Saltbread & House (Ikseon-dong).",
            "“Favorite of Ikseon” restaurant — pork belly rose pasta (same dish as Chwihyang? see flag).",
        ],
        getting=[
            ("Hotel → Ikseon-dong", "Line 2 Euljiro 1-ga → Euljiro 3-ga, transfer Line 3 → Jongno 3-ga Station (Lines 1·3·5). Ikseon Hanok alleys are across from the station area."),
            ("Hotel → Insadong", "Same route to Jongno 3-ga, or Line 3 to Anguk Station for the north end of Insadong-gil."),
        ],
        rows=[
            nv("Chwihyang (pork belly rose pasta)", claim="“Chwihyang — pork belly rose pasta”"),
            nv("Rain Report Cafe — Insadong", claim="“Rain Report Cafe in Insadong”",
               note="Also listed on Day 4 (Seongsu context). Which branch/day is intended is unclear — flagged."),
            nv("Jayeondo Saltbread & House — Ikseon-dong", claim="“Jayeondo Saltbread & House ($8.77 for 4)”",
               note="No official website found. Non-official blogs list ₩12,000 per set of 4 and baking times 6×/day, but that is NOT official — price and hours left blank per rules. Expect queues/sell-outs (unofficial reports)."),
            nv("“Favorite of Ikseon” restaurant", claim="“Favorite of Ikseon (Try pork belly rose pasta $14.50)”",
               note="No venue by this exact name identified from official sources. Note the same signature dish is credited to “Chwihyang” above — possibly the same place noted twice. Price unverified. Flagged for owner clarification."),
        ],
        flags=["F13", "F16", "F19"],
    ),
    dict(
        n=7, slug="day-7", dow="Saturday", date="Nov 7, 2026",
        title="Itaewon",
        area="Itaewon, Yongsan-gu",
        alert="⚠️ <b>No plan yet:</b> the itinerary has only the heading “Itaewon” for this day — no venues, times, or restaurants. Nothing to verify. One cross-reference: “Pig Restaurant 2 — Itaewon” appears as a Day 2 dinner option and could belong here. See Flagged for Review.",
        plan=["(Empty in the itinerary — to be planned.)"],
        getting=[
            ("Hotel → Itaewon", "For when the day is planned: Itaewon Station is on Line 6. From the hotel, Line 2 → Sindang, transfer Line 6 → Itaewon. (Route only; no itinerary claims to verify.)"),
        ],
        rows=[
            nv("Day 7 activities", claim="“Day 7: Saturday - Itaewon (Nov 7)” — heading only",
               note="Incomplete: no entries to verify. Flagged as a planning gap (F4)."),
        ],
        flags=["F4"],
    ),
    dict(
        n=8, slug="day-8", dow="Sunday", date="Nov 8, 2026",
        title="Open day — Seoul",
        area="Seoul (TBD)",
        alert="⚠️ <b>No plan yet:</b> Day 8 is completely blank in the itinerary. Two practical notes for filling it: (1) it's a <b>Sunday</b> — Gwangjang Market's general market is closed Sundays (food street open); (2) if Day 3's palace visit needs a new home because of the Tuesday closure, this open Sunday <i>could</i> host it — the palace is open Sundays (Nov hours 09:00–17:00, verified). Decision is the travelers' — flagged, not changed.",
        plan=["(Empty in the itinerary — to be planned.)"],
        getting=[],
        rows=[
            nv("Day 8 activities", claim="“Day 8: Sunday - (Nov 8)” — blank",
               note="Incomplete: no entries to verify. Flagged as a planning gap (F4). Last full day in Seoul before the Busan transfer."),
        ],
        flags=["F4"],
    ),
    dict(
        n=9, slug="day-9", dow="Monday", date="Nov 9, 2026",
        title="Seoul → Busan (KTX) — Haeundae",
        area="Myeongdong → Seoul Station → Busan → Haeundae",
        plan=[
            "Check out of Stanford Hotel by 12:00; aim to leave by 10:00.",
            "Uber/taxi to Seoul Station. Be at the KTX ~45 min early to secure luggage space (itinerary's own buffer).",
            "KTX to Busan (itinerary estimates 2 h 45 min — varies by train, see table).",
            "Uber/taxi Busan Station → L7 Haeundae by LOTTE HOTELS. Check in & relax.",
            "Optional walk toward Haeundae Beach; evening street food at Haeundae Market (hotteok, tteokbokki, mandu, Korean fried chicken, seafood).",
        ],
        getting=[
            ("Hotel → Seoul Station", "Taxi (itinerary's choice) or Line 4 Myeongdong → Seoul Station (2 stops via Hoehyeon). With luggage, the taxi is the low-stress option."),
            ("Seoul Station → Busan Station", "KTX high-speed train. Book on Korail's official site/app — tickets open ~1 month ahead; pick the train by its stated journey time (stops vary)."),
            ("Busan Station → Haeundae (subway option)", "Line 1 Busan Station → Seomyeon, transfer Line 2 → Haeundae Station; hotel and market are in the Haeundae Station/beach area. Itinerary chooses taxi — fine with bags."),
        ],
        rows=[
            row("Stanford Hotel Myeongdong — check-out", "84, Namdaemun-ro, Jung-gu, Seoul",
                hours="Check-out until 12:00 (late check-out ₩20,000/hr, subject to occupancy)",
                claim="“Check out by 12:00pm. Try to leave by 10:00am”", status=V, src="STANFORD_FAQ",
                note="Matches official hotel policy. The 10:00 departure is the travelers' buffer — good practice for a KTX morning."),
            row("KTX — Seoul Station → Busan Station", "Seoul Station (Lines 1·4, AREX) → Busan Station (Line 1)",
                hours="First/last trains & exact journey time depend on the specific train — see Korail booking",
                cost="(left blank — see note)",
                claim="“Takes 2 hours and 45 minutes to get to Busan”", status=P, src="KORAIL",
                note="Journey time varies by stopping pattern: fastest services ≈2 h 15 min; trains with more stops run longer (≈2 h 30–45 min+). “2 h 45” is plausible for a stopping service but is NOT a fixed official value. Fare: Korail publishes fares only in its live booking system, and third-party reports conflict after the reported Sep 1, 2026 Korail–SR merger/fare adjustment (₩59,800 vs ₩54,400 standard) — so the fare is left blank. Verify both time and fare for your exact train at korail.com."),
            row("L7 Haeundae by LOTTE HOTELS", "55, Haeun-daero 570beon-gil, Haeundae-gu, Busan · +82-51-771-1000",
                hours="(check-in/out left blank — see note)",
                claim="“Take uber/taxi to L7 Haeundae Lotte Hotel; check in & relax”", status=P, src="L7",
                note="Name, address and phone verified on Lotte Hotels' official site. Check-in/check-out times could not be read from a static official page (the official site is JavaScript-driven), so they are left blank per the verification rules — confirm in your booking. Traveler task: if the KTX gets in early, ask about luggage drop."),
            row("Haeundae Beach", "264, Haeundaehaebyeon-ro, Haeundae-gu, Busan",
                hours="Beach admin hours listed 09:00–18:00 · Free",
                claim="“Walk from hotel toward Haeundae Beach”", status=V, src="HAEUNDAE_BEACH",
                note="November is outside the summer swimming season — this is a scenic walk, not a swim. Boardwalk/promenade strolling works any time."),
            row("Haeundae Market (Haeundae Traditional Market)", "22-1, Gunam-ro 41beon-gil, Haeundae-gu (Haeundae Stn, Line 2)",
                hours="09:00–22:00 (varies by store)", days="Open year-round",
                claim="“Evening: Haeundae Market street food — hotteok, tteokbokki, mandu, fried chicken, seafood”",
                status=V, src="HAEUNDAE_MKT",
                note="Hours/address verified via Busan's official tourism board (Visit Busan); Korea Tourism Organization agrees (09:00–22:00, varies by store). Food stalls peak late afternoon/evening — fits the plan."),
        ],
        flags=["F14", "F15"],
    ),
]

# ---------------------------------------------------------------- flagged items
# (id, severity, title, detail, source_key or None, related)
FLAGGED = [
    ("F1", "Critical", "Day 3: Gyeongbokgung Palace is CLOSED on Tuesdays — and Day 3 is Tuesday Nov 3, 2026",
     "The palace's official page: closed Tuesdays; Nov hours 09:00–17:00 (last admission 16:00) on open days. Nov 3, 2026 is not a Korean public holiday (no November holidays in 2026 per Korea Tourism Organization), so the holiday exception does not apply. Suggested fix (travelers' call): swap Day 3 with Day 4 (Wed), Day 6 (Fri), or the empty Day 8 (Sun).",
     "PALACE", "Day 3"),
    ("F2", "Critical", "Day 3: No Royal Guard Changing Ceremony on Tuesdays",
     "Korea Heritage Agency: ceremony at 10:00 & 14:00 except Tuesdays (palace closure). Same fix as F1.",
     "GUARD", "Day 3"),
    ("F3", "Check", "Trip year reads “2006” in the itinerary — assumed 2026",
     "Day 2 is dated “Nov 2, 2006.” Every weekday/date pair in the plan (Nov 2 = Monday … Nov 9 = Monday) matches November 2026 exactly, so the site is built for Oct 31 – Nov 9, 2026. Please confirm the year.",
     None, "Whole trip"),
    ("F4", "Check", "Days 7 (Itaewon) and 8 are empty",
     "Day 7 has only the heading “Itaewon”; Day 8 is blank. Cross-reference: “Pig Restaurant 2 — Itaewon” sits in the Day 2 dinner options and may belong on Day 7. Day 8 (Sunday) could absorb the displaced palace visit (F1) — the palace is open Sundays.",
     None, "Days 7–8"),
    ("F5", "Mismatch", "Olive Young hours in the itinerary (8:00–24:00) don't match the official store page (10:00–22:30)",
     "Olive Young Myeongdong Town's official store site lists 10:00–22:30 daily. Early-morning or post-22:30 beauty runs won't work there.",
     "OLIVEYOUNG", "Day 2"),
    ("F6", "Mismatch", "N Seoul Tower times are ambiguous + plan mixes bus and cable car",
     "Itinerary: “Observatory 10:00-10:30 / Cable Car 10:00-10:30.” Official: observatory weekdays 10:00–22:30 (last entry 22:00), weekends –23:00; cable car 10:00–23:00. Also, step 1 says “take bus” but the budget line is for a cable-car ticket — the shuttle bus (₩1,500) makes the cable car unnecessary. Pick one way up.",
     "TOWER_HOURS", "Day 2"),
    ("F7", "Unverified", "Gwangjang Market “some stalls open until 2:00 AM” is not supported by the official listing",
     "Korea Tourism Organization: food street 09:00–23:00 (year-round), general market 09:00–18:00 (closed Sundays). Plan the evening to end by 23:00.",
     "GWANGJANG_VK", "Day 2"),
    ("F8", "Mismatch", "Crystal Jade (Shinsegae B1) closes at 20:00 on Mondays — conflicts with its slot as a late dinner option",
     "Crystal Jade Korea's official store page ties its hours to the department store (weekdays 10:30–20:00). On Monday Nov 2 it only works as an early dinner, before — not after — night-market time. The itinerary's “2 locations in Myeongdong” also wasn't confirmed on the official page.",
     "CRYSTALJADE", "Day 2"),
    ("F9", "Changed", "Myeongdong Kyoja's main restaurant RELOCATED in 2026 — old address still circulates",
     "Official site: main restaurant now at 129 Toegye-ro, Jung-gu (10:30–21:00, closed only Seollal/Chuseok day). The MICHELIN Guide and older listings still show 29 Myeongdong 10-gil. Navigate to the official address.",
     "KYOJA", "Day 2"),
    ("F10", "Missing", "Bukchon Hanok Village has legal tourist visiting hours (10:00–17:00) that the itinerary omits",
     "Seoul Metropolitan Government: in the Red Zone (Bukchon-ro 11-gil) tourist sightseeing is restricted 17:00–10:00, with ₩100,000 fines, enforced since Mar 1, 2025. Schedule Bukchon photos before 17:00; it's a residential neighborhood.",
     "BUKCHON_SMG", "Day 3"),
    ("F11", "Mismatch", "Day 4: DDP is in Dongdaemun, not Seongsu — and its description fits Seongsu, not DDP",
     "“Industrial warehouses converted into flagship fashion pop-ups & artisan bakeries” describes Seongsu-dong. DDP is a cultural complex at 281 Eulji-ro (10:00–20:00). Both are on Line 2 — doable in one day, but it's an extra cross-town leg to budget.",
     "DDP", "Day 4"),
    ("F12", "Unverified", "Day 5: “Soul Market” at COEX could not be identified",
     "No COEX tenant by this name was found in official sources during verification. The bakery/coffee shop name may be misremembered — please confirm the intended shop so its hours can be verified.",
     "COEX_VK", "Day 5"),
    ("F13", "Unverified", "All USD ($) prices in the itinerary are unverified estimates",
     "$7 (AREX), $13 (bus), $31 (tower combo), $10 (Hongojib), $7–$14 (Solsot), $8.77 (salt bread), $14.50 (pasta), ~$2.30 (palace). Where an official KRW price exists, the site shows KRW and labels the USD figure as the itinerary's own estimate. No exchange rate was assumed.",
     None, "Whole trip"),
    ("F14", "Check", "KTX “2 h 45 min” is not a fixed time, and the fare must be checked at booking",
     "Seoul→Busan journey time depends on the train's stops (fastest ≈2 h 15 min). Korail shows fares only in its live booking flow, and third-party reports conflict on the standard fare after the reported Sep 1, 2026 Korail–SR integration (₩59,800 vs ₩54,400). Both fields are treated as “verify for your exact train” on korail.com. The 45-min-early arrival is the travelers' own luggage buffer, not a Korail rule.",
     "KORAIL", "Day 9"),
    ("F15", "Check", "L7 Haeundae check-in / check-out times could not be confirmed from a readable official page",
     "Lotte Hotels' official page verifies the hotel, address (55 Haeun-daero 570beon-gil) and phone (+82-51-771-1000), but its check-in/out times sit behind JavaScript and couldn't be captured. Per the no-inference rule they are left blank — please confirm from your booking confirmation.",
     "L7", "Day 9 / Hotels"),
    ("F16", "Unverified", "Independent cafés/shops/bars with no official source confirmed (hours & prices left blank)",
     "Day 2: Pig Restaurant 2, Hongojib, Myeongdong Sookhee. Day 4: Solsot, Hanjungsun, caricature (no venue named), Eternalog, Blue Elephant, Cafe Far Ben, Cafe Onion Seongsu branch hours, Rain Report, Jayeondo Sogeumppang (third-party hours conflict), “Musina Standard” (likely MUSINSA STANDARD — spelling?), Marge Sherwood, Ader Error, Brandy Melville (locations not specified), Break Silence, Chuncheongol Dakgalbi. Day 6: Chwihyang, Jayeondo Saltbread & House, “Favorite of Ikseon.” For these, check the venue's official Instagram/Naver listing on the day — small Seoul shops often post hours only there.",
     None, "Days 2, 4, 6"),
    ("F17", "Mismatch", "AREX: “45 min, $7” merges two different trains, and AREX doesn't reach Myeongdong",
     "Express = 43 min / ₩13,000; All-stop = 59 min / ₩4,150–4,750 (Seoul Metropolitan Government). Both end at Seoul Station — add Line 4 or a taxi to the hotel. With luggage, the 6015 limousine bus (₩17,000, operator-verified) drops nearer the hotel.",
     "SMG_AIRPORT", "Day 1 / Transport"),
    ("F18", "Mismatch", "Day 4 dinner: “Uri Wang Galbitang located in Gangdong. Favorite of Ikseon-dong” — two different areas",
     "Gangdong-gu (far east Seoul) and Ikseon-dong (Jongno, central) are ~40+ minutes apart. One of the two notes is wrong; the venue couldn't be verified until the intended restaurant is clarified.",
     None, "Day 4"),
    ("F19", "Check", "Rain Report Cafe appears on both Day 4 (Seongsu) and Day 6 (Insadong)",
     "Possibly two branches, possibly a duplicate note. Neither branch's hours were confirmable from an official source in this pass. Please confirm which branch belongs on which day.",
     None, "Days 4, 6"),
    ("F20", "Check", "Flight details (airline, flight numbers, times, terminal) are not in the itinerary",
     "Day 1 says only “Flight from SFO to ICN.” Arrival terminal (T1 vs T2) changes AREX times (43 vs 51 min Express) and the bus stop number. Add flight info when booked; hotel check-in is from 15:00, so a morning arrival may mean a luggage-drop wait.",
     "Stanford", "Day 1"),
]

# ---------------------------------------------------------------- hotels
HOTELS = [
    dict(name="Stanford Hotel Myeongdong", nights="Nights 1–8 · Sun Nov 1 → Mon Nov 9, 2026",
         rows=[
             row("Address", "84, Namdaemun-ro, Jung-gu, Seoul (opposite Lotte Department Store; same building as the Apple Store, per hotel FAQ)", status=V, src="STANFORD_FAQ"),
             row("Check-in / Check-out", hours="Check-in from 15:00 · Check-out until 12:00", status=V, src="Stanford"),
             row("Early check-in / late check-out", cost="₩20,000 per hour, subject to occupancy", status=V, src="STANFORD_FAQ",
                 note="Useful if the incoming flight lands early on Nov 1 — not guaranteed."),
             row("Nearest subway", "Euljiro 1-ga Station (Line 2) — hotel FAQ references Exit 7·8; Myeongdong Station (Line 4) is the other walkable option", status=P, src="STANFORD_FAQ",
                 note="Station exit reference verified from the hotel's own FAQ; walking times not stated officially — check a map on arrival."),
             row("From ICN Airport", "Limousine bus 6015/6001 toward Myeongdong, or AREX → Seoul Station → Line 4/taxi", status=V, src="LIMOBUS",
                 note="See the Transport page for the verified comparison."),
         ]),
    dict(name="L7 Haeundae by LOTTE HOTELS", nights="From Night 9 · Mon Nov 9, 2026 (end date not in itinerary)",
         rows=[
             row("Address", "55, Haeun-daero 570beon-gil, Haeundae-gu, Busan", status=V, src="L7"),
             row("Phone", "+82-51-771-1000", status=V, src="L7"),
             row("Check-in / Check-out", hours="(blank — not confirmable from a readable official page; see flag F15)", status=U, src="L7",
                 note="Confirm from your booking confirmation. The official page is linked for manual review."),
             row("From Busan Station", "Taxi (itinerary's plan), or Subway Line 1 → Seomyeon → Line 2 → Haeundae Station", status=P, src=None,
                 note="Subway route is standard line topology; no official journey-time claim is made. Haeundae Market (09:00–22:00, verified) and the beach are the evening plan."),
             row("Stay end date / departure", status=U,
                 note="The itinerary ends on Day 9 (arrival in Busan). Number of Busan nights and the return journey aren't specified — planning gap to close."),
         ]),
]

# ---------------------------------------------------------------- transport
TRANSPORT_SECTIONS = [
    ("ICN Airport → Stanford Hotel Myeongdong (Day 1)", [
        row("AREX Express (non-stop)", "ICN T1/T2 → Seoul Station, then Line 4 or taxi to Myeongdong",
            hours="43 min (T1) / 51 min (T2) train time", cost="₩13,000 adult", status=V, src="SMG_AIRPORT",
            note="Fastest fixed-time ride into Seoul, reserved seats. Does not stop at Myeongdong — budget the Seoul Station transfer."),
        row("AREX All-stop", "ICN T1/T2 → Seoul Station (stops incl. Hongik Univ., Gimpo Airport)",
            hours="59 min (T1) / 66 min (T2) train time", cost="₩4,150–4,750 adult", status=V, src="SMG_AIRPORT",
            note="Cheapest. Commuter seating, pay by transport card. Handy if you prefer transferring to Line 2 at Hongik Univ. instead — ends closer to Euljiro 1-ga (hotel side)."),
        row("Airport Limousine Bus 6015", "ICN → Myeongdong-area stops (via Mapo · Chungjeongno · Hoehyeon)",
            cost="₩17,000 adult / ₩12,000 child", status=V, src="LIMOBUS",
            note="Simplest with suitcases: bags go in the hold, drop-off near Myeongdong hotels. Journey time is traffic-dependent (not officially fixed). Buy the ticket at the airport counter/kiosk first."),
    ]),
    ("Getting around Seoul from the Myeongdong base", [
        row("Base stations", "Euljiro 1-ga (Line 2) & Myeongdong (Line 4)",
            status=P, src="STANFORD_FAQ",
            note="Line 2 is the workhorse for this trip: Seongsu (Day 4), DDP (Day 4), COEX/Samseong (Day 5) are all direct rides. Line 4 covers Myeongdong→Chungmuro (tower bus) and Seoul Station (KTX day)."),
        row("Day 2 — N Seoul Tower", "Line 4 Myeongdong → Chungmuro Exit 2 → Shuttle Bus 01A/01B (₩1,500, card only) — or board 01A at Myeongdong Cathedral stop",
            status=V, src="TOWER_BUS",
            note="Cars are restricted on Namsan; shuttle bus or cable car (₩15,000 RT) are the ways up. Last shuttle 23:00."),
        row("Day 2 — Gwangjang Market", "Line 2 → Euljiro 4-ga, or Line 1 → Jongno 5-ga", status=V, src="GWANGJANG_VK",
            note="Food street until 23:00 — check the last-train time for your return leg, or taxi back (short hop)."),
        row("Day 3 — Palace / Bukchon / Anguk", "Line 2 → Euljiro 3-ga → Line 3 → Gyeongbokgung or Anguk",
            status=P, src="ONION",
            note="Cafe Onion's official page puts it 3 min from Anguk Exit 3. Bukchon Red Zone sightseeing ends 17:00 (F10). Palace closed Tuesdays (F1)."),
        row("Day 4 — Seongsu & DDP", "Line 2 direct: Euljiro 1-ga → Seongsu; Seongsu → Dongdaemun History & Culture Park (DDP)",
            status=V, src="DDP", note="No transfers needed all day."),
        row("Day 5 — COEX (Gangnam)", "Line 2 direct: Euljiro 1-ga → Samseong (mall-connected)",
            status=P, src="COEX", claim="Itinerary: “47 min”",
            note="Route verified; the 47-minute door-to-door figure is an unverified estimate."),
        row("Day 6 — Ikseon-dong / Insadong", "Line 2 → Euljiro 3-ga → Line 3 → Jongno 3-ga (Ikseon) / Anguk (Insadong)",
            status=P, note="Standard line topology; the Jongno 3-ga area is also a manageable walk from Myeongdong in good weather."),
        row("Transport card", "T-money (or similar) — required for the Namsan shuttle (₩1,500, card only) and best for subway/bus transfers",
            status=V, src="TOWER_BUS", note="Buy/top up at the airport or any convenience store or station machine."),
    ]),
    ("Seoul → Busan (Day 9) and around Haeundae", [
        row("Hotel → Seoul Station", "Taxi (itinerary), or Line 4 Myeongdong → Seoul Station", status=P,
            note="Itinerary leaves the hotel 10:00 for a 12:00 check-out deadline — comfortable buffer either way."),
        row("KTX Seoul Station → Busan Station", "Book at Korail (official)",
            hours="≈2 h 15 min (fastest) to ≈2 h 45 min+ (more stops) — pick by the train's stated time",
            cost="(blank — live fares only; sources conflict post-merger, see F14)", status=P, src="KORAIL",
            note="Tickets typically open ~1 month ahead. The itinerary's “board 45 min early for luggage space” is a sensible personal buffer, not an official requirement."),
        row("Busan Station → L7 Haeundae", "Taxi (itinerary), or Line 1 → Seomyeon → Line 2 → Haeundae Station", status=P,
            note="No official journey-time claim made. With luggage after a long train ride, the taxi is the itinerary's (reasonable) choice."),
    ]),
]

# ---------------------------------------------------------------- rendering
STATUS_CLASS = {V: "ok", P: "warn", C: "bad", U: "mut"}
STATUS_LABEL = {V: "✅ Verified", P: "🟡 Partial", C: "🔴 Conflict", U: "⚪ Unverified"}
NAV = [("Home", "index.html")] + [(f"Day {d['n']}", f"pages/{d['slug']}.html") for d in DAYS] + \
      [("Transport", "pages/transport.html"), ("Hotels", "pages/hotels.html"), ("⚠️ Flagged for Review", "pages/flagged.html")]


def esc(s):
    return html.escape(s or "", quote=True)


_SRC_UPPER = {k.upper(): v for k, v in SRC.items()}


def src_link(key):
    if not key:
        return '<span class="nosrc">No official source found</span>'
    label, url = _SRC_UPPER[key.upper()]
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)} ↗</a>'


def depth_prefix(depth):
    return "" if depth == 0 else "../"


def layout(title, body, depth=0, active=""):
    p = depth_prefix(depth)
    nav = "\n".join(
        f'<a href="{p}{href}" class="{"active" if href == active else ""}">{esc(label)}</a>'
        for label, href in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Korea Trip 2026</title>
<meta name="description" content="Verified day-by-day Korea itinerary for two travelers — Seoul & Busan, Nov 1–9 2026. Every fact checked against official sources.">
<link rel="stylesheet" href="{p}assets/style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="{p}index.html">🇰🇷 Korea Trip <span>Nov 1–9, 2026 · Seoul → Busan</span></a>
  <button class="nav-toggle" aria-label="Toggle navigation" onclick="document.body.classList.toggle('nav-open')">☰</button>
</header>
<nav class="mainnav">{nav}</nav>
<main class="wrap">
{body}
</main>
<footer class="foot">
  <p>Built for two travelers. Facts verified line by line against official sources on 2026-10-21 —
  hours and fares can change, so tap any source link to re-check before you go.
  Unverified items are labeled, never guessed. · <a href="{p}pages/flagged.html">Flagged for Review</a></p>
</footer>
<script src="{p}assets/app.js"></script>
</body>
</html>"""


def table(rows, claim_label="As written in itinerary"):
    out = ['<div class="table-wrap"><table class="data"><thead><tr>'
           "<th>Place / item</th><th>Location</th><th>Hours</th><th>Days open</th><th>Cost (official)</th>"
           f"<th>{esc(claim_label)}</th><th>Status</th><th>Official source</th><th>Notes</th>"
           "</tr></thead><tbody>"]
    for r in rows:
        sc = STATUS_CLASS[r["status"]]
        out.append(
            f'<tr class="st-{sc}">'
            f'<td data-label="Place / item"><b>{esc(r["name"])}</b></td>'
            f'<td data-label="Location">{esc(r["location"]) or "—"}</td>'
            f'<td data-label="Hours">{esc(r["hours"]) or "—"}</td>'
            f'<td data-label="Days open">{esc(r["days"]) or "—"}</td>'
            f'<td data-label="Cost (official)">{esc(r["cost"]) or "—"}</td>'
            f'<td data-label="{esc(claim_label)}"><i>{esc(r["claim"]) or "—"}</i></td>'
            f'<td data-label="Status"><span class="chip {sc}">{STATUS_LABEL[r["status"]]}</span></td>'
            f'<td data-label="Official source">{src_link(r["src"])}</td>'
            f'<td data-label="Notes">{r["note"]}</td></tr>')
    out.append("</tbody></table></div>")
    return "\n".join(out)


def counts(rows):
    c = {V: 0, P: 0, C: 0, U: 0}
    for r in rows:
        c[r["status"]] += 1
    return c


def day_page(d):
    p = "../"
    c = counts(d["rows"])
    alert = f'<div class="alert red">{d["alert"]}</div>' if d.get("alert") else ""
    plan = "\n".join(f"<li>{esc(x)}</li>" for x in d["plan"])
    getting = ""
    if d.get("getting"):
        items = "\n".join(f"<li><b>{esc(k)}:</b> {v}</li>" for k, v in d["getting"])
        getting = f'<section class="card"><h2>🚇 Getting there (from the hotel)</h2><ul class="tight">{items}</ul></section>'
    flags = " · ".join(f'<a href="{p}pages/flagged.html#{f.lower()}">{f}</a>' for f in d.get("flags", []))
    prevnext = ""
    idx = d["n"] - 1
    links = []
    if idx > 0:
        prev = DAYS[idx - 1]
        links.append(f'<a class="btn" href="{prev["slug"]}.html">← Day {prev["n"]}: {esc(prev["title"])}</a>')
    if idx < len(DAYS) - 1:
        nxt = DAYS[idx + 1]
        links.append(f'<a class="btn" href="{nxt["slug"]}.html">Day {nxt["n"]}: {esc(nxt["title"])} →</a>')
    prevnext = f'<div class="prevnext">{" ".join(links)}</div>'
    body = f"""
<div class="crumbs"><a href="{p}index.html">Home</a> › Day {d['n']}</div>
<h1>Day {d['n']} — {esc(d['title'])}</h1>
<p class="meta">📅 {esc(d['dow'])}, {esc(d['date'])} &nbsp;·&nbsp; 📍 {esc(d['area'])} &nbsp;·&nbsp;
<span class="chip ok">{c[V]} verified</span> <span class="chip warn">{c[P]} partial</span>
<span class="chip bad">{c[C]} conflict</span> <span class="chip mut">{c[U]} unverified</span></p>
{alert}
<section class="card"><h2>🗒️ The plan (in the itinerary's own order)</h2><ol class="tight">{plan}</ol></section>
{getting}
<section class="card"><h2>🔎 Verified details — every row sourced</h2>
<p class="hint">✅ Verified = confirmed on an official site · 🟡 Partial = partly confirmed / estimate ·
🔴 Conflict = official source contradicts the plan · ⚪ Unverified = no official source found, values left blank.</p>
{table(d['rows'])}</section>
{f'<p class="flagrefs">⚠️ Flags on this day: {flags} — see the <a href="{p}pages/flagged.html">Flagged for Review</a> page.</p>' if flags else ''}
{prevnext}
"""
    return layout(f"Day {d['n']} — {d['title']}", body, depth=1, active=f"pages/{d['slug']}.html")


def home_page():
    total = {V: 0, P: 0, C: 0, U: 0}
    for d in DAYS:
        for k, v in counts(d["rows"]).items():
            total[k] += v
    cards = []
    for d in DAYS:
        c = counts(d["rows"])
        badge = ""
        if c[C]:
            badge = f'<span class="chip bad">{c[C]} conflict</span>'
        elif d["n"] in (7, 8):
            badge = '<span class="chip warn">not planned yet</span>'
        cards.append(f"""
<a class="daycard" href="pages/{d['slug']}.html">
  <div class="dc-top"><span class="dc-day">DAY {d['n']}</span><span class="dc-date">{esc(d['dow'][:3])} · {esc(d['date'].replace(', 2026',''))}</span></div>
  <h3>{esc(d['title'])}</h3>
  <p class="dc-area">📍 {esc(d['area'])}</p>
  <p class="dc-meta"><span class="chip ok">{c[V]} verified</span> <span class="chip mut">{c[U]} unverified</span> {badge}</p>
</a>""")
    body = f"""
<section class="hero">
  <h1>Korea, day by day — verified.</h1>
  <p class="lede">Two travelers · SFO → Seoul (Myeongdong base) → Busan (Haeundae) · <b>Nov 1–9, 2026</b>.
  Open today's card and you know the plan: where, when it opens, what it costs, and how to get there —
  every claim checked against an <b>official source</b>, anything we couldn't confirm clearly labeled instead of guessed.</p>
  <p class="countdown" id="countdown">📆 <span id="cd-text">Trip starts Sun Nov 1, 2026</span></p>
  <div class="stats">
    <div class="stat ok"><b>{total[V]}</b><span>verified facts</span></div>
    <div class="stat warn"><b>{total[P]}</b><span>partial / estimates</span></div>
    <div class="stat bad"><b>{total[C]}</b><span>plan conflicts</span></div>
    <div class="stat mut"><b>{total[U]}</b><span>unverified — flagged</span></div>
  </div>
</section>

<div class="alert red">
  🚨 <b>Read first — Day 3 needs a change:</b> Gyeongbokgung Palace and its Royal Guard Ceremony are
  <b>closed on Tuesdays</b>, and Day 3 is Tuesday Nov 3. Swap it with Day 4, 6, or the open Day 8.
  Full list of issues & evidence: <a href="pages/flagged.html"><b>Flagged for Review →</b></a>
</div>

<h2 class="section-title">🗓️ The 9 days</h2>
<div class="grid">{''.join(cards)}</div>

<h2 class="section-title">🧭 Plan the logistics</h2>
<div class="grid">
  <a class="daycard" href="pages/transport.html"><h3>🚇 Transport</h3>
    <p class="dc-area">ICN airport transfers compared (AREX vs limousine bus), subway routes from the Myeongdong base for every day, and the KTX run to Busan — with official fares and times where they exist.</p></a>
  <a class="daycard" href="pages/hotels.html"><h3>🏨 Hotels</h3>
    <p class="dc-area">Stanford Hotel Myeongdong (8 nights) and L7 Haeundae by LOTTE HOTELS — verified addresses and check-in/out policies, next to each day's first move.</p></a>
  <a class="daycard" href="pages/flagged.html"><h3>⚠️ Flagged for Review</h3>
    <p class="dc-area">Every irregularity found while verifying: the Tuesday palace closure, wrong shop hours, a relocated restaurant, empty Days 7–8, and everything we could NOT verify — each with its evidence link.</p></a>
</div>

<section class="card">
<h2>📌 How to read this site</h2>
<ul class="tight">
<li><b>Each day page</b> keeps the itinerary's own order, then shows a sourced table: location, hours, days open, official price.</li>
<li><span class="chip ok">✅ Verified</span> confirmed on the venue's/operator's/government's site &nbsp;
<span class="chip warn">🟡 Partial</span> partly confirmed or a planning estimate &nbsp;
<span class="chip bad">🔴 Conflict</span> official source contradicts the plan &nbsp;
<span class="chip mut">⚪ Unverified</span> no official source found — values left blank on purpose.</li>
<li>Prices in <b>₩ (KRW)</b> are official. Dollar figures come from the original itinerary and are labeled as its estimates.</li>
<li>Hours were verified in October 2026 for a November 2026 trip — seasonal hours (e.g., the palace) are the November ones. Re-check linked sources right before each day.</li>
</ul>
</section>
"""
    return layout("Korea Trip 2026 — verified itinerary dashboard", body, depth=0, active="index.html")


def transport_page():
    sections = ""
    for title, rows_ in TRANSPORT_SECTIONS:
        sections += f'<section class="card"><h2>{esc(title)}</h2>{table(rows_, claim_label="Itinerary claim")}</section>'
    body = f"""
<div class="crumbs"><a href="../index.html">Home</a> › Transport</div>
<h1>🚇 Transport — getting everywhere on this plan</h1>
<p class="meta">Base 1: Stanford Hotel Myeongdong (Seoul) · Base 2: L7 Haeundae (Busan). All fares/times below are official unless a row says otherwise.</p>
<div class="alert">💳 <b>One card for everything:</b> pick up a transport card (e.g., T-money) at the airport — the Namsan shuttle bus is card-only (₩1,500), and subway/bus transfers are simplest by card. The airport <i>limousine bus</i> needs a ticket bought at the airport counter/kiosk before boarding.</div>
{sections}
<section class="card"><h2>🧭 Route map of the trip</h2>
<ol class="tight">
<li><b>Nov 1:</b> SFO → ICN → (AREX or bus 6015) → Stanford Hotel Myeongdong.</li>
<li><b>Nov 2–8:</b> Seoul subway/bus days from Myeongdong (Lines 2 &amp; 4 do most of the work).</li>
<li><b>Nov 9:</b> Taxi/subway → Seoul Station → KTX → Busan Station → taxi (or Line 1→2) → L7 Haeundae.</li>
</ol>
<p class="hint">Return journey from Busan is not in the itinerary yet — see the Hotels page note and Flagged for Review.</p>
</section>
"""
    return layout("Transport", body, depth=1, active="pages/transport.html")


def hotels_page():
    sections = ""
    for h in HOTELS:
        sections += f'<section class="card"><h2>🏨 {esc(h["name"])}</h2><p class="meta">{esc(h["nights"])}</p>{table(h["rows"], claim_label="Detail")}</section>'
    body = f"""
<div class="crumbs"><a href="../index.html">Home</a> › Hotels</div>
<h1>🏨 Hotels — the two bases</h1>
<p class="meta">Everything below is checked against each hotel's official site. Anything we couldn't read on an official page is left blank and flagged — confirm it in your booking.</p>
{sections}
"""
    return layout("Hotels", body, depth=1, active="pages/hotels.html")


def flagged_page():
    sev_class = {"Critical": "bad", "Mismatch": "warn", "Changed": "warn", "Missing": "warn", "Check": "warn", "Unverified": "mut"}
    items = ""
    for fid, sev, title, detail, src, related in FLAGGED:
        items += f"""
<article class="flag {sev_class.get(sev, 'mut')}" id="{fid.lower()}">
  <header><span class="flag-id">{fid}</span><span class="chip {sev_class.get(sev,'mut')}">{esc(sev)}</span>
  <h3>{esc(title)}</h3><span class="flag-rel">{esc(related)}</span></header>
  <p>{detail}</p>
  <p class="flag-src">Evidence: {src_link(src) if src else '<span class="nosrc">From the itinerary itself / absence of an official source — see detail.</span>'}</p>
</article>"""
    body = f"""
<div class="crumbs"><a href="../index.html">Home</a> › Flagged for Review</div>
<h1>⚠️ Flagged for Review</h1>
<p class="meta">Nothing here blocks the trip — but each item needs a human decision or a same-day check.
The itinerary was published <i>as written</i>; conflicts are flagged, never silently “fixed.”
Filter: <button class="fbtn" data-f="all">All</button>
<button class="fbtn" data-f="bad">Critical</button>
<button class="fbtn" data-f="warn">Mismatch / check</button>
<button class="fbtn" data-f="mut">Unverified</button></p>
{items}
<section class="card"><h2>✅ How to clear these flags</h2>
<ol class="tight">
<li><b>Decide the Day-3 swap</b> (F1/F2) — pick the new palace day (Wed/Fri/Sun all work; palace Nov hours 09:00–17:00).</li>
<li><b>Confirm the trip year is 2026</b> (F3) and add flight details (F20) + Busan nights/return plan.</li>
<li><b>Fill Days 7–8</b> (F4) or mark them as rest days on purpose.</li>
<li><b>Same-day checks for indie spots</b> (F16): open the venue's official Instagram/Naver listing the night before; sold-out-prone bakeries (salt bread, Cafe Onion) reward arriving at opening.</li>
<li><b>At booking time:</b> KTX train time/fare (F14) on korail.com; L7 check-in/out (F15) from your confirmation.</li>
</ol></section>
"""
    return layout("Flagged for Review", body, depth=1, active="pages/flagged.html")


CSS = """/* Korea Trip 2026 — mobile-first dashboard */
:root{
  --ink:#14213d; --mut:#5b6b82; --line:#e3e8f0; --bg:#f6f8fb; --card:#fff;
  --blue:#0047a0; --red:#cd2e3a; --ok:#137333; --okbg:#e6f4ea;
  --warn:#8a5a00; --warnbg:#fef7e0; --bad:#a50e0e; --badbg:#fce8e6; --mutbg:#eef1f5;
  --radius:14px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.55;font-size:16px}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:16px 14px 40px}
.topbar{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;
  background:#0f2440;color:#fff;padding:10px 14px}
.brand{color:#fff;font-weight:700;font-size:1.15rem}
.brand:hover{text-decoration:none}
.brand span{display:block;font-weight:400;font-size:.78rem;opacity:.85}
.nav-toggle{background:none;border:1px solid #ffffff55;color:#fff;border-radius:8px;font-size:1.1rem;padding:4px 12px}
.mainnav{display:none;flex-wrap:wrap;gap:6px;background:#0f2440;padding:0 12px 12px}
body.nav-open .mainnav{display:flex}
.mainnav a{color:#dbe7ff;padding:7px 12px;border-radius:999px;border:1px solid #ffffff33;font-size:.9rem}
.mainnav a.active{background:#fff;color:#0f2440;font-weight:700}
.mainnav a:hover{text-decoration:none;background:#1d3a63}
h1{font-size:1.55rem;line-height:1.25;margin:.3em 0 .4em}
h2.section-title{font-size:1.2rem;margin:26px 0 10px}
.meta{color:var(--mut);font-size:.93rem}
.hint{color:var(--mut);font-size:.88rem}
.crumbs{font-size:.85rem;color:var(--mut)}
.hero{background:linear-gradient(135deg,#0f2440,#0047a0);color:#fff;border-radius:var(--radius);padding:22px 18px;margin-top:6px}
.hero h1{margin-top:0;font-size:1.7rem}
.hero .lede{opacity:.95;max-width:65ch}
.countdown{background:#ffffff1f;display:inline-block;padding:6px 14px;border-radius:999px;font-weight:600}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:16px}
.stat{background:#fff;color:var(--ink);border-radius:12px;padding:12px;text-align:center}
.stat b{font-size:1.5rem;display:block}
.stat span{font-size:.8rem;color:var(--mut)}
.stat.ok b{color:var(--ok)} .stat.warn b{color:var(--warn)} .stat.bad b{color:var(--bad)} .stat.mut b{color:var(--mut)}
.alert{background:var(--warnbg);border:1px solid #f0d48a;border-radius:var(--radius);padding:14px 16px;margin:16px 0}
.alert.red{background:var(--badbg);border-color:#f2b8b5}
.grid{display:grid;grid-template-columns:1fr;gap:12px}
.daycard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;color:var(--ink);display:block}
.daycard:hover{text-decoration:none;border-color:var(--blue);box-shadow:0 4px 16px #0047a01f}
.daycard h3{margin:.2em 0 .3em;font-size:1.08rem}
.dc-top{display:flex;justify-content:space-between;font-size:.78rem;letter-spacing:.06em}
.dc-day{font-weight:800;color:var(--blue)} .dc-date{color:var(--mut)}
.dc-area{color:var(--mut);margin:.2em 0 .6em;font-size:.93rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px;margin:16px 0}
.card h2{margin-top:0;font-size:1.12rem}
ul.tight,ol.tight{margin:.3em 0 .3em 1.2em;padding:0}
ul.tight li,ol.tight li{margin:.35em 0}
.chip{display:inline-block;padding:1px 9px;border-radius:999px;font-size:.76rem;font-weight:600;white-space:nowrap}
.chip.ok{background:var(--okbg);color:var(--ok)} .chip.warn{background:var(--warnbg);color:var(--warn)}
.chip.bad{background:var(--badbg);color:var(--bad)} .chip.mut{background:var(--mutbg);color:var(--mut)}
/* tables: cards on mobile, grid on desktop */
.table-wrap{overflow-x:auto}
table.data{width:100%;border-collapse:collapse;font-size:.92rem}
table.data th{text-align:left;background:#0f2440;color:#fff;padding:8px;font-size:.8rem}
table.data td{border-top:1px solid var(--line);padding:8px;vertical-align:top}
table.data tr.st-bad td{background:#fff5f5}
table.data tr.st-ok td:first-child{border-left:4px solid var(--ok)}
table.data tr.st-warn td:first-child{border-left:4px solid #e0a800}
table.data tr.st-bad td:first-child{border-left:4px solid var(--bad)}
table.data tr.st-mut td:first-child{border-left:4px solid #c3ccd8}
.nosrc{color:var(--mut);font-style:italic;font-size:.88rem}
@media (max-width:760px){
  table.data thead{display:none}
  table.data,table.data tbody,table.data tr,table.data td{display:block;width:100%}
  table.data tr{border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:6px 4px;background:#fff}
  table.data td{border:none;padding:4px 10px}
  table.data td::before{content:attr(data-label);display:block;font-size:.7rem;font-weight:700;
    letter-spacing:.05em;color:var(--mut);text-transform:uppercase;margin-bottom:1px}
  h1{font-size:1.32rem}
}
.flag{background:var(--card);border:1px solid var(--line);border-left:6px solid #c3ccd8;border-radius:12px;padding:14px 16px;margin:12px 0}
.flag.bad{border-left-color:var(--bad)} .flag.warn{border-left-color:#e0a800}
.flag header{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.flag h3{margin:.2em 0;font-size:1.05rem;flex:1 1 100%}
.flag-id{font-weight:800;background:#0f2440;color:#fff;border-radius:6px;padding:1px 8px;font-size:.8rem}
.flag-rel{color:var(--mut);font-size:.85rem;margin-left:auto}
.flag-src{font-size:.9rem}
.fbtn{border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 12px;cursor:pointer;font-size:.85rem}
.fbtn.on{background:#0f2440;color:#fff}
.flagrefs{font-size:.92rem}
.prevnext{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.btn{background:#0f2440;color:#fff;padding:10px 16px;border-radius:10px;font-weight:600}
.btn:hover{text-decoration:none;background:#1d3a63}
.foot{border-top:1px solid var(--line);color:var(--mut);font-size:.85rem;padding:18px 14px;max-width:1080px;margin:0 auto}
@media (min-width:761px){
  .grid{grid-template-columns:repeat(3,1fr)}
  .stats{grid-template-columns:repeat(4,1fr)}
  .nav-toggle{display:none}
  .mainnav{display:flex}
  body{font-size:16.5px}
}
@media print{ .topbar,.mainnav,.foot,.prevnext,.nav-toggle{display:none} body{background:#fff} }
"""

JS = """// Korea Trip 2026 — tiny helpers
(function () {
  // Countdown to departure (client-side arithmetic only)
  var el = document.getElementById('cd-text');
  if (el) {
    var start = new Date('2026-11-01T00:00:00+09:00');
    var end = new Date('2026-11-09T23:59:59+09:00');
    var now = new Date();
    if (now < start) {
      var days = Math.ceil((start - now) / 86400000);
      el.textContent = days + (days === 1 ? ' day' : ' days') + ' until takeoff — Sun Nov 1, 2026';
    } else if (now <= end) {
      var dayN = Math.floor((now - start) / 86400000) + 1;
      el.textContent = 'You are on Day ' + dayN + ' of the trip — have a great day!';
    } else {
      el.textContent = 'Trip dates: Nov 1–9, 2026 (completed)';
    }
  }
  // Flag filters
  var btns = document.querySelectorAll('.fbtn');
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      btns.forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var f = b.getAttribute('data-f');
      document.querySelectorAll('.flag').forEach(function (card) {
        card.style.display = (f === 'all' || card.classList.contains(f)) ? '' : 'none';
      });
    });
  });
})();
"""


def main():
    os.makedirs(os.path.join(ROOT, "pages"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    files = {
        "index.html": home_page(),
        "pages/transport.html": transport_page(),
        "pages/hotels.html": hotels_page(),
        "pages/flagged.html": flagged_page(),
        "assets/style.css": CSS,
        "assets/app.js": JS,
        ".nojekyll": "",
    }
    for d in DAYS:
        files[f"pages/{d['slug']}.html"] = day_page(d)
    for path, content in files.items():
        with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote", path)


if __name__ == "__main__":
    main()
