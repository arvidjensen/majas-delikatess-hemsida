#!/usr/bin/env python3
"""
Majas Delikatess - Facebook Backup
Använder en kopia av din Chrome-profil (fungerar även om Chrome är öppet).
Laddar ner alla foton + text + kommentarer per bild.
"""

import os, sys, time, re, zipfile, shutil, random, tempfile
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("Selenium saknas. Kör: pip install selenium")
    sys.exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("webdriver-manager saknas. Kör: pip install webdriver-manager")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup saknas. Kör: pip install beautifulsoup4")
    sys.exit(1)

try:
    import requests as req_lib
except ImportError:
    print("requests saknas. Kör: pip install requests")
    sys.exit(1)

# ============================================================
# KONFIGURATION
# ============================================================
CHROME_USER_DATA = r"C:\Users\jense\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE = "Profile 1"  # AJ-profilen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "majas_delikatess_backup")
ZIP_FILENAME = os.path.join(SCRIPT_DIR, "majas_delikatess_facebook.zip")

PHOTO_IDS = [
    918771860663533, 918771853996867, 912740744599978, 912740664599986,
    906738465200206, 906738418533544, 906738411866878, 901849539022432,
    901132042427515, 901126012428118, 901126002428119, 895998582940861,
    895555706318482, 895555699651816, 892974923243227, 890237466850306,
    890237393516980, 890237390183647, 880908261116560, 870143195526400,
    868018602405526, 867815425759177, 867815369092516, 865463192661067,
    865463185994401, 863718356168884, 861968209677232, 860025589871494,
    860025539871499, 860025533204833, 857680923439294, 857122640161789,
    857122633495123, 856232116917508, 854982057042514, 854982063709180,
    853393367201383, 851075530766500, 851075450766508, 851075447433175,
    850993707441349, 849798450894208, 849798440894209, 849798377560882,
    849798370894216, 846480591225994, 846480577892662, 844954291378624,
    844954234711963, 844954228045297, 844178918122828, 844178911456162,
    841393688401351, 839693045238082, 822938036913583, 820580673815986,
    820580617149325, 820580610482659, 814409754433078, 814409681099752,
    814409674433086, 808934211647299, 808934191647301, 808335175040536,
    808335121707208, 808335115040542, 802828165591237, 802828158924571,
    797757939431593, 797757882764932, 797757872764933, 792988439908543,
    791528226721231, 791528166721237, 791528160054571, 789732576900796,
    789732570234130, 786935937180460, 786272707246783, 783181110889276,
    783181104222610, 781657481041639, 781657411041646, 781657401041647,
    781657331041654, 780834381123949, 780834374457283, 778328948041159,
    776757921531595, 775385731668814, 775385718335482, 775385651668822,
    775385645002156, 729147052959349, 729146966292691, 729146956292692,
    727078096499578, 719435060597215, 718772153996839, 717643917442996,
    716815564192498, 716815504192504, 716815494192505, 714599571080764,
    712944091246312, 711787028028685, 711786974695357, 711786964695358,
    707638231776898, 707638211776900, 706833778524010, 706833718524016,
    706833708524017, 703252705548784, 703252698882118, 702180422322679,
    702180368989351, 700307445843310, 699412099266178, 699412029266185,
    699412019266186, 698275476046507, 697504879456900, 697504826123572,
    697504812790240, 693525926521462, 692346566639398, 692346553306066,
    690658653474856, 687096620497726, 687096563831065, 684739414066780,
    684273224113399, 684273214113400, 684013314139390, 681915007682554,
    681914977682557, 681914957682559, 680154674525254, 677174804823241,
    677174798156575, 676574884883233, 676574838216571, 676574824883239,
    670988475441874, 670988462108542, 665700645970657, 665700582637330,
    662115216329200, 662115196329202, 660533639820691, 660533583154030,
    660533569820698, 655465766994145, 655465746994147, 655465703660818,
    655465686994153, 653806680493387, 653806667160055, 653069603900428,
    653069587233763, 650356340838421, 650356317505090, 650356297505092,
    648023911071664, 646881257852596, 646881244519264, 645352621338793,
    645352491338806, 645352471338808, 640883418452380, 640883408452381,
    640883368452385, 640883355119053, 640127641861291, 640127625194626,
    637103948830327, 637103928830329, 635124922361563, 635124882361567,
    635124869028235, 630499422824113, 630499379490784, 630499362824119,
    625568643317191, 625568589983863, 625568583317197, 621404790400243,
    620856187121770, 620856143788441, 620856133788442, 616019820938740,
    616019767605412, 616019754272080, 607972045076851, 606572198550169,
    603162482224474, 603162468891142, 596994426174613, 596994406174615,
    594824506391605, 594502959757093, 593223816551674, 593223803218342,
    593223766551679, 593223749885014, 592435739963815, 592435726630483,
    589260773614645, 589260736947982, 589260720281317, 587808823759840,
    587808770426512, 587808760426513, 585254684015254, 585194947354561,
    585194934021229, 583606320846757, 583606244180098, 583123650895024,
    583123594228363, 583123587561697, 578327828041273, 578327811374608,
    578327751374614, 578327741374615, 576164881590901, 575471111660278,
    574496365091086, 574496348424421, 573597275180995, 573597261847663,
    573597201847669, 573597195181003, 568753568998699, 568753562332033,
    564230856117637, 563839549490101, 563839499490106, 563839486156774,
    563176536223069, 558888819985174, 558888786651844, 558888769985179,
    556531053554284, 554714827069240, 553844930489563, 553844900489566,
    551220227418700, 551220214085368, 549839740890082, 547834501090606,
    547834457757277, 547834441090612, 543445761529480, 543445721529484,
    543445698196153, 538296115377778, 538296078711115, 538296062044450,
    534578345749555, 534578305749559, 534578289082894, 533856772488379,
    533281979212525, 533281912545865, 533281899212533, 531067892767267,
    531067879433935, 530029772871079, 528659809674742, 528659769674746,
    528659753008081, 526679006539489, 526554376551952, 524265436780846,
    524265423447514, 519735290567194, 519734710567252, 519734693900587,
    516887664185290, 515163417691048, 515163387691051, 515163367691053,
    512725991268124, 510754721465251, 510754704798586, 479242947949762,
    473411908532866, 473411888532868, 469940052213385, 469326465608077,
    469326462274744, 465270492680341, 465270429347014, 465270426013681,
    462408569633200, 461110343096356, 461110323096358, 461110273096363,
    456557756884948, 456557723551618, 456557703551620, 452307053976685,
    452307023976688, 452307007310023, 449131624294228, 447965991077458,
    447965974410793, 447965924410798, 447965914410799, 446693781204679,
    443746191499438, 443746171499440, 439661431907914, 439661421907915,
    439661371907920, 439661361907921, 436589625548428, 435577925649598,
    435577865649604, 435577862316271, 431492286058162, 431492236058167,
    431492212724836, 428949112979146, 428949049645819, 428949046312486,
    427233549817369, 427233349817389, 427233286484062, 427233276484063,
    426541996553191, 425228043351253, 424202643453793, 423106053563452,
    423106046896786, 419759807231410, 419759793898078, 419359747271416,
    419359713938086, 419359693938088, 415394961001228, 415394897667901,
    415394894334568, 413033324570725, 413033317904059, 411506568056734,
    411506551390069, 407496831791041, 407496801791044, 407496791791045,
    405816111959113, 404476592093065, 404018945472163, 403457518861639,
    403457488861642, 403457455528312, 401527559054635, 401422445731813,
    400212225852835, 400212195852838, 399230172617707, 399230145951043,
    399230102617714, 394947396379318, 394947373045987, 391849560022435,
    390872536786804, 390872496786808, 390872486786809, 386772837196774,
    386772793863445, 386772777196780, 384270664113658, 382783404262384,
    382783364262388, 382783337595724, 377781838095874, 375583258315732,
    375583241649067, 373848405155884, 371929918681066, 371929912014400,
    370967445443980, 370967395443985, 367857222421669, 367857172421674,
    367857165755008, 366978115842913, 366978085842916, 366978059176252,
    366377622569629, 366377582569633, 366377572569634, 364760496064675,
    363968489477209, 363278192879572, 361378953069496, 361378939736164,
    360871733120218, 360871699786888, 360871693120222, 360397346500990,
    359495029924555, 359495019924556, 358275346713190, 357962266744498,
    357962256744499, 356927436847981, 355998706940854, 355998683607523,
    355998653607526, 352259093981482, 352259080648150, 352259040648154,
    352259033981488, 349863937554331, 349863924220999, 348891597651565,
    348891587651566, 346327414574650, 345378178002907, 345378164669575,
    345378118002913, 345378108002914, 344890171385041, 342337341640324,
    341638335043558, 341638301710228, 341638295043562, 337914502082608,
    337914492082609, 333655705841821, 333655672508491, 333655662508492,
    329926049548120, 329921042881954, 329921002881958, 328408473033211,
    327352629805462, 326332526574139, 326332483240810, 326332453240813,
    322418530298872, 322418490298876, 322418486965543, 318734810667244,
    318734774000581, 318734767333915, 316979187509473, 315848820955843,
    314982394375819, 314982364375822, 314982347709157, 311685648038827,
    311685614705497, 311685604705498, 308221701718555, 308221658385226,
    308221651718560, 304697268737665, 304697232071002, 304697222071003,
    302688008938591, 274089451798447, 267836795757046, 267836769090382,
    267836762423716, 267648252442567, 266673812540011, 264278936112832,
    264278932779499, 263323352875057, 263323322875060, 263323316208394,
    262028263004566, 262028226337903, 262028223004570, 259510813256311,
    259510763256316, 259510753256317, 257466113460781, 257466083460784,
    257466063460786, 255623030311756, 255543596986366, 255543586986367,
    255543553653037, 255543550319704, 254254353781957, 253650293842363,
    251674690706590, 251674647373261, 251674640706595, 249753894232003,
    249753860898673, 249753854232007, 247469634460429, 247469611127098,
    247469584460434, 247469577793768, 246917801182279, 244469484760444,
    244469464760446, 244469448093781, 243978358142890, 243913751482684,
    243913708149355, 242073991666660, 240029765204416, 240029738537752,
    240029728537753, 236265008914225, 236162848924441, 236162825591110,
    236162818924444, 234223955784997, 233986305808762, 233986202475439,
    232509345956458, 232509315956461, 232509309289795, 231541476053245,
    228960912977968, 228960859644640, 228960872977972, 224985676708825,
    224985653375494, 224985633375496, 222619336945459, 222024403671619,
    221069857100407, 221069823767077, 221069817100411, 218585730682153,
    217079147499478, 217079120832814, 217079110832815, 212772971263429,
    212772931263433, 212772921263434, 211905624683497, 210783538129039,
    210783501462376, 210783498129043, 210783478129045, 210783464795713,
    209230521617674, 209230514951008, 209230488284344, 209230481617678,
    208791428328250, 207720675101992, 207720668435326, 207720638435329,
    207720631768663, 206185245255535, 206185238588869, 206185208588872,
    206185205255539, 204669242073802, 204669232073803, 204388825435177,
    203194768887916, 203194762221250, 203194728887920, 203194718887921,
    201720382368688, 201720375702022, 200367119170681, 200221819185211,
    200221812518545, 199498419257551, 198680729339320, 198680712672655,
    198680692672657, 198680676005992, 198447392695987, 197854032755323,
    196481279559265, 196201116253948, 195618776312182, 195618769645516,
    195618736312186, 195618732978853, 194879526386107, 194069989800394,
    194069959800397, 194069953133731, 192626503278076, 191928960014497,
    191928950014498, 191203630087030, 191203596753700, 191203593420367,
    189897240217669, 189737286900331, 189737256900334, 189737250233668,
    188186410388752, 188186380388755, 188186373722089, 187259023814824,
    187259017148158, 186726507201409, 186726477201412, 186726467201413,
    185811713959555, 185310167343043, 185310137343046, 185310130676380,
    183828220824571, 183828190824574, 183828184157908, 182299397644120,
    182299367644123, 182299360977457, 180924324448294, 180924274448299,
    180924271114966, 179630784577648, 179630781244315, 178830654657661,
    178830651324328, 178255338048526, 178255298048530, 178255291381864,
    176844651522928, 176844644856262, 176844601522933, 176844598189600,
    175458464994880, 175458431661550, 175458414994885, 174389228435137,
    174389041768489, 173995868474473, 173995861807807, 173995818474478,
    173995811807812, 173831271824266, 173831255157601,
    196081016148828, 196080999482163, 196080962815500, 196080956148834,
    194796319610631, 194796286277301, 194796276277302, 194012893022307,
    183469997409930, 181624520927811, 180008497756080, 180008491089414,
    178519361238327, 176913748065555, 176913744732222, 176913688065561,
    176913681398895, 175386304884966, 175386271551636, 175386268218303,
    174444298312500, 174444291645834, 174444248312505, 174444241645839,
    173901535033443, 173901498366780, 173901505033446, 172359581854305,
    172359548520975, 172359541854309, 171640821926181, 171224425301154,
    171224365301160, 171224358634494, 170795012010762,
]


