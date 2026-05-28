from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app import db
from app.models import Shifokor, Xizmat, Bemor, Qabul, Xarajat, Smena
from datetime import datetime, date
from sqlalchemy import func

main = Blueprint('main', __name__)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import Foydalanuvchi
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Foydalanuvchi.query.get(int(user_id))




@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        parol = request.form.get('parol')
        user = Foydalanuvchi.query.filter_by(username=username).first()
        if user and check_password_hash(user.parol, parol):
            login_user(user)
            if user.rol == 'direktor':
                return redirect('/direktor')
            return redirect('/kassa')
        return render_template("login.html", error="Username yoki parol noto'g'ri!")
    return render_template('login.html', error=None)

@main.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/kassa')
@login_required
def kassa():
    return render_template('kassa.html')

@main.route('/direktor')
@login_required
def direktor():
    return render_template('direktor.html')

# --- SHIFOKORLAR ---
@main.route('/api/shifokorlar', methods=['GET'])
def get_shifokorlar():
    shifokorlar = Shifokor.query.filter_by(faol=True).all()
    return jsonify([{
        'id': s.id, 'ism': s.ism, 'mutaxassislik': s.mutaxassislik,
        'tashqi': s.tashqi, 'bonus_foiz': s.bonus_foiz
    } for s in shifokorlar])

@main.route('/api/shifokorlar', methods=['POST'])
def add_shifokor():
    d = request.json
    s = Shifokor(ism=d['ism'], mutaxassislik=d.get('mutaxassislik',''),
                 telefon=d.get('telefon',''), tashqi=d.get('tashqi', False),
                 bonus_foiz=d.get('bonus_foiz', 0))
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id, 'ism': s.ism})

@main.route('/api/shifokorlar/<int:id>', methods=['DELETE'])
def delete_shifokor(id):
    s = Shifokor.query.get_or_404(id)
    s.faol = False
    db.session.commit()
    return jsonify({'ok': True})

# --- XIZMATLAR ---
@main.route('/api/xizmatlar', methods=['GET'])
def get_xizmatlar():
    xizmatlar = Xizmat.query.filter_by(faol=True).all()
    return jsonify([{
        'id': x.id, 'nomi': x.nomi, 'narxi': x.narxi, 'kategoriya': x.kategoriya
    } for x in xizmatlar])

@main.route('/api/xizmatlar', methods=['POST'])
def add_xizmat():
    d = request.json
    x = Xizmat(nomi=d['nomi'], narxi=d['narxi'], kategoriya=d.get('kategoriya',''))
    db.session.add(x)
    db.session.commit()
    return jsonify({'id': x.id, 'nomi': x.nomi})

@main.route('/api/xizmatlar/<int:id>', methods=['PUT'])
def update_xizmat(id):
    x = Xizmat.query.get_or_404(id)
    d = request.json
    x.nomi = d.get('nomi', x.nomi)
    x.narxi = d.get('narxi', x.narxi)
    x.kategoriya = d.get('kategoriya', x.kategoriya)
    db.session.commit()
    return jsonify({'ok': True})

@main.route('/api/xizmatlar/<int:id>', methods=['DELETE'])
def delete_xizmat(id):
    x = Xizmat.query.get_or_404(id)
    x.faol = False
    db.session.commit()
    return jsonify({'ok': True})

# --- BEMORLAR ---
@main.route('/api/bemorlar', methods=['GET'])
def get_bemorlar():
    bemorlar = Bemor.query.order_by(Bemor.yaratilgan.desc()).limit(100).all()
    return jsonify([{
        'id': b.id, 'ism': b.ism, 'telefon': b.telefon
    } for b in bemorlar])

@main.route('/api/bemorlar', methods=['POST'])
def add_bemor():
    d = request.json
    b = Bemor(ism=d['ism'], telefon=d.get('telefon',''))
    db.session.add(b)
    db.session.commit()
    return jsonify({'id': b.id, 'ism': b.ism})

