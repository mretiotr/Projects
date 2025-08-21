document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.querySelector("#name").value.trim();
    const email = document.querySelector("#email").value.trim();
    const password = document.querySelector("#password").value.trim();

    // ✅ Validim frontend
    if (!name || !email || !password) {
      alert("Ju lutem plotësoni të gjitha fushat!");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert("Ju lutem vendosni një email të vlefshëm!");
      return;
    }

    if (password.length < 6) {
      alert("Fjalëkalimi duhet të ketë të paktën 6 karaktere!");
      return;
    }

    try {
      const res = await fetch("http://localhost:3000/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
      });

      const data = await res.json();

      if (res.ok) {
        alert(data.message);
        window.location.href = "signin.html"; // ridrejtohesh pas suksesit
      } else {
        alert(data.message || "Gabim gjatë regjistrimit.");
      }
    } catch (err) {
      console.error("Gabim:", err);
      alert("Nuk u lidh me serverin.");
    }
  });
});
