# dorker
Perform a list of google dorks on a given domain (and its subdomains)


# Usage

``` 
python dorker.py --domain a.com --payloads dorks.txt
or
python dorker.py --domain a.com,b.com --payloads dorks.txt --output  output-dir --additional-query 'ext:php'

To use proxy (export HTTPS_PROXY=10.10.10.10:1010)
```


Argument | Description
-------------- | ----------------
`-d` or `--domain` | Target domain or comma seperated multiple domains (i.e. "a.com,b.com,c.com")
`-p` or `--payloads` | Payloads list of google dorks
`-a` or `--additional-query` | Additional Query
`-o` or `--output` | Output directory


## Requirements
* python2
* googlesearch
* requests
* termcolor
* argparse

## Notes
This tool is old -but working as of November 2020- and not maintained anymore. This program is created for educational purpose only ,the creator assume no liability and is not responsible for any misuse or damage caused by this program. Only use legally.
