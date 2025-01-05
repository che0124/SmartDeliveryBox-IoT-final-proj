import os
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyotp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# 初始化 Firebase
cred = credentials.Certificate('food-delivery-2bb20-firebase-adminsdk-2j5dr-cc1397bedd.json')
firebase_admin.initialize_app(cred)

# Firestore 資料庫初始化
db = firestore.client()

@app.route('/')
def index():
    """首頁渲染"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """註冊頁面渲染"""
    if request.method == 'POST':
        data = request.get_json()
        uid = data.get('uid')
        email = data.get('email')
        role = data.get('role')
        try:
            user = auth.get_user(uid)
            auth.set_custom_user_claims(user.uid, {'role': role})
            session['user_id'] = user.uid
            session['email'] = email
            session['role'] = role
            if session['role'] == 'delivery':
                return jsonify({'success': True, 'redirect_url': url_for('delivery_dashboard')})
            else:
                return jsonify({'success': True, 'redirect_url': url_for('customer_dashboard')})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登錄頁面渲染"""
    if request.method == 'POST':
        data = request.get_json()
        uid = data.get('uid')
        email = data.get('email')
        try:
            user = auth.get_user(uid)
            session['user_id'] = user.uid
            session['email'] = email
            custom_claims = user.custom_claims or {}
            session['role'] = custom_claims.get('role')
            if session['role'] == 'delivery':
                return jsonify({'success': True, 'redirect_url': url_for('delivery_dashboard')})
            else:
                return jsonify({'success': True, 'redirect_url': url_for('customer_dashboard')})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('成功登出！', 'success')
    return jsonify({'success': True, 'redirect_url': url_for('login')})

@app.route('/delivery_dashboard')
def delivery_dashboard():
    if 'user_id' in session and session['role'] == 'delivery':
        return render_template('delivery_dashboard.html')
    return redirect(url_for('login'))

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'user_id' in session and session['role'] == 'customer':
        return render_template('customer_dashboard.html')
    return redirect(url_for('login'))

@app.route('/group')
def group():
    if 'user_id' in session:
        return render_template('group.html')
    return redirect(url_for('login'))

@app.route('/get_user_role', methods=['POST'])
def get_user_role():
    """獲取當前使用者的角色"""
    data = request.get_json()
    uid = data.get('uid')
    try:
        user = auth.get_user(uid)
        role = user.custom_claims.get('role') if user.custom_claims else None
        return jsonify({'role': role})
    except Exception as e:
        return jsonify({'role': None, 'message': str(e)})

@app.route('/create_group', methods=['POST'])
def create_group():
    """創建群組"""
    if 'user_id' not in session or session['role'] != 'customer':
        return redirect(url_for('login'))
    
    data = request.get_json()
    group_name = data.get('group_name')
    member_emails = data.get('members')  # 這應該是一個包含成員電子郵件地址的列表
    
    try:
        members = []
        member_uids = []
        for email in member_emails:
            user = auth.get_user_by_email(email)
            members.append({'uid': user.uid, 'email': email})
            member_uids.append(user.uid)
        
        # 將擁有者添加到成員列表中
        owner_id = session['user_id']
        owner_email = session['email']
        if owner_id not in member_uids:
            members.append({'uid': owner_id, 'email': owner_email})
            member_uids.append(owner_id)
        
        group_ref = db.collection('groups').document(group_name)
        group_ref.set({
            'owner': {'uid': owner_id, 'email': owner_email},
            'members': members,
            'member_uids': member_uids
        })
        return jsonify({'success': True, 'message': '群組創建成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_groups', methods=['GET'])
def get_groups():
    """獲取當前用戶的群組"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '未授權的操作'})
    
    user_id = session['user_id']
    
    try:
        groups = db.collection('groups').where('member_uids', 'array_contains', user_id).stream()
        group_list = []
        for group in groups:
            group_data = group.to_dict()
            group_data['group_name'] = group.id
            group_list.append(group_data)
        
        return jsonify({'success': True, 'groups': group_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_group_details', methods=['POST'])
def get_group_details():
    """獲取群組詳細信息"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '未授權的操作'})
    
    data = request.get_json()
    group_name = data.get('group_name')
    
    try:
        group_ref = db.collection('groups').document(group_name)
        group = group_ref.get()
        if group.exists:
            group_data = group.to_dict()
            return jsonify({'success': True, 'group': group_data})
        else:
            return jsonify({'success': False, 'message': '群組不存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/control_lock', methods=['POST'])
def control_lock():
    """控制箱子的鎖"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '未授權的操作'})
    
    user_id = session['user_id']
    data = request.get_json()
    group_name = data.get('group_name')
    action = data.get('action')
    
    try:
        group_ref = db.collection('groups').document(group_name)
        group = group_ref.get()
        if group.exists:
            group_data = group.to_dict()
            if user_id not in group_data['member_uids']:
                return jsonify({'success': False, 'message': '未授權的操作'})
        else:
            return jsonify({'success': False, 'message': '群組不存在'})
        
        if action == 'lock':
            requests.post('http://172.20.10.14:5001/lock')
            return
        elif action == 'unlock':
            requests.post('http://172.20.10.14:5001/unlock')
            return
        else:
            return jsonify({'success': False, 'message': '無效的操作'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

delivery_person = {
    "otp": None
}

# 生成 OTP
def generate_otp():
    """生成 OTP 並返回"""
    otp = pyotp.TOTP('base32secret3232')  # 使用密鑰生成 OTP
    return otp.now()

# 發送 OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    """生成並發送 OTP"""
    delivery_person["otp"] = generate_otp()
    return jsonify({"otp": delivery_person["otp"], "message": "OTP 已發送"})

# 驗證 OTP
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    """驗證 OTP"""
    otp_received = request.json.get('otp')  # 從前端接收 OTP
    if otp_received == delivery_person["otp"]:
        # 向樹莓派發送解鎖請求
        try:
            requests.post(
                "http://172.20.10.14:5001/unlock",
            )
        except requests.exceptions.RequestException as e:
            # 捕獲錯誤
            return jsonify({"message": f"解鎖請求失敗：{str(e)}"})
    else:
        return jsonify({"message": "OTP 驗證失敗，請重新輸入"})
    
@app.route('/lock', methods=['POST'])
def lock():
    """鎖定箱子"""
    requests.post(
        "http://172.20.10.14:5001/lock",
    )

if __name__ == '__main__':
    app.run(debug=True)
