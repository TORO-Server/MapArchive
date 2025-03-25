# 自動 Git 処理
$AutoGit = {
    param($WORLD, $YEAR , $MONTH)
    &git add $(Join-Path "." $WORLD $YEAR $MONTH)
    &git commit -m "$YEAR $MONTH $WORLD"
    &git push origin
}

# 一時的にファイル情報を保持する連想配列
$file_map = @{}
# 作業ディレクトリ内のフォルダをすべて取得
Get-ChildItem -Path "." -Directory | ForEach-Object {
    $WORLD = $_.Name
    Get-ChildItem -Path $_.FullName -Directory | ForEach-Object {
        $YEAR = $_.Name
        Get-ChildItem -Path $_.FullName -Directory | ForEach-Object {
            $MONTH = $_.Name
            $file_map.Add("$YEAR-$MONTH-$WORLD" , @($WORLD, $YEAR, $MONTH))
        }
    }
}
# キーの昇順に並べ替える
$file_map = $file_map.GetEnumerator() | Sort-Object -Property key

foreach ($entry in $file_map) {
    $val = $entry.Value
    # 自動 Git 処理 呼び出し
    &$AutoGit -WORLD $val[0] -YEAR $val[1] -MONTH $val[2]
}
