from django.contrib import admin
from check_app.models import Device, MTT, Token, PhoneDevice
import random
import uuid
import requests

# Register your models here.

INTEGRITY_TOKEN = '''eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2R0NNIn0.pvAf1tptqcHdPT27g0PppFHhw0e63NuUb9LyU9665VGmtUYPiB-vlw.mljJaFoH678Xbvey.qxZL2W3ESWsxvflSOcYOkmTjbcnY54Lqqd-U9vsbtQZXC1V0cll2cCg50dngUlenLxkBhVgGqgQAZ80IeiVoYlgymyUDAGz-hET64s6ZnzYVwsY2ifRPPllllucR-H1swFWSAQS52VInWW0vvSJXGtKqbboS_FX7Fz0p7nfDAG-slKoDGO-WfS9Eq1nUUoZYYL16-lZmgS6nlunjFdrvuyBnTkYLnJrX1CsjDtDueGcTHt1w7Viy27dMlvGMgeS-53sRtr9LnzmwAbdtRH_6Ss7WT8Ph_HjAdkPPAvFHDNKdDdiSo2cRBkSzJcEFDTM908Z4CiGykZtqoGbRNKD_oaOeYcHcBeBkwkMc02du9dC8CE0XkktZwr7TSA8cPokJsLx-DttPZxvI5iZdZw_QaociMRpXqLx_gmhbb0hAx3xBU79714UAZ-JdoLcoOYg3mUv-HZFuODkDNXQLRtRy00S09O-HWiLt7V9B0uvJ2Eb0IAbyxcjeSBbhcsbp0EimY9aB7TSX3SUdVV6n1x_xcdJiQ6fAGU4vDoMyztkNA3SipTr8xn37HL_yh-1eLmsQS4XlKIJj0OCp6INygTcCAwekyBTDsfRRQBuQ-fWZd6ZYYtTe24EifYJMiHM--pZvRXpxESWIpRvjE-_kzDcceEoW9oL-KiAPnyiHj2S58Zh8Tmzi3KRINkuEuWh46L6BENdhWOKJUpcfCDCBkyIaqwrn6X58NrpDRr0fVO4kWyd2ZsXAlgvoDz4h1hzrCWbO99hyEFHvVZS8PxuPsqKAcpyVjTXNBj2WIY2MyvAFXIdGxP483FEbFwSRemOw2nGiK_ihPB5b2IHolgaMYg9Fu9p8A3k5ZJIZaKYJc4Gw69TLh2Ga6yu1z5Ok9eaaAc7p42KQ3OlrgaxhaCWVmZ3ORfqRnQoZf-1otE8WfPH3ELGTaX0qW8o781iB1pl7PEmdwzrJE_UOWXyOLMw4lKNNAAS8gMFy3pzGFoQfg8Wjk5DlT0ix7P7crm0dDtQiiT_Qw4RM0RR3Ul0MCITFGxfeXmbD8YFanYMnkEh1zqzlVBUDwCcghQ6N0yb9eDThFdaIOdhUWgg0y7Ad4ows2Xqi1UvMX6j6-gEw3nzynh3wK82_83cXrj7D1PEFRsidDX8jErj1Sp81Nm9JzqpuNthSSl9yazSPQnv_5FdQNqtRVMvoasZiY7BsohlArh74cow_I6vntzsBzbHWoAt7EwGNiU8mneWNstK_xs3MEoXMuQo3lIiFV1rog4mWBkrwQxP_gqsO_z4uhMrwgYrz7MDQndvFmtDPpRu40RxaE84jfpE174h52AS-rdRzdX1w80p3t8IXfxgC7KU8GXqBKDDvM3omYAPGCdiRYnmBCPqokmYzBWb2rn78kG1HIsSQNcKsyKPi2Knp1E5bWxdCFkJZ6wu9YuTPvzSs0KOIFrCbT15eSvfIuvZzY9fknwVXFE_1Yphz5P03PoDZFxETCKXLPcddVFR0bfenPAZLoikpf07bw3xry1xu2Y6bC44SZZAlrT7PXO_NJkdFCxNl2qnrbaQMWOTJ0zjafzCwzRQ1GYE.bWJN1b_l1z3MqmWjGb9JjA'''

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('license', 'status', 'is_delete', 'created_at', 'updated_at')
    search_fields = ('license',)
    list_filter = ('status', 'is_delete')
    ordering = ('-created_at',)
    list_per_page = 100

