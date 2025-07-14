document.getElementById("autofill").addEventListener("click", function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;

                fetch(`/get_weather?lat=${lat}&lon=${lon}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.error("Error:", data.error);
                            return;
                        }
                        document.getElementById("pressure").value = data.pressure;
                        document.getElementById("dewpoint").value = data.dewpoint;
                        document.getElementById("humidity").value = data.humidity;
                        document.getElementById("cloud").value = data.cloud;
                        document.getElementById("sunshine").value = data.sunshine;
                        document.getElementById("winddirection").value = data.winddirection;
                        document.getElementById("windspeed").value = data.windspeed;
                    })
                    .catch(error => console.error("Fetch error:", error));
            },
            function(error) {
                console.error("Geolocation error:", error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("theme-toggle");
    const body = document.body;
    const themeIcon = document.getElementById("theme-icon");

    // Check if user already selected a theme before
    if (localStorage.getItem("darkMode") === "enabled") {
        body.classList.add("dark-mode");
        toggleSwitch.checked = true;
        themeIcon.textContent = "🌙"; // Moon icon
    }

    // Toggle Dark Mode
    toggleSwitch.addEventListener("change", function () {
        if (this.checked) {
            body.classList.add("dark-mode");
            themeIcon.textContent = "🌙"; // Switch to Moon
            localStorage.setItem("darkMode", "enabled");
        } else {
            body.classList.remove("dark-mode");
            themeIcon.textContent = "☀️"; // Switch to Sun
            localStorage.setItem("darkMode", "disabled");
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const toggleSwitch = document.getElementById("mode-toggle");
    const body = document.body;

    // Check saved mode and apply
    const savedMode = localStorage.getItem("theme");
    if (savedMode === "dark") {
        body.classList.add("dark-mode");
        toggleSwitch.checked = true;
    }

    // Toggle mode on switch
    toggleSwitch.addEventListener("change", function () {
        if (toggleSwitch.checked) {
            body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark");
        } else {
            body.classList.remove("dark-mode");
            localStorage.setItem("theme", "light");
        }
    });
});



