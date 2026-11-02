"""デモサイトのHTMLを生成する。 python tools/build.py

ファイル名は現行サイトのURLスラッグ（/zeimu, /staff ...）に合わせてある。
本番移行時は同じURLで公開すれば、検索順位・被リンクをそのまま引き継げる。
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "site"
ORIGIN = "https://akari-z.com"

OFFICE = {
    "name": "税理士法人ACEあかり事務所",
    "zip": "760-0080",
    "addr": "香川県高松市木太町5050番地17",
    "tel": "087-814-7134",
    "fax": "087-814-7135",
    "hours": "9:00〜17:30",
    "closed": "土・日・祝日",
}
MAP_SRC = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1647.740610001718!2d134.06898102416645"
           "!3d34.31276223658335!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3553ea571a60e401%3A0x9539121c8e846ffd"
           "!2z56iO55CG5aOr5rOV5Lq6QUNF44GC44GL44KK5LqL5YuZ5omA!5e0!3m2!1sja!2sjp!4v1772593034555!5m2!1sja!2sjp")


def u(slug):
    """ローカル確認用のリンク。本番では /slug になる。"""
    return "index.html" if slug == "" else f"{slug}.html"


# CSS/JSの中身から版番号を作る（公開サーバーのキャッシュ対策）
import hashlib
ASSET_VER = hashlib.md5((OUT / "css" / "style.css").read_bytes() + (OUT / "js" / "main.js").read_bytes()).hexdigest()[:8]

TEL_LINK = "tel:" + OFFICE["tel"].replace("-", "")

NAV = [
    ("service", "業務案内"),
    ("fee", "料金"),
    ("houzin", "事務所案内"),
    ("staff", "スタッフ"),
    ("voice", "お客様の声"),
    ("yorozu", "よくある質問"),
    ("recruit", "採用情報"),
]

SERVICES = [
    ("zeimu", "会計・税務", "main-zeimu",
     "毎月の訪問で試算表を一緒に確認し、決算の着地点や納税額を早めに予測。決算書・申告書の作成、税務調査の対応まで担当します。"),
    ("souzoku", "相続・事業承継", "main-souzoku",
     "生前の相続税対策から申告、後継者への株式承継やM&Aまで。弁護士・司法書士・不動産鑑定士と連携します。"),
    ("support", "経営サポート", "main-support",
     "個人か法人か迷う起業前のご相談から、資金繰りや収益改善まで。元地方銀行員の経営承継アドバイザーが在籍しています。"),
    ("school", "経営実務スクール", "main-school",
     "経営者のためのB/S講座、簿記3級、法人税申告書の作成まで。実例をもとに、明日から使える知識をお伝えします。"),
    ("roumu", "労務・社会保険", "main-roumu",
     "同じ事務所の氏家社会保険労務士事務所と連携。社会保険の手続きから就業規則の作成まで、税務とまとめてご相談いただけます。"),
    ("cowork", "他士業との連携", "main-cowork",
     "税理士の業務範囲を超えるご相談は、信頼できる弁護士・司法書士・土地家屋調査士などの専門家をご紹介します。"),
]

# (画像, 氏名, 肩書, プロフィール[(項目, 内容)], ひとこと, 要確認メモ)
STAFF = [
    ("p-staff13", "藤本 博之", "代表社員 税理士",
     [("生まれ", "1969年10月"), ("税理士登録", "平成13年"), ("尊敬する人", "中村天風・稲盛和夫"), ("趣味", "テニス・読書"), ("今年のテーマ", "謙虚にして驕らず")],
     "若手税理士のつもりがいつの間にか20年。税理士は奥が深く幅広い知識と経験が求められる仕事です。スタッフも増えこれまで以上にお客様のご期待に応えお役に立てるよう一同頑張ります。", None),
    ("p-staff3", "氏家 奈都美", "社会保険労務士",
     [("最近ハマってること", "キャンプとロードバイク"), ("最近気付いたこと", "ホットサンドメーカーの無限の可能性"), ("最近のお気に入り", "ウイスキーの飲み比べ")],
     "お客様のお役に立てるよう、日々知識を深め、精進してまいります。", None),
    ("staff-morigami", "森上", "",
     [], "", "現行サイトのスタッフ紹介に未掲載。フルネーム・担当業務・プロフィールを要確認"),
    ("p-staff-aihara-2", "相原 由敬", "経営承継アドバイザー",
     [("趣味", "なかなか100が切れないゴルフと　実家の田畑の草刈り")],
     "地方銀行を早期退職。今後のライフワークは企業再生ビジネス！", None),
    ("p-staff2", "常盤 みゆき", "",
     [("好きな言葉", "日々是好日"), ("尊敬する人", "ターシャ・テューダー"), ("最近買ったもの", "フレンチプレス"), ("マイブーム", "バタやんちゃんねる，全粒粉")],
     "皆様のお役に立てるよう、より一層努めて参ります。", None),
    ("p-staff5", "大森 友貴", "",
     [("今年の目標", "バイクで８８ヵ所制覇。"), ("うれしかった事", "ハチワレ怪異化暗示回が無事夢オチでおわったこと。"), ("最近の楽しみ", "NHK月曜22：00～映像の世紀")],
     "神速・丁寧な対応を心がけ、お客様のニーズにこたえられるよう、精進してまいります。", None),
    ("p-staff7", "黒川 由規", "",
     [("趣味", "月いちゴルフ"), ("好きな物", "ジャンクフード")],
     "体力の低下を感じる事が年々増加してきました。今年は積極的に身体を動かします。<br>近年、税制など目まぐるしく変化している中、常にベストな選択を意識しながら取り組んでいきます。", None),
    ("p-staff15", "井口 哲成", "",
     [("趣味", "映画鑑賞、目的地のないドライブ"), ("最近の小さな目標", "最低週1回はプールで泳ぐこと")],
     "税制改正等が行われる業界の中で、まだまだ勉強の日々が続いております。今後は知識習得とあわせて、進化するITツール等も上手く活用しながら、お客様にあったご提案や相談が出来るように努めて参ります。", None),
    ("p-staff-kagawa", "香川 健司", "",
     [("最近の趣味", "猫と遊ぶこと"), ("好きなもの", "高温で湿度の高めなサウナ")],
     "丁寧でお客様に合わせた対応を心がけて精進して参りますので、宜しくお願い致します。", None),
    ("p-staff9", "三浦 万里江", "",
     [("好きな食べ物", "チーズ、ナッツ"), ("最近めざめたこと", "シンプルライフ"), ("挑戦したいこと", "スカイダイビング")],
     "迅速誠実な対応を心がけ、日々精進してまいります。", None),
    ("p-staff-mabe", "真部 浩介", "",
     [("趣味", "アクアリウム　観賞魚ショップ巡り"), ("毎朝のルーティーン", "魚の餌やり"), ("好きな言葉", "縁の下の力持ち"), ("最近うれしかったこと", "インペリアルゼブラプレコの繁殖に成功")],
     "日々新しいことに直面し、四苦八苦しています。多くの経験を積み、今よりも大きくなれるよう努めます。", None),
    ("p-staff10", "山下 美香", "",
     [("趣味", "ペットショップ巡り"), ("毎日習慣", "朝イチのエナジーチャージ！"), ("最近の悩み", "猫のおやつの買いすぎで家計圧迫")],
     "経験を積むごとに奥深い税務の仕事が楽しく感じるようになりました。感謝の気持ちを忘れず謙虚な姿勢で日々努力してまいります。", None),
    ("p-staff12", "鏡原 深雪", "",
     [("最近の癒し", "孫2人の成長、猫３匹とまったりすること。"), ("最近のツボ", "日々成長する孫の話し方。"), ("これからしたい事", "いろんなところへ小旅行に行って美味しいものとビールをあじわいたい。")],
     "スタッフ一同気持ちよく仕事ができるよう心掛けます。近くまでお越しの際には、ぜひお立ち寄りください。", None),
    ("p-staff-fujimoto", "藤本 健一", "",
     [],
     "引退間近なので今は、仕事半分あとの半分は、地域の自治会活動や、趣味のカメラとゴルフ。この仕事で沢山の人との出会いが、人生の楽しみでした。又京セラ会長の、稲盛和夫氏の経営哲学には深く感銘しました。<br>これからは、仕事を離れてもお付き合いお願いします。", "「引退間近」の記載あり。在籍状況を要確認"),
]

# スタッフ写真 → 自己紹介動画（現行サイトの video2023 を tools/convert_videos.sh で変換したもの）
VIDEOS = {
    "p-staff13": "fujimoto-h", "p-staff3": "ujike", "p-staff-aihara-2": "aihara", "p-staff2": "tokiwa",
    "p-staff5": "omori", "p-staff7": "kurokawa", "p-staff15": "iguchi", "p-staff-kagawa": "kagawa",
    "p-staff9": "miura", "p-staff-mabe": "manabe", "p-staff10": "yamashita", "p-staff12": "kagamihara",
    "p-staff-fujimoto": "fujimoto-kenichi",
}

VOICES = [
    # (写真, お客様名, 一覧用の補足, トップ用の抜粋, 詳細[(見出し, 本文)], URL, 住所・電話)
    ("voice-kawaji", "医療法人社団川地クリニック 様", "高松市松縄町・診療所",
     "開業するまでは、患者様のことだけを診ていれば良かったのですが、いざ開業するとなると全てが初めてのことで、右も左も分からない中、藤本先生には税務・経理のことだけでなく、様々なことを教えていただきました。",
     [("担当者の印象", "大変勉強熱心で仕事面はもちろん、何よりも誠実で実直なお人柄を（家族の話題にも先生の話が上がるほど）人間として全面的に信頼しています。ものの考え方や価値観が私たち家族とよく似ているのだと思います。また、仕事以外でも多趣味な方で、色々なお話を伺うのも毎月の楽しみのひとつです。"),
      ("お客様のご紹介", "川地クリニックは日赤病院出身の川地康司先生が開業された診療所です。<br>私が税理士登録をした当初からのお付き合いでとても思い入れのあるお客様です。<br>また、風邪をひいた時などは家族全員が川地先生にお世話になっています。<br>（担当：藤本）"),
      ("税理士法人ACEあかり事務所を知ったきっかけ", "藤本先生とは平成13年の開業時からお付き合いさせていただいています。<br>開業するまでは、患者様のことだけを診ていれば良かったのですが、いざ開業するとなると全てが初めてのことで、右も左も分からない中、藤本先生には税務・経理のことだけでなく、様々なことを教えていただきました。"),
      ("これからの仕事内容に期待することなど", "平成18年に医療法人設立の際にも大変お世話になりました。<br>藤本先生も平成22年に法人化され、ともに時間を経て成長あることを嬉しく思っています。<br>これからも、公私共々、末永くよろしくお願いいたします。")],
     "http://www.myclinic.ne.jp/kawajicl/pc/", "香川県高松市松縄町1117-16　tel.087-815-2110"),
    ("voice-enpachi", "喜多猿八 様", "木田郡三木町・農薬・肥料・生産資材の販売など",
     "月に1回の打ち合わせをすることで決算月に慌てることなく対応できるようになりました。メールでの対応も迅速で丁寧に説明して頂き助かります。森上さんにはいつも笑顔で経理のことだけではなく様々なことを教えて頂いています。",
     [("担当者の印象", "月に1回の打ち合わせをすることで決算月に慌てることなく対応できるようになりました。<br>メールでの対応も迅速で丁寧に説明して頂き助かります。<br>森上さんにはいつも笑顔で経理のことだけではなく様々なことを教えて頂いています。"),
      ("お客様のご紹介", "1900年（明治33年）に創業、農薬、肥料、生産資材の販売、害虫駆除などを行っています。<br>「日本一の農業経営支援集団になる」というビジョンの元、スマート農業化をテーマにドローンを使った農業の省力化に取り組んでいます。"),
      ("税理士法人ACEあかり事務所を知ったきっかけ", "香川胆識の会（旧 盛和塾香川）の塾生として藤本先生とは懇意にさせていただいていました。"),
      ("これからの仕事内容に期待することなど", "月に1回の打合せにて疑問が解消されるたび前向きな気持ちになれます。<br>これからもよろしくお願いいたします。")],
     "https://www.enpachi.co.jp/", "〒761-0611 香川県木田郡三木町田中 2582　tel. 087-898-1200"),
]

FAQ = [
    # 先頭5問は現行サイト「よろず相談」の原文（「方法をを」「シュミレーション」などの誤字のみ修正）
    ("見積もりだけでも対応していただけますか？", "もちろんお見積もりだけでも無料で対応させていただきます。"),
    ("料金はどのように決められますか？", "料金は、ご依頼内容、仕事量、難易度等によって異なります。当事務所はお客様のご要望をお伺いしながら、いくらかかるか事前にご相談させていただきます。お見積もりをさせていただき、お客様の同意のもと、決定させていただくシステムを徹底しております。目安は<a href=\"fee.html\">料金ページ</a>をご覧ください。"),
    ("起業したいのですが、会社設立前から相談にのっていただけますか？", "会社設立手続きから税務労務等の申請手続きまで、ご相談のうえお客様の起業をサポートいたします。"),
    ("先代からの事業承継で悩んでいます。相談に乗っていただけますでしょうか？", "今までの実績と経験を元に、問題点を洗い出して最適な方法を一緒に考えさせていただきます。"),
    ("相続について相談できますか？", "当事務所は生前からの相続税対策、納税額のシミュレーション、納税方法の提案などお客様に寄り添った提案をしてまいります。"),
    ("今の会計ソフトのままでも依頼できますか？", "<span class=\"tbd\">対応している会計ソフト（例：freee、マネーフォワード、弥生 など）と、導入支援の有無を記載</span>"),
    ("事務所に行かなくても相談できますか？", "毎月のご訪問が基本です。<span class=\"tbd\">オンライン面談（Zoom等）への対応可否を記載</span>。"),
]


# ---------------------------------------------------------------- layout

def jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "AccountingService",
        "name": OFFICE["name"],
        "url": ORIGIN + "/",
        "logo": ORIGIN + "/img/logo-mark.webp",
        "image": ORIGIN + "/img/hero-team.webp",
        "telephone": "+81-" + OFFICE["tel"][1:],
        "faxNumber": "+81-" + OFFICE["fax"][1:],
        "address": {"@type": "PostalAddress", "postalCode": OFFICE["zip"], "addressRegion": "香川県",
                    "addressLocality": "高松市", "streetAddress": "木太町5050番地17", "addressCountry": "JP"},
        "geo": {"@type": "GeoCoordinates", "latitude": 34.3128, "longitude": 134.0690},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "09:00", "closes": "17:30"}],
        "areaServed": ["高松市", "香川県"],
        "founder": {"@type": "Person", "name": "藤本 博之", "jobTitle": "代表社員 税理士"},
    }
    return json.dumps(data, ensure_ascii=False)


def header(current):
    items = "".join(
        f'<li><a href="{u(s)}"{" aria-current=\"page\"" if s == current else ""}>{t}</a></li>' for s, t in NAV)
    return f"""<div class="demo-ribbon">リニューアル提案用のデモサイトです。<span class="tbd">黄色の下線</span>は仮の内容で、正式な情報に差し替えます。</div>
