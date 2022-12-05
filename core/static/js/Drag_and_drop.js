const dropArea = document.querySelector('.drag-area');
const dragText = dropArea.querySelector('h2');
const button = dropArea.querySelector('#drag-area-button');
const input = document.querySelector('#input-file');
let files;

button.addEventListener('click', (event) => {
    input.click();
});

input.addEventListener('change', (event) => {
    files = event.target.files;
    dropArea.classList.add('active');
    showFiles(files);
    dropArea.classList.remove('active');
});

// input.addEventListener('change', (event) => {
//     files = this.files;
//     dropArea.classList.add('active');
//     showFiles(files);
//     dropArea.classList.remove('active');
// });

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropArea.classList.add('active');
    dragText.textContent = 'Suelta para subir el archivo';
});


dropArea.addEventListener('dragleave', (event) => {
    event.preventDefault();
    dropArea.classList.remove('active');
    dragText.textContent = 'Arrastra y suelta tu archivo aquí';
});

dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    files = event.dataTransfer.files;
    showFiles(files);
    dropArea.classList.remove('active');
});

function showFiles(files) {
    console.log(files)
    if (files.length === 1) {
        processFile(files);
    } else {
        alert('Solo se puede subir un archivo');
    }
}

function processFile(files) {
    const docType = files[0].type;
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];

    if (validTypes.includes(docType)) {
        if (files[0].size <= 1024 * 1024*5) {
            dragText.textContent =  files[0].name;
            input.files = files;
        }
        else {
            alert('El archivo es muy grande');
            input.value = '';
        }
    } 
    else {
        alert(`El archivo no es una imagen`);
        input.value = '';
    }
}