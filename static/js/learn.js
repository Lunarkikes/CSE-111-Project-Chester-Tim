document.getElementById('demo').innerHTML = "This was created with JS";

function register_student(){
    var username = document.getElementById("nombre").value;
    var password = document.getElementById("precent").value;
    var xhttp = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/register";
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body = { "username": username, "password": password };
    xhttp.send(JSON.stringify(body));
    xhttp.onload = function () {
        let data = this.responseText;
        data = JSON.parse(data);
        document.getElementById("2").innerHTML = this.responseText;
    };
}