<header class="site-header">
  <div class="container header-inner">
    <a class="logo" href="{u('')}"><img src="img/logo-yoko.png" alt="税理士法人ACEあかり事務所" width="410" height="51"></a>
    <nav class="gnav" aria-label="メインメニュー"><ul>{items}<li class="sp-only"><a href="{u('contact')}">お問い合わせ</a></li></ul></nav>
    <div class="header-cta">
      <a class="header-tel" href="{TEL_LINK}"><strong>{OFFICE['tel']}</strong><small>平日 {OFFICE['hours']}</small></a>
      <a class="btn btn-primary btn-sm" href="{u('contact')}">無料相談</a>
    </div>
    <button class="menu-btn" aria-label="メニュー" aria-expanded="false"><span></span></button>
  </div>
</header>"""


def cta_block():
    return f"""<section class="cta">
  <div class="container">
    <span class="sec-en">Contact</span>
    <h2>まずは、話してみませんか。</h2>
    <p>ご相談・お見積もりは無料です。「何から聞けばいいか分からない」という段階でも大丈夫です。</p>
    <div class="cta-actions">
      <a class="btn btn-primary" href="{u('contact')}">メールで相談する <span class="arrow">→</span></a>
      <a class="cta-tel" href="{TEL_LINK}"><b>{OFFICE['tel']}</b><small>平日 {OFFICE['hours']}（{OFFICE['closed']}休み）</small></a>
    </div>
  </div>