COOKIES_FILE = os.path.join(SCRIPT_DIR, "cookies.json")


def setup_driver():
    """Starta Chrome med no-sandbox (krävs i denna miljö)."""
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver


def load_cookies(driver):
    """Ladda Facebook-cookies från cookies.json (sparade av puppeteer-scrapern)."""
    import json
    if not os.path.exists(COOKIES_FILE):
        print("  VARNING: Ingen cookies.json hittad - du maste logga in manuellt!")
        return False

    # Navigera till FB först (cookies kräver rätt domän)
    driver.get("https://www.facebook.com/")
    time.sleep(2)

    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for cookie in cookies:
        # Selenium kräver att vi anpassar cookie-formatet
        sel_cookie = {
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": cookie.get("domain", ".facebook.com"),
            "path": cookie.get("path", "/"),
            "secure": cookie.get("secure", True),
        }
        # Sätt expiry om det finns (Selenium vill ha int, inte float)
        if cookie.get("expires") and cookie["expires"] > 0:
            sel_cookie["expiry"] = int(cookie["expires"])
        try:
            driver.add_cookie(sel_cookie)
        except Exception:
            pass  # Vissa cookies kan inte sättas (httpOnly etc)

    # Ladda om sidan med cookies
    driver.get("https://www.facebook.com/")
    time.sleep(3)

    # Kolla om vi är inloggade
    if "login" in driver.current_url.lower():
        print("  VARNING: Cookies fungerade inte!")
        return False

    return True


