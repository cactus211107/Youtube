import subprocess
import json

curl_command = '''
curl 'https://spclient.wg.spotify.com/color-lyrics/v2/track/1ChulFMnwxoD74Me8eX2TU/image/https%3A%2F%2Fi.scdn.co%2Fimage%2Fab67616d0000b273bd0c47e4cfb4ee327e53bc73?format=json&vocalRemoval=false&market=from_token' \
  -H 'authority: spclient.wg.spotify.com' \
  -H 'accept: application/json' \
  -H 'accept-language: en' \
  -H 'app-platform: WebPlayer' \
  -H 'authorization: Bearer BQBG12sy2Wt4TLH_MwYV7MFHt-TM6QNUV73TdWuI5Ud9yEiC7G3wiv9MVG9RvjBe0WYuPIAT4XzIEX4mGVu1rkjSikdMaqKhViu9zNRCefo5BiNokjVbYx98NLooX_mspzfvB-Vowul46xpNkjzC5Cj1zlx_ntdr2BT9L5KnoDamyjB-tjlS-OwyN0_YLPy6-7VZkXLpfNCHsul0Z9SqpM5TlCovf26Kya5HNBJ4Pae7orM3A7QMlxMRP10IxVWIn9fngUZ_XarDR5GWwbhE6NWvQGIXd_zInHuxOZwPr7e3Go53t9Xa6dM3xFSbaw1Thj77aD0sbV7EHrUCwdJb-Nsmwtlb' \
  -H 'cache-control: no-cache' \
  -H 'client-token: AADV+t7jMUYiRYPGETyagma/qrR5cz1QetSQgwdH1HCQROA1+iVA9Envaa6PwWWEFp40x5SznPzH1XsIv6RredgL+d5P+aiUZ2beoSg0VOLwD/duGcZMWR82DLgbNIh6GbXpvdpmTp0MdRLfcvd7sxVfumLSlJmzjmZ1eggER+EfAUAfwMGldoVz8Kc1Nuw10I4osp2VBWp2Ifq7p7AC/JWoxoJZudZT8ixEGc6Z1D2s4W8isXzDuuTW+b0RQhJQM2PkpkkVhtKwko6ZgKmKHNxwko56saP4/aI4Ja+yWg==' \
  -H 'origin: https://open.spotify.com' \
  -H 'pragma: no-cache' \
  -H 'referer: https://open.spotify.com/' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'spotify-app-version: 1.2.34.412.geaac6107' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0' \
  -v
'''

# Execute the cURL command and capture its output
process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Check if there's any error
if stderr:
    print("Error occurred:", stderr)
    json_response = None
else:
    # Parse the JSON response
    json_response = json.loads(stdout.decode('utf-8'))

# Now you can use json_response as needed
print(json_response)