</section>"""


def footer():
    svc = "".join(f'<a href="{u(s)}">{t}</a>' for s, t, *_ in SERVICES) + f'<a href="{u("fee")}">料金について</a>'
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="img/logo-yoko-white.png" alt="税理士法人ACEあかり事務所" width="410" height="51">
        <p>〒{OFFICE['zip']} {OFFICE['addr']}</p>
        <p>TEL {OFFICE['tel']} ／ FAX {OFFICE['fax']}</p>
        <p>受付 {OFFICE['hours']}（{OFFICE['closed']}休み）</p>
        <p style="margin-top:14px">同所：氏家社会保険労務士事務所</p>
      </div>
      <div class="footer-nav">
        <div><h4>業務案内</h4>{svc}</div>
        <div><h4>事務所について</h4><a href="{u('greeting')}">代表挨拶</a><a href="{u('houzin')}">事務所案内・アクセス</a><a href="{u('staff')}">スタッフ紹介</a><a href="{u('voice')}">お客様の声</a><a href="{u('news')}">お知らせ</a></div>
        <div><h4>ご相談</h4><a href="{u('yorozu')}">よくある質問</a><a href="{u('contact')}">お問い合わせ</a><a href="{u('recruit')}">採用情報</a><a href="https://z-ace.or.jp/" target="_blank" rel="noopener">税理士法人ACE ↗</a></div>
      </div>
    </div>
    <div class="copyright"><span>© 2026 税理士法人ACEあかり事務所</span><a href="{u('contact')}#policy">プライバシーポリシー</a></div>
  </div>
</footer>
<div class="sp-cta">
  <a class="tel" href="{TEL_LINK}">電話する<small>平日 {OFFICE['hours']}</small></a>
  <a class="mail" href="{u('contact')}">無料相談<small>24時間受付</small></a>
</div>
<script src="js/main.js?v={ASSET_VER}"></script>"""


def page(slug, title, desc, body, current=None, home=False):
    full_title = title if home else f"{title}｜高松市の税理士 税理士法人ACEあかり事務所"
    canonical = ORIGIN + "/" + slug
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">  <!-- デモ用。本番では削除 -->
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'website' if home else 'article'}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/img/hero-team.webp">
<meta property="og:locale" content="ja_JP">
<meta name="theme-color" content="#fbf9f4">
<link rel="icon" href="img/logo-mark.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Shippori+Mincho+B1:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css?v={ASSET_VER}">
<script type="application/ld+json">{jsonld()}</script>
</head>
<body>
{header(current)}
<main>
{body}
</main>
{cta_block()}
{footer()}
</body>
</html>
"""
    (OUT / u(slug)).write_text(html, encoding="utf-8")


def page_hero(crumbs, h1, lead=""):
    trail = '<span><a href="index.html">ホーム</a></span>' + "".join(
        f'<span><a href="{u(s)}">{t}</a></span>' if s else f"<span>{t}</span>" for s, t in crumbs)
    lead_html = f"<p>{lead}</p>" if lead else ""
    return f"""<section class="page-hero"><div class="container">
  <nav class="breadcrumb" aria-label="パンくずリスト">{trail}</nav>
  <h1>{h1}</h1>{lead_html}
</div></section>"""


def svc_side(current):
    links = "".join(
        f'<a href="{u(s)}"{" aria-current=\"page\"" if s == current else ""}>{t}</a>' for s, t, *_ in SERVICES)
    links += f'<a href="{u("fee")}"{" aria-current=\"page\"" if current == "fee" else ""}>料金について</a>'
    return f"""<aside class="side-nav"><h4>業務案内</h4>{links}
  <div class="side-cta">ご相談・お見積もりは無料です<a class="btn btn-primary btn-sm" href="{u('contact')}">無料相談する</a></div>
</aside>"""


def sub_figure(slug, alt):
    """現行サイトの各業務ページ下部にある写真"""
    if not (OUT / "img" / f"sub-{slug}.webp").exists():
        return ""
    return f'<figure class="sub-figure"><img src="img/sub-{slug}.webp" alt="{alt}" loading="lazy"></figure>'


def svc_page(slug, h1, lead, img, content):
    body = page_hero([("service", "業務案内"), (None, h1)], h1, lead) + f"""
<section class="section"><div class="container layout-2col">
  <article class="prose">
    <figure class="lead-figure"><img src="img/main-{slug}.webp" alt="{h1}" loading="eager"></figure>
    {content}
    {sub_figure(slug, h1)}
  </article>
  {svc_side(slug)}
</div></section>"""
    return body


def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in items) + "</div>"


def info_table():
    return f"""<table class="info-table">
  <tr><th>名称</th><td>{OFFICE['name']}</td></tr>
  <tr><th>代表者</th><td>代表社員 税理士 藤本 博之</td></tr>
  <tr><th>所在地</th><td>〒{OFFICE['zip']}<br>{OFFICE['addr']}</td></tr>
  <tr><th>電話 / FAX</th><td><a href="{TEL_LINK}">{OFFICE['tel']}</a> ／ {OFFICE['fax']}</td></tr>
  <tr><th>受付時間</th><td>{OFFICE['hours']}（{OFFICE['closed']}休み）</td></tr>
  <tr><th>駐車場</th><td><span class="tbd">あり（◯台）</span></td></tr>
  <tr><th>同所</th><td>氏家社会保険労務士事務所</td></tr>
</table>"""


# ---------------------------------------------------------------- pages

def build_index():
    reasons = [
        ("01", "毎月、顔を合わせる税理士", "毎月の訪問で会計資料を確認し、経営状況を分かりやすくご説明します。決算の着地点や納税額を早めに予測できるので、「決算で慌てない」状態をつくれます。"),
        ("02", "税理士と社労士が、同じ事務所に", "同じ建物に氏家社会保険労務士事務所があります。給与計算・社会保険・就業規則まで、税務とまとめて一つの窓口でご相談いただけます。"),
        ("03", "相続・事業承継は、専門家チームで", "弁護士・司法書士・不動産鑑定士などと連携し、ご家族みんなが納得できる承継を考えます。元地方銀行員の経営承継アドバイザーも在籍しています。"),
    ]
    reasons_html = "".join(
        f'<div class="reason reveal"><span class="reason-no">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in reasons)
    cards = "".join(f"""<a class="svc-item reveal" href="{u(s)}">
  <img src="img/circle-{s}.webp" alt="{t}" loading="lazy" width="326" height="326">
  <span class="svc-label">{t}</span>
  <p>{d}</p>
