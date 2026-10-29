let actiefleerkracht = false
let actiefleerling = false

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function leerkracht_actief(){
    if (actiefleerkracht){
        document.getElementById("Knop_Leerkracht").style.backgroundColor = 'rgb(206, 205, 205)';
        document.getElementById("Knop_Leerkracht").style.color = 'black';
        actiefleerkracht = false;
    }else{
        document.getElementById("Knop_Leerling").style.backgroundColor = 'rgb(206, 205, 205)';
        document.getElementById("Knop_Leerling").style.color = 'black';
        actiefleerling = false;
        document.getElementById("Knop_Leerkracht").style.backgroundColor = 'rgb(0, 183, 255)';
        document.getElementById("Knop_Leerkracht").style.color = 'white';
        actiefleerkracht = true;
    }
}

function leerling_actief(){
    if (actiefleerling){
        document.getElementById("Knop_Leerling").style.backgroundColor = 'rgb(206, 205, 205)';
        document.getElementById("Knop_Leerling").style.color = 'black';
        actiefleerling = false;
    }else{
        document.getElementById("Knop_Leerkracht").style.backgroundColor = 'rgb(206, 205, 205)';
        document.getElementById("Knop_Leerkracht").style.color = 'black';
        actiefleerkracht = false;
        document.getElementById("Knop_Leerling").style.backgroundColor = 'rgb(0, 183, 255)';
        document.getElementById("Knop_Leerling").style.color = 'white';
        actiefleerling = true;
    }
}

async function inloggen(){
    if (actiefleerkracht){
        window.location.href = "./Project_LEER_Inloggen_Registreren/Project_LEER_Leerkracht_Inloggen.html";
    }else if (actiefleerling){
        window.location.href = "./Project_LEER_Inloggen_Registreren/Project_LEER_Leerling_Inloggen.html";
    }else{
        document.getElementById("Knop_Inloggen").style.backgroundColor = 'red';
        document.getElementById("Knop_Inloggen").style.color = 'white';
        await sleep(250);
        document.getElementById("Knop_Inloggen").style.backgroundColor = 'rgb(206, 205, 205)';
        document.getElementById("Knop_Inloggen").style.color = 'black';
    }
}

async function registreren(){
    if (actiefleerkracht){
        window.location.href = "./Project_LEER_Inloggen_Registreren/Project_LEER_Leerkracht_Registreren.html";
    }else if (actiefleerling){
        window.location.href = "./Project_LEER_Inloggen_Registreren/Project_LEER_Leerling_Registreren.html";
    }else{
        document.getElementById("Knop_Registreren").style.backgroundColor = 'red';
        document.getElementById("Knop_Registreren").style.color = 'white';
        await sleep(250);
        document.getElementById("Knop_Registreren").style.backgroundColor = 'rgb(206, 205, 205)';
        document.getElementById("Knop_Registreren").style.color = 'black';
    }
}