def human_delay(min_sec=1.5, max_sec=4.0):
    time.sleep(random.uniform(min_sec, max_sec))


def scrape_photo_page(driver, photo_id):
    """
    1. Ladda fotosidan -> hämta bild-URL + alt-text från DOM
    2. Klicka 'Visa inlägg' -> hämta inläggstext + kommentarer
    """
    url = f"https://www.facebook.com/photo.php?fbid={photo_id}&set=pb.100075921818044.-2207520000&type=3"

    try:
        driver.get(url)
        time.sleep(random.uniform(4, 6))

        # 1. Hämta bild från DOM (scontent img med stor storlek)
        img_data = driver.execute_script('''
            let imgs = document.querySelectorAll("img");
            for (let img of imgs) {
                if (img.src.includes("scontent") && img.naturalWidth > 100) {
                    return {src: img.src, alt: img.alt || ""};
                }
            }
            return null;
        ''')

        img_url = img_data["src"] if img_data else ""
        alt_text = img_data["alt"] if img_data else ""

        # 2. Klicka 'Visa inlägg' för att komma till posten
        post_text = ""
        kommentarer = []

        post_link = driver.execute_script('''
            let links = document.querySelectorAll("a");
            for (let a of links) {
                if (a.innerText && a.innerText.includes("Visa inl")) return a.href;
            }
            return null;
        ''')

        if post_link:
            driver.get(post_link)
            time.sleep(random.uniform(3, 5))

            # Hämta inläggstext (dir=auto divs med >15 tecken)
            text_blocks = driver.execute_script('''
                let blocks = [];
                document.querySelectorAll("div[dir=auto]").forEach(el => {
                    let t = el.innerText.trim();
                    if (t.length > 15 && t.length < 3000) blocks.push(t);
                });
                return [...new Set(blocks)];
            ''')
            # Filtrera bort knappar/menytext, behåll inläggstext
            post_parts = []
            seen = set()
            skip = ["Maja's Delikatess", "Inga kommentarer", "Bli först med",
                    "Kommentera", "Gilla", "Dela", "Skicka"]
            for block in text_blocks:
                if any(block.startswith(s) for s in skip):
                    continue
                # Dedup: hoppa över om vi redan har denna text
                norm = block.strip().lower()
                if norm in seen:
                    continue
                seen.add(norm)
                post_parts.append(block)
            post_text = "\n".join(post_parts)

            # Klicka 'Visa fler kommentarer' om det finns
            try:
                for _ in range(3):
                    btns = driver.find_elements(
                        By.XPATH,
                        "//span[contains(text(),'Visa') and (contains(text(),'kommentar') or contains(text(),'tidigare'))]"
                    )
                    if btns:
                        driver.execute_script("arguments[0].click();", btns[0])
                        time.sleep(2)
                    else:
                        break
            except Exception:
                pass

            # Hämta kommentarer
            comment_data = driver.execute_script('''
                let comments = [];
                document.querySelectorAll("[role=article]").forEach(art => {
                    let label = (art.getAttribute("aria-label") || "").toLowerCase();
                    if (label.includes("kommentar") || label.includes("comment")) {
                        let text = art.innerText.trim();
                        if (text.length > 3) comments.push(text.substring(0, 500));
                    }
                });
                return comments;
            ''')
            kommentarer = comment_data or []

        return {
            "photo_id": photo_id,
            "url": url,
            "img_url": img_url,
            "alt_text": alt_text,
            "post_text": post_text,
            "kommentarer": kommentarer,
        }

    except Exception as e:
        print(f"  X Fel vid foto {photo_id}: {e}")
        return {
            "photo_id": photo_id,
            "url": url,
            "img_url": "",
            "alt_text": "",
            "post_text": "",
            "kommentarer": [],
        }