</a>""" for s, t, img, d in SERVICES)
    worries = ["決算のたびに、納税額を見て驚いている", "試算表は届くけれど、数字の見方が分からない",
               "起業したいが、個人と法人のどちらが得か迷っている", "うちに相続税がかかるのか、まず知りたい",
               "そろそろ後継者への引き継ぎを考えはじめた", "従業員が増えて、社会保険や就業規則が不安"]
    worries_html = "".join(f'<li class="reveal">{w}</li>' for w in worries)
    voices = "".join(f"""<div class="voice reveal"><img class="voice-photo" src="img/{im}.webp" alt="{n}" loading="lazy"><blockquote>{q}</blockquote>
  <div class="voice-who"><b>{n}</b><span>{k}</span></div></div>""" for im, n, k, q, *_ in VOICES)
    faces = "".join(f'<img src="img/{s[0]}.webp" alt="{s[1]}" loading="lazy" width="480" height="480">'
                    for s in STAFF if s[0].startswith("p-"))
    body = f"""<section class="hero">
  <figure class="hero-photo">
    <img src="img/hero-team.webp" alt="税理士法人ACEあかり事務所のスタッフ集合写真" width="2000" height="1500" fetchpriority="high">
  </figure>
  <div class="container hero-body">
    <div class="hero-card">
      <span class="hero-eyebrow">香川県高松市の税理士事務所</span>
      <h1>一隅を照らす、<br><span class="light">町の税理士。</span></h1>
      <p class="hero-lead">毎月の訪問で数字を一緒に見て、決算の着地点を早めにつかむ。税務・会計から相続、労務まで、高松の経営者とご家族のいちばん近い相談相手でありたいと考えています。</p>
      <p class="hero-lead">私たち税理士法人ACEあかり事務所のスタッフは誠実をモットーとし、税務・会計の専門家として貴社の発展を全力でサポートいたします。</p>
      <ul class="hero-badges"><li>毎月の訪問</li><li>社労士が同じ事務所</li><li>相続・事業承継</li><li>見積もり無料</li></ul>
      <div class="hero-actions">
        <a class="btn btn-primary" href="{u('contact')}">無料で相談する <span class="arrow">→</span></a>
        <a class="hero-tel" href="{TEL_LINK}"><b>{OFFICE['tel']}</b><small>平日 {OFFICE['hours']}</small></a>
      </div>
      <div class="hero-stats">
        <div class="hero-stat"><b>2001<small>年</small></b><span>開業</span></div>
        <div class="hero-stat"><b class="tbd">13<small>名</small></b><span>スタッフ</span></div>
        <div class="hero-stat"><b>税理士×社労士</b><span>同じ事務所でワンストップ</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="sec-head center"><span class="sec-en">Why Akari</span><h2>あかり事務所が選ばれる理由</h2></div>
    <div class="reasons">{reasons_html}</div>
  </div>
</section>

<section class="section section-ink">
  <div class="container">
    <div class="sec-head center"><span class="sec-en">Worries</span><h2>こんなこと、ありませんか？</h2></div>
    <ul class="worries">{worries_html}</ul>
    <p class="worries-answer reveal">「どこに聞けばいいか分からない」は、<em>まず私たちに。</em></p>
  </div>
</section>

<section class="section section-yellow">
  <div class="container">
    <div class="sec-head center"><span class="sec-en">Service</span><h2>業務案内</h2><p>日々の記帳から決算、相続、労務まで。ひとつの事務所で、経営と暮らしのお金をまとめてサポートします。</p></div>
    <div class="svc-grid">{cards}</div>
    <p style="text-align:center;margin-top:40px"><a class="btn btn-ghost" href="{u('fee')}">料金の目安を見る <span class="arrow">→</span></a></p>
  </div>
</section>

<section class="section section-alt">
  <div class="container message">
    <div class="message-photo reveal"><img src="img/top-ichigu.webp" alt="税理士法人ACE 四国税理士会 会員之証" loading="lazy"></div>
    <div class="reveal">
      <span class="sec-en">Message</span>
      <h3>一隅を照らす</h3>
      <p>税理士法人ACE「あかり事務所」の名称の由来は「一隅を照らす」という言葉です。</p>
      <p>ひとりひとりがそれぞれの立場・役割において全力をつくしその場を照らす、そのことがひいては社会全体をあかるく照らすことに繋がっていく。</p>
      <p>私たちは税理士という役割を担いその使命を果たすことで少しでも皆様のお役に立ちたい。そんな思いが込められております。</p>
      <div class="message-sign"><small>代表社員 税理士</small><b>藤本 博之</b></div>
      <p style="margin-top:24px"><a href="{u('greeting')}">代表挨拶を読む →</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head center"><span class="sec-en">Voice</span><h2>お客様の声</h2></div>
    <div class="voices">{voices}</div>
    <p style="text-align:center;margin-top:36px"><a href="{u('voice')}">お客様の声をもっと見る →</a></p>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="team reveal">
      <figure class="team-photo"><img src="img/top-staff.webp" alt="税理士法人ACEあかり事務所のスタッフ" loading="lazy" width="1400" height="788"></figure>
      <div class="team-body">
        <span class="sec-en">Our Team</span>
        <h2>チームでサポートします</h2>
        <p>税理士・社会保険労務士・経営承継アドバイザーを含むスタッフが、チームでお客様を担当します。</p>
        <p>スタッフ紹介では、一人ひとりのプロフィールと<b>自己紹介動画</b>をご覧いただけます。どんな人が担当するのか、ご相談の前にぜひご覧ください。</p>
        <a class="btn btn-primary" href="{u('staff')}">スタッフ紹介を見る <span class="arrow">→</span></a>
      </div>
    </div>
    <div class="recruit-band reveal">
      <div><h3>一緒に働く仲間を募集しています</h3><p>簿記2級以上の方、税理士・科目合格者の方。通年で採用しています。</p></div>
      <a class="btn btn-primary" href="{u('recruit')}">採用情報を見る <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head center"><span class="sec-en">Q&amp;A</span><h2>よくあるご質問</h2></div>
    {faq_html(FAQ[:4])}
    <p style="text-align:center;margin-top:32px"><a href="{u('yorozu')}">すべての質問を見る →</a></p>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="sec-head"><span class="sec-en">Access</span><h2>事務所・アクセス</h2></div>
    <div class="access">
      <div class="reveal">{info_table()}</div>
      <div class="map reveal"><iframe src="{MAP_SRC}" loading="lazy" title="税理士法人ACEあかり事務所の地図" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
  </div>
</section>"""
    page("", "高松市の税理士事務所｜税理士法人ACEあかり事務所",
         "香川県高松市木太町の税理士法人ACEあかり事務所。毎月の訪問による会計・税務サポート、相続・事業承継、起業支援、社労士と連携した労務まで。ご相談・お見積もりは無料です。",
         body, home=True)


def build_service():
    cards = "".join(f"""<a class="svc-item reveal" href="{u(s)}">
  <img src="img/circle-{s}.webp" alt="{t}" loading="lazy" width="326" height="326">
  <span class="svc-label">{t}</span>
  <p>{d}</p>
</a>""" for s, t, img, d in SERVICES)
    body = page_hero([(None, "業務案内")], "業務案内",
                     "日々の記帳から決算・申告、相続、労務まで。ひとつの窓口で、経営と暮らしのお金のことをまとめてご相談いただけます。") + f"""
