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
    changeScreen("download");
}