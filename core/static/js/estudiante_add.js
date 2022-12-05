function addInput() {
    function add(valor){
        var input = document.querySelector('#'+valor+'-1').cloneNode(true);
        var label = document.querySelector('[for="'+valor+'-1').cloneNode(true);
        switch (valor) {
        case 'rut':
            var col = document.createElement('div');
            col.classList.add("col-9");
            col.id = 'col-'+valor+'-'+inputValue.value;
            
            document.querySelector('#row-'+inputValue.value).appendChild(col);

            input.name = valor+'-'+inputValue.value;
            input.id = valor+'-'+inputValue.value;
            label.htmlFor = valor+'-'+inputValue.value;
            label.id = valor+'-'+inputValue.value;

            document.querySelector('#col-'+valor+'-'+inputValue.value).appendChild(label);
            document.querySelector('#col-'+valor+'-'+inputValue.value).appendChild(input).value="";
            break;
        case 'dv':
            var col = document.createElement('div')
            col.classList.add("col-3");
            col.id = 'col-'+valor+'-'+inputValue.value

            input.name = valor+'-'+inputValue.value;
            input.id = valor+'-'+inputValue.value;
            label.htmlFor = valor+'-'+inputValue.value;
            label.id = valor+'-'+inputValue.value;
            
            document.querySelector('#row-'+inputValue.value).appendChild(col)
            document.querySelector('#col-'+valor+'-'+inputValue.value).appendChild(label);
            document.querySelector('#col-'+valor+'-'+inputValue.value).appendChild(input).value="";
            break;
        default:
            input.name = valor+'-'+inputValue.value;
            input.id = valor+'-'+inputValue.value;
            label.htmlFor = valor+'-'+inputValue.value;
            label.id = valor+'-'+inputValue.value;

            document.querySelector('#formContent').appendChild(label);
            document.querySelector('#formContent').appendChild(input).value="";
            break;
        }
    }
    var inputValue = document.querySelector('#cantidad');
    inputValue.value = parseInt(inputValue.value) + 1

    const p = document.getElementById('Cant-estudiantes');
    const pa = document.getElementById('Cant-estudiantes-mobile');
    const N = 1;
    if (inputValue.value == 1){
        p.innerText = "Añadiendo " + inputValue.value + " estudiante";
        pa.innerText = "Añadiendo " + inputValue.value + " estudiante";
    }
    else{
        p.innerText = "Añadiendo " + inputValue.value + " estudiantes";
        pa.innerText = "Añadiendo " + inputValue.value + " estudiantes";
    }
    var hr = document.createElement('hr');
    hr.classList.add('add_user_rut');
    hr.id = 'add_user_rut_'+inputValue.value;
    document.querySelector('#formContent').appendChild(hr);
    var pc = document.createElement('p');
    pc.classList.add('estudiante');
    pc.id = 'estudiante' + inputValue.value;
    pc.innerText = 'estudiante N°' + inputValue.value;
    document.querySelector('#formContent').appendChild(pc);
    add('nombre');
    add('email');
    var div = document.createElement('div');
    div.classList.add('row');
    div.id = 'row-'+inputValue.value;
    document.querySelector('#formContent').appendChild(div);
    add('rut');
    add('dv');
}

function deleteInput() {
    var inputValue = document.querySelector('#cantidad');
    
    if (inputValue.value !=1 ){
        document.querySelector('#estudiante'+inputValue.value).remove();
        document.querySelector('#add_user_rut_'+inputValue.value).remove();
        del('nombre');
        del('email');
        del('rut');
        del('dv');
        document.querySelector('#row-'+inputValue.value).remove();
        function del(valor){
            for (var i = 0; i < 1; i++) {
                document.querySelector('[for="'+valor+'-'+inputValue.value).remove();
                document.querySelector('#'+valor+'-'+inputValue.value).remove();
            }
        }
        inputValue.value = parseInt(inputValue.value) - 1
        const p = document.getElementById('Cant-estudiantes');
        const pa = document.getElementById('Cant-estudiantes-mobile');
        const N = 1;
        if (inputValue.value == 1){
            p.innerText = "Añadiendo " + inputValue.value + " estudiante";
            pa.innerText = "Añadiendo " + inputValue.value + " estudiante";
        }
        else{
            p.innerText = "Añadiendo " + inputValue.value + " estudiantes";
            pa.innerText = "Añadiendo " + inputValue.value + " estudiantes";
        }
    }
    else{
        alert("No se pueden eliminar más estudiantes");
    }
}