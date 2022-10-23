
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

function boton1(){
    alert ("Su apuesta fue aceptada. Se incrementó en 500 pesos")
}

function boton2(){
    alert ("Su apuesta fue aceptada. Se incrementó en 1000 pesos")
}

function boton3(){
    alert ("Su apuesta fue aceptada. Se incrementó en 2500 pesos")
}