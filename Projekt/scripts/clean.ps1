# Remove working folders and files.
 
$source = "source"
$target = "target"

if (Test-Path -path $source) {
    Remove-Item -Force -Recurse $source
} 

if (Test-Path -path $target) {
    Remove-Item -Force -Recurse $target

}