<section class="section section-yellow"><div class="container"><div class="svc-grid">{cards}</div>
<p style="text-align:center;margin-top:40px"><a class="btn btn-ghost" href="{u('fee')}">料金の目安を見る <span class="arrow">→</span></a></p></div></section>"""
    page("service", "業務案内", "税理士法人ACEあかり事務所の業務案内。会計・税務、相続・事業承継、経営サポート、経営実務スクール、労務・社会保険、他士業との連携。", body, "service")


def build_zeimu():
    content = """
<h2>経営者のベストパートナーとして</h2>
<p>正確な会計記録はあらゆる業務の基本となるものです。毎月のご訪問を通じ、経営者のベストパートナーとして税務や経営などのよき相談相手となり問題解決をご支援いたします。</p>
<p>また、複雑な税務については日頃からの研鑽を活かし、正確で無駄のない処理を心がけております。「あたりまえをあたりまえに」と「プロフェッショナルのサービスを」が私たちの合言葉です。</p>

<h2>月次決算報告</h2>
<p>試算表や伝票・会計資料等をチェックし、正しくスピーディな月次決算をサポートすることにより経営状況を分かりやすくご説明いたします。決算着地点、納税予測などの基礎となる大切な業務になります。</p>

<h2>決算・税務申告</h2>
<p>決算書・税務申告書などを作成し、所轄税務署や県税事務所、市役所に提出します。電子申告・電子納税にも対応しています。毎年変更となる煩雑な年末調整や償却資産税申告もおまかせください。また、税務調査においても経験豊富な税理士が全力で対応させていただきます。</p>

<h2>その他の対応業務</h2>
<p><span class="tbd">記帳代行、会計ソフトの導入支援、給与計算など、ほかに対応している業務があれば記載</span></p>"""
    s = SERVICES[0]
    page("zeimu", "会計・税務", "毎月の訪問による月次決算報告、決算書・税務申告書の作成、電子申告、年末調整・償却資産税申告、税務調査の対応。高松市の税理士法人ACEあかり事務所。",
         svc_page("zeimu", "会計・税務", "毎月の訪問で数字を一緒に確認し、決算の着地点を早めにつかむ。経営者のベストパートナーとして、税務と経営の相談相手になります。", s[2], content), "service")


def build_souzoku():
    content = """
<h2>相続・事業承継</h2>
<p>近年特に関心の高まっている分野です。相続・事業承継における様々な場面に対応するため、弁護士・司法書士・不動産鑑定士等と連携してスムーズで無駄なく、また、関係者皆が納得できるようお客様に寄り添った提案をしてまいります。</p>

<h2>相続</h2>
<p>豊富な経験と知識を駆使し、相続税の適正な申告はもちろん、事前の相続税対策、納税資金対策など総合的な提案をさせていただきます。</p>

<h2>事業承継</h2>
<p>事業承継の場面は様々です。後継者がいらっしゃる方には事業承継税制のご提案や株式の贈与など、後継者不在の場合にはＭ＆Ａなど、お客様のご希望と実状にあわせた方法を提案させていただきます。</p>

<h2>ご相談の流れ</h2>
<ol class="flow">
  <li><b>無料相談</b>ご家族構成や財産の状況、気になっていることをお聞かせください。</li>
  <li><b>現状の把握と試算</b>相続税がかかるか、どのくらいになりそうかを試算します。</li>
  <li><b>対策のご提案・お見積もり</b>必要に応じて専門家と連携し、具体的な方法と費用をご説明します。</li>
  <li><b>実行・申告</b>ご同意いただいた内容で手続きを進め、申告まで担当します。</li>
</ol>"""
    page("souzoku", "相続・事業承継", "相続税の試算・対策・申告、事業承継税制、株式の贈与、M&Aまで。弁護士・司法書士と連携して対応する高松市の税理士法人ACEあかり事務所。",
         svc_page("souzoku", "相続・事業承継", "「うちは相続税がかかるの？」という段階から。ご家族みんなが納得できる承継を、専門家と一緒に考えます。", "main-souzoku", content), "service")


def build_support():
    content = """
<h2>経営サポート</h2>
<p>税務や会計の業務を行っていると自然と経営の相談を受けることが多くなってきました。私どもは経営コンサルタントではありませんが、出来る限りお客様に寄り添い、一緒になって経営に取り組んでいこうと考えております。</p>

<h2>起業支援</h2>
<p>個人業と法人を設立するのはどちらかメリットがあるのか？また、開業後においては税務署等への書類作成、会計帳簿の記帳、給与計算など会社の基礎となる項目の整備をお手伝いします。</p>

<h2>企業経営支援</h2>
<div class="mini-card" style="display:grid;grid-template-columns:120px 1fr;gap:20px;align-items:center">
  <img src="img/p-staff-aihara-2.webp" alt="経営承継アドバイザー 相原由敬" style="border-radius:50%" loading="lazy">
  <div><h3>経営承継アドバイザー 相原 由敬</h3><p>経営環境の変化等により収益性や資金繰りに問題を抱える企業に対して、事業面、財務面及び人事面等多角的な視点から現状分析し企業と一緒になり事業継続するためのソリューションを実践いたします。</p></div>
</div>"""
    page("support", "経営サポート", "起業支援（個人・法人の比較、設立手続き）と、資金繰り・収益改善などの企業経営支援。元地銀の経営承継アドバイザーが在籍。",
         svc_page("support", "経営サポート", "起業前のご相談から、資金繰り・収益改善まで。数字を一番よく知る立場から、経営に伴走します。", "main-support", content), "service")


def build_school():
    content = """
<h2>経営実務スクール</h2>
<p>経営者や経理担当者はもちろんのこと、それ以外の方も会計や税務の知識を身につけることにより業務の幅が広がります。私たちが講師として実務に則した内容の講座を受講者様のご要望に応じて展開していきます。</p>

<h2>経営実務講座</h2>
<p>会計基礎講座をはじめ、税務の知識、法律の知識などを中心として、実例に基づきながら役に立つ講座を開催しております。</p>

<h2>開催講座実績</h2>
<div class="cards-2">
  <div class="mini-card"><h3>経営者のためのＢ／Ｓ講座</h3></div>
  <div class="mini-card"><h3>税理士が教える簿記３級講座</h3></div>
  <div class="mini-card"><h3>法人税申告書作成講座</h3></div>
  <div class="mini-card"><h3>実例で学ぶ相続講座</h3></div>
  <div class="mini-card"><h3>７つの習慣勉強会</h3></div>
</div>
<p>その他ご要望に応じてカリキュラムを組むことができます。</p>
<p><span class="tbd">次回の開催予定・申込方法を記載</span></p>"""
    page("school", "経営実務スクール", "経営者のためのB/S講座、簿記3級講座、法人税申告書作成講座、相続講座など。税理士が講師を務める実務講座。",
         svc_page("school", "経営実務スクール", "税理士が講師を務める、実例ベースの会計・税務講座。社員研修としてのご依頼も承ります。", "main-school", content), "service")


def build_roumu():
    content = """
<h2>労務・社会保険</h2>
<p>企業にとっての関心ごとは様々ですが、近年は労務問題が大きくクローズアップされてきており、経営者の視点からは全体を見渡した俯瞰的な対応が必要となります。</p>
<p>私どもは、あかり税理士×氏家社労士の組み合わせで税務・労務をトータル的にサポートできる体制を整えております。</p>
<div class="mini-card" style="display:grid;grid-template-columns:120px 1fr;gap:20px;align-items:center;margin:28px 0">
  <img src="img/p-staff3.webp" alt="社会保険労務士 氏家奈都美" style="border-radius:50%" loading="lazy">
  <div><h3>氏家社会保険労務士事務所</h3><p>社会保険労務士 氏家 奈都美</p></div>
</div>

