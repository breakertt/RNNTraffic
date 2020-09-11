# Usage: PS Y:\py-repos\RNNTraffic> .\datasets_processed\packet2seesion.ps1

$SOURCE_DATASET_DIR = ".\datasets_selected\"

foreach($filename in Get-ChildItem -Recurse $SOURCE_DATASET_DIR *.pcap)
{
    $new_path = Resolve-Path -relative $filename.FullName
    $new_path = $new_path -replace [regex]::Escape($filename.Name), ''
    $new_path = $new_path -replace [regex]::Escape("datasets"), 'datasets_processed'
    $new_path = $new_path + $filename.BaseName

    datasets_processed\SplitCap -p 100000 -b 100000 -r $filename.FullName -o $new_path

    Get-ChildItem $new_path | ?{$_.Length -eq 0} | del
}