const d = document;

d.addEventListener("DOMContentLoaded", (e) => {
    countdown("countdown", "Nov 17, 2022 18:00:00", "¡Comienza la gran subasta!");
});


function countdown(id, limitDate, finalMessage) {
 const $countdown = d.getElementById(id),
  countdownDate = new Date(limitDate).getTime();


  let countdownTempo = setInterval(() => {
   let now = new Date().getTime(),
    limitTime = countdownDate - now,
    days = Math.floor(limitTime / (1000 * 60 * 60 * 24 )),
    hours = (
      "0" + Math.floor(limitTime % (1000 * 60 *60 * 24) / (1000 * 60 * 60))
    ).slice(-2),
    minutes = (
      "0" + Math.floor(limitTime % (1000 * 60 *60) / (1000 * 60))
    ).slice(-2),
    seconds = (
      "0" + Math.floor(limitTime % (1000 * 60) / (1000))
    ).slice(-2);
    
   $countdown.innerHTML = `<h3>Para la subasta faltan: ${days} días - ${hours} horas - ${minutes} minutos - ${seconds} seguntos</h3>`;

  if(limitTime < 0){
    clearInterval(countdownTempo);
    $countdown.innerHTML = `<h3>${finalMessage}</h3>`;
  }
 },1000);
}