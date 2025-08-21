document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.querySelector('#email').value.trim();
    const password = document.querySelector('#password').value.trim();

    if (!email || !password) {
      alert('Ju lutem vendosni email-in dhe fjalëkalimin!');
      return;
    }

    try {
      const response = await fetch('http://localhost:3000/api/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (response.ok) {
        // ✅ Ruaj token dhe rolin
        localStorage.setItem('token', data.token);
        localStorage.setItem('role', data.user.role); // ruaj rolin

        alert('Hyrja u krye me sukses!');

        // ✅ Shko te faqja e duhur sipas rolit
        if (data.user.role === 'admin') {
          window.location.href = 'admin-messages.html';
        } else {
          window.location.href = 'index.html';
        }

      } else {
        alert(data.error || 'Gabim gjatë hyrjes');
      }
    } catch (err) {
      console.error(err);
      alert('Nuk u lidh me serverin.');
    }
  });
});
localStorage.setItem('token', data.token);
localStorage.setItem('userName', data.user.name);
localStorage.setItem('role', data.user.role);
