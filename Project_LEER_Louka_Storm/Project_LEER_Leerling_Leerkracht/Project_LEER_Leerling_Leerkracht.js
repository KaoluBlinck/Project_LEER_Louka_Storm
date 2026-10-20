let actiefleerkracht = false
let actiefleerling = false

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function leerkracht_actief(){
    if (actiefleerling){
        document.getElementById("Knop_Leerling").style.backgroundColor = 'rgb(206, 205, 205)';
        actiefleerling = false;
    }

    document.getElementById("Knop_Leerkracht").style.backgroundColor = 'blue';
    actiefleerkracht = true;
}

function leerling_actief(){
    if (actiefleerkracht){
        document.getElementById("Knop_Leerkracht").style.backgroundColor = 'rgb(206, 205, 205)';
        actiefleerkracht = false;
    }

    document.getElementById("Knop_Leerling").style.backgroundColor = 'blue';
    actiefleerling = true;
}

async function inloggen(){
    if (actiefleerkracht){
        window.location.href = "Project_LEER_Leerkracht_Inloggen.html";
    }

    if (actiefleerling){
        window.location.href = "Project_LEER_Leerling_Inloggen.html";
    }

    else{
        document.getElementById("Knop_Inloggen").style.display = 'red';
        await sleep(250);
        document.getElementById("Knop_Inloggen").style.display = 'rgb(206, 205, 205)';
    }
}