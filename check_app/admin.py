from django.contrib import admin
from check_app.models import Device, MTT, Token, PhoneDevice
import random
import uuid
import requests

# Register your models here.

INTEGRITY_TOKEN = '''eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2R0NNIn0.wKD7hvqtiabejfWtYzVO9Syn5G22sLHTKNQjzT5mMAApVS9Wy4XSfQ.9q24rU-YjWuxKRpz.wWJWJ6ocntM8pI4ai3m0NaFMaPrP2hiGkx0XVGvXVzVQaauvN9Vf0z8wES0Dr96xj5-PP5hWl9Ydotl_DNxhZ35OEimhIA9NLBjAfmu_mfAIBDgXFl2octtGH5szzCHCjI_1Hnd2nHm6xEf9-Lq6PfdrvV5PaYsVjRzO3MUoiCZnM1fZQGOohytxDvEcKQMlEbBOjItJBnXWRX6GhPY3Ej306IU4iavwYIka_LQs91hKyN6c80KQmETKZIpRjtuLwmWwhU3gqv9uus55LTflkGnAerft3xCvvDJeCkcM05TLSVDawKjAKyUfBHhDbDqlJZSJQs_pT0BeuwmTTIR7iUHyUk4F1cIDh-Diq0Dy3J9rmNctI_VHcrcGtOYAz2jV9hdeD_rQOVMZgrn0NCXHlaRD62hM-bx4B0Md9xAO7Q43OyiC8aZ_RmneRD4otp_K_zEmBvZ5rEbxPnrqm8Wa9ffP-AlnJQsc7P4D8iJDrQc6Vk0NKXe_DIwNN8qnuSodG5XXpnSB7ZENGG5xoK2bxWuLv9mwsDwI-jJt_2SR0_Z1PNecjmnsPFVmt2S-cV6ftTGmIvmBf6T3YCctP7f-oOO5z5UE1IAKw2FOR4iBRdS4-eMODiU52lsYDnrY5FaDjiRkGi50fIo9ebS6KoHSxD8KN2Xpq8ySZWt3aKZLNnot7uFjJvwbrlQEueSlZlLY3JtnMblDNNkpdJOAp1l2wrNjCSGnSn5ntNrAwvz4JUODfaFuD-09H92oqcy1Zpn3AmaP13CnmQUjHNDGTbsWHowLK4ilgybdzApoj2AVk6AQP4cNvKKe_2sacwGsaUr7R-862AOQTMHemm7j_ung0DBv9xBWw9G7D0jRypu6g6w-lLAjy6W5N5CGigKPz56v_Iaz06a9KfnLUgBJm1_OU5lZhqnAqAhladUoOXH1F_74ZbaILzsFLanjQrJhTzz9qVRZ6svNJ6T1RIl-Dab2lmQiNjSyBl0ihXtrVl2KHr0rm-94aMUJYRZkCjH4ofNOl14GGBiBbQ9jynKKg3VSiLnlXjJcfTuzJD1aOqG0OBqI4CBJoURciVrJYOTAYHncKE14CtuLv2O5LivytZSEMW-Hnsr2Xl3qEapNQPbkFbl-mMS8yzmMxqR23sBRctmGSAf4XgOte_sSEsnesbDvfXoQ52VdGEnhXdaQFWVeLORwYPsE45_a5YHgw5mDplopewPqmfk6UIuLm10jYfd9CMSVeb_kn4fvcB_27olv6lAenlAPc-jm8wSVXsOWdojF2954zV67HVk6CmMJ047AnqaGC-qNqKqW8FioXlwSbdds6oWZzRrUFwzrc48xQsoMkOyAjCrQ9pq_3-_sGv_r11DXrGCxDaHnXnTnIyj8XUTCB5a50jue61d4iC0-apbCtlooEwB0Xr03PVIn0McRWBOsuBezwZQbgn_B8ZE3nHH74MJBEXJDbE9kJePU7WI_3bkqQfumaQGmKdsFW5uvQm4zOmEV3BDqixhPRtM_ZeAX69vbPmbnwjy_cXfkNLjgv2kRPNAxe3nP0xPnbZspkaoZfzLeqWiebXfwXMM-tk0.QWnrCd7vWISR-Kmg3cNzYQ'''

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('license', 'status', 'is_delete', 'created_at', 'updated_at')
    search_fields = ('license',)
    list_filter = ('status', 'is_delete')
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(MTT)
class MTTAdmin(admin.ModelAdmin):
    list_display = ('license', 'username', 'password', 'created_at', 'updated_at')
    search_fields = ('username',)
    list_filter = ['device']
    ordering = ('-created_at',)
    list_per_page = 20

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
            "device_manufacturer": manufacturer,
            "device_model": device_model,
            "device_name": device_name,
            "os": "34"
        }
    
    def token_func_v3(self, username: str, password: str, app_version, device_id, device_model, device_manafacture,device_name) -> str:
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
            "App-Version-Name": "1.3.2-pm",
            "Device-Id": device_id,
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
                    app_version="1212",
                    device_id=device_info['device_id'],
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
                        device_name=device_info['device_name']
                    )

        return 'Success'
    
    generate_tokens.short_description = 'Generate tokens for MTTs without tokens'
    actions = ['generate_tokens']


@admin.register(PhoneDevice)
class PhoneDeviceAdmin(admin.ModelAdmin):
    list_display = ('model', 'manafacturer', 'device_id', 'device_name', 'token__mtt_username')
    search_fields = ('token__mtt__username', 'model', 'token__token')
    
    list_filter = ['token__mtt__username']
    ordering = ('-created_at',)
    list_per_page = 20

    def token(self, obj: PhoneDevice):
        return obj.token.mtt.username
    token.short_description = 'MTT Username'