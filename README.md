ComicInfoEditor
===============
#What is This?
[Comicrack](http://comicrack.cyolito.com/)で自炊した同人誌を管理する際のサポートツールです。。
[The Doujinshi & Manga Lexicon](http://www.doujinshi.org/)、以下doujinshi.orgと連携することにより、
書誌情報の入力する手間を大きく省くことができます。

#What Can This Programme Do?
Comicrackではコミックアーカイブの管理に多くのメタデータを入れることができますが、このアプリケーションがサポートしているのは以下の項目のみです。
* Series
* Writer
* Penciller
* Genre
* Year
* Month
* Day
doujinshi.orgにおける情報とはこのように対応しています。
* Series → 原題
* Writer → 発行サークル名
* Penciller → 著者名

#Needed Libraries
beautifulsoup4
wxPython
また、動作確認はPython3.4.1で行っています。

#How to Use
このスクリプトを使ってメタデータを編集する前にComicrackで入力されているメタデータをすべてクリアしてください。
Comicrackが各ファイルに埋め込むメタデータファイルとは別にデータベースがあるようで、メタデータファイルとデータベースがコンフリクトした場合はデータベースのほうが優先されるようになっています。
つまりComicrack外でいくらメタデータを編集してもComicrackが読み込むと同時に書き戻してしまうということです。これはComicrack側の問題なので修正は難しいと思います。
フィールドが空白になっている場合だけは変更が正しく反映されるので、編集前に空白にしておく必要があるということです。

ComicInfoEdirtorスクリプトを実行すると、メインウィンドウが出てきます。
...ボタンを押すとファイル選択ダイアログが出てくるのでComicrackの管理下に入っているアーカイブを開いてください。
ウィンドウにドラッグアンドドロップすることでも開くことができます。
この際、Comicrack側でアーカイブ内にメタデータを管理するComicInfo.xmlがアーカイブ内に埋め込まれていることが前提となります。
Comicrackの設定からメタデータをファイルに書き込む設定にしておいてください。
ComicInfo.xmlがいつ埋め込まれるか、細かいことはわかりませんが一度Comicrackのファイル形式変換を使ってアーカイブを処理すると確実です。

メタデータの入力は手入力でも可能ですが、doujinshi.org連携機能を利用すると便利です。
タイトルの一部を入力しSearchボタンを押すと自動で書誌情報の候補を取得できます。候補の中に答えがあればそれをダブルクリックしてください。
フィールドに書誌情報が自動入力されます。
ただし、doujinshi.orgの検索仕様により、タイトルはトークンごとの前方一致検索しかできません。
たとえば「東方浮世絵巻 霊夢のどきどき玩具箱」というタイトルの場合、「東方浮世」や「霊夢のどき」ではヒットしますが「浮世絵巻」などではヒットしません。
また、英語など非日本語タイトルの作品、記号からタイトルがはじまる作品の検索もあまり良い精度ではないので過度な期待はしないでください。
もちろんdoujinshi.orgに登録されていない作品もあります。

タイトル検索では難しい場合はdoujinshi.orgの個別ページURLを入力することで直接情報を取得することができます。
先ほどの「東方浮世絵巻 霊夢のどきどき玩具箱」の場合はhttp://www.doujinshi.org/book/701010/になります。

入力が完了したら、Saveボタンを押すとComicInfo.xmlに書き込まれます。
この際エラーが発生するとComicInfo.xmlが消えたりすることがあります。しかしアーカイブ自体が破損ような事態は発生していませんし、おそらくしないと思うので
もう一度Comicrackでxmlを生成させてやり直してください。
