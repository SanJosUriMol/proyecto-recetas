const API = "http://localhost:8000";

// LOGIN

async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if(!email || !password){
        document.getElementById("mensaje").innerText =
            "Debe completar todos los campos";
        return;
    }

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type":
            "application/x-www-form-urlencoded"
        },
        body: formData
    });

    const data = await response.json();

    if(data.access_token){

        localStorage.setItem(
            "token",
            data.access_token
        );

        window.location.href =
            "dashboard.html";

    }else{

        document.getElementById("mensaje")
            .innerText =
            "Credenciales inválidas";
    }
}

// REGISTRO

async function registro(){

    const nombre =
        document.getElementById("nombre").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    if(!nombre || !email || !password){
        document.getElementById("mensaje").innerText =
            "Debe completar todos los campos";
        return;
    }

    const response = await fetch(
        `${API}/auth/registro`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                nombre,
                email,
                password
            })
        }
    );

    if(response.ok){

        alert("Usuario registrado");

        window.location.href =
            "login.html";
    }
}

// TOKEN

function getToken(){
    return localStorage.getItem("token");
}

// INGREDIENTES

async function cargarIngredientes(){

    const response = await fetch(
        `${API}/ingredientes`,
        {
            headers:{
                Authorization:
                `Bearer ${getToken()}`
            }
        }
    );

    const data = await response.json();

    let html = "";

    data.forEach(i => {

        html += `
        <div class="card">
            <b>${i.nombre}</b>
            (${i.cantidad || ""} ${i.unidad || ""})

            <button
            onclick="eliminarIngrediente(${i.id})">
            Eliminar
            </button>
        </div>`;
    });

    document.getElementById(
        "ingredientes"
    ).innerHTML = html;
}

async function agregarIngrediente(){

    const nombre =
        document.getElementById(
            "nombreIngrediente"
        ).value;

    const cantidad =
        document.getElementById(
            "cantidadIngrediente"
        ).value;

    const unidad =
        document.getElementById(
            "unidadIngrediente"
        ).value;

    await fetch(`${API}/ingredientes`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            Authorization:
            `Bearer ${getToken()}`
        },
        body:JSON.stringify({
            nombre,
            cantidad,
            unidad
        })
    });

    cargarIngredientes();
}

async function eliminarIngrediente(id){

    if(!confirm("¿Desea eliminar este ingrediente?")){
        return;
    }


    await fetch(
        `${API}/ingredientes/${id}`,
        {
            method:"DELETE",
            headers:{
                Authorization:
                `Bearer ${getToken()}`
            }
        }
    );

    cargarIngredientes();
}

// RECETAS

async function generarReceta(){

    await fetch(
        `${API}/recetas/generar`,
        {
            method:"POST",
            headers:{
                Authorization:
                `Bearer ${getToken()}`
            }
        }
    );

    cargarRecetas();
}

async function cargarRecetas(){

    const response =
        await fetch(
            `${API}/recetas`,
            {
                headers:{
                    Authorization:
                    `Bearer ${getToken()}`
                }
            }
        );

    const recetas =
        await response.json();

    let html = "";

    recetas.forEach(r => {

        html += `
        <div class="card">

            <h3>${r.nombre_plato}</h3>

            <p>
                Tiempo:
                ${r.tiempo_estimado || "N/A"}
            </p>

            <p>
                Dificultad:
                ${r.nivel_dificultad || "N/A"}
            </p>

            <button
             onclick="eliminarReceta(${r.id})">
             Eliminar
            </button>

        </div>`;
    });

    document.getElementById(
        "recetas"
    ).innerHTML = html;
}

async function eliminarReceta(id){

    if(!confirm("¿Desea eliminar esta receta?")){
        return;
    }


    await fetch(
        `${API}/recetas/${id}`,
        {
            method:"DELETE",
            headers:{
                Authorization:
                `Bearer ${getToken()}`
            }
        }
    );

    cargarRecetas();
}

function inicializarDashboard(){

    if(!getToken()){
        window.location.href = "login.html";
        return;
    }

    cargarIngredientes();
    cargarRecetas();
}