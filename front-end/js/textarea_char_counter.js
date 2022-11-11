const mensaje = document.getElementById('mensaje');
const contador = document.getElementById('contador');

mensaje.addEventListener('input', function(e) {
    const target = e.target;
    const longitudMax = target.getAttribute('maxlength');
    const longitudAct = target.value.length;
    contador.innerHTML = `${longitudAct}/${longitudMax}`;
});

// fuente: https://www.bufa.es/javascript-contar-numero-de-caracteres-de-un-textarea/