@admin.register(MTT)
class MTTAdmin(admin.ModelAdmin):
    list_display = ('license', 'username', 'password', 'created_at', 'updated_at')
    search_fields = ('username',)
    list_filter = ['device']
    ordering = ('-created_at',)
    list_per_page = 100

    def license(self, obj: MTT):
        return obj.device.license
    
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'mtt', 'created_at', 'updated_at')
    search_fields = ('mtt__username',)
    list_filter = ['mtt']
    ordering = ('-created_at',)
    list_per_page = 20

    def mtt(self, obj: Token):
        return obj.mtt.username
    mtt.short_description = 'MTT Username'

    def generate_android_device_info(self):
        manufacturers_models = {
            "Samsung": [
                "SM-G991B", "SM-G996B", "SM-G998B", "SM-N986B", "SM-S908E",
                "SM-A526B", "SM-A325F", "SM-M326B", "SM-F926B", "SM-T870"
            ],
            "Xiaomi": [
                "M2011K2G", "M2007J20CG", "M2101K6G", "M2102J20SG", "M2104K10C",
                "M2012K11AC", "M2101K7AG", "M2010J19SI", "M2105K81C", "M2106K7AI"
            ],
            "Huawei": [
                "ELS-NX9", "MAR-LX1M", "INE-LX1", "ELS-N29", "ELS-NX0",
                "ART-L29", "ELS-TL00", "MAR-LX3A", "BKL-L09", "YKUD-W09"
            ],
            "OnePlus": [
                "IN2013", "KB2001", "HD1913", "LE2121", "LE2117",
                "PHB110", "LE2123", "M2007J20CG", "EB2101", "EB2105"
            ],
            "Realme": [
                "RMX3085", "RMX3063", "RMX3201", "RMX2151", "RMX2193",
                "RMX3031", "RMX2141", "RMX2176", "RMX2202", "RMX3261"
            ],
            "Infinix": [
                "X692", "X682", "X657", "X650", "X681B",
                "X688B", "X670", "X677B", "X689", "X685C"
            ]
        }

        manufacturer = random.choice(list(manufacturers_models.keys()))
        model_full = random.choice(manufacturers_models[manufacturer])

        # Toza model nomi (brendsiz) qoldirish uchun,
        # agar model kodida brend nomi boshida bo'lsa, strip qilamiz
        prefix = manufacturer + " "
        if model_full.startswith(prefix):
            device_model = model_full[len(prefix):]
        else:
            device_model = model_full

        device_name = f"{manufacturer} {device_model}"

        return {
            "device_id": str(uuid.uuid4()),
            "base_device_id": str(uuid.uuid4()),
            "device_manufacturer": manufacturer,
            "device_model": device_model,
            "device_name": device_name,
            "os": "34"
        }
    
    def token_func_v3(self, username: str, password: str, app_version, device_id, base_device_id, device_model, device_manafacture,device_name) -> str:
        # print(username, password)
        url = "https://kindergarten2.istream.uz/customer/token"
        data = {
            "username": username.strip(),
            "password": password.strip()
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "integrity-token": INTEGRITY_TOKEN,
            "X-App-Source": "PlayMarket",
            "App-Version-Code": app_version,
            "App-Version-Name": "1.4.6-pm",
            "Device-Id": device_id,
            "Base-Device-Id": base_device_id,
            "Device-Name": device_name,
            "Device-Manufacturer": device_manafacture,
            "Device-Model": device_model,
            "Android-OS": "34",
            "Accept-Language": "uz",
            "User-Agent": "okhttp/4.9.3"
        }
        session = requests.Session()
        session.trust_env = False

        session.proxies = {
        "http": None,
        "https": None,
    }
        
        r = session.post(url, data=data, headers=headers, timeout=100)
        # print('\n\n\n')
        # print(r.text)
        # print('\n\n\n')
        if r.status_code != 200:
            mtt = MTT.objects.filter(username=username, password=password)
            
            if mtt:
                mtt.delete()
            return None
        
        return r.json()['access_token']
    


    def generate_tokens(self, request, queryset):
        print("Generating tokens for MTTs without tokens...")
        tokens = Token.objects.all()
        mtt_username_and_pwd_without_token = MTT.objects.exclude(token__in=tokens).values_list('username', 'password')
        print(f"Found {len(mtt_username_and_pwd_without_token)} MTTs without tokens.")
        if True:
            for username, password in mtt_username_and_pwd_without_token:
                device_info = self.generate_android_device_info()
                token = self.token_func_v3(
                    username=username,
                    password=password,
                    app_version="1226",
                    device_id=device_info['device_id'],
                    base_device_id=device_info['base_device_id'],
                    device_model=device_info['device_model'],
                    device_manafacture=device_info['device_manufacturer'],
                    device_name=device_info['device_name']
                )
                print(f"Generated token for {username}: {token}")
                if not token:
                    print(f"Failed to generate token for {username}")
                    continue
                if token:
                    token = Token.objects.create(
                        mtt=MTT.objects.filter(username=username).first(),
                        token=token
                    )
                    phone_device = PhoneDevice.objects.create(
                        token=token,
                        model=device_info['device_model'],
                        manafacturer=device_info['device_manufacturer'],
                        device_id=device_info['device_id'],
                        base_device_id=device_info['base_device_id'],
                        device_name=device_info['device_name']
                    )

        return 'Success'
    
    generate_tokens.short_description = 'Generate tokens for MTTs without tokens'
    actions = ['generate_tokens']


@admin.register(PhoneDevice)
class PhoneDeviceAdmin(admin.ModelAdmin):
    list_display = ('model', 'manafacturer', 'device_id', 'device_name', 'mtt')
    search_fields = ('token__mtt__username', 'model', 'token__token', 'manafacturer', 'device_id', 'device_name')
    
    list_filter = ['token__mtt__username']
    # ordering = ('-created_at',)
    list_per_page = 20

    def mtt(self, obj: PhoneDevice):
        return obj.token.mtt.username if obj.token and obj.token.mtt else 'No MTT'

    def token(self, obj: PhoneDevice):
        return obj.token.mtt.username
    token.short_description = 'MTT Username'