# --- QABULLAR ---
@main.route('/api/qabullar', methods=['POST'])
def add_qabul():
    d = request.json
    q = Qabul(
        bemor_id=d['bemor_id'], shifokor_id=d['shifokor_id'],
        xizmat_id=d['xizmat_id'], summa=d['summa'],
        tolov_turi=d['tolov_turi'], izoh=d.get('izoh','')
    )
    db.session.add(q)
    db.session.commit()
    return jsonify({'id': q.id})

@main.route('/api/qabullar/bugun', methods=['GET'])
def bugungi_qabullar():
    bugun = date.today()
    qabullar = Qabul.query.filter(
        func.date(Qabul.sana) == bugun
    ).order_by(Qabul.sana.desc()).all()
    return jsonify([{
        'id': q.id, 'bemor': q.bemor.ism, 'shifokor': q.shifokor.ism,
        'xizmat': q.xizmat.nomi, 'summa': q.summa,
        'tolov_turi': q.tolov_turi, 'sana': q.sana.strftime('%H:%M')
    } for q in qabullar])

# --- XARAJATLAR ---
@main.route('/api/xarajatlar', methods=['GET'])
def get_xarajatlar():
    xarajatlar = Xarajat.query.order_by(Xarajat.sana.desc()).limit(100).all()
    return jsonify([{
        'id': x.id, 'nomi': x.nomi, 'summa': x.summa,
        'kategoriya': x.kategoriya, 'sana': x.sana.strftime('%Y-%m-%d')
    } for x in xarajatlar])

@main.route('/api/xarajatlar', methods=['POST'])
def add_xarajat():
    d = request.json
    x = Xarajat(nomi=d['nomi'], summa=d['summa'],
                kategoriya=d.get('kategoriya',''), izoh=d.get('izoh',''))
    db.session.add(x)
    db.session.commit()
    return jsonify({'id': x.id})

@main.route('/api/xarajatlar/<int:id>', methods=['DELETE'])
def delete_xarajat(id):
    x = Xarajat.query.get_or_404(id)
    db.session.delete(x)
    db.session.commit()
    return jsonify({'ok': True})

# --- STATISTIKA ---
@main.route('/api/statistika/oylik', methods=['GET'])
def oylik_statistika():
    oy = request.args.get('oy', datetime.now().month, type=int)
    yil = request.args.get('yil', datetime.now().year, type=int)
    
    tushum = db.session.query(func.sum(Qabul.summa)).filter(
        func.extract('month', Qabul.sana) == oy,
        func.extract('year', Qabul.sana) == yil
    ).scalar() or 0
    
    xarajat = db.session.query(func.sum(Xarajat.summa)).filter(
        func.extract('month', Xarajat.sana) == oy,
        func.extract('year', Xarajat.sana) == yil
    ).scalar() or 0
    
    bemorlar_soni = db.session.query(func.count(Qabul.id)).filter(
        func.extract('month', Qabul.sana) == oy,
        func.extract('year', Qabul.sana) == yil
    ).scalar() or 0
    
    foyda = tushum - xarajat
    
    return jsonify({
        'tushum': tushum, 'xarajat': xarajat,
        'foyda': foyda, 'bemorlar': bemorlar_soni
    })

@main.route('/api/statistika/shifokorlar', methods=['GET'])
def shifokor_statistika():
    oy = request.args.get('oy', datetime.now().month, type=int)
    yil = request.args.get('yil', datetime.now().year, type=int)
    
    natija = db.session.query(
        Shifokor.ism,
        func.count(Qabul.id).label('qabullar'),
        func.sum(Qabul.summa).label('tushum')
    ).join(Qabul).filter(
        func.extract('month', Qabul.sana) == oy,
        func.extract('year', Qabul.sana) == yil
    ).group_by(Shifokor.id).all()
    
    return jsonify([{
        'ism': r.ism, 'qabullar': r.qabullar, 'tushum': r.tushum or 0
    } for r in natija])

