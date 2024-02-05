const axios = require('axios');
const ytdl = require('ytdl-core');
const cheerio = require('cheerio');
const fs = require('fs');

async function getSongInfo(link) {
  try {
      const response = await axios.get(link);

      const $ = cheerio.load(response.data);
      const title = $(`meta[property='og:title']`).attr('content');
      const tmpDuration = $(`meta[itemprop='duration']`).attr('content');

      const match = tmpDuration.match(/PT(\d+)M(\d+)S/);
      const minutes = parseInt(match[1]);
      const seconds = parseInt(match[2]);
      const duration = `${minutes}:${seconds.toString().padStart(2, '0')}`;
      
      return { erro: false, title: title, duration: duration };
  } catch (error) {
      return { erro: true, mensagem: '' };
  }
}

function createJson(path) {
  let jsonUser = {
      'caminho' : `${path}\\`
  };

  let jsonLinks = {};
  
  const userJSON = JSON.stringify(jsonUser);
  const linksJSON = JSON.stringify(jsonLinks);
  
  fs.writeFile('src/config/links.json', linksJSON, (err) => {
      if (err) throw err;
  });

  fs.writeFile('src/config/user.json', userJSON, (err) => {
      if (err) throw err;
  });
}

function writeJson(link) {
  fs.readFile('src/config/links.json', 'utf8', (err, data) => {
      if (err) {
          console.error('Erro ao ler o arquivo:', err);
          return;
      }
  
      try {
          const obj = JSON.parse(data);

          const numeroDeLinhas = Object.keys(obj).length;
          obj[numeroDeLinhas] = link;
          const jsonString = JSON.stringify(obj, null, 2);
  
          fs.writeFile('src/config/links.json', jsonString, 'utf8', (err) => {
              if (err) {
                  console.error('Erro ao escrever no arquivo:', err);
                  return;
              }
          });
      } catch (err) {
          console.error('Erro ao analisar JSON:', err);
      }
  });
}

async function valueExists(link) {
  try {
      const data = fs.readFileSync('src/config/links.json', 'utf8');
      const obj = JSON.parse(data);
      const existe = Object.values(obj).some(value => value === link);

      if (existe) {
          return { existe: true, mensagem: 'O dado já existe no JSON.' };
      } else {
          return { existe: false, mensagem: 'O dado ainda não existe no JSON.' };
      }
  } catch (err) {
      console.error('Erro ao ler o arquivo ou analisar JSON:', err);
      return { erro: true, mensagem: 'Erro ao verificar o dado no JSON.' };
  }
}

async function getLen() {
    return new Promise((resolve, reject) => {
      fs.readFile('src/config/links.json', 'utf8', (err, data) => {
          if (err) {
              console.error('Erro ao ler o arquivo:', err);
              return;
          }
      
          try {
              const obj = JSON.parse(data);
              const numeroDeLinhas = Object.keys(obj).length;
              resolve({ erro: false, num: numeroDeLinhas, json: obj });
          } catch (err) {
              console.error('Erro ao analisar JSON:', err);
              reject({ erro: true, mensagem: err });
          }
      });
  });
}

function corrigirIndice(jsonObj, indexToRemove, keys) {
    let lastIndex = keys.length - 1;

    if (indexToRemove == lastIndex) {
        delete jsonObj[indexToRemove];
    } else {
        for (let i = indexToRemove; i < lastIndex; i++) {
            jsonObj[i] = jsonObj[i + 1];
            delete jsonObj[i + 1];
        }
    }

    let updatedJsonString = JSON.stringify(jsonObj, null, 2);

    return updatedJsonString;
}

async function removeSong(ids) {
  return new Promise((resolve, reject) => {
      fs.readFile('src/config/links.json', 'utf8', (err, data) => {
            if (err) {
                console.error('Erro ao ler o arquivo:', err);
                return;
            }

            try {
                let obj = JSON.parse(data);

                for (let item in ids) {
                    corrigirIndice(obj, parseInt(item), Object.keys(obj))
                }

                const jsonString = JSON.stringify(obj);

                fs.writeFile('src/config/links.json', jsonString, 'utf8', (err) => {
                    if (err) {
                        console.error('Erro ao escrever no arquivo:', err);
                        return;
                    }
                    resolve({ erro: false });
                });
            } catch (err) {
              console.error('Erro ao analisar JSON:', err);
              reject({ erro: true });
          }
      });
  });
}

function getDownPath() {
    return new Promise((resolve, reject) => {
        fs.readFile('src/config/user.json', 'utf8', (err, data) => {
            if (err) {
                console.error('Erro ao ler o arquivo:', err);
                return;
            }

            try {
                const obj = JSON.parse(data);
                const path = obj['caminho'];
                resolve({ erro: false, path: path });
            } catch (err) {
                console.error('Erro ao analisar JSON:', err);
                reject({ erro: true, mensagem: err });
            }
        })
    })
}

async function clearJson() {
    const rawJson = await getLen();
    return new Promise((resolve, reject) => {
        if (rawJson['erro']) {
            return { erro: true, mensagem: rawJson['mensagem'] };
        } else {
            let jsonResponse = rawJson['json'];
            jsonResponse = {};
            const jsonString = JSON.stringify(jsonResponse);
            fs.writeFile('src/config/links.json', jsonString, 'utf8', (err) => {
                if (err) {
                    console.error('Erro ao escrever no arquivo:', err);
                    reject({ erro: true, mensagem: err });
                }

                resolve({ erro: false });
            });
        }
    });
}

async function downloadSong() { 
    return new Promise(async (resolve, reject) => {
        const responsePath = await getDownPath();
        let output = responsePath['path'];

        const options = { quality: 'highestaudio', filter: 'audioonly' };
        const links = await getLen();

        if (links['erro']) {
            reject({ erro: true, mensagem: links['mensagem'] });
        } else {
            for (let i = 0; i < links['num']; i++) {
                const link = links['json'][i];
                const songInfo = await getSongInfo(link);
                if (songInfo['erro']) {
                    reject({ erro: true, mensagem: songInfo['mensagem'] });
                } else {
                    const title = songInfo['title'];
                    ytdl(link, options)
                    .pipe(fs.createWriteStream(`${output}${title}.mp3`))
                    .on('finish', () => {
                        const clearResponse = clearJson();
                        if (clearResponse['erro']) {
                            reject({ erro: true, mensagem: clearResponse['mensagem'] });
                        } else {
                            resolve({ erro: false });
                        }
                    })
                    .on('error', (err) => {
                        console.error('Erro durante o download:', err);
                        reject({ erro: true, mensagem: err });
                    });
                }
            }
            resolve({ erro: false });
        }
    });
}

module.exports = {
    getSongInfo, 
    createJson, 
    writeJson, 
    valueExists, 
    getLen, 
    removeSong,
    downloadSong
};