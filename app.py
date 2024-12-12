from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc

app = Flask(__name__)
app.secret_key = 's3cr3t'

# Veritabanı bağlantısı
def get_db_connection():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                          f'SERVER=localhost;'
                          f'DATABASE=fintek_db;'
                          f'UID=sa;'
                          f'PWD=Mei@2024!')
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Kullanicilar WHERE eposta = ?', (email,))
            user = cursor.fetchone()

            # Eğer kullanıcı bulunmazsa
            if not user:
                flash('E-posta adresi bulunamadı.', 'error')
                return render_template('login.html')

            print(f"Veritabanından gelen şifre: {user[5]}")  # Hashli şifreyi yazdıralım
            if check_password_hash(user[5], password):
                session['user_id'] = user[0]
                return redirect(url_for('home'))
            else:
                flash('Şifreyi kontrol edin', 'error')

        except Exception as e:
            flash(f'Giriş sırasında bir hata oluştu: {str(e)}', 'error')

        finally:
            conn.close()

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Boş alan kontrolü
        if not (first_name and last_name and email and password and phone):
            flash('Boş alanları doldurunuz.', 'error')
            return render_template('signup.html')

        # E-posta kontrolü: Veritabanında bu e-posta ile başka bir kullanıcı var mı?
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Kullanicilar WHERE eposta = ?', (email,))
        existing_user = cursor.fetchone()
        conn.close()

        # Eğer e-posta zaten kayıtlıysa, kullanıcıyı uyar
        if existing_user:
            flash('Bu e-posta ile zaten bir hesap bulunmaktadır.', 'error')
            return render_template('signup.html')

        # Şifreyi hash'leyin
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Kullanıcıyı veritabanına ekle
            cursor.execute('''
                INSERT INTO Kullanicilar (ad, soyad, eposta, telefon, sifre)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone, hashed_password))

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash('Kayıt sırasında bir hata oluştu.', 'error')

        finally:
            conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Kullanıcı bilgilerini veritabanından al
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Kullanicilar WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()

    # BIST100 şirketlerini al
    cursor.execute('SELECT * FROM Bist100Sirketleri')
    companies = cursor.fetchall()
    
    print(companies)

    conn.close()

    return render_template('home.html', user=user, companies=companies)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    # BIST100 şirketinin ID'sini URL'den al
    company_id = request.args.get('company_id')

    # Şirket bilgilerini veritabanından al
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bist100Sirketleri WHERE id = ?', (company_id,))
    company = cursor.fetchone()
    conn.close()

    # Burada tahminleme işlemi yapılacak

    return render_template('prediction.html', company=company)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
