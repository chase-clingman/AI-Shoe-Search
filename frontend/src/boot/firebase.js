// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAxjvbO21irfP42VecertiWhVnpvjsjNuA",
  authDomain: "automotiveai.firebaseapp.com",
  projectId: "automotiveai",
  storageBucket: "automotiveai.appspot.com",
  messagingSenderId: "203526068783",
  appId: "1:203526068783:web:088a9211f8b152460884da"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
const db = getFirestore(app);
export default db;
console.log("Firebase initialized");
