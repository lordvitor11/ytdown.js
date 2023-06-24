async function download() {
    const tempLinks = await eel.getArrayLinks()();

    let songName = document.querySelector("div.progress p");
    let qtd;
    let w = 0;
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
            songName.innerHTML = `Baixando ${links[item]['name']}...`;
            const result = await eel.download(links[item]['link'])();
          
            return result;
        }

        let response = await asyncResponse();
        console.log(response);
        moveProgressBar(qtd, w);
        w += qtd;
    }

    songName.innerHTML = "Tudo pronto.";
    eel.clearJson();
}

function moveProgressBar(qtd, width) {
    let progressBar = document.querySelector("div.progress-container div.progress-bar");
    let total = qtd + width
    console.log("qtd: " + qtd)
    console.log("width: " + width)
    console.log("total:" + total)
    progressBar.style.width = total + "%";
}

download();