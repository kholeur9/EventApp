const underBlock = document.getElementById('under-block');
const changePhoto = document.getElementById('change-photo');
const blockPhoto = document.getElementById('block-photo');
const body = document.querySelector('body');

changePhoto.addEventListener('click', () => {
  blockPhoto.classList.remove('hidden');
  underBlock.classList.remove('hidden');
  body.classList.add('overflow-hidden');
});
underBlock.addEventListener('click', () => {
  blockPhoto.classList.add('hidden');
  underBlock.classList.add('hidden');
  body.classList.remove('overflow-hidden');
});