ComicInfoEditor
===============
#What is This?
Comicrackで生成されるComicInfo.xmlを快適に修正できるソフトを目指しています。
将来的には[The Doujinshi & Manga Lexicon](http://www.doujinshi.org/)から情報を取ってくれるようなものになります。
（その機能がなければ、Comicrack組み込みのタグエディターがあればいい話だし）

#What Can This Programme Do?
現在、Comicrackでメタデータを埋め込んだアーカイブファイル（ZIP形式）に含まれているComicInfo.xmlを開いて
情報を取り出して表示することまではできます。ただし、設計者である自分が使っているフィールドしか扱えないようにしているので
他のフィールドも使いたい、という場合は各自修正する必要がありますね。
現在取り扱えるようになっているフィールドは
* Series
* Number
* Title
* Writer
* Penciller
* Genre
* Year
* Month
* Day
のみです。

GuiWindow.pyにエントリーポイントがあるので、そちらを実行するとひとつのウィンドウが現れます。
現時点ではフィールドをとりあえず作っただけで何がなんだかわからないですが、各ボックスが上記のフィールドのどれかに対応しています。

ファイルを開くには、'...'ボタンでファイル選択ダイアログを出して選ぶか、ウィンドウにzip,もしくはcbzアーカイブをドラッグアンドドロップすることでも開けます。
ただし、現在間違ったファイルを開いたりComicInfo.xmlが入っていないファイルを開いた時の処理が実装できていないのでエラーが発生するはずです。
一応複数のファイルをドラッグアンドドロップしたときだけはちゃんとエラーメッセージを表示してファイルを開かないような処理をします。
ファイルが正しく開けたら、いくつかのテキストボックスに値が入っているはずです。現状表示するだけで書き換え・追記はできません。

サンプルの~.cbzファイルたちにはすでにComicInfo.xmlが入っているので、Comicrackを使っていなくても動作確認をすることができます。
もちろん、画像ファイルはすべて削除しているので読むことはできません。