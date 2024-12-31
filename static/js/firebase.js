const firebaseConfig = {
  apiKey: "AIzaSyDOldQSuNMAlQMTT7Jy9dWdfHZXg2BU3S4",
  authDomain: "food-delivery-2bb20.firebaseapp.com",
  projectId: "food-delivery-2bb20",
  storageBucket: "food-delivery-2bb20.firebasestorage.app",
  messagingSenderId: "146241836563",
  appId: "1:146241836563:web:965723e8ab2e91b5d1d1e6",
  measurementId: "G-EL13FFNMDQ"
};

const app = firebase.initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
