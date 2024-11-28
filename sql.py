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

# Kullanıcılar tablosunu oluştur (eposta alanı UNIQUE olarak ayarlandı)
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

# Bağlantıyı kapat
cursor.close()
conn.close()
