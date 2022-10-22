
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