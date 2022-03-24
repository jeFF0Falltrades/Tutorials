# AsyncRAT Configuration Parser
## YouTube Video
* https://youtu.be/xV0x7kNZ_Yc

## YARA Rule for Hunting
* https://github.com/jeFF0Falltrades/YARA-Signatures/blob/master/Broadbased/asyncrat.yar

## Requirements
```
pip install cryptography
```

or

```
pip install -r requirements.txt
```

## Usage
```
usage: asyncrat_config_parser.py [-h] [-d] file_paths [file_paths ...]

positional arguments:
  file_paths   One or more AsyncRAT payload file paths (deobfuscated)

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Enable debug logging
```

## Example Input/Output
```
$ python3 asyncrat_config_parser.py ReverseMe.exe | python -m json.tool
{
    "aes_key": "40766aef6f9d6980c001babeef7020446eff2ef31cf910cab59d5429d7a89c37",
    "aes_salt": "bfeb1e56fbcd973bb219022430a57843003d5644d21e62b9d4f180e7e6c33941",
    "config": {
        "Anti": "false",
        "BDOS": "false",
        "Certificate": "MIIE8jCCAtqgAwIBAgIQAMe2UpmBbjqdMItW7xySBzANBgkqhkiG9w0BAQ0FADAaMRgwFgYDVQQDDA9Bc3luY1JBVCBTZXJ2ZXIwIBcNMjExMjA3MDE0NTQ1WhgPOTk5OTEyMzEyMzU5NTlaMBoxGDAWBgNVBAMMD0FzeW5jUkFUIFNlcnZlcjCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAPHqNpoIpvegBcEOCxChs8Nw2/fS/hTdwqoaD0KkwGB52FRN/YncQZm3N1uqPRRM+nDslfwCdPlF7m895TnA7CB6NPUrGdi3Sbt5OE30a4gNrguHdC8MNVqoBA3mWZfT/nxmzXn7/KJfUH9UWPTJbC32B7ELwR71RALMPzIgE78AtpC3uU3f8Y+QTDt5xSR3MhfGFnIaMUuMRyZUMO9VV/7Ik4t2uUSsnYB8M6c6ytHkFokxNxdQJTWuJEW5ckGbWyWXkZlkGBcGz/6/cH1PdJBa/jK73xfwgrNoKKKvv+bWoBUPGg98jsXAfhIBOhkb9XVSp9t7bLNDuAh2uhbQejI3ZbSGwOYWWJGZYue92VuY/KPDZabD8IzwHLVdNAfQNSNzJXBycljYFzpErYp28j81/d2l+2I2DTdf1eZKiHHvNxeHPRpCNt05bk5NTl4gAtnOKwErV181jRnjMiB2oWWxAF2p2whU+85OeUywz/Ge7gmRgFW/pIqSReBA874YLmwRih51U0V1rr+oQlkk6qpvDW5tdpsuodlVL8R6lDx3pE88uPXDdfUdqyfjdF9zKyuk4K55LmBAwD/MgB+XtnZA74n0zG/vKyJQJa8yeJpHXOwt7hgtg5HJt+8cMdwh9L3J7ZWRqZchFvNeYSM9DW5c/uff33txCaLWrlHdeJOPAgMBAAGjMjAwMB0GA1UdDgQWBBQ2SPyox4Jk9VX7tmV493O/6f9oNDAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBDQUAA4ICAQDspo2PPJ/sPl8+SZQ7NXokPB8D8cFlFsDDSi2q1TWJQ+qtMO+74U2I2h2FBBTPH6hB+F/2NW1pq49B9n/v41Wg5YKbifR9mUnueTL//r0c8dW+Fr7+Teji4ZDuOPypL9/IbM3eLflTpofVhHRWZCZ5gboX16gCMQUoOPMNWFmssPX8SJSwNO1TqnaceWU6+bmHIpNuryU/tvut3wXQEV0x7lszB0veBYy9dkhwIz+Y8VfqH9ID4i2fn5ATepialht0v4TALwA65/Tc/y9aXcxPr9JbhSP+hLkE13QzHFUEmGOgvd7XHUJKkD7pU3grbxO75osuCWRSv7L1PRX5EvYMGMfe8mFWJioI0VEFgZqvMH5jSfCDN+bqAkJVmG5Y9a9b5DmbZARTujI0XvDbmzRYPuwqntU0HZryxGhiOnDTPKsguvpmaJuzUPW+BN5y3aGuuwAvp+++yAMihVpc77rqcpocn/j6olN9jtL0GAGqYQtBVlAgMVyLX47TOM1GxcL7S9TCwDJ/xvUMc4Hhw63bcpYX8SjssCFzhXCB3Xr79KdKxE78M5YGG8Jj3bzlxLQAqV/1air5+pDLmQq6bUJ2UZnHgZxG5K9QjsQU0emJP0IyashQMBCG2uGuElXh2W4oy4SmIj5BE0ztFpDqQwTGJAzgrXIMBj8l4zJtKDlH2Q==",
        "Delay": "3",
        "Group": "Default",
        "Hosts": "test.me.com",
        "Install": "false",
        "InstallFile": "",
        "InstallFolder": "%AppData%",
        "Key": "N3UwelhLaE5BaTE5Z3piMFEwMFZlWHI2Z01Nc3dPOWM=",
        "MTX": "AsyncMutex_6SI8OkPnk",
        "Pastebin": "null",
        "Ports": "8808,7707",
        "Serversignature": "ZKSsdlzb5lEwgaF35KH+qv8Ai7M74R+W9CU2NpGy4ucvLuKhDbUpJtqllJuFAk22wP6qgCQ8lvE8zy+LlVHmCRovNGIcLKEIERkQGZDB7+puIsVLV2dzrcO4uRdKdcQWef+9T8rpzS3uuQ3YXuBwCEq70GpIz3ngiq9vlukj+ZvdBCVZRYve+Pc2dHsUPU413OpWFRQsOSnCZPohd0IzdrD4AXOBIeBOlpFFfuLzNaA5rze7l+6ovEG8G31A+GafpXEso5Hs3dD7y7hy1mL1Wf7pH0Mu94bUfYfQamCZxWrGHIDa4O+2uEkrEsWKkvDDVXzLq8HxaSJBYhixq3mesV79zWX+ZytTN5R7kdDBN5+ZyICQgjWtUTAyoIulylwbHcSVZ4ODv+5R29OD/7RoHFfsQNCHjGvMIWiVsTUqi6fLGj3GButFDZldse10P4gaeDn6h6bfsfNCGK5J+86slLI3/kR/PSV71tH4ABWv/pgWFbRnRTbDUmuCekAdG8c1yBObyYIphRNjNqRoH8Lu5o+onzAT7giI1EdMAGDase5cQ3T9DOC9XDTJ6OFYdbz9RFQSKQGM1UuSecIi/CDQ9XvyHMYUr0yjXhYzbXEFSdydwr0nSz//Nk+7nPS4NiY2MuA/uJKvG4YkFJkG13eUltweM8Zeb1FzZPaw0CRDmes=",
        "Version": "0.5.7B"
    },
    "file_path": "ReverseMe.exe"
}
```
