# あかり事務所 HPリニューアル（デモ）

税理士法人ACEあかり事務所（https://akari-z.com/）のリニューアル提案用デモ。方針・交渉状況は `C:\Users\hangx\Documents\org\akari-hp.md`。

## 構成
- `site/` … 公開物。ブラウザで `site/index.html` を開けば確認できる（`site/proposal.html` は父向けの提案書、noindex）
- `tools/build.py` … 全ページのHTMLを生成（`python tools/build.py`）。事務所情報・スタッフ・お客様の声・FAQは冒頭の定数にある。**HTMLを直接編集せず、ここを直して再生成する**（proposal.html だけは手書き）
- `tools/optimize_images.py` … 現行サイトの画像をWebPに変換（元画像→`site/img`）
- `tools/convert_videos.sh` … スタッフ動画（現行 `wp-content/themes/akari/video/video2023/`）をH.264のMP4＋サムネイルに変換（→`site/video`）。写真と動画の対応は `build.py` の `VIDEOS`
- `tools/make_logo.py` … 白背景ロゴを透過化（ヘッダー用・フッター白文字用）
- `site/css/style.css`, `site/js/main.js`

## 決まりごと
- ファイル名＝現行サイトのURLスラッグ。本番は同じURL（拡張子なし）で公開し、SEOを引き継ぐ
- canonical / og:url は本番URL（https://akari-z.com/xxx）で出力済み
- `.tbd`（黄色下線）は仮の内容。父の確認が取れたら定数を直して外す
- お問い合わせフォームはデモ（送信しない）。本番は送信先の実装が必要
- 上部の「デモサイトです」帯（`header()` 内 `.demo-ribbon`）は本番で削除
