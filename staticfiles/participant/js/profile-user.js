document.getElementById('form').addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  fetch('https://400ec572-498f-451e-a9b0-896fce31e52b-00-2i82ivtdlr154.worf.replit.dev/participant/profile-user/', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
  .then(data => document.getElementById('pro-img').src = data.photo);
  });
});