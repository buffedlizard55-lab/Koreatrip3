# Current-source limitations — 26 October 2026

An HTTP-success fetch is not sufficient verification: error pages, bot challenges,
empty navigation shells and inconsistent translations are treated as failures or
limited evidence. These attempts are listed for traceability, **not as supported
facts**. These are attempted URLs; they are not promised working links.

| Attempted official / candidate source | Observed result | Treatment |
|---|---|---|
| smart.letskorail.com/ebizbf/EbizBfTicketSearchM.do?lang=EN | HTTP404ERROR page | Replaced in current rows with opened korail.com/global/eng/main. No exact timetable/fare inferred. |
| airportlimousine.co.kr/sub/sub01.php | Fetch HTTP 500 | Route 6001 fare, stop and hotel walk remain empty. |
| lottehotel.com/haeundae-l7/en/hotel-overview and /location | Operator page-unavailable response | L7 property identity from working homepage only; exact policy/address fields blank. |
| mdkj.co.kr | 406 Not Acceptable | Do not treat prior-session relocation claims as verified. KTO English/Korean street addresses conflict, so address blank. |
| english.visitseoul.net/PalaceArea/Recommendations-for-Hanok-Caf%C3%A9-in-Seoul/ENN031658/ | 404 | No tea-house or tea ceremony schedule adopted. |
| english.visitseoul.net/restaurants/rainreport/ENP933ykf | 404 | No operating hours, address or closure inferred for Rain Report Insadong. |
| english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=175514 | 400 error page | No closure inferred for Rain Report Seongsu. |
| en.blueelephant.co/product/seongsu-flagship-store/3725/ | Cafe24 browser challenge | Store hours/address blank. |
| instagram.com/solsot_seongsu/ | HTTP 403 | Restaurant details blank; no third-party fallback presented as official verification. |
| instagram.com/cafe.farben/ | HTTP 403 | Café hours, location and pistachio latte claim blank. |
| instagram.com/favorite_ikseon | HTTP 403 | No identity equivalence to Chwihyang assumed; menu/price/hours blank. |
| eternalog-fotobooth.com | Navigation-only content | No branch/location/hours extracted. |
| break-silence.com | Images/categories without sufficient venue identity details | Does not substantiate the intended R&B cocktail bar; hours/location blank. |
| gwangallimdrone.co.kr/en/ | 404 | Replaced with opened /en/overview. Exact trip-date cancellation status not established. |
| visitbusan.net/index.do?menuCd=DOM_000000202001001000 | Site error page | Specific working city destination pages used instead. |

## Conflicting official statements

- **Myeongdong Kyoja:** opened KTO page vcontsId=99925 gives English
  `29 Myeongdong 10-gil` and Korean `서울특별시 중구 퇴계로 129`.
  Exact street address deliberately blank in the integrated dataset.
- **Cheongsapo Daritdol:** opened KTO vcontsId=112698 lists Sep–Nov 09:00–21:00;
  opened Visit Busan skywalk article uc_seq=282 lists 09:00–18:00.
  Exact hours deliberately blank in the row; both sources provided for review.
- **X the SKY:** current opened operator lists adult ₩29,000; older Visit Busan
  entry found in official search lists ₩27,000. Operator listing is used,
  explicitly not the unconfirmed $17.59 reseller deal.
- **Accor walking time:** same operator page uses 1-, 2-, and 5-minute station
  access descriptions. Those refer to differing access points; no precise
  AREX-platform-to-hotel or supplied eight-minute time is adopted.

All current supported references, evidence snippets and methods are recorded in
`current-sources.json`. The integrated site never labels an entire row verified.
