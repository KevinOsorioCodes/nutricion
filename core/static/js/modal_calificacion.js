const open = document.getElementById('calif-button');
const modal_container = document.getElementById('modal_container_calificacion');
const close = document.getElementById('calif-button-modal');

open.addEventListener('click', () => {
    modal_container.classList.add('show');
});

close.addEventListener('click', () => {
    modal_container.classList.remove('show');
});