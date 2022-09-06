const btnActivar =  document.querySelectorAll(".btnActivar");
console.log("Se cargo correctamente ");
(function() {
    btnActivar.forEach(btn=>{
        console.log(btn);
       btn.addEventListener('click',function(e) {
            let confrmacion = confirm('Activar el usuario?')
            if(!confrmacion){
                e.preventDefault()
            }
       })

    })
})()