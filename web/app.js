import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-auth.js";
import { getDatabase, ref, onValue, update } from "https://www.gstatic.com/firebasejs/9.17.2/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCGpbIhsDogNMAZkRlWdvhWjFfN39nxBfQ",
  authDomain: "smart-lab-2025.firebaseapp.com",
  databaseURL: "https://smart-lab-2025-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "smart-lab-2025",
  storageBucket: "smart-lab-2025.firebasestorage.app",
  messagingSenderId: "503064583220",
  appId: "1:503064583220:web:b67cd9dbc1b340ae96fe61",
  measurementId: "G-C2W897SLE3",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getDatabase(app);

onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("User is authenticated:", user.displayName);
    document.getElementById("user-email").textContent = user.email;
  } else {
    console.log("User is not authenticated. Redirecting to login...");
    window.location.href = "./login.html";
  }
});

// Reference to database
const dbRef = ref(db, "lab1");

// DOM elements
const airQualityElem = document.getElementById("air-quality");
const brightnessElem = document.getElementById("brightness");
const temperatureElem = document.getElementById("temperature");
const humidityElem = document.getElementById("humidity");
const currentElem = document.getElementById("current");
const voltageElem = document.getElementById("voltage");

// Appliance controls
const acSlider = document.getElementById("ac-slider");
const acValue = document.getElementById("ac-value");
const lightSlider = document.getElementById("light-slider");
const lightValue = document.getElementById("light-value");
const fanToggle = document.getElementById("fan-toggle");
const fanState = document.getElementById("fan-state");

// Update sensor values
onValue(dbRef, (snapshot) => {
  const data = snapshot.val();

  // Sensors
  airQualityElem.textContent = `${data.sensors.air_quality} %`;
  brightnessElem.textContent = data.sensors.brightness;
  temperatureElem.textContent = `${data.sensors.temperature} °C`;
  humidityElem.textContent = `${data.sensors.humidity} %`;
  currentElem.textContent = `${data.sensors.current} A`;
  voltageElem.textContent = `${data.sensors.voltage} V`;

  // Appliances
  acSlider.value = data.appliances.ac || 18;
  acValue.textContent = acSlider.value;
  lightSlider.value = data.appliances.light || 0;
  lightValue.textContent = lightSlider.value;
  fanToggle.checked = data.appliances.fan || false;
  fanState.textContent = fanToggle.checked ? "ON" : "OFF";
});

// Add event listeners for user interactions to update Firebase
acSlider.addEventListener("input", () => {
  const ac = parseFloat(acSlider.value);
  acValue.textContent = ac;

  // Update Firebase
  update(ref(db, "lab1/appliances"), { ac });
});

lightSlider.addEventListener("input", () => {
  const light = parseFloat(lightSlider.value);
  lightValue.textContent = light;

  // Update Firebase
  update(ref(db, "lab1/appliances"), { light });
});

fanToggle.addEventListener("change", () => {
  const fan = fanToggle.checked ? 1 : 0;
  fanState.textContent = fanToggle.checked ? "ON" : "OFF";

  // Update Firebase
  update(ref(db, "lab1/appliances"), { fan });
});

// Plotly charts
const voltageChart = document.getElementById("voltage-chart");
const currentChart = document.getElementById("current-chart");
const powerChart = document.getElementById("power-chart");

onValue(dbRef, (snapshot) => {
  const data = snapshot.val();
  const voltageHistory = data.voltage_history;
  const currentHistory = data.current_history;

  // Calculate power history
  const powerHistory = voltageHistory.map((v, i) => v * currentHistory[i]);

  // Common layout for all charts to fully utilize their containers
  const layout = {
    margin: { t: 10, r: 10, b: 20, l: 37 }, // Minimal margins for a larger plot area
    autosize: true, // Automatically fit the container
  };

  // Plot each chart
  Plotly.newPlot(voltageChart, [{ y: voltageHistory, type: "scatter" }], layout, { responsive: true, displayModeBar: false});
  Plotly.newPlot(currentChart, [{ y: currentHistory, type: "scatter" }], layout, { responsive: true, displayModeBar: false});
  Plotly.newPlot(powerChart, [{ y: powerHistory, type: "scatter" }], layout, { responsive: true, displayModeBar: false});

  Plotly.relayout(voltageChart, {
    width: voltageChart.offsetWidth,
     height: voltageChart.offsetHeight,
   });
   Plotly.relayout(currentChart, {
     width: currentChart.offsetWidth,
     height: currentChart.offsetHeight,
   });
   Plotly.relayout(powerChart, {
     width: powerChart.offsetWidth,
     height: powerChart.offsetHeight,
   });
});

// Ensure charts resize when the window is resized
window.addEventListener("resize", () => {
  Plotly.relayout(voltageChart, {
    width: voltageChart.offsetWidth,
     height: voltageChart.offsetHeight,
   });
   Plotly.relayout(currentChart, {
     width: currentChart.offsetWidth,
     height: currentChart.offsetHeight,
   });
   Plotly.relayout(powerChart, {
     width: powerChart.offsetWidth,
     height: powerChart.offsetHeight,
   });
});

// Function to toggle the visibility of the dropdown menu
function toggleDropdown() {
  const dropdown = document.getElementById('dropdown-menu');
  if (dropdown.style.display === 'block') {
    dropdown.style.display = 'none';
  } else {
    dropdown.style.display = 'block';
  }
}

// Function to sign out (placeholder for actual functionality)
function signOut() {
  auth.signOut()
    .then(() => {
      // Redirect to the login page after sign-out
      window.location.href = "login.html"; // Change this to your login page URL
    })
    .catch((error) => {
      console.error("Error signing out:", error.message);
    });
}

document.querySelector('.user-icon').addEventListener('click', toggleDropdown);
document.getElementById('sign-out').addEventListener('click', signOut);
