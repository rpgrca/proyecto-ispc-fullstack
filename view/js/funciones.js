
function mostrar_respuesta_remota_para_formulario(nombre) {
    document.forms[nombre].addEventListener('submit', (event) => {
        event.preventDefault();
        fetch(event.target.action, {
            method: 'POST',
            body: new URLSearchParams(new FormData(event.target))
        }).then((response) => {
            return response.json()
        }).then((body) => {
            alert(body["mensaje"])
        })
    })
}

function sube_puja(){
    alert ("Su apuesta fue aceptada. Se incrementó en 500 pesos")
}

function sube_puja_un_poco(){
    alert ("Su apuesta fue aceptada. Se incrementó en 1000 pesos")
}

function sube_puja_un_poco_mas(){
    alert ("Su apuesta fue aceptada. Se incrementó en 2500 pesos")
}