@main.route('/api/statistika/kunlik', methods=['GET'])
def kunlik_statistika():
    from datetime import timedelta
    kun = request.args.get('kun', date.today().isoformat())
    kun_date = date.fromisoformat(kun)
    
    tushum = db.session.query(func.sum(Qabul.summa)).filter(
        func.date(Qabul.sana) == kun_date
    ).scalar() or 0
    
    bemorlar = db.session.query(func.count(Qabul.id)).filter(
        func.date(Qabul.sana) == kun_date
    ).scalar() or 0
    
    xarajat = db.session.query(func.sum(Xarajat.summa)).filter(
        func.date(Xarajat.sana) == kun_date
    ).scalar() or 0
    
    qabullar = Qabul.query.filter(
        func.date(Qabul.sana) == kun_date
    ).order_by(Qabul.sana.desc()).all()
    
    return jsonify({
        'sana': kun,
        'tushum': tushum,
        'xarajat': xarajat,
        'foyda': tushum - xarajat,
        'bemorlar': bemorlar,
        'qabullar': [{
            'vaqt': q.sana.strftime('%H:%M'),
            'bemor': q.bemor.ism,
            'shifokor': q.shifokor.ism,
            'xizmat': q.xizmat.nomi,
            'summa': q.summa,
            'tolov_turi': q.tolov_turi
        } for q in qabullar]
    })

@main.route('/api/statistika/haftalik', methods=['GET'])
def haftalik_statistika():
    from datetime import timedelta
    bugun = date.today()
    natija = []
    for i in range(6, -1, -1):
        kun = bugun - timedelta(days=i)
        tushum = db.session.query(func.sum(Qabul.summa)).filter(
            func.date(Qabul.sana) == kun
        ).scalar() or 0
        bemorlar = db.session.query(func.count(Qabul.id)).filter(
            func.date(Qabul.sana) == kun
        ).scalar() or 0
        natija.append({
            'sana': kun.isoformat(),
            'kun': kun.strftime('%a'),
            'tushum': tushum,
            'bemorlar': bemorlar
        })
    return jsonify(natija)

@main.route('/api/smena/bugun', methods=['GET'])
def smena_bugun():
    bugun = date.today()
    smena = Smena.query.filter_by(sana=bugun).first()
    
    naqd = db.session.query(func.sum(Qabul.summa)).filter(
        func.date(Qabul.sana) == bugun,
        Qabul.tolov_turi == 'naqd'
    ).scalar() or 0
    terminal = db.session.query(func.sum(Qabul.summa)).filter(
        func.date(Qabul.sana) == bugun,
        Qabul.tolov_turi == 'terminal'
    ).scalar() or 0
    aralash = db.session.query(func.sum(Qabul.summa)).filter(
        func.date(Qabul.sana) == bugun,
        Qabul.tolov_turi == 'aralash'
    ).scalar() or 0
    bemorlar = db.session.query(func.count(Qabul.id)).filter(
        func.date(Qabul.sana) == bugun
    ).scalar() or 0
    
    return jsonify({
        'sana': bugun.isoformat(),
        'naqd': naqd,
        'terminal': terminal,
        'aralash': aralash,
        'jami': naqd + terminal + aralash,
        'bemorlar': bemorlar,
        'yopilgan': smena.yopilgan if smena else False,
        'izoh': smena.izoh if smena else ''
    })

@main.route('/api/smena/yopish', methods=['POST'])
def smena_yopish():
    bugun = date.today()
    d = request.json
    smena = Smena.query.filter_by(sana=bugun).first()
    if not smena:
        smena = Smena(sana=bugun)
        db.session.add(smena)
    smena.naqd_tushum = d.get('naqd', 0)
    smena.terminal_tushum = d.get('terminal', 0)
    smena.aralash_tushum = d.get('aralash', 0)
    smena.jami_tushum = d.get('jami', 0)
    smena.bemorlar_soni = d.get('bemorlar', 0)
    smena.izoh = d.get('izoh', '')
    smena.yopilgan = True
    smena.yopilgan_vaqt = datetime.utcnow()
    db.session.commit()
    return jsonify({'ok': True, 'sana': bugun.isoformat()})

@main.route('/api/smena/tarix', methods=['GET'])
def smena_tarix():
    smenalar = Smena.query.filter_by(yopilgan=True).order_by(Smena.sana.desc()).limit(30).all()
    return jsonify([{
        'sana': s.sana.isoformat(),
        'naqd': s.naqd_tushum,
        'terminal': s.terminal_tushum,
        'aralash': s.aralash_tushum,
        'jami': s.jami_tushum,
        'bemorlar': s.bemorlar_soni,
        'izoh': s.izoh
    } for s in smenalar])

