import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDOldQSuNMAlQMTT7Jy9dWdfHZXg2BU3S4",
    authDomain: "food-delivery-2bb20.firebaseapp.com",
    projectId: "food-delivery-2bb20",
    storageBucket: "food-delivery-2bb20.firebasestorage.app",
    messagingSenderId: "146241836563",
    appId: "1:146241836563:web:965723e8ab2e91b5d1d1e6",
    measurementId: "G-EL13FFNMDQ"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

document.getElementById('login-form')?.addEventListener('submit', login);
document.getElementById('register-form')?.addEventListener('submit', register);

function login(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user;
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ uid: user.uid, email: user.email })
        })
        .then(response => response.json())
        .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    alert('登入失敗');
                }
            });
        })
        .catch((error) => {
            alert("Error: " + error.message);
        });
}

function register(event) {
    event.preventDefault();
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const role = document.getElementById("register-role").value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ uid: user.uid, email: user.email, role: role })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    alert('註冊失敗');
                }
            });
        })
        .catch((error) => {
            alert("Error: " + error.message);
        });
}

function logout() {
    signOut(auth).then(() => {
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(() => {
            window.location.href = '/login';
        });
    }).catch((error) => {
        alert("Error: " + error.message);
    });
}

window.logout = logout;

function checkCurrentUser() {
    onAuthStateChanged(auth, (user) => {
        if (user) {
            console.log('User is signed in:', user.email);
        } else {
            console.log('No user is signed in.');
        }
    });
}

checkCurrentUser();

export { login, register, logout };