<h2>手続き代行</h2>
<p>各種保険の届け出業務です。社会保険の手続き、雇用保険手続き、労働保険手続き等をお客様に代わって行います。</p>

<h2>就業規則の作成・見直し</h2>
<p>お客様の現状とご希望を照らし合わせながら、最適な規定づくりをしていきます。オーダーメイドでお客様に合った就業規則・賃金規定・退職金規程・慶弔見舞規程・旅費規定等を作成します。</p>"""
    page("roumu", "労務・社会保険", "同じ事務所の氏家社会保険労務士事務所と連携し、社会保険・雇用保険の手続き代行、就業規則の作成・見直しまで対応します。",
         svc_page("roumu", "労務・社会保険", "税理士と社労士が同じ事務所に。給与・社会保険・就業規則まで、まとめてご相談いただけます。", "main-roumu", content), "service")


def build_cowork():
    partners = [
        ("弁護士", "紛争解決における示談・交渉・裁判", ["高橋総合法律事務所"]),
        ("司法書士", "会社設立登記、相続登記", ["白井司法書士事務所", "ひろせ司法書士事務所"]),
        ("不動産鑑定士", "相続財産の評価、関連会社間取引の評価", ["株式会社名渕総合鑑定所", "ながお不動産鑑定"]),
        ("土地家屋調査士", "不動産の表示に関する登記・調査・測量", ["久保利司土地家屋調査士事務所", "佐藤光成土地家屋調査士事務所"]),
        ("行政書士", "各種許認可", ["村井総合法務事務所"]),
        ("その他の専門家", "IT化支援、ソフトウェア開発", ["株式会社ユニーク", "ペダル株式会社"]),
    ]
    cards = "".join(f'<div class="mini-card"><h3>{k}</h3><p class="note" style="margin:0 0 8px">{d}</p><ul>' + "".join(f"<li>{n}</li>" for n in v) + "</ul></div>" for k, d, v in partners)
    content = f"""
<h2>他士業との連携</h2>
<p>経営者の方は、様々な問題に直面し、日々その判断を迫られていると思います。税理士は経営者の方にとって最も親しい話し相手として、営業に関すること、法律に関することなど分野を問わずいろいろなご相談をいただきます。</p>
<p>問題解決のため、私たちで行うことが出来ない分野の業務については信頼できる専門家をご紹介させていただいております。経営を行う上で財務にとどまらないご相談事に対して、弁護士などの専門家と連携し、総合的にサポートいたします。</p>
<h2>他士業・その他専門家のご紹介</h2>
<figure class="diagram"><img src="img/cowork-diagram.webp" alt="税理士法人ACEあかり事務所・氏家社会保険労務士事務所と、弁護士・司法書士・不動産鑑定士・土地家屋調査士・行政書士・その他の専門家との連携図" loading="lazy"></figure>
<div class="partner-list">{cards}</div>"""
    page("cowork", "他士業との連携", "弁護士・司法書士・不動産鑑定士・土地家屋調査士・行政書士など、信頼できる専門家と連携して経営者のご相談に総合的に対応します。",
         svc_page("cowork", "他士業との連携", "税理士の守備範囲を超えるご相談も、まずはお聞かせください。信頼できる専門家におつなぎします。", "main-cowork", content), "service")


def build_fee():
    rows = [
        ("法人 顧問契約（毎月訪問・月次決算）", "月額 ◯◯,000円〜", "売上規模・仕訳数により変動"),
        ("法人 決算・申告", "◯◯◯,000円〜", "顧問契約の方は別料金表"),
        ("個人事業 確定申告", "◯◯,000円〜", "記帳代行の有無により変動"),
        ("年末調整", "◯◯,000円〜", "+1名あたり ◯,000円"),
        ("相続税申告", "遺産総額の ◯%〜", "土地の評価数などにより変動"),
        ("会社設立サポート", "◯◯,000円〜", "顧問契約とセットで割引"),
    ]
    tr = "".join(f'<tr><th>{a}</th><td class="num"><span class="tbd">{b}</span></td><td class="note">{c}</td></tr>' for a, b, c in rows)
    body = page_hero([("service", "業務案内"), (None, "料金について")], "料金について",
                     "ご依頼の内容・仕事量・難易度によって異なります。必ず事前にお見積もりし、ご同意いただいてから決定します。") + f"""
<section class="section"><div class="container layout-2col">
  <article class="prose">
    <h2>料金の目安</h2>
    <table class="price-table"><thead><tr><th>業務</th><th>料金（税込）</th><th>備考</th></tr></thead><tbody>{tr}</tbody></table>
    <p class="note">※上記は目安です。お客様の状況をうかがったうえで、正式にお見積もりします。</p>
    <h2>料金が決まるまで</h2>
    <ol class="flow">
      <li><b>無料相談</b>お電話・メールで、ご依頼内容や会社の状況をお聞かせください。</li>
      <li><b>お見積もり（無料）</b>業務の範囲と金額を、書面で事前にご提示します。</li>
      <li><b>ご契約</b>内容にご納得いただいてから契約となります。見積もりだけでも構いません。</li>
    </ol>
  </article>
  {svc_side('fee')}
</div></section>"""
    page("fee", "料金について", "税理士法人ACEあかり事務所の料金の目安。顧問契約、決算申告、確定申告、年末調整、相続税申告、会社設立。お見積もりは無料です。", body, "fee")


def build_greeting():
    body = page_hero([("houzin", "事務所について"), (None, "代表挨拶")], "代表挨拶") + f"""
<section class="section"><div class="container message" style="align-items:start">
  <div class="message-photo"><img src="img/p-staff13.webp" alt="代表社員 税理士 藤本博之" width="480" height="480"></div>
  <article class="prose">
    <p class="note" style="background:var(--akari-soft);padding:12px 16px;border-radius:10px">※この挨拶文は、現行サイトの掲載内容をもとに作成した<b>叩き台</b>です。ご本人の言葉で差し替えます。</p>
    <h2>一隅を照らす</h2>
    <p>税理士法人ACE「あかり事務所」の名前は、「一隅を照らす」という言葉に由来しています。ひとりひとりがそれぞれの立場・役割において全力をつくし、その場を照らす。そのことが、ひいては社会全体を明るく照らすことにつながっていく。私たちは税理士という役割を担い、その使命を果たすことで、少しでも皆様のお役に立ちたいと考えています。</p>
    <p>平成13年に開業し、平成22年に法人化しました。開業当初からお付き合いいただいているお客様も多く、会社の設立から医療法人化、代替わりまで、お客様の節目に立ち会えることがこの仕事の何よりの喜びです。</p>
    <p>「若手税理士のつもりが、いつの間にか20年」。税理士は奥が深く、幅広い知識と経験が求められる仕事です。スタッフも増え、社会保険労務士とも同じ事務所で連携できる体制になりました。これまで以上にお客様のご期待に応えられるよう、「謙虚にして驕らず」を胸に、一同取り組んでまいります。</p>
    <div class="message-sign"><small>税理士法人ACEあかり事務所 代表社員 税理士</small><b>藤本 博之</b></div>
    <h2>プロフィール</h2>
    <ul class="dots"><li>1969年10月生まれ</li><li>平成13年 税理士登録・開業</li><li>平成22年 法人化</li><li>尊敬する人：中村天風、稲盛和夫</li><li>趣味：テニス、読書</li></ul>
  </article>
</div></section>"""
    page("greeting", "代表挨拶", "税理士法人ACEあかり事務所 代表社員 税理士 藤本博之のご挨拶。「一隅を照らす」に込めた想い。", body, "houzin")


def build_houzin():
    body = page_hero([(None, "事務所案内")], "事務所案内・アクセス") + f"""