@main.route('/api/tashqi-xarajat', methods=['GET'])
def get_tashqi_xarajatlar():
    from app.models import TashqiShifokorXarajat
    xarajatlar = TashqiShifokorXarajat.query.order_by(TashqiShifokorXarajat.sana.desc()).limit(50).all()
    return jsonify([{
        'id': x.id,
        'shifokor': x.shifokor.ism,
        'sana': x.sana.isoformat(),
        'operatsiyalar_soni': x.operatsiyalar_soni,
        'operatsiya_tushum': x.operatsiya_tushum,
        'yol_haqi': x.yol_haqi,
        'yashash': x.yashash,
        'ovqatlanish': x.ovqatlanish,
        'xizmat_haqi': x.xizmat_haqi,
        'bonus_foiz': x.bonus_foiz,
        'bonus_summa': x.bonus_summa,
        'jami_xarajat': x.jami_xarajat,
        'izoh': x.izoh or ''
    } for x in xarajatlar])

@main.route('/api/tashqi-xarajat', methods=['POST'])
def add_tashqi_xarajat():
    from app.models import TashqiShifokorXarajat
    d = request.json
    bonus_summa = d.get('bonus_summa', 0)
    if d.get('bonus_foiz', 0) > 0:
        bonus_summa += d.get('operatsiya_tushum', 0) * d.get('bonus_foiz', 0) / 100
    jami = (d.get('yol_haqi', 0) + d.get('yashash', 0) +
            d.get('ovqatlanish', 0) + d.get('xizmat_haqi', 0) + bonus_summa)
    x = TashqiShifokorXarajat(
        shifokor_id=d['shifokor_id'],
        sana=date.fromisoformat(d['sana']),
        operatsiyalar_soni=d.get('operatsiyalar_soni', 0),
        operatsiya_tushum=d.get('operatsiya_tushum', 0),
        yol_haqi=d.get('yol_haqi', 0),
        yashash=d.get('yashash', 0),
        ovqatlanish=d.get('ovqatlanish', 0),
        xizmat_haqi=d.get('xizmat_haqi', 0),
        bonus_foiz=d.get('bonus_foiz', 0),
        bonus_summa=bonus_summa,
        jami_xarajat=jami,
        izoh=d.get('izoh', '')
    )
    db.session.add(x)
    db.session.commit()
    return jsonify({'id': x.id, 'jami': jami})

@main.route('/api/tashqi-xarajat/<int:id>', methods=['DELETE'])
def delete_tashqi_xarajat(id):
    from app.models import TashqiShifokorXarajat
    x = TashqiShifokorXarajat.query.get_or_404(id)
    db.session.delete(x)
    db.session.commit()
    return jsonify({'ok': True})

@main.route('/api/bemorlar/tarix', methods=['GET'])
def bemorlar_tarix():
    search = request.args.get('q', '')
    query = Bemor.query
    if search:
        query = query.filter(Bemor.ism.ilike(f'%{search}%'))
    bemorlar = query.order_by(Bemor.yaratilgan.desc()).limit(100).all()
    natija = []
    for b in bemorlar:
        qabullar = Qabul.query.filter_by(bemor_id=b.id).order_by(Qabul.sana.desc()).all()
        if qabullar:
            natija.append({
                'id': b.id,
                'ism': b.ism,
                'telefon': b.telefon or '—',
                'qabullar_soni': len(qabullar),
                'oxirgi_tashrif': qabullar[0].sana.strftime('%Y-%m-%d'),
                'jami_tolov': sum(q.summa for q in qabullar),
                'tarix': [{
                    'sana': q.sana.strftime('%Y-%m-%d %H:%M'),
                    'shifokor': q.shifokor.ism,
                    'xizmat': q.xizmat.nomi,
                    'summa': q.summa,
                    'tolov_turi': q.tolov_turi
                } for q in qabullar]
            })
    natija.sort(key=lambda x: x['qabullar_soni'], reverse=True)
    return jsonify(natija)
