const favoris = document.getElementById('favoris')
const evt = document.getElementById('evt')

favoris.addEventListener('click', (e) => {
  const id = favoris.getAttribute('data-event-id')
  favoris.classList.remove('bg-gray-400')
  favoris.classList.add('bg-[#FF0000]')
  favoris.innerText = 'Favoris'
  evt.innerText = id;
})