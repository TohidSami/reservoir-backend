import pandas as pd
import numpy as np

print("--- شروع ساخت داده‌های تولیدی واقع‌گرایانه (1000 روز) ---")

days = 1000
time_vector = np.arange(days) # یک آرایه از 0 تا 999

# تعریف پارامترهای شبیه‌سازی برای هر چاه
# ما 3 چاه خود را با رفتارهای متفاوت تعریف می‌کنیم
well_params = {
    'Well-A1': {
        'oil_initial': 2000,   # دبی اولیه نفت (bbl/d)
        'oil_decline': 0.0005, # ضریب کاهش نمایی روزانه (D)
        'gor_initial': 800,    # GOR اولیه (scf/bbl)
        'gor_increase': 0.5,   # افزایش GOR در هر روز
        'wc_initial': 0.02,    # Water Cut اولیه (2%)
        'wc_increase': 0.00025 # افزایش WC در هر روز (تا 27% در 1000 روز)
    },
    'Well-B2': {
        'oil_initial': 3000,   # چاه قوی‌تر
        'oil_decline': 0.0008, # اما با افت سریع‌تر
        'gor_initial': 600,
        'gor_increase': 0.3,
        'wc_initial': 0.05,    # مشکل آب بیشتر از اول
        'wc_increase': 0.0003
    },
    'Well-C13': {
        'oil_initial': 1500,   # چاه ضعیف‌تر
        'oil_decline': 0.0003, # اما با افت بسیار کم
        'gor_initial': 1200,   # گازی‌تر
        'gor_increase': 0.8,
        'wc_initial': 0.01,
        'wc_increase': 0.00015
    }
}

data_frames = []

for well_name, params in well_params.items():
    print(f"در حال شبیه‌سازی داده برای چاه: {well_name}...")
    
    # 1. شبیه‌سازی نفت (Exponential Decline)
    # q(t) = q_i * exp(-D*t) + noise
    noise_oil = np.random.normal(loc=1.0, scale=0.03, size=days) # نویز 3%
    oil_base = params['oil_initial'] * np.exp(-params['oil_decline'] * time_vector)
    oil_rate = (oil_base * noise_oil).clip(min=0)
    
    # 2. شبیه‌سازی گاز (Increasing GOR)
    # GOR(t) = GOR_i + C*t + noise
    noise_gor = np.random.normal(loc=1.0, scale=0.05, size=days) # نویز 5%
    gor_trend = params['gor_initial'] + params['gor_increase'] * time_vector
    gor = gor_trend * noise_gor
    # Gas Rate = Oil Rate * GOR (و تبدیل از scf به Mscf)
    gas_rate = (oil_rate * gor / 1000).clip(min=0)
    
    # 3. شبیه‌سازی آب (Increasing Water Cut)
    # WC(t) = WC_i + C*t + noise
    noise_wc = np.random.normal(loc=1.0, scale=0.05, size=days) # نویز 5%
    wc_trend = params['wc_initial'] + params['wc_increase'] * time_vector
    wc = (wc_trend * noise_wc).clip(min=0.01, max=0.9) # Water cut بین 1% و 90%
    
    # محاسبه دبی آب از روی دبی نفت و WC
    # WC = Water / (Oil + Water)  =>  Water = Oil * (WC / (1 - WC))
    water_rate = (oil_rate * (wc / (1 - wc))).clip(min=0)
    
    # ساخت DataFrame برای این چاه
    dates = pd.date_range(start='2021-01-01', periods=days, freq='D')
    df = pd.DataFrame({
        'WellName': well_name,
        'ReportDate': dates,
        'OilProduction': oil_rate,
        'GasProduction': gas_rate,
        'WaterProduction': water_rate
    })
    data_frames.append(df)

# چسباندن داده‌های هر 3 چاه به هم (مجموعاً 3000 ردیف)
final_df = pd.concat(data_frames, ignore_index=True)

# ذخیره کردن در یک فایل اکسل
file_name = 'production_data_1000d.xlsx'
final_df.to_excel(file_name, index=False, engine='openpyxl')

print(f"--- فایل '{file_name}' با {len(final_df)} ردیف داده ساخته شد. ---")
print("می‌توانید این فایل را در اکسل باز کنید تا روندها را مشاهده کنید.")