var sub = document.getElementById('addtask')

var sbutton = sub.querySelector('.submit-op')
sbutton.addEventListener('click',(e) =>{
    
    e.preventDefault()
    var data = new FormData(document.getElementById("addtask"));
    console.log(data)
    fetch('/todo', { method: "post", body: data });
    location.reload()
})

