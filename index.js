const { app, BrowserWindow, dialog } = require('electron');
const { getSongInfo, createJson, writeJson, valueExists, getLen, removeSong, downloadSong } = require('./utils/toolbox.js');
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');

let mainWindow;
const appExpress = express();
const port = 3000;

fs.mkdir("src/config", (err) => {
    if (err) {
        console.error('Ocorreu um erro ao criar a pasta:', err);
        return;
    }
    console.log('A pasta foi criada com sucesso!');
});

appExpress.use(bodyParser.json());

appExpress.post('/config', (req, res) => {
    const comando = req.body.comando;
    const arg = req.body.arg;

    if (comando == "make-config") {
        createJson(arg);
        res.json({ resposta: "JSON criado som sucesso!" });
    } else if (comando == "add-song") {
        (async () => {
            try {
                const resultado = await valueExists(arg);
                
                if (resultado.erro) {
                    console.error(resultado.mensagem);
                } else {
                    if (resultado.existe) {
                        res.json({ resposta: 1 });
                    } else {
                        writeJson(arg);
                        res.json({ resposta: 0 });
                    }
                }
            } catch (err) {
                console.error('Ocorreu um erro:', err);
            }
        })();
    } else if (comando == "get-info") {
        (async () => {
            try {
                const resultado = await getSongInfo(arg);
                
                if (resultado.erro) {
                    console.error(resultado.mensagem);
                    res.json({ resposta: 1 });
                } else {
                    res.json({ resposta: 0, title: resultado.title, duration: resultado.duration });
                }
            } catch (err) {
                console.error('Ocorreu um erro:', err);
                res.json({ resposta: 1 });
            }       
        })();
    } else if (comando == "get-len") {
        getLen()
        .then(resultado => {
            res.json({ resposta: 0, numero: resultado.num, links: resultado.json });   
        })
        .catch(error => {
            console.log('Deu erro:', error);
            res.json({ resposta: 1 });
        });
    } else if (comando == "remove-song") {
        (async () => {
            try {
                const resultado = await removeSong(arg);
                
                if (resultado.erro) {
                    res.json({ resposta: 1 });
                } else {
                    res.json({ resposta: 0 });
                }
            } catch (err) {
                console.error('Ocorreu um erro:', err);
            }
        })();
    } else if (comando == "download-song") {
        (async () => {
            try {
                const resultado = await downloadSong();

                if (resultado.erro) {
                    res.json({ resposta: 1 });
                } else {
                    res.json({ resposta: 0 });
                }
            } catch (err) {
                console.error('Ocorreu um erro:', err);
            }
        })();
    } else if (comando == "quit") {
        app.quit();
    } else if (comando == "get-path") {
        dialog.showOpenDialog({
            properties: ['openDirectory']
        }).then(result => {
        const directories = result.filePaths;
        if (directories && directories.length > 0) {
            const directoryPath = directories[0];
            res.json({ resposta: 0, dir: directoryPath });
        } else {
            console.log("Nenhum diretório selecionado.");
        }
        }).catch(err => {
            res.json({ resposta: 1, mensagem: err });
        });
    }
});

function createWindow () {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        autoHideMenuBar: true,
        resizable: false,
        maximizable: false,
        minimizable: false, 
        closable: true,
        openDevTools: false,
        webPreferences: {
            nodeIntegration: true
        }
    });

    if (fs.existsSync('src/config/user.json')) {
        mainWindow.loadFile('src/index.html');
    } else {
        mainWindow.loadFile('src/config.html');
    }

    appExpress.listen(port);
}

app.whenReady().then(() => {
    createWindow();
});