def download_image(img_url, filepath, driver):
    """Ladda ner bild via requests med Selenium-cookies"""
    if not img_url:
        return False
    try:
        cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
        headers = {"User-Agent": driver.execute_script("return navigator.userAgent")}

        resp = req_lib.get(img_url, cookies=cookies, headers=headers, timeout=20)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return True
    except Exception as e:
        print(f"    Bildnedladdning misslyckades: {e}")
    return False


def save_info_file(data, filepath):
    """Spara textfil med all info om fotot"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"FOTO ID: {data['photo_id']}\n")
        f.write(f"URL: {data['url']}\n")
        f.write(f"Alt-text: {data['alt_text']}\n")
        f.write(f"\nINLAGGSTEXT:\n{data['post_text']}\n")
        if data["kommentarer"]:
            f.write(f"\nKOMMENTARER ({len(data['kommentarer'])} st):\n")
            for i, k in enumerate(data["kommentarer"], 1):
                f.write(f"  {i}. {k}\n")
        else:
            f.write("\nKOMMENTARER: Inga hittades\n")
        f.write(f"\nBild-URL: {data['img_url']}\n")


def create_zip():
    print(f"\nSkapar ZIP: {ZIP_FILENAME} ...")
    with zipfile.ZipFile(ZIP_FILENAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(OUTPUT_DIR):
            for file in files:
                fp = os.path.join(root, file)
                zf.write(fp, os.path.relpath(fp, os.path.dirname(OUTPUT_DIR)))
    size = os.path.getsize(ZIP_FILENAME) / 1024 / 1024
    print(f"ZIP klar: {ZIP_FILENAME} ({size:.1f} MB)")


BATCH_SIZE = 25  # Foton per batch innan vi startar om Chrome
BATCH_PAUSE = 600  # 10 minuters paus mellan batchar
CONSECUTIVE_FAIL_LIMIT = 5  # Starta om sessionen efter 5 misslyckanden i rad


def main():
    print("=" * 50, flush=True)
    print("  MAJAS DELIKATESS - FACEBOOK BACKUP", flush=True)
    print("  BATCH-LAGE: 25 foton per omgang", flush=True)
    print("=" * 50, flush=True)
    print(f"  Antal foton: {len(PHOTO_IDS)}", flush=True)
    print(f"  Output: {OUTPUT_DIR}/", flush=True)
    print(flush=True)

    # Skapa mappar
    img_dir = os.path.join(OUTPUT_DIR, "bilder")
    info_dir = os.path.join(OUTPUT_DIR, "bildinfo")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(info_dir, exist_ok=True)

    # Filtrera bort redan nedladdade
    remaining = []
    already_done = 0
    for photo_id in PHOTO_IDS:
        img_path = os.path.join(img_dir, f"photo_{photo_id}.jpg")
        info_path = os.path.join(info_dir, f"info_{photo_id}.txt")
        if os.path.exists(img_path) and os.path.exists(info_path):
            already_done += 1
        else:
            remaining.append(photo_id)

    print(f"  Redan nedladdade: {already_done}", flush=True)
    print(f"  Kvar att hamta: {len(remaining)}", flush=True)
    print(flush=True)

    if not remaining:
        print("Alla foton redan nedladdade!", flush=True)
        return

    ok = already_done
    fail = 0
    total = len(PHOTO_IDS)

    # Dela upp i batchar
    batches = [remaining[i:i+BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
    print(f"  Antal batchar: {len(batches)} (a {BATCH_SIZE} foton)", flush=True)

    for batch_num, batch in enumerate(batches, 1):
        print(f"\n{'='*50}", flush=True)
        print(f"  BATCH {batch_num}/{len(batches)} ({len(batch)} foton)", flush=True)
        print(f"{'='*50}", flush=True)

        # Starta ny Chrome-session for varje batch
        print("Startar Chrome...", flush=True)
        driver = setup_driver()
        print("Laddar cookies...", flush=True)
        logged_in = load_cookies(driver)
        if not logged_in:
            print("MISSLYCKAD INLOGGNING - avbryter", flush=True)
            driver.quit()
            break
        print("Inloggad!", flush=True)

        consecutive_fails = 0

        for j, photo_id in enumerate(batch):
            img_path = os.path.join(img_dir, f"photo_{photo_id}.jpg")
            info_path = os.path.join(info_dir, f"info_{photo_id}.txt")

            # Dubbelkolla (kanske nedladdad i mellanrummet)
            if os.path.exists(img_path) and os.path.exists(info_path):
                ok += 1
                continue

            current = ok + fail + 1
            print(f"[{current}/{total}] Foto {photo_id}...", flush=True)

            data = scrape_photo_page(driver, photo_id)

            if data["img_url"]:
                success = download_image(data["img_url"], img_path, driver)
                if success:
                    save_info_file(data, info_path)
                    print(f"  OK", flush=True)
                    ok += 1
                    consecutive_fails = 0
                else:
                    print(f"  X Bild misslyckades", flush=True)
                    fail += 1
                    consecutive_fails += 1
            else:
                print(f"  X Ingen bild", flush=True)
                fail += 1
                consecutive_fails += 1

            # Om manga misslyckanden i rad -> troligen blockerad
            if consecutive_fails >= CONSECUTIVE_FAIL_LIMIT:
                print(f"\n  !!! {CONSECUTIVE_FAIL_LIMIT} misslyckanden i rad - FB blockerar troligen", flush=True)
                print(f"  Avbryter batch och tar langre paus...", flush=True)
                break

            # Mänsklig paus
            human_delay(3, 7)

        # Stäng Chrome efter varje batch
        try:
            driver.quit()
        except Exception:
            pass

        print(f"\nBatch {batch_num} klar: {ok} OK, {fail} misslyckade", flush=True)

        # Paus mellan batchar (om inte sista)
        if batch_num < len(batches):
            pause_min = BATCH_PAUSE // 60
            # Variera pausen lite
            actual_pause = BATCH_PAUSE + random.randint(-60, 120)
            print(f"Pausar ~{pause_min} min innan nasta batch...", flush=True)
            time.sleep(actual_pause)

    print(f"\n{'='*50}")
    print(f"  KLART: {ok} lyckades, {fail} misslyckades")
    print(f"{'='*50}\n")

    create_zip()
    print(f"\nAllt sparat i: {OUTPUT_DIR}/")
    print(f"ZIP: {ZIP_FILENAME}")


if __name__ == "__main__":
    main()
