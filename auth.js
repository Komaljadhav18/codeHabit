let isLogin = true;

// Toggle Login / Signup
function toggleForm() {
    isLogin = !isLogin;

    document.getElementById("title").innerText =
        isLogin ? "Login" : "Sign Up";

    document.querySelector("button").innerText =
        isLogin ? "Login" : "Create Account";

    document.querySelector(".toggle").innerHTML = isLogin
        ? `Don't have an account? <span onclick="toggleForm()">Sign up</span>`
        : `Already have an account? <span onclick="toggleForm()">Login</span>`;
}

// Handle Login / Signup submit
function submitForm() {
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();

    // ℹ️ Info – empty fields
    if (username === "" || password === "") {
        alert("ℹ️ Please enter both username and password.");
        return;
    }

    // ℹ️ Info – signup password rule
    if (!isLogin && password.length < 5) {
        alert("ℹ️ Password must be at least 5 characters.");
        return;
    }

    let url = isLogin ? "/login" : "/register";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.text())
    .then(message => {

        // ✅ Success messages
        if (message.toLowerCase().includes("successful")) {
            alert("✅ " + message);

            // After successful signup → switch to login
            if (!isLogin) {
                toggleForm();
            }
        }
        // ❌ Error messages
        else {
            alert("❌ " + message);
        }
    })
    .catch(() => {
        alert("❌ Server error. Please try again later.");
    });
}
