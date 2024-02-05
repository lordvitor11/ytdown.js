export function makeConfig(value) {
  const dados = { comando: "make-config", arg: value }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(resposta => { resolve(resposta); })
    .catch(error => { reject(error); });
  });
}

export function addSong(value) {
  const dados = { comando: "add-song", arg: value }
  
  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(resposta => { resolve(resposta); })
    .catch(error => { reject(error); });
  });
}

export function getSong(value) {
  const dados = { comando: "get-info", arg: value }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
   .then(response => response.json())
   .then(resposta => { resolve(resposta); })
   .catch(error => { reject(error); });
  });
}

export function getLen() {
  const dados = { comando: "get-len", arg: "" }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(resposta => { resolve(resposta); })
    .catch(error => { reject(error); });
  });
}

export function removeSong_(ids) {
  const dados = { comando: "remove-song", arg: ids }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
   .then(response => response.json())
   .then(resposta => { resolve(resposta); })
   .catch(error => { reject(error); });
  });
}

export function downloadSong_() {
  const dados = { comando: "download-song", arg: "" }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
   .then(response => response.json())
   .then(resposta => { resolve(resposta); })
   .catch(error => { reject(error); });
  });
}

export function quit() {
  const dados = { comando: "quit", arg: "" }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
   .then(response => response.json())
   .then(resposta => { resolve(resposta); })
   .catch(error => { reject(error); });
  });
}

export function getPath_() {
  const dados = { comando: "get-path", arg: "" }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:3000/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dados)
    })
   .then(response => response.json())
   .then(resposta => { resolve(resposta); })
   .catch(error => { reject(error); });
  });
}