<section class="section"><div class="container">
  <figure class="sub-figure" style="margin:0 0 56px"><img src="img/hero-team.webp" alt="税理士法人ACEあかり事務所のスタッフと事務所の外観"></figure>
  <div class="access">
    <div>{info_table()}
      <p style="margin-top:28px"><a href="{u('greeting')}">代表挨拶 →</a>　<a href="{u('staff')}">スタッフ紹介 →</a></p></div>
    <div class="map"><iframe src="{MAP_SRC}" loading="lazy" title="税理士法人ACEあかり事務所の地図" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</div></section>
<section class="section section-alt"><div class="container prose">
  <h2>税理士法人ACE</h2>
  <p>当事務所は税理士法人ACEのグループ事務所です。<a href="https://z-ace.or.jp/" target="_blank" rel="noopener">税理士法人ACEのサイト ↗</a></p>
</div></section>"""
    page("houzin", "事務所案内・アクセス", "税理士法人ACEあかり事務所の所在地（高松市木太町）、電話番号、受付時間、地図。同所に氏家社会保険労務士事務所。", body, "houzin")


def build_staff():
    cards = []
    for img, name, role, prof, msg, memo in STAFF:
        dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in prof)
        role_html = f'<span class="staff-role">{role}</span>' if role else ""
        memo_html = f'<p><span class="tbd">{memo}</span></p>' if memo else ""
        msg_html = f"<p>{msg}</p>" if msg else ""
        lead = " lead" if name == "藤本 博之" else ""
        photo = f'<img src="img/{img}.webp" alt="{name}" loading="lazy" width="480" height="480">'
        if img in VIDEOS:
            v = VIDEOS[img]
            photo = (f'<div class="staff-media" data-video="video/{v}.mp4" data-poster="video/{v}.webp">{photo}'
                     f'<button class="play-btn" type="button" aria-label="{name}の動画を再生">▶ 動画を見る</button></div>')
        cards.append(f"""<div class="staff{lead} reveal">{photo}
<div class="staff-body">{role_html}<h3>{name}</h3>{f'<dl>{dl}</dl>' if dl else ''}{msg_html}{memo_html}</div></div>""")
    body = page_hero([("houzin", "事務所について"), (None, "スタッフ紹介")], "スタッフ紹介",
                     "お客様を担当するスタッフを、写真とひとこと動画でご紹介します。<span class=\"tbd\">掲載内容は2023年秋時点。最新の在籍状況に更新します。</span>") + f"""
<section class="section"><div class="container"><div class="staff-grid">{''.join(cards)}</div></div></section>"""
    page("staff", "スタッフ紹介", "税理士法人ACEあかり事務所で働く税理士・社会保険労務士・スタッフのご紹介。", body, "staff")


def build_voice():
    items = []
    for im, n, k, q, details, url, addr in VOICES:
        dl = "".join(f"<h3>{h}</h3><p>{t}</p>" for h, t in details)
        items.append(f"""<article class="voice-detail reveal">
  <div class="voice-head"><img class="voice-photo" src="img/{im}.webp" alt="{n}" loading="lazy">
    <div><h2>{n}</h2><p class="note"><a href="{url}" target="_blank" rel="noopener">{url}</a><br>{addr}</p></div></div>
  <div class="prose">{dl}</div>
</article>""")
    body = page_hero([(None, "お客様の声")], "お客様の声", "長くお付き合いいただいているお客様に、あかり事務所について伺いました。") + f"""
<section class="section"><div class="container">{''.join(items)}
<p class="note" style="text-align:center;margin-top:28px"><span class="tbd">掲載件数を増やす（業種・規模の異なる3〜5社が理想）</span></p></div></section>"""
    page("voice", "お客様の声", "税理士法人ACEあかり事務所をご利用のお客様の声。医療法人、農業資材販売会社など。", body, "voice")


def build_yorozu():
    body = page_hero([(None, "よくある質問")], "よろず相談・よくある質問",
                     "ご相談・ご質問お気軽にお問い合わせください。<br>税務・会計について、相続・事業承継について、経営サポートについて、経営実務スクールについて、社会保険・労務について、料金・見積もりについて、その他何から質問したら良いかわからない…などお気軽にお問い合わせください。") + f"""
<section class="section"><div class="container">{faq_html(FAQ)}</div></section>"""
    page("yorozu", "よくある質問", "見積もりだけの依頼、料金の決まり方、起業前の相談、事業承継、相続など、よくいただくご質問にお答えします。", body, "yorozu")


def build_news():
    items = [
        ("2026.11.01", "お知らせ", "年末調整の資料ご提出のお願い（記事の例）", True),
        ("2026.10.01", "税制・制度", "インボイス制度の経過措置について（記事の例）", True),
        ("2023.05.18", "お知らせ", "ウェブサイトの情報を一部リニューアルいたしました", False),
        ("2022.05.18", "お知らせ", "ウェブサイト、一部リニューアルのお知らせ", False),
        ("2021.11.02", "お知らせ", "スタッフ紹介を更新いたしました", False),
    ]
    li = "".join(
        f'<li><div class="row"><time>{d}</time><span class="tag">{t}</span><span class="ttl">{f"<span class=tbd>{x}</span>" if s else x}</span></div></li>'
        for d, t, x, s in items)
    body = page_hero([(None, "お知らせ")], "お知らせ") + f"""
<section class="section"><div class="container prose" style="max-width:920px"><ul class="news-list">{li}</ul></div></section>"""
    page("news", "お知らせ", "税理士法人ACEあかり事務所からのお知らせ。税制改正、年末調整、事務所からのご案内。", body, "news")


def build_recruit():
    body = page_hero([(None, "採用情報")], "採用情報",
                     "一隅を照らす仕事を、一緒に。税理士・科目合格者の方、簿記2級以上の知識をお持ちの方を通年で募集しています。") + f"""
<section class="section"><div class="container layout-2col">
  <article class="prose">
    <h2>あかり事務所で働くということ</h2>
    <p>担当するのは、高松・香川の中小企業や個人事業主、医療法人など。毎月の訪問を通じて経営者と直接向き合い、数字から会社を支えるやりがいのある仕事です。同じ事務所に社会保険労務士がおり、税務だけでなく労務や相続など幅広い経験を積めます。</p>
    <h2>先輩スタッフの声</h2>
    <div class="voices" style="grid-template-columns:1fr">
      <div class="voice"><blockquote>経験を積むごとに、奥深い税務の仕事が楽しく感じるようになりました。</blockquote><div class="voice-who"><b>山下 美香</b></div></div>
      <div class="voice"><blockquote>税制改正が続く業界で、まだまだ勉強の日々。知識の習得とあわせて、進化するITツールも上手に活用していきたいと思っています。</blockquote><div class="voice-who"><b>井口 哲成</b></div></div>
    </div>
    <h2>募集要項</h2>
    <table class="info-table">
      <tr><th>職種</th><td>税理士業務補助（決算・申告書の作成など）</td></tr>
      <tr><th>雇用形態</th><td>正社員</td></tr>
      <tr><th>応募資格</th><td>簿記2級または同等以上の知識をお持ちの方、税理士又は科目合格者</td></tr>
      <tr><th>求める人物像</th><td>明るく元気で意欲のある方</td></tr>
      <tr><th>勤務地</th><td>{OFFICE['addr']}</td></tr>
      <tr><th>勤務時間</th><td>{OFFICE['hours']}</td></tr>
      <tr><th>休日</th><td>土・日・祝日<span class="tbd">、年末年始、夏季休暇、有給休暇</span></td></tr>
      <tr><th>給与</th><td><span class="tbd">月給 ◯◯万円〜（経験・資格を考慮）</span></td></tr>
      <tr><th>待遇</th><td><span class="tbd">社会保険完備、資格取得支援（受験休暇など）、交通費支給、マイカー通勤可</span></td></tr>
      <tr><th>募集期間</th><td>随時（通年採用）</td></tr>
    </table>
    <h2>応募の流れ</h2>
    <ol class="flow"><li><b>お問い合わせ・応募</b>詳細は電話またはメールにてお問い合わせください／担当：藤本</li><li><b>事務所見学・面接</b>まずは気軽に雰囲気を見にきてください。</li><li><b>内定</b>入社日はご相談に応じます。</li></ol>
    <p><a class="btn btn-primary" href="{u('contact')}">応募・お問い合わせ <span class="arrow">→</span></a></p>
  </article>
  <aside class="side-nav"><h4>採用について</h4><a href="{u('staff')}">スタッフ紹介</a><a href="{u('greeting')}">代表挨拶</a><a href="{u('houzin')}">事務所案内</a>
    <div class="side-cta">見学だけでも歓迎です<a class="btn btn-primary btn-sm" href="{TEL_LINK}">{OFFICE['tel']}</a></div></aside>
