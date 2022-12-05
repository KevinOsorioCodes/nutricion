const open = document.getElementById('open_ep_modal');
const modal_container = document.getElementById('modal_container_profile');
const close = document.getElementById('close_ep_modal');

open.addEventListener('click', () => {
    modal_container.classList.add('show');
});

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
});