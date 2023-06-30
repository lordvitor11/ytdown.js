let input = document.querySelector("input#inputLink");

input.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) {
        appendLink();
    }
});

function verifyInput() {
    let input = document.querySelector("div.t input");
    let btn = document.querySelector("button#proceed");

    if (input.value.length == 0) {
        btn.disabled = true;
        btn.classList.add("disabled");
    } else {
        btn.disabled = false;
        btn.classList.remove("disabled");
    }
}

function changeScreen(screen) {
    switch (screen) {
        case "index": window.location.assign("index.html"); break;
        case "setup": window.location.assign("setup.html"); break;
        case "download": window.location.assign("download.html"); break;
    }
}

function getLink() {
    let input = document.querySelector("div.t input");
    eel.setPath()(function (response) {
        input.setAttribute('value', response);
        verifyInput();
    });
}

function appendLink() {
    let input = document.querySelector("div.t input");
    eel.appendLink(input.value)(function (response) {
        input.value = "";

        if (response == "duplicate") {
            showFeedback("Este link já existe na lista!");
        } else if (response == "none") {
            showFeedback("Link adicionado!");
        }
    });
}

function saveSettings() {
    eel.createJson();
    changeScreen('index');
}

function editSettings() {
    eel.setPath()(function (response) {
        eel.editPath();
        showFeedback("Caminho editado");
    });
}

function openDir() {
    eel.openDir();
}

function showFeedback(message) {
    let feedback = document.querySelector("div.feedback");
    let p = document.querySelector("div.feedback p");
    p.innerHTML = message;

    feedback.classList.contains("none")
    feedback.style.opacity = "1";
    feedback.classList.remove("none");

    setTimeout(() => {
        feedback.style.opacity = "0";
        feedback.classList.add("none");
    }, 2500)

    // else {
    //     feedback.style.opacity = "0";
    //     feedback.classList.add("none");
    // }
}

function clearJson() {
    eel.clearJson();
    // changeScreen("download");
}

async function download() {
    const tempLinks = await eel.getArrayLinks()();
    let qtd;
    let links = [];
    
    for (let item in tempLinks) {
        const asyncResponse = async () => {
            const result = await eel.getInfo(tempLinks[item])();
          
            return result;
        }

        let response = await asyncResponse();

        links.push({"name" : response, "link" : tempLinks[item]});
    }

    qtd = 100 / links.length;

    for (let item in links) {
        const asyncResponse = async () => {
            console.log(`Baixando agora ${links[item]['name']} . . .`);
            const result = await eel.download(links[item]['link'])();
          
            return result;
        }

        let response = await asyncResponse();
        console.log(response);
        moveProgressBar(qtd);
    }

    clearJson();
}

function moveProgressBar(qtd) {
    let progressBar = document.querySelector("div.progress-container div.progress-bar");
    progressBar.style.width = qtd + "%";
    // let width = 0;
    // let interval = setInterval(frame, 2000);
  
    // function frame() {
    //   if (width >= 100) {
    //     clearInterval(interval);
    //   } else {
    //     width += 20;
    //   }
    // }
}
  