</div></section>"""
    page("recruit", "採用情報", "税理士法人ACEあかり事務所（高松市）の採用情報。税理士・科目合格者、簿記2級以上の方を正社員として通年募集。", body, "recruit")


def build_contact():
    topics = ["会計・税務の顧問", "決算・確定申告", "相続・事業承継", "起業・会社設立", "労務・社会保険", "料金・見積もり", "採用への応募", "その他"]
    chips = "".join(f'<label><input type="checkbox" name="topic" value="{t}"><span>{t}</span></label>' for t in topics)
    body = page_hero([(None, "お問い合わせ")], "お問い合わせ・無料相談",
                     "ご相談・お見積もりは無料です。1〜2営業日以内に担当者からご連絡します。") + f"""
<section class="section"><div class="container layout-2col">
  <div>
    <div class="contact-tel"><span>お電話でのご相談</span><a href="{TEL_LINK}">{OFFICE['tel']}</a><small>平日 {OFFICE['hours']}（{OFFICE['closed']}休み）</small></div>
    <form class="form" id="contact-form">
      <div class="form-row"><label class="lbl">ご相談の内容 <span class="opt">複数選択可</span></label><div class="chips">{chips}</div></div>
      <div class="form-row"><label class="lbl" for="f-name">お名前 <span class="req">必須</span></label><input type="text" id="f-name" required autocomplete="name" placeholder="高松 太郎"></div>
      <div class="form-row"><label class="lbl" for="f-company">会社名・屋号 <span class="opt">任意</span></label><input type="text" id="f-company" autocomplete="organization"></div>
      <div class="form-row"><label class="lbl" for="f-tel">電話番号 <span class="req">必須</span></label><input type="tel" id="f-tel" required autocomplete="tel" inputmode="tel" placeholder="090-1234-5678"></div>
      <div class="form-row"><label class="lbl" for="f-mail">メールアドレス <span class="req">必須</span></label><input type="email" id="f-mail" required autocomplete="email"></div>
      <div class="form-row"><label class="lbl">ご希望の連絡方法</label><div class="chips">
        <label><input type="radio" name="via" checked><span>どちらでも</span></label><label><input type="radio" name="via"><span>電話</span></label><label><input type="radio" name="via"><span>メール</span></label></div></div>
      <div class="form-row"><label class="lbl" for="f-body">ご相談内容 <span class="opt">任意</span></label><textarea id="f-body" rows="6" placeholder="分かる範囲でご記入ください"></textarea></div>
      <div class="policy" id="policy"><b>プライバシーポリシー</b><br>税理士法人ACEあかり事務所（以下、当方）では、お客様のプライバシーを尊重し、お客様の個人情報を大切に保護することを重要な責務と考えております。当ウェブサイトでは、個人情報保護に関する法令を遵守するとともに、個人情報の取り扱いに関して次のような姿勢で行動しています。<br><br><b>【個人情報の利用目的】</b><br>お客様から個人情報をご提供いただく場合、その情報は、お客様からのお問い合わせおよびご要望に対して回答または対応する目的、または個人情報をご提供いただく際に予め明示する目的のみに利用いたします。<br>お客様の個人情報をこれら正当な目的以外に無断で利用することはありません。<br><br><b>【第三者への提供】</b><br>お客様からご提供いただいた個人情報は、以下のそれぞれの場合を除き、如何なる第三者にも開示または提供することはありません。<br>・お問い合わせまたはご要望に対し、適切な回答または対応をさせていただく為に、お問い合わせ・ご要望に関連する内容を開示する場合<br>・個人情報をご提供いただく際に予め明示した第三者に提供する場合<br>・法令に基づく場合その他個人情報保護法により第三者への提供が認められている場合<br>・お客様にご承諾頂いた場合<br><br><b>【個人情報の開示、訂正、削除について】</b><br>お客様がご提供された個人情報の開示、訂正、削除を希望される場合、合理的な範囲で速やかに対応いたします。 その場合は、個人情報をご提供いただいた個々のウェブページにてお知らせした窓口までご連絡ください。<br><br><b>【安全対策】</b><br>お客様の個人情報を安全に管理・運営するよう鋭意努力しており、個人情報への外部からの不正なアクセス、個人情報の紛失・破壊・改ざん・漏えいなどへの危険防止に対する合理的かつ適切な安全対策を行っています。 また個人情報を取り扱う部門ごとに情報管理責任者を置き、個人情報の適切な管理に努めるとともに、情報セキュリティに関する規程を設けて社員への周知徹底を実施しています。<br><br><b>【特定または不特定情報の収集】</b><br>当ウェブサイトでは、アクセスされたお客様個人を特定できる情報（お名前、ご住所、お電話番号、電子メールアドレス等）を、お客様のご承諾なく収集することはありません。 その一方、当ウェブサイトでは、お客様個人を特定できない情報を収集することがあります。 このタイプの情報の例としては、お客様が当ウェブサイトのどのページにご訪問されたのか、またどのドメイン名のウェブサイトから当ウェブサイトにアクセスされたのかの記録等があります。<br>これらの情報は、当ウェブサイトの内容改善等に用いられることがあります。<br><br><b>【本ポリシーの適用範囲】</b><br>本ポリシーの適用範囲は当ウェブサイト内とします。 当ウェブサイトからリンクの張られている他のウェブサイトのプライバシー保護についての責任は負いかねますので、それぞれのウェブサイトのプライバシーポリシーをご確認ください。</div>
      <div class="form-row"><label><input type="checkbox" required> プライバシーポリシーに同意する</label></div>
      <button class="btn btn-primary" type="submit" style="width:100%">送信する <span class="arrow">→</span></button>
    </form>
    <div class="form-done form"><h3 style="font-size:22px;margin-bottom:12px">送信を受け付けました（デモ）</h3><p>本番では、担当者から1〜2営業日以内にご連絡します。<br>※デモサイトのため、実際には送信されていません。</p></div>
  </div>
  <aside class="side-nav"><h4>ご相談の前に</h4>
    <a href="{u('yorozu')}">よくある質問</a><a href="{u('fee')}">料金について</a><a href="{u('houzin')}">事務所案内・アクセス</a>
  </aside>
</div></section>"""
    page("contact", "お問い合わせ", "税理士法人ACEあかり事務所へのお問い合わせ・無料相談。お電話（087-814-7134）またはフォームから。", body, "contact")


if __name__ == "__main__":
    for fn in [build_index, build_service, build_zeimu, build_souzoku, build_support, build_school, build_roumu,
               build_cowork, build_fee, build_greeting, build_houzin, build_staff, build_voice, build_yorozu,
               build_news, build_recruit, build_contact]:
        fn()
    print("built:", sorted(p.name for p in OUT.glob("*.html")))
