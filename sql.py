import pyodbc

server = 'localhost'  # MSSQL server'ınızın adresi
database = 'fintek_db'  # Oluşturduğunuz veritabanı adı
username = 'sa'  # SQL Server admin kullanıcısı
password = 'Mei@2024!'  # SQL Server admin şifresi

# Bağlantıyı kurma
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'UID={username};'
                      f'PWD={password}')

print("Veritabanına bağlantı başarılı!")

cursor = conn.cursor()

# Kullanıcılar tablosunu oluştur
cursor.execute('''
    IF OBJECT_ID('dbo.Kullanicilar', 'U') IS NULL
    CREATE TABLE Kullanicilar (
        id INT IDENTITY(1,1) PRIMARY KEY,
        ad NVARCHAR(50),
        soyad NVARCHAR(50),
        eposta NVARCHAR(100) UNIQUE,  -- E-posta alanını UNIQUE yaptık
        telefon NVARCHAR(15),
        sifre NVARCHAR(255)
    )
''')
conn.commit()

# BIST 100 Şirketleri tablosunu oluştur
cursor.execute('''
    IF OBJECT_ID('dbo.Bist100Sirketleri', 'U') IS NULL
    CREATE TABLE Bist100Sirketleri (
        id INT IDENTITY(1,1) PRIMARY KEY,
        sirket_kodu NVARCHAR(10) NOT NULL UNIQUE
    )
''')
conn.commit()

print("BIST100Sirketleri tablosu oluşturuldu.")

# Şirketleri eklemek için liste
bist100_sirketleri = [
    "ADEL", "AGHOL", "AGROT", "AKBNK", "AKFGY", "AKFYE", "AKSA", "AKSEN",
    "ALARK", "ALFAS", "ALTNY", "ANSGR", "AEFES", "ARCLK", "ARDYZ", "ASELS",
    "ASTOR", "BTCIM", "BERA", "BJKAS", "BIMAS", "BRSAN", "BRYAT", "CCOLA",
    "CWENE", "CANTE", "CLEBI", "CIMSA", "DOHOL", "DOAS", "EGEEN", "ECILC",
    "EKGYO", "ENJSA", "ENERY", "ENKAI", "EREGL", "EUPWR", "FENER", "FROTO",
    "GESAN", "GOLTS", "GUBRF", "SAHOL", "HEKTS", "ISMEN", "KLSER", "KRDMD",
    "KARSN", "KTLEV", "KCAER", "KCHOL", "KONTR", "KONYA", "KOZAL", "KOZAA",
    "LMKDC", "MAVI", "MIATK", "MGROS", "MPARK", "OBAMS", "ODAS", "OTKAR",
    "OYAKC", "PAPIL", "PGSUS", "PEKGY", "PETKM", "REEDR", "RGYAS", "SASA",
    "SMRTG", "SKBNK", "SOKM", "TABGD", "TAVHL", "TKFEN", "TOASO", "TUKAS",
    "TCELL", "TMSN", "TUPRS", "THYAO", "TTKOM", "TTRAK", "GARAN", "HALKB",
    "ISCTR", "TSKB", "TURSG", "SISE", "VAKBN", "ULKER", "VESBE", "VESTL",
    "YKBNK", "YEOTK", "ZOREN", "BINHO"
]

# Şirketleri sıralı bir şekilde ekleme
for index, sirket in enumerate(bist100_sirketleri, start=1):
    try:
        cursor.execute('INSERT INTO Bist100Sirketleri (sirket_kodu) VALUES (?)', (sirket,))
        print(f"{index}. Şirket {sirket} başarıyla eklendi.")
    except pyodbc.IntegrityError:
        print(f"{sirket} zaten tabloya eklenmiş.")
conn.commit()

print("BIST 100 şirketleri sıralı şekilde başarıyla eklendi.")

# Bağlantıyı kapat
cursor.close()
conn.close()
